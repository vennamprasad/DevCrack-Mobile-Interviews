# 📶 Level 1: Offline-First Mobile System Design

> **Architecting resilient offline-first mobile applications: Single Source of Truth (SSOT), optimistic UI updates, the Transactional Outbox Pattern, conflict resolution (LWW vs. CRDTs), and two-way sync with Room and WorkManager.**

---

## 📌 Executive Summary & Interview Framing

In a Senior or Staff Mobile System Design interview, **"Design an Offline-First Application"** (e.g., Google Keep, Slack, or an offline-capable E-commerce app) is one of the most frequently asked problems.

The key to passing this round is avoiding the rookie mistake: **making network calls directly from ViewModels and caching the response as an afterthought**. 

A true offline-first system guarantees:
1. **Zero-Latency Interactions**: The UI immediately reflects user actions without waiting for a server round-trip.
2. **Deterministic State Synchronization**: State is driven exclusively by a local database as the **Single Source of Truth (SSOT)**.
3. **Guaranteed Eventual Delivery**: Local mutations are queued and reliably synced via background work, even across process kills or device reboots.

---

## 🏗️ The Single Source of Truth (SSOT) Architecture

```
                    ┌──────────────────────────────────────────────┐
                    │               UI Layer (Compose)             │
                    └──────────────┬───────────────────────────────┘
                                   ▲
                         (Observes Flow<List<Item>>)
                                   │
                    ┌──────────────┴───────────────────────────────┐
                    │       Local Database (Room / SQLite)         │
                    │         "Single Source of Truth"             │
                    └──────────────▲──────────────┬────────────────┘
                                   │              │
                   (Writes Data)   │              │ (Queries Pending Mutations)
                                   │              ▼
┌──────────────────────────────────┴──────────────┴───────────────────────────────┐
│                           Repository & Sync Engine                              │
│                                                                                 │
│   [ Local Mutation ] ──> [ Write to DB ] ──> [ Insert into Outbox Table ]       │
│                                                                │                │
│                                                     (WorkManager Trigger)       │
│                                                                ▼                │
│   [ Network Fetch ]  <── [ Sync Worker ] <── [ Dequeue & Batch Dispatch ]       │
└──────────────────────────────────┬──────────────────────────────────────────────┘
                                   │ (HTTPS / gRPC)
                                   ▼
                    ┌──────────────────────────────┐
                    │         Backend API          │
                    └──────────────────────────────┘
```

---

## 🔄 The Read and Write Paths

### 1. The Read Path (Unidirectional Reactive Stream)
* The UI **never** reads from the network directly.
* The UI observes a reactive query from the local database:
  ```kotlin
  @Dao
  interface NoteDao {
      @Query("SELECT * FROM notes WHERE is_deleted = 0 ORDER BY updated_at DESC")
      fun observeActiveNotes(): Flow<List<NoteEntity>>
  }
  ```
* When network data arrives, it is written directly into the database. The Room library automatically re-emits the updated dataset through the `Flow`, re-rendering the UI seamlessly.

---

### 2. The Write Path: The Transactional Outbox Pattern & Optimistic Updates

If a user edits a note or taps "Like" while on an airplane:
1. **Immediate Local Mutation (Optimistic Update)**:
   - Update the local item in the `notes` table with a temporary state (`sync_status = "PENDING_UPDATE"`).
   - Insert a mutation record into the **Outbox Table** within the **same atomic database transaction**.
2. **UI Reflection**: Because the local database was updated, the UI updates within 16ms (60fps), giving the user a fast, native experience.
3. **Background Dispatch**: Enqueue a unique WorkManager task to drain the outbox.

```kotlin
@Database(entities = [NoteEntity::class, OutboxEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun noteDao(): NoteDao
    abstract fun outboxDao(): OutboxDao

    // Atomic transaction ensuring outbox and data never go out of sync
    suspend fun saveNoteOptimistically(note: NoteEntity, mutationType: MutationType) {
        withTransaction {
            noteDao().insertOrUpdate(note.copy(syncStatus = SyncStatus.PENDING))
            outboxDao().insert(
                OutboxEntity(
                    entityId = note.id,
                    entityType = "NOTE",
                    mutationType = mutationType,
                    payloadJson = Json.encodeToString(note),
                    createdAt = System.currentTimeMillis()
                )
            )
        }
    }
}
```

---

## 🗑️ Deletions: Why You Must Use "Tombstoning"

In offline-first architectures, **hard-deleting a row from the local SQLite database (`DELETE FROM notes WHERE id = ?`) is a fatal design flaw**:
- If you delete the local record while offline, when the app connects to the internet and performs a `GET /notes` sync, the server doesn't know you deleted it and **re-downloads the old note**, resurrecting the deleted item!

### The Tombstone Pattern:
Instead of `DELETE`, set a soft-deletion flag:
```sql
UPDATE notes SET is_deleted = 1, updated_at = :now, sync_status = 'PENDING_DELETE' WHERE id = :id;
```
1. Filter out tombstoned items from the UI queries (`WHERE is_deleted = 0`).
2. When the background sync worker contacts the backend (`DELETE /notes/{id}`):
   - The backend marks the note as deleted.
   - Once the server acknowledges (HTTP 200), the app safely hard-deletes the tombstone locally.

---

## ⚔️ Conflict Resolution Strategies

What happens when User A edits Note 1 while offline on their tablet, while User A (or a collaborator) edits Note 1 on their laptop?

```
Device (Offline):  "Buy Milk and Eggs" (Local Time: 10:02 AM)
Server (Online):  "Buy Milk and Bread" (Server Time: 10:01 AM)
```

| Strategy | Mechanism | Pros & Cons | Production Use Case |
| :--- | :--- | :--- | :--- |
| **1. Last-Write-Wins (LWW)** | Compare timestamps; highest timestamp overwrites. | **Pro:** Trivial to implement.<br>**Con:** High risk of data loss; vulnerable to client clock drift (NTP skew). | Simple profile field edits (e.g., updating user bio or display name). |
| **2. Lamport / Vector Clocks** | Logical monotonic version counters incremented on every edit. | **Pro:** Eliminates dependency on physical wall-clock time.<br>**Con:** Requires version metadata exchange on every request. | Multi-device sync (e.g., Notion, Evernote). |
| **3. Client-Side 3-Way Merge** | Compares `Base`, `Client`, and `Server` diffs. | **Pro:** Merges non-overlapping field changes automatically.<br>**Con:** Complex logic; requires storing the baseline snapshot. | Complex enterprise forms, multi-field record edits. |
| **4. User Prompt (Manual)** | Detect conflict and prompt user: "Keep local or server version?" | **Pro:** Zero accidental data destruction.<br>**Con:** Poor UX; interrupts user workflow. | Critical documents, financial records. |
| **5. CRDTs (Conflict-Free Replicated Data Types)** | Mathematically provable convergence (State-based or Operation-based). | **Pro:** Seamless collaborative editing without central locking.<br>**Con:** Memory/storage overhead (growing tombstones). | Collaborative tools (Google Docs, Figma, Apple Notes). |

---

## ⚙️ Guaranteed Delivery with Android WorkManager

Never use coroutines launched in `viewModelScope` to sync data with the backend; if the user backgrounds or swipes away the app, Android will kill the process and abandon the request.

Use **WorkManager** with constraints and exponential backoff:

```kotlin
class SyncOutboxWorker(
    appContext: Context,
    workerParams: WorkerParameters,
    private val db: AppDatabase,
    private val api: NotesApi
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val pendingMutations = db.outboxDao().getOldestPendingMutations(batchSize = 20)

        if (pendingMutations.isEmpty()) {
            return@withContext Result.success()
        }

        for (mutation in pendingMutations) {
            try {
                when (mutation.mutationType) {
                    MutationType.UPSERT -> {
                        val response = api.syncNote(mutation.payloadJson)
                        if (response.isSuccessful) {
                            db.withTransaction {
                                db.outboxDao().deleteById(mutation.id)
                                db.noteDao().markAsSynced(mutation.entityId)
                            }
                        } else if (response.code() == 409) {
                            // Conflict detected! Trigger merge strategy
                            handleConflict(mutation, response.errorBody())
                        } else {
                            // 5xx Server Error -> Retry with exponential backoff
                            return@withContext Result.retry()
                        }
                    }
                    MutationType.DELETE -> {
                        api.deleteNote(mutation.entityId)
                        db.outboxDao().deleteById(mutation.id)
                        db.noteDao().hardDelete(mutation.entityId)
                    }
                }
            } catch (e: IOException) {
                // Network unreachable -> Auto-retry when connection restores
                return@withContext Result.retry()
            }
        }

        Result.success()
    }
}
```

### Scheduling with Network Constraints
```kotlin
val syncConstraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED)
    .build()

val syncWorkRequest = OneTimeWorkRequestBuilder<SyncOutboxWorker>()
    .setConstraints(syncConstraints)
    .setBackoffCriteria(
        BackoffPolicy.EXPONENTIAL,
        WorkRequest.MIN_BACKOFF_MILLIS, // 10 seconds
        TimeUnit.MILLISECONDS
    )
    .build()

WorkManager.getInstance(context).enqueueUniqueWork(
    "outbox_sync_work",
    ExistingWorkPolicy.APPEND_OR_REPLACE,
    syncWorkRequest
)
```

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How do you generate unique IDs for new records created offline without colliding with IDs generated by other users or the server?"
* **Answer**:
  - **Never use auto-incrementing integer IDs** (e.g., `1, 2, 3...`) in offline-first applications. If Device A creates item #5 offline and Device B creates item #5 offline, sync will collide catastrophically.
  - **Solution**: Use **UUID v4** or **UUID v7** (time-ordered UUIDs) or **ULIDs** (Universally Unique Lexicographically Sortable Identifiers) generated directly on the mobile client.
  - Client-generated UUIDs are globally unique with near-zero probability of collision and allow the app to establish relationships between child records (e.g., attaching an image to a note) completely offline before any network connection exists.

### Q2: "How do you handle pagination in an offline-first app where local database items and server items might diverge?"
* **Answer**:
  - Standard offset-based pagination (`page=2&limit=20`) breaks when local insertions shift offsets.
  - **Architecture Solution**:
    1. Implement **Cursor-based pagination** using an immutable, monotonic sort key (e.g., `(created_at, id)`).
    2. Maintain a separate `RemoteKeys` table in Room to store the `prevKey` and `nextKey` cursors for each item (standard Jetpack `RemoteMediator` pattern).
    3. The UI queries Room via `PagingSource`. When the user scrolls near the end, `RemoteMediator` fetches the next cursor batch from the network, inserts it into Room within a transaction, and the UI paginates seamlessly from disk.
