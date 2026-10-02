# 🏛️ Mobile System Design Masterclass

> **Senior and Staff-level system design blueprints for mobile engineers: Offline-first data synchronization, resilient real-time protocols, high-performance image rendering engines, and extreme-throughput streaming architectures.**

---

## 📖 System Design Curriculum

| Level | Architecture Blueprint | Key Concepts & Patterns |
| :--- | :--- | :--- |
| **Level 1** | **[Offline-First Mobile Architecture](./01_Level_1_Offline-First_Architecture.md)** | Single Source of Truth (SSOT), Transactional Outbox Pattern, Optimistic UI updates, Tombstoning deletions, Conflict resolution (LWW vs. CRDTs), and Room + WorkManager sync. |
| **Level 2** | **[Real-Time Synchronization & Messaging](./02_Level_2_Real-Time_Synchronization.md)** | WebSocket connection lifecycles, half-open TCP detection via ping/pong heartbeats, 4-stage delivery receipt protocol (WhatsApp model), monotonic sequence gap recovery, and hybrid FCM fallback. |
| **Level 3** | **[Image Loading Library from Scratch](./03_Level_3_Image_Loading_Library.md)** | Multi-tier caching (RAM LRU, DiskLruCache, BitmapPool memory recycling via `inBitmap`), mathematical `inSampleSize` downsampling to prevent OOM, request coalescing, and lifecycle-aware cancellation. |
| **Level 4** | **[Large-Scale Streaming Scenarios](./04_Level_4_Large_Scale_Scenarios.md)** | **Instagram Stories / TikTok Feed**: Dual-player pre-warming pool, HLS/DASH chunk pre-fetching, 24h TTL eviction, and resumable multipart uploads.<br>**10,000 Ticks/Sec Stock Ticker**: Conflated UI state engine, binary Protobuf/FlatBuffers zero-copy serialization, and frame-rate decoupling. |

---

[⬅️ Back to Android Curriculum](../../README.md)
