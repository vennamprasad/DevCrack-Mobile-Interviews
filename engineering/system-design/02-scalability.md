# 📈 Scalability
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Learn how to design systems that grow with user demand.

![Scalability](https://img.shields.io/badge/Concept-Scalability-orange?style=for-the-badge&logo=googlecloud&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Scale Up vs Scale Out](#types-of-scalability)
- [2. Mobile Implementation](#mobile-client-considerations-for-scalable-backend)
- [3. Database Sharding](#database-scalability-patterns)

---

### Q3. What is scalability and how do you design for it?

**Answer:**

**Types of Scalability:**

**1. Vertical Scaling (Scale Up):**
- Example: upgrade a server from 4 CPU / 8GB RAM to 16 CPU / 64GB RAM.
- Pros: quick and simple. Cons: finite, expensive.

**2. Horizontal Scaling (Scale Out):**
- Example: run many smaller servers behind a load balancer.
- Pros: better fault tolerance and near-unlimited growth. Cons: more complex (data partitioning, coordination).

**Mobile Client Considerations for Scalable Backend:**

```kotlin
// 1. Design for eventual consistency
class MessageRepository @Inject constructor(
    private val apiService: ApiService,
    private val database: MessageDao,
    private val syncManager: SyncManager
) {
    // Send message optimistically
    suspend fun sendMessage(message: Message): Result<Message> {
        // 1. Save locally first (instant feedback)
        val localMessage = message.copy(
            id = UUID.randomUUID().toString(),
            status = MessageStatus.SENDING,
            timestamp = System.currentTimeMillis()
        )
        database.insert(localMessage)

        // 2. Sync to server in background
        return try {
            val serverMessage = apiService.sendMessage(localMessage)
            // 3. Update with server response
            database.update(serverMessage.copy(status = MessageStatus.SENT))
            Result.Success(serverMessage)
        } catch (e: Exception) {
            // 4. Mark as failed, retry later
            database.update(localMessage.copy(status = MessageStatus.FAILED))
            syncManager.scheduleRetry(localMessage.id)
            Result.Error(e)
        }
    }

    // UI shows optimistic update immediately
    fun getMessages(): Flow<List<Message>> {
        return database.getMessagesFlow()
            .map { messages ->
                messages.sortedByDescending { it.timestamp }
            }
    }
}

// 2. Implement client-side load balancing awareness
class ApiConfig {
    // Multiple API endpoints for redundancy
    val endpoints = listOf(
        "https://api-us-east.example.com",
        "https://api-us-west.example.com",
        "https://api-eu.example.com"
    )

    // Choose based on latency
    suspend fun getFastestEndpoint(): String {
        return endpoints.minByOrNull { endpoint ->
            measureLatency(endpoint)
        } ?: endpoints.first()
    }

    private suspend fun measureLatency(endpoint: String): Long {
        val start = System.currentTimeMillis()
        try {
            apiService.ping(endpoint)
        } catch (e: Exception) {
            return Long.MAX_VALUE
        }
        return System.currentTimeMillis() - start
    }
}

// 3. Handle rate limiting gracefully
class RateLimitHandler @Inject constructor(
    private val apiService: ApiService
) {
    suspend fun <T> executeWithRateLimit(
        block: suspend () -> T
    ): Result<T> {
        return try {
            Result.Success(block())
        } catch (e: HttpException) {
            when (e.code()) {
                429 -> {  // Too Many Requests
                    val retryAfter = e.response()
                        ?.headers()
                        ?.get("Retry-After")
                        ?.toLongOrNull() ?: 60

                    // Show user friendly message
                    Result.Error(
                        RateLimitException("Please try again in $retryAfter seconds")
                    )
                }
                else -> Result.Error(e)
            }
        }
    }
}

// 4. Batch requests to reduce server load
class BatchRequestManager @Inject constructor(
    private val apiService: ApiService
) {
    private val pendingUserIds = mutableListOf<String>()
    private val batchJob: Job? = null

    suspend fun getUser(userId: String): User {
        pendingUserIds.add(userId)

        // Wait for more requests or timeout
        delay(100)  // Collect requests for 100ms

        if (pendingUserIds.size >= 10 || batchJob?.isCompleted == true) {
            val ids = pendingUserIds.toList()
            pendingUserIds.clear()

            // Single batch request instead of multiple individual requests
            val users = apiService.getUsersBatch(ids)
            return users.first { it.id == userId }
        }

        return getUser(userId)  // Continue collecting
    }
}

// API for batch request
interface ApiService {
    @POST("users/batch")
    suspend fun getUsersBatch(@Body userIds: List<String>): List<User>
}
```

**Database Scalability Patterns:**

```kotlin
// 1. Database Sharding (Split data across databases)
class UserRepository @Inject constructor(
    private val userShardManager: UserShardManager
) {
    suspend fun getUser(userId: String): User {
        // Determine which database shard has this user
        val shard = userShardManager.getShardForUser(userId)
        return shard.getUser(userId)
    }
}

class UserShardManager {
    private val shards = listOf(
        DatabaseShard("shard_1", userIds = 0..1000000),
        DatabaseShard("shard_2", userIds = 1000001..2000000),
        DatabaseShard("shard_3", userIds = 2000001..3000000)
    )

    fun getShardForUser(userId: String): DatabaseShard {
        val userIdNum = userId.hashCode().absoluteValue
        return shards.first { userIdNum in it.userIds }
    }
}

// 2. Read Replicas (Scale reads)
/*
Primary Database (Writes)
         ↓
          (Replication)
        ↙       ↘
                  
Read Replica 1   Read Replica 2
(Reads only)     (Reads only)
*/

class UserRepository @Inject constructor(
    private val primaryDb: UserDao,  // For writes
    private val readReplicaDb: UserDao  // For reads
) {
    // Write to primary
    suspend fun createUser(user: User) {
        primaryDb.insert(user)
    }

    // Read from replica (reduces load on primary)
    suspend fun getUser(userId: String): User {
        return readReplicaDb.getUser(userId)
    }
}
```

<!-- replace corrupted read-replica diagram with plain text -->
Read replicas:
- Primary handles writes; replicas handle reads.
- Replica lag should be considered for read-after-write semantics.
- Use replicas to reduce load on the primary for read-heavy endpoints.
