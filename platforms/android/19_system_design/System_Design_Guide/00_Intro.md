# 📱 Mobile System Design Interview Framework

> **A battle-tested 45-minute system design framework for Senior, Staff, and Principal Mobile Engineers.**

---

## 🧭 The 45-Minute Mobile System Design Blueprint

Unlike backend system design—which focuses on microservices, sharding, and database replication—**mobile system design evaluates client-side constraints: memory limits, CPU/battery thermal throttling, asynchronous network instability, and offline state consistency**.

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                        The 4-Phase Interview Flow                      │
  ├───────────────────┬───────────────────┬───────────────────┬────────────┤
  │ Phase 1: Clarify  │ Phase 2: High-    │ Phase 3: Deep     │ Phase 4:   │
  │ Requirements      │ Level Design      │ Dive Bottlenecks  │ Edge Cases │
  │ (5 - 8 mins)      │ (10 - 15 mins)    │ (15 - 20 mins)    │ (5 mins)   │
  └───────────────────┴───────────────────┴───────────────────┴────────────┘
```

---

### Phase 1: Clarification & Constraint Definition (5–8 mins)
Never jump directly into drawing boxes! Ask clarifying questions to establish boundaries:
1. **Functional Requirements**:
   - What are the top 2–3 core user journeys? (e.g., viewing news articles offline, liking an article, bookmarking).
   - What features are explicitly out of scope for this 45-minute discussion?
2. **Non-Functional Requirements & Mobile Constraints**:
   - **Offline Capability**: Must the app support read-only offline viewing, or full offline writes with queueing?
   - **Target Hardware & OS**: Flagship devices only, or low-RAM (2GB RAM) emerging market Android Go devices?
   - **Network Profile**: Fast 5G or intermittent 3G cellular with frequent dropouts?
   - **Battery & Data Budget**: Can we poll, or must we rely strictly on push notifications?

---

### Phase 2: High-Level Client Architecture (10–15 mins)
Establish a clean Unidirectional Data Flow (UDF) across architectural boundaries:

```
[ UI / Presentation Layer ] ──(Emits User Actions)──> [ ViewModel / Presenter ]
                                                              │
                                                   (Calls UseCases / Domain)
                                                              ▼
                                                    [ Repository Engine ]
                                                              │
                             ┌────────────────────────────────┴────────────────────────────────┐
                             ▼                                                                 ▼
                [ Local Storage (Room/SQLite) ]                                   [ Remote Network API ]
                 • Single Source of Truth                                          • Retrofit / OkHttp
                 • Offline Cache & Outbox                                          • WebSocket Gateway
```

---

### Phase 3: Deep Dives into Core Bottlenecks (15–20 mins)
Choose the 2 or 3 hardest technical challenges in the system and demonstrate staff-level depth:
1. **Offline Synchronization & Conflict Resolution**:
   - Outbox Pattern, Room + WorkManager background synchronization, and tombstoning deletions.
2. **Memory & Performance Profiling**:
   - Downsampling bitmaps with `inSampleSize` and `BitmapPool` (`inBitmap`) to prevent OOM.
   - Throttling high-frequency streams with `Flow.conflate()` or `sample(16ms)`.
3. **Network Resiliency & Connection Management**:
   - WebSocket exponential backoff with full jitter and heartbeat ping-pong frames.

---

### Phase 4: Failure Modes & Edge Cases (5 mins)
Proactively lead the discussion on real-world mobile failure scenarios:
- **Process Death & Memory Trimming**: What happens when Android kills the app in the background during a multi-step checkout flow? (Use `SavedStateHandle` and local persistence).
- **Corrupted Local Database**: How does the app recover if the SQLite database is corrupted? (Fallback schema recreation and automated telemetry report).
- **Clock Drift**: Never rely on `System.currentTimeMillis()` for ordering events; use monotonic server timestamps or Lamport clocks.

---

## 📚 Curriculum Navigation

- **[Level 1: Offline-First Architecture](./01_Level_1_Offline-First_Architecture.md)**
- **[Level 2: Real-Time Synchronization & Messaging](./02_Level_2_Real-Time_Synchronization.md)**
- **[Level 3: Image Loading Library from Scratch](./03_Level_3_Image_Loading_Library.md)**
- **[Level 4: Large Scale Streaming Scenarios](./04_Level_4_Large_Scale_Scenarios.md)**
