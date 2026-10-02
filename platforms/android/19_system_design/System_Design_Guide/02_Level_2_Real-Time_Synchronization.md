## Level 2: Real-Time Synchronization

### Q3. Push Notifications vs WebSockets vs Polling?

**Comparison**:

- **Polling**: Periodic HTTP GET. High battery drain. High latency.
- **Long Polling**: Server holds connection open until data available. Better latency.
- **WebSockets**: Bi-directional, persistent. Best for Chat/Trading. High complexity to maintain state.
- **FCM (Push)**: OS managed. Best for occasional updates (New Email). efficient for battery.

### Q4. Design a "Chat Application" Sync Protocol.

**Architecture**:

1.  **Local DB**: Stores messages.
2.  **Socket**: Receives `NewMessage(id: 101)`.
3.  **Sync Logic**:
    - On Connect: generic `sync(lastReceivedId: 100)`. Server sends 101, 102, 103.
    - Ack: Client sends `ack(103)`.
4.  **Queue**: Outgoing messages stored in `PendingMessages` table. "Worker" flushes them when online.
