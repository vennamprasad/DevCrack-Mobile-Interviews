# Kotlin Coroutines
Coroutines in Kotlin are lightweight, asynchronous programming constructs that simplify concurrency by allowing developers to write sequential-looking code while avoiding callback hell. They are managed by Kotlin’s runtime (not OS threads), making them efficient for tasks like network calls or database operations. Coroutines integrate with Android’s lifecycle (via viewModelScope or lifecycleScope) to ensure structured concurrency and prevent memory leaks.

## 1. Coroutine Scopes
**What They Are:**  
Scopes define the lifecycle and context of coroutines. Structured concurrency ensures coroutines are canceled when their parent scope ends.  

**GlobalScope**:  
- **Use Case**: Launches coroutines outside any lifecycle (e.g., background tasks that outlive an Activity).  
- **Caution**: Avoid in Android apps (manual cancellation required; risk of memory leaks).  
- **Example**:  
  ```kotlin  
  GlobalScope.launch {  
      delay(1000L)  
      println("GlobalScope: Not tied to lifecycle")  
  }  
  ```  
**runBlocking**:  
- **Use Case**: Blocks the current thread until coroutines finish (used in `main()` or tests).  
- **Example**:  
  ```kotlin  
  fun main() = runBlocking {  
      launch {  
          delay(500L)  
          println("runBlocking: Main thread waits")  
      }  
  }  
  ```  

**lifecycleScope (Android)**:  
- **Use Case**: Tied to an Activity/Fragment lifecycle. Auto-canceled when destroyed.  
- **Why It Matters**: Prevents memory leaks (no manual cancellation needed).  
- **Example**:  
  ```kotlin  
  class MyActivity : AppCompatActivity() {  
      override fun onCreate(savedInstanceState: Bundle?) {  
          lifecycleScope.launch {  
              fetchData() // Auto-canceled when Activity is destroyed  
          }  
      }  
  }  
  ```  

**viewModelScope**:  
- **Use Case**: Tied to ViewModel lifecycle. Auto-canceled when ViewModel is cleared.  
- **Why It Matters**: Ensures lifecycle-safe operations (e.g., long-running tasks in ViewModels).  
- **Example**:  
  ```kotlin  
  class MyViewModel : ViewModel() {  
      init {  
          viewModelScope.launch {  
              fetchData() // Auto-canceled when ViewModel is cleared  
          }  
      }  
  }  
  ```  

---

### **2. `delay()` vs. `Thread.sleep()`**  
**`delay()`**:  
- **Behavior**: Suspends the coroutine without blocking the thread.  
- **Use Case**: Non-blocking delays (e.g., animations, timed UI updates).  
- **Example**:  
  ```kotlin  
  launch {  
      delay(1000L)  
      println("Non-blocking delay")  
  }  
  ```  

**`Thread.sleep()`**:  
- **Behavior**: Blocks the entire thread (not coroutine-aware).  
- **Caution**: Avoid on the main thread (causes ANRs in Android).  

---

### **3. Coroutine Cancellation When Main Thread Ends**  
**Problem**:  
Coroutines in `GlobalScope` outlive the main thread unless explicitly canceled.  

**Solution with `runBlocking`**:  
```kotlin  
fun main() = runBlocking {  
    launch {  
        delay(1000L)  
        println("runBlocking ensures this runs")  
    }  
    delay(1500L) // Keep scope alive  
}  
```  
**Why It Works**: `runBlocking` keeps the main thread alive until all child coroutines finish.  

---

### **4. `runBlocking` Explained**  
**Purpose**:  
Bridges blocking and suspending code. Blocks the thread until all child coroutines finish.  

**Example**:  
```kotlin  
fun main() = runBlocking {  
    launch(Dispatchers.IO) {  
        // Background task  
        println("IO Dispatcher: ${Thread.currentThread().name}")  
    }  
    println("Main thread blocked until child completes")  
}  
```  
**Why It Matters**: Essential for testing or blocking the main thread until async work completes.  

---

### **5. `launch(Dispatchers.IO)` in `runBlocking`**  
**`Dispatchers.IO`**:  
- **Use Case**: For blocking IO tasks (e.g., disk/network).  
- **Example**:  
  ```kotlin  
  launch(Dispatchers.IO) {  
      val result = fetchDataFromNetwork()  
      println("Result: $result")  
  }  
  ```  
**Why It Matters**: Prevents blocking the main thread (critical for Android UI responsiveness).  

---

### **6. Job, withTimeout, and Cancellation**  
**`Job` Interface**:  
- **Function**: Manages coroutine lifecycle (cancel, join).  
- **Example**:  
  ```kotlin  
  val job = launch {  
      repeat(1000) { i ->  
          println("Job: $i")  
          delay(500L)  
      }  
  }  
  job.cancel() // Cancel after 1.2s  
  ```  

**`withTimeout`**:  
- **Use Case**: Cancels coroutines exceeding a time limit.  
- **Example**:  
  ```kotlin  
  withTimeout(1300L) {  
      repeat(1000) {  
          delay(400L)  
          println("This repeats until timeout")  
      }  
  }  
  ```  

---

### **7. `async/await` for Concurrent Tasks**  
**`async`**:  
- **Use Case**: Runs tasks concurrently and returns a result.  
- **Example**:  
  ```kotlin  
  val result1 = async { fetchUser() }  
  val result2 = async { fetchOrders() }  
  println("Combined Result: ${result1.await()} + ${result2.await()}")  
  ```  
**Why It Matters**: Efficiently combines results from multiple network/API calls.  

---

### **8. `lifecycleScope` & `viewModelScope` in Android**  
**`lifecycleScope`**:  
- **Use Case**: Tied to Activity/Fragment lifecycle. Auto-canceled when destroyed.  
- **Example**:  
  ```kotlin  
  lifecycleScope.launch {  
      val data = fetchData()  
      updateUI(data)  
  }  
  ```  

**`viewModelScope`**:  
- **Use Case**: Tied to ViewModel lifecycle. Auto-canceled when cleared.  
- **Example**:  
  ```kotlin  
  viewModelScope.launch {  
      val result = processInBackground()  
      _uiState.value = result  
  }  
  ```  

---

### **Best Practices**  
1. **Avoid `GlobalScope`**: Use lifecycle-aware scopes to prevent memory leaks.  
2. **Use Appropriate Dispatchers**:  
   - `Dispatchers.Main` for UI updates.  
   - `Dispatchers.IO` for disk/network.  
   - `Dispatchers.Default` for CPU-intensive tasks.  
3. **Cancel Coroutines Explicitly**: Cancel jobs when no longer needed.  
4. **Handle Exceptions**: Use `try/catch` with `async` or `CoroutineExceptionHandler`.  

---

### **Common Pitfalls**  
- **Blocking the Main Thread**: Never use `Thread.sleep()` or long sync tasks on the main thread.  
- **Ignoring Cancellation**: Failing to cancel coroutines leads to memory leaks.  
- **Misusing Dispatchers**: Using `Dispatchers.Main` for IO tasks causes ANRs.  

---

### **Conclusion**
Kotlin Coroutines streamline asynchronous programming with structured concurrency. For Android, prioritize `lifecycleScope` and `viewModelScope` to ensure lifecycle safety. By mastering scopes, dispatchers, and cancellation, you can build responsive, efficient apps while avoiding common pitfalls.

---

# Real-World Problems & Solutions

## **1. Sequential vs Parallel API Calls**

### **Problem**: Fetching data from multiple APIs efficiently

**Sequential (Slower - takes sum of all times)**:
```kotlin
class UserRepository {
    suspend fun loadUserProfile(userId: String): UserProfile {
        // Takes 2s + 1.5s + 1s = 4.5s total
        val user = api.fetchUser(userId)        // 2 seconds
        val posts = api.fetchUserPosts(userId)  // 1.5 seconds
        val friends = api.fetchFriends(userId)  // 1 second

        return UserProfile(user, posts, friends)
    }
}
```

**Parallel (Faster - takes max of all times)**:
```kotlin
class UserRepository {
    suspend fun loadUserProfile(userId: String): UserProfile {
        // All run concurrently - takes ~2s (longest call)
        return coroutineScope {
            val userDeferred = async { api.fetchUser(userId) }
            val postsDeferred = async { api.fetchUserPosts(userId) }
            val friendsDeferred = async { api.fetchFriends(userId) }

            UserProfile(
                user = userDeferred.await(),
                posts = postsDeferred.await(),
                friends = friendsDeferred.await()
            )
        }
    }
}
```

**Key Insight**: Use `async` when calls are independent. If one depends on another, use sequential.

**Dependent Calls** (User ID needed for subsequent calls):
```kotlin
suspend fun loadUserDetails(username: String): UserDetails {
    val userId = api.getUserId(username)  // Must complete first

    // Now fetch in parallel using the userId
    return coroutineScope {
        val profile = async { api.getProfile(userId) }
        val settings = async { api.getSettings(userId) }
        UserDetails(profile.await(), settings.await())
    }
}
```

---

## **2. Error Handling Patterns**

### **Problem**: One failed coroutine shouldn't crash the entire app

**Basic Try-Catch**:
```kotlin
viewModelScope.launch {
    try {
        val data = repository.fetchData()
        _uiState.value = UiState.Success(data)
    } catch (e: IOException) {
        _uiState.value = UiState.Error("Network error")
    } catch (e: Exception) {
        _uiState.value = UiState.Error("Unknown error")
    }
}
```

**CoroutineExceptionHandler** (Global handler):
```kotlin
class MyViewModel : ViewModel() {
    private val exceptionHandler = CoroutineExceptionHandler { _, exception ->
        _errorState.value = exception.message
        logErrorToAnalytics(exception)
    }

    fun loadData() {
        viewModelScope.launch(exceptionHandler) {
            val data = repository.fetchData() // Any unhandled exception goes to handler
            _uiState.value = data
        }
    }
}
```

**supervisorScope** (One failure doesn't cancel siblings):
```kotlin
suspend fun loadDashboard(): Dashboard {
    return supervisorScope {
        val news = async {
            try { fetchNews() }
            catch (e: Exception) { emptyList() }  // Fail gracefully
        }
        val weather = async {
            try { fetchWeather() }
            catch (e: Exception) { null }
        }
        val stocks = async {
            try { fetchStocks() }
            catch (e: Exception) { emptyList() }
        }

        Dashboard(
            news = news.await(),
            weather = weather.await(),
            stocks = stocks.await()
        )
    }
}
```

**Why It Matters**: In `coroutineScope`, if one child fails, all siblings are canceled. With `supervisorScope`, siblings continue even if one fails.

---

## **3. Thread Safety & Race Conditions**

### **Problem**: Multiple coroutines accessing shared mutable state

**❌ Race Condition (Unsafe)**:
```kotlin
class Counter {
    private var count = 0

    fun increment() {
        viewModelScope.launch {
            count++  // NOT thread-safe! Can lose updates
        }
    }
}
```

**✅ Using Mutex (Thread-safe)**:
```kotlin
class Counter {
    private var count = 0
    private val mutex = Mutex()

    suspend fun increment() {
        mutex.withLock {
            count++  // Only one coroutine at a time
        }
    }

    suspend fun getCount(): Int = mutex.withLock { count }
}
```

**✅ Using AtomicInteger**:
```kotlin
class Counter {
    private val count = AtomicInteger(0)

    fun increment() {
        viewModelScope.launch {
            count.incrementAndGet()  // Thread-safe atomic operation
        }
    }
}
```

**✅ Using Single Dispatcher** (Confine to one thread):
```kotlin
class BankAccount {
    private var balance = 0
    private val accountDispatcher = Dispatchers.Default.limitedParallelism(1)

    suspend fun deposit(amount: Int) = withContext(accountDispatcher) {
        balance += amount  // Always runs on same thread
    }

    suspend fun getBalance(): Int = withContext(accountDispatcher) {
        balance
    }
}
```

---

## **4. Network Retry Logic with Exponential Backoff**

### **Problem**: API calls fail intermittently - need smart retry

```kotlin
class ApiRepository {
    suspend fun <T> retryWithExponentialBackoff(
        times: Int = 3,
        initialDelay: Long = 1000L,
        maxDelay: Long = 10000L,
        factor: Double = 2.0,
        block: suspend () -> T
    ): T {
        var currentDelay = initialDelay

        repeat(times - 1) { attempt ->
            try {
                return block()
            } catch (e: IOException) {
                Log.e("Retry", "Attempt ${attempt + 1} failed: ${e.message}")
            }

            delay(currentDelay)
            currentDelay = (currentDelay * factor).toLong().coerceAtMost(maxDelay)
        }

        return block() // Last attempt - let exception propagate
    }

    suspend fun fetchUserData(userId: String): User {
        return retryWithExponentialBackoff {
            api.getUser(userId)
        }
    }
}
```

**Advanced Retry with Conditional Logic**:
```kotlin
suspend fun <T> retryIO(
    retryCondition: (Exception) -> Boolean = { it is IOException },
    block: suspend () -> T
): T {
    var currentDelay = 1000L
    var lastException: Exception? = null

    repeat(3) {
        try {
            return block()
        } catch (e: Exception) {
            lastException = e
            if (!retryCondition(e)) {
                throw e  // Don't retry 4xx errors, auth failures, etc.
            }
            delay(currentDelay)
            currentDelay *= 2
        }
    }

    throw lastException!!
}

// Usage
val user = retryIO(
    retryCondition = {
        it is IOException || (it as? HttpException)?.code() == 503
    }
) {
    api.fetchUser(userId)
}
```

---

## **5. Coordinating Network + Database (Offline-First)**

### **Problem**: Show cached data immediately, then update from network

```kotlin
class ArticleRepository(
    private val api: ArticleApi,
    private val database: ArticleDatabase
) {
    suspend fun getArticle(id: String): Article {
        // First, show cached data immediately
        val cached = database.getArticle(id)

        return try {
            // Then fetch fresh data in background
            val fresh = api.fetchArticle(id)
            database.saveArticle(fresh)
            fresh
        } catch (e: IOException) {
            // Network failed - return cached or throw if no cache
            cached ?: throw e
        }
    }

    // Flow-based approach (better for reactive UI)
    fun observeArticle(id: String): Flow<Article> = flow {
        // Emit cached first
        database.observeArticle(id).firstOrNull()?.let { emit(it) }

        // Then fetch and emit fresh data
        try {
            val fresh = api.fetchArticle(id)
            database.saveArticle(fresh)
            emit(fresh)
        } catch (e: Exception) {
            // Already emitted cache, so just log
            Log.e("Repo", "Failed to fetch fresh data", e)
        }
    }
}
```

---

## **6. Proper Cancellation Handling**

### **Problem**: Coroutines doing work after they're canceled

**❌ Ignores Cancellation**:
```kotlin
suspend fun processImages(images: List<Bitmap>) {
    images.forEach { image ->
        processImage(image)  // Continues even if canceled!
    }
}
```

**✅ Respects Cancellation**:
```kotlin
suspend fun processImages(images: List<Bitmap>) {
    images.forEach { image ->
        ensureActive()  // Throws if canceled
        processImage(image)
    }
}

// Or use yield()
suspend fun processLargeList(items: List<Item>) {
    items.forEach { item ->
        yield()  // Checks for cancellation and allows other coroutines
        processItem(item)
    }
}
```

**Cleanup on Cancellation**:
```kotlin
suspend fun downloadFile(url: String): File {
    val tempFile = File.createTempFile("download", ".tmp")

    try {
        return withContext(Dispatchers.IO) {
            // Download logic
            tempFile
        }
    } catch (e: CancellationException) {
        tempFile.delete()  // Cleanup on cancellation
        throw e  // Re-throw CancellationException
    }
}
```

**Using invokeOnCompletion**:
```kotlin
val job = viewModelScope.launch {
    try {
        heavyOperation()
    } finally {
        cleanup()  // Always runs, even on cancellation
    }
}

job.invokeOnCompletion { exception ->
    when (exception) {
        is CancellationException -> Log.d("Job", "Canceled")
        null -> Log.d("Job", "Completed successfully")
        else -> Log.e("Job", "Failed with exception", exception)
    }
}
```

---

## **7. Testing Coroutines**

### **Problem**: Testing async code is tricky

**Using TestDispatcher**:
```kotlin
@ExperimentalCoroutinesApi
class MyViewModelTest {
    private val testDispatcher = UnconfinedTestDispatcher()

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `test user data loading`() = runTest {
        val viewModel = MyViewModel(fakeRepository)

        viewModel.loadUser()

        // Assert immediately - no need to wait
        assertEquals(UserState.Success, viewModel.uiState.value)
    }
}
```

**Testing with delays**:
```kotlin
@Test
fun `test retry logic with delays`() = runTest {
    var attempts = 0
    val repository = ApiRepository()

    val result = repository.retryWithExponentialBackoff(times = 3) {
        attempts++
        if (attempts < 3) throw IOException("Fail")
        "Success"
    }

    assertEquals("Success", result)
    assertEquals(3, attempts)
    // runTest auto-advances virtual time, so test is instant
}
```

---

## **8. Performance Optimizations**

### **Batch Processing with Channels**:
```kotlin
fun CoroutineScope.batchProcessor(
    batchSize: Int = 10,
    delayMs: Long = 1000L
): SendChannel<Item> = Channel<Item>(Channel.UNLIMITED).also { channel ->
    launch {
        val batch = mutableListOf<Item>()

        while (!channel.isClosedForReceive) {
            select<Unit> {
                channel.onReceive { item ->
                    batch.add(item)
                    if (batch.size >= batchSize) {
                        processBatch(batch.toList())
                        batch.clear()
                    }
                }

                onTimeout(delayMs) {
                    if (batch.isNotEmpty()) {
                        processBatch(batch.toList())
                        batch.clear()
                    }
                }
            }
        }
    }
}

// Usage
val processor = viewModelScope.batchProcessor()
processor.send(item1)
processor.send(item2)  // Batched together for efficiency
```

**Limiting Concurrent Operations**:
```kotlin
suspend fun downloadImages(urls: List<String>) {
    val semaphore = Semaphore(3)  // Max 3 concurrent downloads

    coroutineScope {
        urls.map { url ->
            async {
                semaphore.withPermit {
                    downloadImage(url)
                }
            }
        }.awaitAll()
    }
}
```

---

## **Real-World Interview Scenarios**

### **Scenario 1**: Multiple API calls for a screen
**Question**: Load user profile, posts, and comments for a social media app.

```kotlin
class ProfileViewModel(private val repository: ProfileRepository) : ViewModel() {
    private val _uiState = MutableStateFlow<ProfileUiState>(ProfileUiState.Loading)
    val uiState = _uiState.asStateFlow()

    fun loadProfile(userId: String) {
        viewModelScope.launch {
            _uiState.value = ProfileUiState.Loading

            try {
                // Parallel fetch for speed
                coroutineScope {
                    val userDeferred = async { repository.fetchUser(userId) }
                    val postsDeferred = async { repository.fetchPosts(userId) }
                    val followersDeferred = async { repository.fetchFollowers(userId) }

                    _uiState.value = ProfileUiState.Success(
                        user = userDeferred.await(),
                        posts = postsDeferred.await(),
                        followers = followersDeferred.await()
                    )
                }
            } catch (e: Exception) {
                _uiState.value = ProfileUiState.Error(e.message ?: "Unknown error")
            }
        }
    }
}
```

### **Scenario 2**: Handle cancellation during screen rotation
**Answer**: Use `viewModelScope` - it automatically survives rotation and cancels when ViewModel is cleared.

### **Scenario 3**: Implement pull-to-refresh with proper cancellation
```kotlin
class FeedViewModel : ViewModel() {
    private var refreshJob: Job? = null

    fun refresh() {
        refreshJob?.cancel()  // Cancel previous refresh
        refreshJob = viewModelScope.launch {
            try {
                _isRefreshing.value = true
                val fresh = repository.fetchLatestFeed()
                _feedData.value = fresh
            } finally {
                _isRefreshing.value = false
            }
        }
    }
}
```

---

## **Common Production Bugs & Fixes**

### **Bug 1**: Memory leak from GlobalScope
```kotlin
// ❌ BAD - leaks if Activity is destroyed
GlobalScope.launch {
    val data = fetchData()
    updateUI(data)
}

// ✅ GOOD - auto-canceled with lifecycle
lifecycleScope.launch {
    val data = fetchData()
    updateUI(data)
}
```

### **Bug 2**: ANR from blocking main thread
```kotlin
// ❌ BAD - blocks UI
viewModelScope.launch(Dispatchers.Main) {
    val result = blockingIOOperation()  // ANR!
}

// ✅ GOOD - use IO dispatcher
viewModelScope.launch {
    val result = withContext(Dispatchers.IO) {
        blockingIOOperation()
    }
    updateUI(result)  // Back to Main
}
```

### **Bug 3**: Race condition in shared state
```kotlin
// ❌ BAD - multiple coroutines modify state
var count = 0
repeat(1000) {
    viewModelScope.launch { count++ }  // Final count unpredictable!
}

// ✅ GOOD - use atomic or single-threaded dispatcher
val count = AtomicInteger(0)
repeat(1000) {
    viewModelScope.launch { count.incrementAndGet() }
}
```

---

## **Key Takeaways for Production**

1. **Always use lifecycle-aware scopes** (`viewModelScope`, `lifecycleScope`)
2. **Use `async` for parallel independent tasks**, sequential for dependent ones
3. **Handle errors with try-catch or CoroutineExceptionHandler**
4. **Use `Mutex` or `AtomicInteger` for thread safety**
5. **Implement retry logic for network calls**
6. **Coordinate network + DB for offline-first apps**
7. **Respect cancellation with `ensureActive()` or `yield()`**
8. **Test with TestDispatcher and `runTest`**
9. **Batch operations and limit concurrency for performance**
10. **Never block Dispatchers.Main - use withContext(Dispatchers.IO)**