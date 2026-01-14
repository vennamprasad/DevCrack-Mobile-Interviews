# 📱 Mobile System Design

> **Target Audience:** Staff/Principal Engineers.
> **Scope:** End-to-End Architecture, Offline-First, Synchronization, and scalability.

![System Design](https://img.shields.io/badge/Design-System_Design-blueviolet?style=for-the-badge&logo=diagrams.net)

---

## 📖 Table of Contents
- [Level 1: Offline-First Architecture](#level-1-offline-first-architecture)
- [Level 2: Real-Time Synchronization](#level-2-real-time-synchronization)
- [Level 3: Image Loading Library (Design a Glide clone)](#level-3-image-loading-library)
- [Level 4: Large Scale Scenarios](#level-4-large-scale-scenarios)

---

## Level 1: Offline-First Architecture

### Q1. How do you design an Offline-First News App?
**Pattern**: "Database as Source of Truth".
1.  **Read Path**: UI always observes Database (Room/SQLite). Never observes Network directly.
2.  **Write Path**:
    *   Network -> Fetch Data -> Write to DB -> UI Updates (via Flow/LiveData).
3.  **Error Handling**: If Network fails, DB still has old data. UI shows "Offline" snackbar.

### Q2. How to handle conflicting edits (Conflict Resolution)?
**Scenario**: User edits a note Offline. Server has a newer version.
**Strategies**:
1.  **Last Write Wins (LWW)**: Simple, based on Timestamp. Prone to data loss.
2.  **Manual Merge**: Show user both versions ("Keep yours" vs "Take Server's").
3.  **Conflict-free Replicated Data Types (CRDTs)**: Advanced math to automatic merge.
4.  **Operational Transformation (OT)**: Google Docs style.

---

## Level 2: Real-Time Synchronization

### Q3. Push Notifications vs WebSockets vs Polling?
**Comparison**:
*   **Polling**: Periodic HTTP GET. High battery drain. High latency.
*   **Long Polling**: Server holds connection open until data available. Better latency.
*   **WebSockets**: Bi-directional, persistent. Best for Chat/Trading. High complexity to maintain state.
*   **FCM (Push)**: OS managed. Best for occasional updates (New Email). efficient for battery.

### Q4. Design a "Chat Application" Sync Protocol.
**Architecture**:
1.  **Local DB**: Stores messages.
2.  **Socket**: Receives `NewMessage(id: 101)`.
3.  **Sync Logic**:
    *   On Connect: generic `sync(lastReceivedId: 100)`. Server sends 101, 102, 103.
    *   Ack: Client sends `ack(103)`.
4.  **Queue**: Outgoing messages stored in `PendingMessages` table. "Worker" flushes them when online.

---

## Level 3: Image Loading Library

### Q5. Design "Glide" or "Picasso" from scratch.
**Requirements**: Async loading, Caching (Memory/Disk), Recycling.
**Components**:
1.  **Request Manager**: Handles lifecycle (Pause requests when Activity stops).
2.  **Engine**:
    *   `MemoryCache` (LRU Cache): Check first.
    *   `DiskCache` (DiskLruCache): Check second.
    *   `NetworkFetcher`: Download Stream.
3.  **Decoder**: Stream -> Bitmap. Downsampling (Resize 4K image to ImageView size).
4.  **Transformation**: Crop, RoundedCorners.
5.  **Target**: Render to ImageView.

**Critical optimization**:
*   **InBitmap**: Re-use bitmap memory.
*   **Pause on Scroll**: Don't load while flinging list.

---

## Level 4: Large Scale Scenarios

### Q6. Design "Instagram Stories" (Heavy Media, Transient).
**Challenges**: Pre-loading, Sequential playback, Bandwidth limits.
**Design**:
1.  **Pre-fetching**: While watching Story A, download Story B (1st chunk).
2.  **Cache Eviction**: Aggressive. Stories expire in 24h. Delete immediately.
3.  **Upload**: Background Service. Resumable Uploads (Chunked).

### Q7. How to handle 10,000 updates per second (Stock Ticker)?
**Answer**:
*   ** throttling/Debouncing**: Don't render every tick. Frame-limit updates to 30fps.
*   **Diffing**: Only re-bind changed fields (DiffUtil).
*   **Binary Protocol**: Use Protobuf or binary WS frames instead of JSON.
