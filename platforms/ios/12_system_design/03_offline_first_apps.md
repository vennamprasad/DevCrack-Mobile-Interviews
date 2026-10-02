# 📶 Offline-First iOS System Design: SwiftData, CoreData & Resilient Sync

> **Architecting resilient offline-first iOS applications: Single Source of Truth (SSOT), SwiftData / CoreData persistence, optimistic UI updates, the Transactional Outbox pattern, and background synchronization via the BackgroundTasks framework.**

---

## 📌 Executive Summary

Building an offline-first iOS app (e.g., Notes, Slack, or Field Service CRM) requires decoupling the user interface from network availability. 

A production offline-first architecture must satisfy three non-negotiable principles:
1. **Local Single Source of Truth (SSOT)**: The UI renders exclusively from a local on-disk database (SwiftData, CoreData, or GRDB/SQLite). It **never binds directly to raw network responses**.
2. **Instant Optimistic Mutations**: User actions immediately mutate local database state and update the screen within 16ms (60fps), eliminating loading spinners.
3. **Guaranteed Eventual Delivery**: Outgoing network mutations are queued into an on-disk Outbox and synced via background workers, resilient to app terminations, airplane mode, or device restarts.

---

## 🏗️ End-to-End iOS Offline-First Architecture

```
                    ┌──────────────────────────────────────────────┐
                    │            SwiftUI View Hierarchy            │
                    └──────────────────────┬───────────────────────┘
                                           ▲
                                (Observes @Query / Combine)
                                           │
                    ┌──────────────────────┴───────────────────────┐
                    │    Local Database: SwiftData / CoreData      │
                    │        "Single Source of Truth (SSOT)"       │
                    └──────────────▲──────────────┬────────────────┘
                                   │              │
                   (Writes Data)   │              │ (Queries Pending Mutations)
                                   │              ▼
┌──────────────────────────────────┴──────────────┴───────────────────────────────┐
│                           Sync Engine & Repository                              │
│                                                                                 │
│   [ User Mutation ] ──> [ Write Local DB ] ──> [ Insert to Outbox Queue ]       │
│                                                                │                │
│                                                   (BackgroundTasks Framework)   │
│                                                                ▼                │
│   [ Network Fetch ]  <── [ BGProcessingTask ] <── [ Batch Dequeue & Dispatch ]  │
└──────────────────────────────────┬──────────────────────────────────────────────┘
                                   │ (HTTPS / gRPC)
                                   ▼
                    ┌──────────────────────────────┐
                    │         Backend API          │
                    └──────────────────────────────┘
```

---

## 🔄 The Read and Write Paths

### 1. The Reactive Read Path
In SwiftUI with SwiftData:
```swift
import SwiftUI
import SwiftData

struct NoteListView: View {
    // UI strictly observes local database!
    @Query(filter: #Predicate<NoteItem> { !$0.isDeleted }, sort: \.updatedAt, order: .reverse)
    private var notes: [NoteItem]

    var body: some View {
        List(notes) { note in
            NoteRow(note: note)
        }
    }
}
```
* When background sync writes new server data into the SwiftData `ModelContext`, SwiftUI automatically calculates diffs and updates the list.

---

### 2. The Write Path: Transactional Outbox & Optimistic Updates

Never execute API calls inside a SwiftUI button action! If the device has no internet or the user kills the app, the write is lost.

```swift
@Model
final class OutboxRecord {
    var id: UUID
    var entityType: String
    var entityId: String
    var mutationType: String // "CREATE", "UPDATE", "DELETE"
    var payloadData: Data
    var createdAt: Date
    var retryCount: Int

    init(entityType: String, entityId: String, mutationType: String, payloadData: Data) {
        self.id = UUID()
        self.entityType = entityType
        self.entityId = entityId
        self.mutationType = mutationType
        self.payloadData = payloadData
        self.createdAt = Date()
        self.retryCount = 0
    }
}

@Model
final class NoteItem {
    @Attribute(.unique) var id: String
    var title: String
    var content: String
    var updatedAt: Date
    var isDeleted: Bool
    var syncStatus: String // "SYNCED", "PENDING_SYNC"
    
    // ...
}
```

### Atomic Repository Mutation:
```swift
@MainActor
final class NoteRepository {
    private let modelContext: ModelContext
    private let syncEngine: SyncEngine

    init(modelContext: ModelContext, syncEngine: SyncEngine) {
        self.modelContext = modelContext
        self.syncEngine = syncEngine
    }

    func saveNoteOptimistically(title: String, content: String) throws {
        let noteId = UUID().uuidString
        let now = Date()

        let note = NoteItem(
            id: noteId,
            title: title,
            content: content,
            updatedAt: now,
            isDeleted: false,
            syncStatus: "PENDING_SYNC"
        )
        
        // 1. Insert note into local DB
        modelContext.insert(note)

        // 2. Insert corresponding mutation into Outbox within same transaction
        let payload = try JSONEncoder().encode(note)
        let outbox = OutboxRecord(
            entityType: "NOTE",
            entityId: noteId,
            mutationType: "CREATE",
            payloadData: payload
        )
        modelContext.insert(outbox)

        try modelContext.save()

        // 3. Trigger immediate sync if network is available
        Task {
            await syncEngine.drainOutbox()
        }
    }
}
```

---

## 🗑️ Deletions: Why You Must Use "Tombstoning"

If a user deletes a note while offline:
- Hard-deleting (`modelContext.delete(note)`) destroys the record locally.
- When the app reconnects to the network and fetches the latest notes from the server (`GET /notes`), the server returns the note that was deleted offline, **resurrecting it on the user's phone!**

### The Solution: Tombstones
1. Set `isDeleted = true` and `syncStatus = "PENDING_DELETE"`.
2. Filter active notes from queries (`!$0.isDeleted`).
3. Outbox sends `DELETE /notes/{id}` to the server.
4. Once the server confirms deletion (HTTP 200/204), hard-delete the tombstone from local storage.

---

## ⚙️ Guaranteed Background Execution: `BackgroundTasks` Framework

iOS restricts background execution heavily to conserve battery. Use the **`BackgroundTasks`** framework (`BGAppRefreshTask` and `BGProcessingTask`) to drain the outbox when the app is suspended:

```swift
import BackgroundTasks

final class BackgroundSyncManager {
    static let shared = BackgroundSyncManager()
    static let syncTaskId = "com.company.app.outbox-sync"

    func registerTasks() {
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: Self.syncTaskId,
            using: nil
        ) { task in
            guard let processingTask = task as? BGProcessingTask else { return }
            self.handleSyncTask(processingTask)
        }
    }

    func scheduleSync() {
        let request = BGProcessingTaskRequest(identifier: Self.syncTaskId)
        request.requiresNetworkConnectivity = true
        request.requiresExternalPower = false
        request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60) // 15 mins

        do {
            try BGTaskScheduler.shared.submit(request)
        } catch {
            print("Failed to schedule background sync: \(error)")
        }
    }

    private func handleSyncTask(_ task: BGProcessingTask) {
        scheduleSync() // Schedule next execution

        let syncOperation = Task {
            await SyncEngine.shared.drainOutbox()
        }

        task.expirationHandler = {
            syncOperation.cancel()
        }

        Task {
            _ = await syncOperation.result
            task.setTaskCompleted(success: true)
        }
    }
}
```

---

## ⚔️ Conflict Resolution Strategies on iOS

When the same note is edited offline on an iPhone and simultaneously edited on a web browser:

| Strategy | Implementation | Tradeoff |
| :--- | :--- | :--- |
| **Last-Write-Wins (LWW)** | Compares ISO-8601 timestamps. Latest timestamp wins. | Simple, but vulnerable to iOS device clock drift (NTP skew). |
| **Lamport Monotonic Clocks** | Monotonically incrementing integer version tag (`version: 4`). | Eliminates physical clock dependency; requires server cooperation. |
| **Field-Level 3-Way Merge** | Compares `BaseVersion`, `ClientDraft`, and `ServerState`. | Auto-merges non-overlapping fields (e.g., Title changed on phone, Body changed on web). |
| **CRDTs (State-based / Op-based)** | Yjs / Automerge algorithms. | True collaborative editing (like Apple Notes); higher memory overhead. |

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "What are the trade-offs of using Apple's CloudKit Sync (`NSPersistentCloudKitContainer`) vs. building a custom REST/GraphQL sync engine?"
* **Answer**:
  - **CloudKit Sync (`NSPersistentCloudKitContainer` / SwiftData CloudKit)**:
    - **Pros:** Zero backend server to build or maintain; handles delta sync, offline queuing, device-to-device push notifications, and cryptographic user security out of the box for free within Apple's ecosystem.
    - **Cons:** Apple-only ecosystem (no Android, Windows, or Web clients without building CloudKit JS web wrappers); zero server-side business logic validation; difficult to execute custom enterprise analytics.
  - **Custom REST/GraphQL Outbox**:
    - **Pros:** Cross-platform parity (iOS, Android, Web share identical database schemas and sync protocols); granular enterprise data governance and fraud validation.
    - **Cons:** High engineering overhead (building conflict resolution, outbox queues, and rate-limiting).

### Q2: "How do you trigger instant background syncing without waiting for Apple's arbitrary `BGTaskScheduler` windows?"
* **Answer**:
  - `BGTaskScheduler` is non-deterministic; iOS runs it based on battery level, user habits, and charging state.
  - To trigger an immediate sync when new server data is available, send a **Silent Remote Push Notification** (`content-available: 1` with no alert, badge, or sound) via APNs.
  - The OS wakes the app in the background for **up to 30 seconds**, during which the app executes `SyncEngine.drainOutbox()`, fetches delta changes, and updates the local SwiftData store.
