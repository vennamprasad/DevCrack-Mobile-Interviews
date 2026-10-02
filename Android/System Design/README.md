# 🏛️ Android Mobile System Design

> **Staff-level architectural frameworks and practical interview blueprints for designing large-scale, high-concurrency, offline-resilient Android apps.**

![SystemDesign](https://img.shields.io/badge/Architecture-Mobile_System_Design-blue?style=for-the-badge&logo=android)
![Scalability](https://img.shields.io/badge/Scope-Large_Scale-orange?style=for-the-badge)
![OfflineFirst](https://img.shields.io/badge/Resilience-Offline_First-green?style=for-the-badge)

---

## 📖 System Design Curriculum

Explore our multi-level architectural blueprint located in **[System Design Guide](./System_Design_Guide/README.md)**:

| Level | Topic | Key Concepts |
| :--- | :--- | :--- |
| **[00. Introduction](./System_Design_Guide/00_Intro.md)** | Interview framework and expectations. | The 45-minute mobile system design template: Requirements clarification, High-level diagram, Deep dives, Edge cases & trade-offs. |
| **[01. Level 1: Offline-First Architecture](./System_Design_Guide/01_Level_1_Offline-First_Architecture.md)** | Data persistence & synchronization. | Single Source of Truth (SSOT), Room + Retrofit coordination, conflict resolution (last-write-wins vs vector clocks), background sync queues with WorkManager. |
| **[02. Level 2: Real-Time Synchronization](./System_Design_Guide/02_Level_2_Real-Time_Synchronization.md)** | WebSockets & live updates. | WebSocket connection management, heartbeat/ping-pong, backoff reconnection, live chat apps, and state synchronization. |
| **[03. Level 3: Image Loading Library](./System_Design_Guide/03_Level_3_Image_Loading_Library.md)** | Designing Coil / Glide from scratch. | L1 Memory Cache (LRU), L2 Disk Cache, bitmap pooling, downsampling, cancellation of scrolled-off requests, and thread pool orchestration. |
| **[04. Level 4: Large-Scale Production Scenarios](./System_Design_Guide/04_Level_4_Large_Scale_Scenarios.md)** | Feed pagination, video streaming, analytics. | Infinite scroll feeds, prefetching, video playback caching, metric batching, and crash resilient pipelines. |

---

> [!TIP]
> For broader cross-platform and backend-to-mobile system design (load balancing, CDN, microservices, databases), see the repository-wide **[System Design for Mobile](../../System%20Design%20for%20Mobile/README.md)** guide.
