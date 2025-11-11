## Caching Strategies

### Q5. What are different caching strategies and when to use each?

**Answer:**

**Cache Levels (simplified):**
- L1: Memory cache (in-process, fastest, clears on app exit).
- L2: Disk cache (persistent across restarts, slower).
- L3: Local DB (Room/SQLite, structured, queryable).
- L4: CDN (edge caches for static assets).
- L5: Server / API cache (origin caching, TTL controlled).

**1. Memory Cache Implementation:**
```kotlin
class MemoryCache<K, V>(
    private val maxSize: Int = 100
) {
    private val cache = object : LinkedHashMap<K, V>(maxSize, 0.75f, true) {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<K, V>): Boolean {
            return size > maxSize
        }
    }

    @Synchronized
    fun get(key: K): V? = cache[key]

    @Synchronized
    fun put(key: K, value: V) {
        cache[key] = value
    }

    @Synchronized
    fun remove(key: K) {
        cache.remove(key)
    }

    @Synchronized
    fun clear() {
        cache.clear()
    }

    fun size() = cache.size
}

// Usage for user profiles
class UserCache @Inject constructor() {
    private val memoryCache = MemoryCache<String, User>(maxSize = 50)

    fun getUser(userId: String): User? {
        return memoryCache.get(userId)
    }

    fun cacheUser(user: User) {
        memoryCache.put(user.id, user)
    }
}
```

**2. Disk Cache (Coil/Glide for Images):**
```kotlin
// Image caching with Coil
@Provides
@Singleton
fun provideImageLoader(
    @ApplicationContext context: Context,
    okHttpClient: OkHttpClient
): ImageLoader {
    return ImageLoader.Builder(context)
        .okHttpClient(okHttpClient)
        .memoryCache {
            MemoryCache.Builder(context)
                .maxSizePercent(0.25)  // 25% of app memory
                .build()
        }
        .diskCache {
            DiskCache.Builder()
                .directory(context.cacheDir.resolve("image_cache"))
                .maxSizeBytes(50 * 1024 * 1024)  // 50 MB
                .build()
        }
        .build()
}

// Usage in Compose
@Composable
fun UserAvatar(imageUrl: String) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(imageUrl)
            .crossfade(true)
            .memoryCachePolicy(CachePolicy.ENABLED)
            .diskCachePolicy(CachePolicy.ENABLED)
            .build(),
        contentDescription = "Avatar"
    )
}
```

**3. Database Cache (Room):**
```kotlin
@Entity(tableName = "posts")
data class PostEntity(
    @PrimaryKey val id: String,
    val userId: String,
    val content: String,
    val imageUrl: String?,
    val likesCount: Int,
    val timestamp: Long,
    val cachedAt: Long = System.currentTimeMillis()
)

@Dao
interface PostDao {
    @Query("SELECT * FROM posts ORDER BY timestamp DESC")
    fun getAllPosts(): Flow<List<PostEntity>>

    @Query("SELECT * FROM posts WHERE id = :postId")
    suspend fun getPost(postId: String): PostEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(posts: List<PostEntity>)

    @Query("DELETE FROM posts WHERE cachedAt < :threshold")
    suspend fun deleteOldCache(threshold: Long)

    @Query("DELETE FROM posts")
    suspend fun clearCache()
}

// Repository with cache
class PostRepository @Inject constructor(
    private val apiService: ApiService,
    private val database: PostDao
) {
    fun getPosts(forceRefresh: Boolean = false): Flow<List<Post>> = flow {
        // Emit cached data first (instant UI)
        database.getAllPosts().first().let { cached ->
            if (cached.isNotEmpty()) {
                emit(cached.map { it.toDomain() })
            }
        }

        // Fetch fresh data if needed
        if (forceRefresh || cached.isEmpty() || isCacheStale(cached)) {
            try {
                val fresh = apiService.getPosts()
                database.insertAll(fresh.map { it.toEntity() })
                emit(fresh.map { it.toDomain() })  // Emit fresh data
            } catch (e: Exception) {
                // Use cache on error
                if (cached.isEmpty()) throw e
            }
        }
    }

    private fun isCacheStale(cached: List<PostEntity>): Boolean {
        val oldestCache = cached.minOfOrNull { it.cachedAt } ?: return true
        val staleThreshold = System.currentTimeMillis() - (5 * 60 * 1000)  // 5 minutes
        return oldestCache < staleThreshold
    }
}
```

**Cache Strategies:**

**1. Cache-Aside (Lazy Loading):**
```kotlin
/*
Flow:
1. App requests data
2. Check cache first
3. If found (cache hit): return cached data
4. If not found (cache miss): fetch from API � cache it � return

Best for: Read-heavy workloads
*/

class UserRepository @Inject constructor(
    private val apiService: ApiService,
    private val userDao: UserDao,
    private val memoryCache: UserCache
) {
    suspend fun getUser(userId: String): Result<User> {
        // 1. Check memory cache
        memoryCache.getUser(userId)?.let {
            return Result.Success(it, source = DataSource.Memory)
        }

        // 2. Check database cache
        userDao.getUser(userId)?.let {
            memoryCache.cacheUser(it)
            return Result.Success(it, source = DataSource.Disk)
        }

        // 3. Fetch from API
        return try {
            val user = apiService.getUser(userId)
            memoryCache.cacheUser(user)
            userDao.insert(user)
            Result.Success(user, source = DataSource.Network)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}
```

**2. Read-Through Cache:**
```kotlin
/*
Flow:
1. App requests data from cache
2. Cache fetches from API if not present
3. Cache returns data

Best for: Simplifying client code
*/

class CachingUserRepository @Inject constructor(
    private val apiService: ApiService,
    private val userDao: UserDao
) {
    // Single method handles everything
    suspend fun getUser(userId: String): User {
        return userDao.getUser(userId) ?: run {
            val user = apiService.getUser(userId)
            userDao.insert(user)
            user
        }
    }
}
```

**3. Write-Through Cache:**
```kotlin
/*
Flow:
1. App writes data
2. Update cache immediately
3. Then update database/API

Best for: Write consistency
*/

class PostRepository @Inject constructor(
    private val apiService: ApiService,
    private val postDao: PostDao,
    private val memoryCache: PostCache
) {
    suspend fun createPost(post: Post): Result<Post> {
        return try {
            // 1. Write to API
            val createdPost = apiService.createPost(post)

            // 2. Update cache immediately
            memoryCache.put(createdPost.id, createdPost)
            postDao.insert(createdPost)

            Result.Success(createdPost)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}
```

**4. Write-Behind (Write-Back) Cache:**
```kotlin
/*
Flow:
1. App writes to cache
2. Return immediately (fast)
3. Sync to server in background (eventually consistent)

Best for: Offline-first apps, high write frequency
*/

class MessageRepository @Inject constructor(
    private val apiService: ApiService,
    private val messageDao: MessageDao,
    private val syncManager: SyncManager
) {
    suspend fun sendMessage(message: Message): Result<Message> {
        // 1. Save locally immediately
        val localMessage = message.copy(
            id = UUID.randomUUID().toString(),
            status = MessageStatus.PENDING,
            localTimestamp = System.currentTimeMillis()
        )
        messageDao.insert(localMessage)

        // 2. Return success immediately (optimistic)
        viewModelScope.launch {
            // 3. Sync to server in background
            try {
                val serverMessage = apiService.sendMessage(localMessage)
                messageDao.update(serverMessage.copy(status = MessageStatus.SENT))
            } catch (e: Exception) {
                messageDao.update(localMessage.copy(status = MessageStatus.FAILED))
                syncManager.scheduleRetry(localMessage.id)
            }
        }

        return Result.Success(localMessage)
    }
}
```

**5. Time-Based Expiration (TTL):**
```kotlin
data class CachedData<T>(
    val data: T,
    val timestamp: Long,
    val ttl: Long = 5 * 60 * 1000  // 5 minutes default
) {
    fun isExpired(): Boolean {
        return System.currentTimeMillis() - timestamp > ttl
    }
}

class TTLCache<K, V>(
    private val defaultTtl: Long = 5 * 60 * 1000
) {
    private val cache = mutableMapOf<K, CachedData<V>>()

    @Synchronized
    fun get(key: K): V? {
        val cached = cache[key] ?: return null

        return if (cached.isExpired()) {
            cache.remove(key)
            null
        } else {
            cached.data
        }
    }

    @Synchronized
    fun put(key: K, value: V, ttl: Long = defaultTtl) {
        cache[key] = CachedData(
            data = value,
            timestamp = System.currentTimeMillis(),
            ttl = ttl
        )
    }
}

// Usage
class FeedRepository @Inject constructor(
    private val apiService: ApiService
) {
    private val feedCache = TTLCache<String, List<Post>>(
        defaultTtl = 2 * 60 * 1000  // 2 minutes for feed
    )

    suspend fun getFeed(userId: String): List<Post> {
        // Check cache with TTL
        feedCache.get(userId)?.let { return it }

        // Fetch and cache
        val feed = apiService.getFeed(userId)
        feedCache.put(userId, feed)
        return feed
    }
}
```

**Cache Invalidation Strategies:**

```kotlin
class CacheManager @Inject constructor(
    private val postDao: PostDao,
    private val userDao: UserDao,
    private val memoryCache: MemoryCache
) {
    // 1. Time-based invalidation
    suspend fun clearExpiredCache() {
        val threshold = System.currentTimeMillis() - (24 * 60 * 60 * 1000)  // 24 hours
        postDao.deleteOldCache(threshold)
    }

    // 2. Event-based invalidation
    fun invalidateUser(userId: String) {
        memoryCache.remove("user_$userId")
        viewModelScope.launch {
            userDao.delete(userId)
        }
    }

    // 3. Size-based eviction (LRU)
    class LRUCache<K, V>(private val maxSize: Int) {
        private val cache = object : LinkedHashMap<K, V>(maxSize, 0.75f, true) {
            override fun removeEldestEntry(eldest: MutableMap.MutableEntry<K, V>): Boolean {
                return size > maxSize
            }
        }
    }

    // 4. Clear all cache (user logout)
    suspend fun clearAllCache() {
        memoryCache.clear()
        postDao.clearCache()
        userDao.clearCache()
    }

    // 5. Selective invalidation
    suspend fun invalidatePostsByUser(userId: String) {
        postDao.deleteByUser(userId)
    }
}
```

**Cache Performance Monitoring:**

```kotlin
class CacheMetrics @Inject constructor(
    private val analytics: Analytics
) {
    private var cacheHits = 0
    private var cacheMisses = 0

    fun recordCacheHit(cacheType: String) {
        cacheHits++
        analytics.logEvent("cache_hit") {
            param("cache_type", cacheType)
        }
    }

    fun recordCacheMiss(cacheType: String) {
        cacheMisses++
        analytics.logEvent("cache_miss") {
            param("cache_type", cacheType)
        }
    }

    fun getCacheHitRate(): Float {
        val total = cacheHits + cacheMisses
        return if (total > 0) cacheHits.toFloat() / total else 0f
    }

    fun reportMetrics() {
        val hitRate = getCacheHitRate()
        analytics.logEvent("cache_metrics") {
            param("hit_rate", hitRate)
            param("total_hits", cacheHits)
            param("total_misses", cacheMisses)
        }

        // Alert if hit rate is low
        if (hitRate < 0.7) {
            analytics.logEvent("low_cache_hit_rate") {
                param("hit_rate", hitRate)
            }
        }
    }
}
```

**Best Practices:**

| Strategy | Use Case | TTL | Invalidation |
|----------|----------|-----|--------------|
| **Memory Cache** | Hot data, user session | App lifetime | Manual |
| **Disk Cache** | Images, assets | Days/weeks | Size-based (LRU) |
| **Database** | Structured data | Hours/days | Time or event-based |
| **CDN** | Static content | Months | Version-based |
| **API Cache** | Dynamic data | Minutes | Event-based |

---

