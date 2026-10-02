# 🚀 Level 4: Large-Scale Mobile System Design (Instagram Stories & High-Frequency Stock Ticker)

> **Architecting extreme-scale mobile client systems: Zero-buffering video pre-warming for Instagram Stories, and 10,000 updates/second real-time streaming engines with binary protocols and conflated UI rendering.**

---

## 📌 Executive Summary & Interview Framing

Level 4 system design questions push mobile candidates beyond standard CRUD operations. These questions test an architect's ability to handle **heavy multimedia streaming pipelines, hardware limitations, network congestion, and high-throughput thread concurrency**.

We analyze two classic large-scale system design problems asked at Meta, Netflix, Robinhood, and Citadel:
1. **Scenario A: Instagram Stories & TikTok Feed (Heavy Media, Transient, Zero-Latency Playback)**.
2. **Scenario B: High-Frequency Trading / Stock Ticker (10,000 Updates/Second Stream)**.

---

# 📱 Scenario A: Instagram Stories & TikTok Video Feed

## 1. Core Requirements & Performance Targets
- **Zero-Latency Playback**: When a user taps to the next story or swipes up on TikTok, playback must start in **< 100 milliseconds** (zero visible buffering spinner).
- **Bandwidth Discipline**: Do not blindly download full 60-second 4K videos that the user might skip after 1 second.
- **Resumable Uploads**: User video uploads must survive network dropouts and app backgrounding.

---

## 2. Video Streaming Architecture: HLS / DASH & Fragmented MP4

Never stream raw, monolithic `.mp4` video files! Monolithic files force the device to download the entire video header before playback can begin.

```
[ Video Server / CDN ] ──(HLS / DASH Manifest)──> [ Master Playlist (.m3u8) ]
                                                            │
                     ┌──────────────────────────────────────┼──────────────────────────────────────┐
                     ▼                                      ▼                                      ▼
            [ Chunk 1: 0-2 sec ]                  [ Chunk 2: 2-4 sec ]                  [ Chunk 3: 4-6 sec ]
           (Pre-fetched instantly)               (Streamed during play)                 (Adaptive bitrate)
```

- **Chunked Segments**: Videos are segmented into **2-second `.ts` or fragmented `.mp4` (`fMP4`) chunks**.
- **Adaptive Bitrate Streaming (ABR)**: The client dynamically switches between 480p, 720p, and 1080p based on measured network bandwidth and dropped frame rate.

---

## 3. The ExoPlayer Dual-Player Pre-Warming Engine

To achieve instant playback when advancing through stories, production apps maintain a **Dual-Player Pool**:

```
                       Current Screen: User Watching Story A
                       ┌─────────────────────────────────────┐
                       │        Active ExoPlayer (Player 1)   │ ──> Rendering to SurfaceView
                       └─────────────────────────────────────┘
                                          │
                                (Pre-warming in Background)
                                          ▼
                       ┌─────────────────────────────────────┐
                       │        Standby ExoPlayer (Player 2) │ ──> Pre-buffers first 2s of Story B
                       └─────────────────────────────────────┘
                                          │
                        (User Taps Screen -> "Next Story")
                                          ▼
         [ Swap Player 2 to Front (Instant 0ms Playback!) ]
         [ Player 1 resets and pre-buffers Story C in background ]
```

### Pre-Fetching Algorithm:
1. Download **only Chunk 1 (the first 2 seconds)** of the next 3 stories into an in-memory disk cache (`SimpleCache` with a 300 MB LRU limit).
2. If the user watches past second 1 of Story A, begin streaming Chunk 2 and Chunk 3 of Story A.
3. If the user skips immediately, discard the remaining chunks of Story A, saving over 80% cellular data.

---

## 4. Resumable Chunked Video Uploads

Uploading a 50 MB video fails frequently on poor cellular connections.

```kotlin
class ResumableVideoUploader(
    private val api: MediaApi,
    private val db: UploadDatabase
) {
    suspend fun uploadVideo(file: File, uploadId: String) = withContext(Dispatchers.IO) {
        val chunkSize = 2 * 1024 * 1024 // 2 MB chunks
        val totalBytes = file.length()
        val totalChunks = (totalBytes + chunkSize - 1) / chunkSize

        var uploadedChunks = db.uploadDao().getCompletedChunkIndices(uploadId)

        file.inputStream().use { stream ->
            val buffer = ByteArray(chunkSize)
            for (chunkIndex in 0 until totalChunks) {
                if (chunkIndex in uploadedChunks) {
                    stream.skip(chunkSize.toLong())
                    continue
                }

                val bytesRead = stream.read(buffer)
                val chunkData = buffer.copyOf(bytesRead)
                val sha256 = MessageDigest.getInstance("SHA-256").digest(chunkData).toHex()

                val response = api.uploadChunk(
                    uploadId = uploadId,
                    chunkIndex = chunkIndex,
                    totalChunks = totalChunks,
                    checksum = sha256,
                    body = chunkData.toRequestBody()
                )

                if (response.isSuccessful) {
                    db.uploadDao().markChunkCompleted(uploadId, chunkIndex)
                } else {
                    throw IOException("Chunk upload failed. Auto-retry via WorkManager.")
                }
            }
        }
    }
}
```

---

# 📈 Scenario B: High-Frequency Stock Ticker (10,000 Updates/Sec)

## 1. The Bottleneck: UI Thread Starvation

In financial trading apps (Robinhood, Coinbase, Binance), market feeds can emit **10,000 tick updates per second** during market volatility:
- The human eye cannot perceive changes faster than **60fps (16.6ms)** or **120fps (8.3ms)**.
- If you dispatch 10,000 state changes to Jetpack Compose or SwiftUI, the UI thread will choke, frame rates will plummet to 0fps, and the app will trigger an ANR crash.

---

## 2. The Solution: Conflation & Frame-Rate Decoupling

```
[ WebSocket: 10,000 Ticks / sec ]
                │
                ▼ (Offloaded to Dispatchers.Default)
[ In-Memory Lock-Free Ring Buffer ]
(Computes latest Price, Volume, & Delta)
                │
                ▼ (Conflated Sampling Rate: Max 60 FPS)
[ Flow.conflate() or Flow.sample(16ms) ]
                │
                ▼ (Dispatches to Main Thread)
[ Jetpack Compose UI (Smooth 60 FPS) ]
```

### Kotlin Conflation Implementation:

```kotlin
data class TickerUpdate(val symbol: String, val price: Double, val timestamp: Long)

class MarketDataEngine(private val socketClient: ResilientWebSocketClient) {

    // 1. High-frequency raw binary stream
    private val rawTickFlow: Flow<TickerUpdate> = socketClient.events
        .filterIsInstance<SocketEvent.MessageReceived>()
        .map { parseProtobufTicker(it.payload) } // Zero-copy Protobuf parsing

    // 2. Conflated UI state stream throttled to display refresh rate
    val uiStateFlow: Flow<Map<String, TickerUpdate>> = flow {
        val latestPrices = ConcurrentHashMap<String, TickerUpdate>()

        rawTickFlow.collect { update ->
            latestPrices[update.symbol] = update
        }
    }
    // sample(16) guarantees we NEVER emit faster than 60 times per second
    .sample(16.milliseconds)
    .flowOn(Dispatchers.Default)
}
```

---

## 3. Protocol Efficiency: Protobuf / FlatBuffers vs. JSON

Parsing 10,000 JSON strings per second produces millions of transient `String` and `JSONObject` allocations in the JVM heap, triggering continuous Garbage Collection (GC) pauses.

### FlatBuffers: Zero-Copy Serialization
- **Protocol Buffers (Protobuf)**: Compresses network payloads by 80% compared to JSON. Requires an unpack parsing step.
- **FlatBuffers**: Reads hierarchical data directly from the binary byte buffer **without unpacking or allocating objects**.
- Accessing a stock price:
  $$\text{Price} = \text{ByteBuffer.getDouble(offset + 8)}$$
  **Allocation cost: Exactly 0 bytes!**

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "In Instagram Stories, how do you handle cache eviction so the app doesn't consume 10 GB of phone storage after a week of browsing?"
* **Answer**:
  - Implement a **Two-Tier Eviction Policy**:
    1. **Time-To-Live (TTL)**: Stories are transient and expire after 24 hours. The local media index periodically deletes any cached chunks older than 24 hours.
    2. **Bounded Least Recently Used (LRU) Disk Cache**: Configure ExoPlayer's `SimpleCache` with a `LeastRecentlyUsedCacheEvictor(maxBytes = 500 * 1024 * 1024)` (500 MB). When the cache reaches 500 MB, ExoPlayer automatically purges the oldest media chunks on background threads.

### Q2: "In a real-time trading app, what is the 'Ghost Tick' problem, and how do you prevent displaying stale prices?"
* **Answer**:
  - **The Problem**: Network packets can arrive out of order over mobile networks, or an old packet buffered in the OS socket queue might be delivered after a newer trade has already occurred.
  - **The Solution**: Every tick payload must include a **Monotonic Server Timestamp / Sequence ID**.
    The mobile client maintains a `lastKnownTimestamp` per ticker symbol. If an incoming packet has $\text{timestamp} \le \text{lastKnownTimestamp}$, it is discarded immediately as an outdated "Ghost Tick."
