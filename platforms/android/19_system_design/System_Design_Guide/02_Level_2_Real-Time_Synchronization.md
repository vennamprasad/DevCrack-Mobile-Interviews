# ⚡ Level 2: Real-Time Mobile Synchronization & Messaging Protocols

> **Architecting low-latency, battery-aware real-time systems: WebSocket connection lifecycles, half-open TCP detection, monotonic gap reconciliation, delivery receipts, and hybrid FCM fallback.**

---

## 📌 Executive Summary & Interview Framing

Designing a real-time mobile system (e.g., WhatsApp, Slack, Uber Driver Location, Robinhood Stock Ticker) tests an engineer's understanding of **networking protocols, battery conservation, and distributed state consistency**.

In production mobile environments, connections are notoriously unstable:
- Devices constantly switch between Wi-Fi and 5G cellular towers.
- Devices enter subway tunnels (dead zones) or airplane mode.
- Operating systems (Android Doze Mode and iOS Background Execution limits) aggressively freeze CPU background threads and terminate open sockets to preserve battery.

A world-class real-time architecture must handle **abrupt disconnects, half-open TCP states, message ordering guarantees, and hybrid push notification wake-ups**.

---

## 🌐 Protocol Selection Matrix for Mobile

| Protocol | Latency | Battery Overhead | Server -> Client | Client -> Server | Mobile Fit & Use Cases |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Short Polling** | High (5–30s) | Catastrophic (Constant radio wakeups) | Pulled | Pulled | ❌ **Anti-pattern for mobile**. Drains battery rapidly. |
| **Long Polling** | Medium (1–3s) | High (Holds HTTP threads) | Pushed on event | Request-based | ⚠️ Legacy web fallback; avoid on modern mobile apps. |
| **Server-Sent Events (SSE)** | Low (<200ms) | Low (Single persistent HTTP/2 stream) | Yes (Streaming) | No (Unidirectional) | ✅ **Excellent for read-heavy feeds** (LaunchDarkly flags, Live Scores, Stock feeds). |
| **WebSockets** | **Sub-50ms** | Medium (Requires heartbeat keepalives) | **Bi-directional** | **Bi-directional** | ✅ **Standard for Interactive Chat & Gaming** (WhatsApp, Discord, Slack). |
| **gRPC Streaming** | Sub-50ms | Low (Protobuf binary framing over HTTP/2) | **Bi-directional** | **Bi-directional** | ✅ **Enterprise Microservices** (Uber, Lyft driver/rider telemetry). |
| **FCM / APNs (Push)** | 500ms – 5s | **Zero active client battery** (OS Daemon) | Push Wakeup | None | ✅ **Background Notifications & Cold App Wakeups**. |

---

## 🏗️ The Hybrid Real-Time Architecture (WebSocket + FCM)

```
                            [ Foreground State ]
                            ┌───────────────────┐
                            │  Active WebSocket │ ──> Sub-50ms messaging
                            └───────────────────┘
                                      │
                   (User Backgrounds App / Screen Locked)
                                      ▼
                      [ Disconnect Active WebSocket ]
                         (Saves Battery & Radio CPU)
                                      │
                                      ▼
                            [ Background State ]
                            ┌───────────────────┐
                            │ FCM / APNs Socket │ ──> OS Daemon receives data payload
                            └───────────────────┘
                                      │
                               (Incoming Message)
                                      ▼
                        [ High-Priority Push Wakeup ]
                        • Wakes app for 10-30 seconds
                        • Writes payload to local SQLite DB
                        • Posts system notification
```

---

## 🔌 Robust WebSocket Connection Lifecycle Management

A naive WebSocket client reconnects in an infinite loop when the internet drops. This creates a **"Thundering Herd"** problem that crashes backend servers when thousands of mobile clients reconnect simultaneously after an outage.

### Production Reconnection Engine:
1. **Exponential Backoff with Full Jitter**:
   $$\text{Delay} = \text{random}(0, \min(\text{MaxDelay}, \text{BaseDelay} \times 2^{\text{attempt}}))$$
2. **Network Callback Integration**: Do not attempt reconnects if Android `ConnectivityManager` indicates `NetworkCapabilities.NET_CAPABILITY_INTERNET` is absent.
3. **Heartbeat / Ping-Pong (Half-Open TCP Detection)**:
   - When a mobile device enters an elevator, the cellular radio often drops without sending a TCP `FIN` or `RST` packet.
   - The phone thinks the socket is still open, but packets are routed into a black hole.
   - **Solution**: The mobile client sends a ping frame every **30 seconds**. If the server doesn't respond with a pong frame within **5 seconds**, the client forcibly terminates the socket (`socket.cancel()`) and initiates reconnection.

---

## 💻 Production WebSocket Client (Kotlin Flow)

```kotlin
sealed class SocketEvent {
    object Connected : SocketEvent()
    data class MessageReceived(val payload: String) : SocketEvent()
    data class ConnectionError(val throwable: Throwable) : SocketEvent()
    object Disconnected : SocketEvent()
}

class ResilientWebSocketClient(
    private val client: OkHttpClient,
    private val request: Request
) {
    private var webSocket: WebSocket? = null
    private val _events = MutableSharedFlow<SocketEvent>(replay = 0, extraBufferCapacity = 64)
    val events: SharedFlow<SocketEvent> = _events.asSharedFlow()

    private var reconnectAttempt = 0
    private val maxDelayMs = 30_000L
    private val baseDelayMs = 1_000L

    fun connect() {
        val listener = object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                this@ResilientWebSocketClient.webSocket = webSocket
                reconnectAttempt = 0
                _events.tryEmit(SocketEvent.Connected)
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                _events.tryEmit(SocketEvent.MessageReceived(text))
            }

            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                webSocket.close(1000, null)
                _events.tryEmit(SocketEvent.Disconnected)
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                _events.tryEmit(SocketEvent.ConnectionError(t))
                scheduleReconnect()
            }
        }

        webSocket = client.newWebSocket(request, listener)
    }

    private fun scheduleReconnect() {
        val delay = calculateExponentialBackoffWithJitter(reconnectAttempt)
        reconnectAttempt++
        CoroutineScope(Dispatchers.IO).launch {
            delay(delay)
            connect()
        }
    }

    private fun calculateExponentialBackoffWithJitter(attempt: Int): Long {
        val exp = min(maxDelayMs, baseDelayMs * (1L shl min(attempt, 10)))
        return Random.nextLong(0, exp)
    }

    fun sendMessage(text: String): Boolean {
        return webSocket?.send(text) ?: false
    }

    fun disconnect() {
        webSocket?.close(1000, "Normal closure")
        webSocket = null
    }
}
```

---

## 📬 The 4-Stage Delivery Receipt Protocol (WhatsApp Model)

A robust chat app provides real-time feedback on message states across devices:

```
[ Sender Device ]              [ Chat Gateway ]             [ Recipient Device ]
        │                             │                              │
        ├── 1. Send Message ─────────>│                              │
        │   (Shows 🕒 Clock icon)     │                              │
        │                             │                              │
        │<── 2. Server ACK ───────────┤                              │
        │   (Shows ✓ Single Tick)     ├── 3. Deliver to Recipient ──>│
        │                             │   (Recipient ACKs delivery)  │
        │<── 4. Delivery Receipt ─────┼──────────────────────────────┤
        │   (Shows ✓✓ Double Grey)    │                              │
        │                             │   (Recipient Opens Screen)   │
        │                             │<── 5. Read Receipt ACK ──────┤
        │<── 6. Read Receipt ─────────┤                              │
        │   (Shows ✓✓ Double Blue)    │                              │
```

### Monotonic Sequence Numbers & Gap Detection
To guarantee no messages are lost when reconnecting:
1. Every message in a conversation has a strictly increasing sequence ID: `seq_id = 101, 102, 103...`.
2. When the app reconnects to the WebSocket, it transmits its latest local sequence:
   ```json
   { "action": "SYNC", "conversation_id": "c_901", "last_seq_id": 102 }
   ```
3. If the server is currently on `seq_id = 107`, it delivers the **delta gap** (messages 103 through 107) in a single compressed batch.

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How do you handle end-to-end encryption (E2EE) key exchange on mobile when a recipient is currently offline?"
* **Answer**:
  - Use the **Signal Protocol (Extended Triple Diffie-Hellman / X3DH) with the Double Ratchet Algorithm**:
    1. During registration, each user publishes a bundle of public keys to the server: an Identity Key, a Signed Pre-key, and a pool of **One-Time Pre-keys**.
    2. When Sender wants to message an offline recipient, the sender asks the server for the recipient’s public Pre-key bundle.
    3. The sender performs a Diffie-Hellman ratchet locally, derives the shared secret session key, and encrypts the message.
    4. The encrypted ciphertext is stored on the server until the recipient reconnects. The server never has access to private keys and cannot decrypt the payload.

### Q2: "How do you prevent UI stutter or memory bloat when a chat room receives hundreds of messages per second?"
* **Answer**:
  1. **Batching Database Inserts**: Buffer incoming WebSocket frames in memory for 100ms and write them to SQLite in a single transaction (`db.withTransaction { insertAll(batch) }`), avoiding continuous disk I/O thrashing.
  2. **DiffUtil & LazyColumn Recycling**: Use stable keys (`items(messages, key = { it.id })`) in Jetpack Compose to avoid recomposing the entire chat history.
  3. **Windowed Memory Cache**: Keep only the most recent 50 messages in the active Compose state. Paginate older messages from SQLite on demand as the user scrolls up.
