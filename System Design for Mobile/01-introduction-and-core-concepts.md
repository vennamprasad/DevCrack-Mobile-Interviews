# System Design for Mobile Engineers

A comprehensive guide to system design for mid to senior-level Android engineers, covering fundamentals, architecture patterns, and real-world examples.

---

## **Table of Contents**

### Part 1: Fundamentals
1. [Introduction to System Design](#introduction-to-system-design)
2. [Core Concepts](#core-concepts)
3. [Scalability](#scalability)
4. [Load Balancing](#load-balancing)
5. [Caching Strategies](#caching-strategies)
6. [Databases](#databases)
7. [API Design](#api-design)
8. [Message Queues](#message-queues)
9. [CDN & Static Content](#cdn--static-content)
10. [Monitoring & Observability](#monitoring--observability)

### Part 2: Mobile-Specific Design
11. [Mobile Architecture Patterns](#mobile-architecture-patterns)
12. [Offline-First Design](#offline-first-design)
13. [Data Synchronization](#data-synchronization)
14. [Push Notifications](#push-notifications)
15. [Mobile Performance Optimization](#mobile-performance-optimization)

### Part 3: Real-World Examples
16. [Design a Chat Application (WhatsApp/Telegram)](#design-a-chat-application)
17. [Design a Social Media Feed (Instagram/Twitter)](#design-a-social-media-feed)
18. [Design a Ride-Sharing App (Uber/Lyft)](#design-a-ride-sharing-app)
19. [Design a Video Streaming App (YouTube/Netflix)](#design-a-video-streaming-app)
20. [Design a Food Delivery App (DoorDash/Uber Eats)](#design-a-food-delivery-app)

---

# Part 1: Fundamentals

## Introduction to System Design

### Q1. What is System Design and why is it important for mobile engineers?

**Answer:**

System design is the process of defining the architecture, components, modules, interfaces, and data flow for a system to satisfy specified requirements.

**Why Mobile Engineers Need System Design:**

<!-- Replaced large corrupted ASCII-art with a clean, simple diagram -->
Architecture overview:

- Mobile Application
  - UI Layer
  - Business Logic
  - Data Layer
  - Network Layer
- API Calls
- Backend System
  - API Gateway
  - Business Logic
  - Database
  - Cache

**Key Responsibilities:**

**1. Understanding Backend Architecture:**
```kotlin
// Mobile engineer needs to understand how backend works
class UserRepository @Inject constructor(
    private val apiService: ApiService,
    private val database: UserDao,
    private val cacheManager: CacheManager
) {
    // Understanding: API � Load Balancer � Server � Database
    suspend fun getUser(userId: String): Result<User> {
        // 1. Check local cache first (fastest)
        cacheManager.get(userId)?.let { return Result.Success(it) }

        // 2. Check local database (offline support)
        database.getUser(userId)?.let {
            cacheManager.put(userId, it)
            return Result.Success(it)
        }

        // 3. Fetch from API (network call)
        return try {
            val user = apiService.getUser(userId)
            database.insert(user)
            cacheManager.put(userId, user)
            Result.Success(user)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}
```

**2. Designing Data Flow:**
```kotlin
// Understanding: How data flows through the system
/*
User Action � ViewModel � Repository � API/Database
     �
  UI Update � StateFlow � Result � Response
*/

@HiltViewModel
class FeedViewModel @Inject constructor(
    private val feedRepository: FeedRepository
) : ViewModel() {

    private val _feedState = MutableStateFlow<FeedState>(FeedState.Loading)
    val feedState: StateFlow<FeedState> = _feedState.asStateFlow()

    fun loadFeed(refresh: Boolean = false) {
        viewModelScope.launch {
            _feedState.value = FeedState.Loading

            // Repository handles: Cache � Database � API
            when (val result = feedRepository.getFeed(refresh)) {
                is Result.Success -> _feedState.value = FeedState.Success(result.data)
                is Result.Error -> _feedState.value = FeedState.Error(result.error)
            }
        }
    }
}
```

**3. Optimizing Performance:**
```kotlin
// Understanding: Network, memory, battery optimization
class ImageRepository @Inject constructor(
    private val imageLoader: ImageLoader,
    private val diskCache: DiskCache,
    private val memoryCache: MemoryCache
) {
    suspend fun loadImage(url: String): Bitmap? {
        // Multi-layer caching strategy
        // L1: Memory Cache (fastest, limited size)
        memoryCache.get(url)?.let { return it }

        // L2: Disk Cache (fast, larger size)
        diskCache.get(url)?.let {
            memoryCache.put(url, it)
            return it
        }

        // L3: Network (slowest, unlimited)
        return downloadAndCache(url)
    }

    private suspend fun downloadAndCache(url: String): Bitmap? {
        return withContext(Dispatchers.IO) {
            val bitmap = imageLoader.download(url)
            bitmap?.let {
                memoryCache.put(url, it)
                diskCache.put(url, it)
            }
            bitmap
        }
    }
}
```

**Why It Matters:**

| Aspect | Impact |
|--------|--------|
| **Performance** | Understanding caching, pagination, lazy loading |
| **Scalability** | Handling growth from 100 to 1M users |
| **Reliability** | Offline support, error handling, retry logic |
| **User Experience** | Fast app, smooth scrolling, instant feedback |
| **Battery Life** | Efficient network calls, background processing |
| **Cost** | Reducing API calls, optimizing bandwidth |

---

## Core Concepts

### Q2. What are the key principles of system design?

**Answer:**

**1. Scalability - Handling Growth:**

<!-- replaced corrupted ASCII-art with simple comparison -->
Vertical Scaling (Scale Up)
- Increase resources on a single machine (CPU, RAM, disk).
- Pros: simple, no code changes. Cons: hardware limits, single point of failure.

Horizontal Scaling (Scale Out)
- Add more machines behind a load balancer.
- Pros: high availability, cost-effective at scale. Cons: added complexity (consistency, orchestration).

**Mobile Implementation:**
```kotlin
// Design for horizontal scaling: Stateless API calls
interface ApiService {
    //  Good: Stateless - can hit any server
    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: String): User

    //  Good: Each request is independent
    @POST("posts")
    suspend fun createPost(
        @Header("Authorization") token: String,  // Auth in request
        @Body post: CreatePostRequest
    ): Post

    // L Bad: Stateful - depends on server session
    // @GET("cart")  // Assumes server remembers your cart
    // suspend fun getCart(): Cart
}

//  Better: Client-side state management
class ShoppingCartManager @Inject constructor(
    private val database: CartDao
) {
    // Store cart locally, sync when needed
    fun addToCart(item: CartItem) {
        database.insert(item)
    }

    suspend fun checkout() {
        val items = database.getAllItems()
        apiService.createOrder(items)  // Send all data in request
    }
}
```

**2. Availability - System Uptime:**

<!-- replaced corrupted diagram with text -->
Availability strategies:
- Use multiple instances behind a load balancer.
- Health checks and automated failover.
- Serve stale/cached data when backend is unavailable.
- Client: fall back to cache and show informative UI.

**Mobile Implementation:**
```kotlin
// Handle server unavailability gracefully
class UserRepository @Inject constructor(
    private val apiService: ApiService,
    private val database: UserDao,
    private val networkMonitor: NetworkMonitor
) {
    suspend fun getUser(userId: String): Result<User> {
        return try {
            // Try primary server
            val user = apiService.getUser(userId)
            database.insert(user)
            Result.Success(user)
        } catch (e: IOException) {
            // Server down, use cached data
            database.getUser(userId)?.let {
                Result.Success(it, fromCache = true)
            } ?: Result.Error(ApiError.NetworkError())
        }
    }
}

// Show appropriate UI based on data source
sealed class DataSource {
    object Live : DataSource()
    object Cached : DataSource()
    object Offline : DataSource()
}

@Composable
fun UserProfile(user: User, source: DataSource) {
    Column {
        if (source is DataSource.Cached) {
            Banner(text = "Showing cached data", color = Yellow)
        }
        // Show user data
    }
}
```

**3. Reliability - Fault Tolerance:**

```kotlin
// Implement retry logic with exponential backoff
class RetryPolicy {
    suspend fun <T> executeWithRetry(
        maxRetries: Int = 3,
        initialDelay: Long = 1000L,
        maxDelay: Long = 10000L,
        factor: Double = 2.0,
        block: suspend () -> T
    ): Result<T> {
        var currentDelay = initialDelay
        var lastException: Exception? = null

        repeat(maxRetries) { attempt ->
            try {
                return Result.Success(block())
            } catch (e: IOException) {
                lastException = e
                if (attempt < maxRetries - 1) {
                    delay(currentDelay)
                    currentDelay = (currentDelay * factor)
                        .toLong()
                        .coerceAtMost(maxDelay)
                }
            }
        }

        return Result.Error(lastException ?: Exception("Max retries exceeded"))
    }
}

// Usage
class FeedRepository @Inject constructor(
    private val apiService: ApiService,
    private val retryPolicy: RetryPolicy
) {
    suspend fun getFeed(): Result<List<Post>> {
        return retryPolicy.executeWithRetry {
            apiService.getFeed()
        }
    }
}
```

**4. Performance - Speed & Efficiency:**

```kotlin
// Optimize with caching, pagination, and prefetching
class FeedRepository @Inject constructor(
    private val apiService: ApiService,
    private val database: PostDao
) {
    // Pagination for large datasets
    fun getFeedPaged(): Flow<PagingData<Post>> {
        return Pager(
            config = PagingConfig(
                pageSize = 20,
                prefetchDistance = 5,  // Prefetch when 5 items from bottom
                enablePlaceholders = false
            ),
            pagingSourceFactory = { FeedPagingSource(apiService, database) }
        ).flow
    }

    // Cache-first strategy
    fun getPost(postId: String): Flow<Post> = flow {
        // Emit cached data immediately (instant UI update)
        database.getPost(postId)?.let { emit(it) }

        // Fetch fresh data in background
        try {
            val freshPost = apiService.getPost(postId)
            database.insert(freshPost)
            emit(freshPost)  // Emit updated data
        } catch (e: Exception) {
            // Cache is still valid even if network fails
        }
    }
}
```

**5. Maintainability - Clean Architecture:**

```kotlin
// Separate concerns for easy testing and modification

// Data Layer - How to get data
interface UserRepository {
    suspend fun getUser(id: String): Result<User>
}

class UserRepositoryImpl @Inject constructor(
    private val remoteDataSource: UserRemoteDataSource,
    private val localDataSource: UserLocalDataSource
) : UserRepository {
    override suspend fun getUser(id: String): Result<User> {
        // Implementation details hidden from other layers
        return remoteDataSource.getUser(id)
            .also { localDataSource.cacheUser(it) }
    }
}

// Domain Layer - Business logic
class GetUserUseCase @Inject constructor(
    private val repository: UserRepository
) {
    suspend operator fun invoke(id: String): Result<User> {
        return repository.getUser(id)
    }
}

// Presentation Layer - UI logic
@HiltViewModel
class UserViewModel @Inject constructor(
    private val getUserUseCase: GetUserUseCase
) : ViewModel() {
    fun loadUser(id: String) {
        viewModelScope.launch {
            when (val result = getUserUseCase(id)) {
                is Result.Success -> updateUi(result.data)
                is Result.Error -> showError(result.error)
            }
        }
    }
}
```

**6. Security - Data Protection:**

```kotlin
// Secure communication and data storage
@Module
@InstallIn(SingletonComponent::class)
object SecurityModule {

    @Provides
    @Singleton
    fun provideSecureOkHttpClient(
        authInterceptor: AuthInterceptor,
        certificatePinner: CertificatePinner
    ): OkHttpClient {
        return OkHttpClient.Builder()
            // HTTPS only
            .addInterceptor(authInterceptor)

            // Certificate pinning
            .certificatePinner(certificatePinner)

            // TLS 1.2+
            .connectionSpecs(listOf(ConnectionSpec.MODERN_TLS))

            // Timeout for security
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)

            .build()
    }

    @Provides
    @Singleton
    fun provideCertificatePinner(): CertificatePinner {
        return CertificatePinner.Builder()
            .add("api.example.com", "sha256/AAAA...")
            .add("api.example.com", "sha256/BBBB...")  // Backup pin
            .build()
    }
}

// Secure local storage
class SecureStorage @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val encryptedPrefs = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveToken(token: String) {
        encryptedPrefs.edit { putString("auth_token", token) }
    }
}
```

---

