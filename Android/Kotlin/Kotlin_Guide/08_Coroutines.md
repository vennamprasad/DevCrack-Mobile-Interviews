## **Coroutines**

### Q25. What are coroutines in Kotlin?

**Answer:**
Coroutines are lightweight threads that allow writing asynchronous code sequentially.

```kotlin
// Basic coroutine
import kotlinx.coroutines.*

fun main() = runBlocking {
    launch {
        delay(1000L)
        println("World!")
    }
    println("Hello")
}
// Output: Hello, World! (after 1 second)

// Structured concurrency
suspend fun doWork() = coroutineScope {
    launch {
        delay(1000L)
        println("Task 1")
    }
    launch {
        delay(500L)
        println("Task 2")
    }
}

// Async/await for results
suspend fun fetchUser(): User {
    return coroutineScope {
        val name = async { fetchUserName() }
        val age = async { fetchUserAge() }
        User(name.await(), age.await())
    }
}
```

**Key Concepts:**
- **Suspend functions:** Can be paused and resumed
- **Coroutine Scope:** Defines lifecycle
- **Dispatchers:** Control which thread executes coroutine
- **Jobs:** Handle for coroutine lifecycle

---

### Q26. What is the difference between `suspend` functions and regular functions?

**Answer:**

```kotlin
// Regular function - blocks thread
fun fetchData(): String {
    Thread.sleep(1000) // Blocks current thread
    return "Data"
}

// Suspend function - suspends coroutine
suspend fun fetchDataSuspend(): String {
    delay(1000) // Suspends coroutine, doesn't block thread
    return "Data"
}

// Suspend functions can call other suspend functions
suspend fun processData() {
    val data = fetchDataSuspend() // Can call suspend function
    // Process data
}

// Can only be called from coroutine or another suspend function
fun normalFunction() {
    // fetchDataSuspend() // ❌ Error - can't call suspend function

    runBlocking {
        fetchDataSuspend() // ✅ OK - inside coroutine
    }
}

// Suspend functions don't block threads
suspend fun example() {
    println("Start: ${Thread.currentThread().name}")
    delay(1000) // Suspends, other coroutines can run
    println("End: ${Thread.currentThread().name}") // May be different thread
}
```

**Key Differences:**
- Suspend functions can be paused and resumed
- Don't block threads
- Can only be called from coroutines
- Marked with `suspend` keyword
- Compiled into state machine by Kotlin compiler

---

### Q27. What is structured concurrency in Kotlin coroutines?

**Answer:**
Structured concurrency ties child coroutines to a parent scope, ensuring proper lifecycle management.

```kotlin
// Structured concurrency ensures:
// 1. Parent waits for all children
// 2. Cancellation propagates
// 3. Exceptions propagate

suspend fun fetchUserData() = coroutineScope {
    // All launched coroutines are children
    val profile = async { fetchProfile() }
    val posts = async { fetchPosts() }
    val friends = async { fetchFriends() }

    // coroutineScope waits for all children
    UserData(
        profile.await(),
        posts.await(),
        friends.await()
    )
} // Won't return until all children complete

// Cancellation propagation
suspend fun example() = coroutineScope {
    val job1 = launch {
        repeat(100) {
            println("Job 1: $it")
            delay(100)
        }
    }

    val job2 = launch {
        repeat(100) {
            println("Job 2: $it")
            delay(100)
        }
    }

    delay(500)
    cancel() // Cancels both job1 and job2
}

// Exception propagation
suspend fun failing() = coroutineScope {
    launch {
        delay(100)
        throw Exception("Failed!") // Cancels parent and siblings
    }

    launch {
        delay(200)
        println("This won't print")
    }
}
```

---

### Q28. What is the difference between `launch` and `async`?

**Answer:**

**launch:**
```kotlin
// Fire and forget
// Returns Job
// For side effects

val job: Job = scope.launch {
    println("Doing work")
    delay(1000)
    println("Done")
}

job.cancel() // Can cancel
job.join() // Can wait for completion
```

**async:**
```kotlin
// Returns result
// Returns Deferred<T>
// For computations

val deferred: Deferred<String> = scope.async {
    delay(1000)
    "Result"
}

val result = deferred.await() // Get result
```

**Comparison:**
```kotlin
suspend fun example() = coroutineScope {
    // launch - no return value
    launch {
        val data = fetchData()
        updateUI(data)
    }

    // async - returns value
    val result1 = async { computeValue1() }
    val result2 = async { computeValue2() }
    val sum = result1.await() + result2.await()

    // Parallel execution
    val results = listOf(
        async { task1() },
        async { task2() },
        async { task3() }
    ).awaitAll()
}
```

| Feature | launch | async |
|---------|--------|-------|
| **Return type** | Job | Deferred<T> |
| **Purpose** | Side effects | Computation |
| **Get result** | N/A | await() |
| **Exception handling** | Crashes parent | Exception stored, thrown on await() |

---

### Q29. What is `withContext` and when to use it?

**Answer:**
`withContext` switches the dispatcher for a block of code while preserving structured concurrency.

```kotlin
suspend fun fetchData(): String = withContext(Dispatchers.IO) {
    // Runs on IO dispatcher
    val response = api.fetch()
    response.data
} // Automatically switches back

// Use cases:
suspend fun loadUser(userId: String) {
    // Default dispatcher
    showLoading()

    // Switch to IO for network/database
    val user = withContext(Dispatchers.IO) {
        database.getUser(userId)
    }

    // Back to original dispatcher
    updateUI(user)
}

// vs launch/async
fun badExample() {
    scope.launch {
        // Create new coroutine (extra overhead)
        val result = async(Dispatchers.IO) {
            fetchData()
        }.await()
    }
}

fun goodExample() {
    scope.launch {
        // Just switch dispatcher (lighter)
        val result = withContext(Dispatchers.IO) {
            fetchData()
        }
    }
}

// Multiple withContext calls
suspend fun complexOperation() {
    // CPU-intensive work
    val processed = withContext(Dispatchers.Default) {
        processData()
    }

    // Save to database
    withContext(Dispatchers.IO) {
        database.save(processed)
    }

    // Update UI
    withContext(Dispatchers.Main) {
        updateUI(processed)
    }
}
```

---

### Q30. How does cancellation work in coroutines?

**Answer:**
Cancellation is cooperative - coroutines must check for cancellation.

```kotlin
// Cancel a coroutine
val job = scope.launch {
    repeat(1000) {
        println("Working $it")
        delay(100)
    }
}

delay(500)
job.cancel() // Request cancellation
job.join() // Wait for cancellation

// Or combine
job.cancelAndJoin()

// Checking cancellation
suspend fun doWork() {
    repeat(1000) { i ->
        // delay() checks cancellation automatically
        delay(100)

        // For non-suspending loops, check manually
        if (!isActive) {
            throw CancellationException()
        }
        // or
        ensureActive()

        println("Work $i")
    }
}

// Non-cancellable work
suspend fun important() {
    withContext(NonCancellable) {
        // This block ignores cancellation
        saveToDatabase()
        cleanupResources()
    }
}

// Finally block for cleanup
val job = launch {
    try {
        repeat(1000) {
            delay(100)
        }
    } finally {
        withContext(NonCancellable) {
            cleanup() // Always executes
        }
    }
}

// Timeout
withTimeout(5000) {
    // Cancelled if takes more than 5 seconds
    longRunningOperation()
}

// Timeout or null (doesn't throw)
val result = withTimeoutOrNull(5000) {
    longRunningOperation()
} // null if timeout
```

---

### Q31. What is a SupervisorJob and when to use it?

**Answer:**
SupervisorJob prevents failure of one child from cancelling siblings.

```kotlin
// Regular Job - one failure cancels all
val scope = CoroutineScope(Job())
scope.launch {
    try {
        throw Exception("Failed!")
    } catch (e: Exception) {
        // Even with try-catch, siblings are cancelled
    }
}
scope.launch {
    // This gets cancelled when sibling fails
    delay(1000)
    println("Won't print")
}

// SupervisorJob - failures are isolated
val supervisorScope = CoroutineScope(SupervisorJob())
supervisorScope.launch {
    throw Exception("Failed!")
}
supervisorScope.launch {
    // This continues running
    delay(1000)
    println("Will print")
}

// SupervisorScope function
suspend fun example() = supervisorScope {
    launch {
        throw Exception("Failed!")
    }

    launch {
        delay(1000)
        println("Still running")
    }
}

// Use case: Independent tasks
class ViewModel : ViewModel() {
    private val viewModelScope = CoroutineScope(
        SupervisorJob() + Dispatchers.Main
    )

    fun fetchData() {
        // Each fetch is independent
        viewModelScope.launch {
            fetchUsers() // If this fails...
        }

        viewModelScope.launch {
            fetchPosts() // ...this continues
        }
    }
}

// Exception handling with SupervisorJob
val scope = CoroutineScope(SupervisorJob())
scope.launch {
    try {
        riskyOperation()
    } catch (e: Exception) {
        handleError(e)
    }
}
```

---

### Q32. What are Dispatchers in Kotlin coroutines?

**Answer:**
Dispatchers determine which thread(s) a coroutine uses.

```kotlin
// Dispatchers.Main - UI thread (Android)
launch(Dispatchers.Main) {
    updateUI()
}

// Dispatchers.IO - I/O operations (network, files, database)
launch(Dispatchers.IO) {
    val data = database.query()
    val response = api.fetch()
}

// Dispatchers.Default - CPU-intensive work
launch(Dispatchers.Default) {
    val result = complexCalculation()
    processLargeData()
}

// Dispatchers.Unconfined - Don't recommend (advanced)
launch(Dispatchers.Unconfined) {
    // Runs in caller thread until first suspension
}

// Custom dispatcher
val customDispatcher = Executors.newFixedThreadPool(4)
    .asCoroutineDispatcher()

launch(customDispatcher) {
    // Work on custom thread pool
}

customDispatcher.close() // Remember to close

// Real-world example
suspend fun loadUser(id: String): User {
    return withContext(Dispatchers.IO) {
        // Network call on IO dispatcher
        val response = api.getUser(id)

        // Parse on Default dispatcher
        withContext(Dispatchers.Default) {
            parseUser(response)
        }
    }
}
```

| Dispatcher | Thread Pool | Use Case |
|------------|-------------|----------|
| **Main** | UI thread | UI updates |
| **IO** | 64 threads | Network, file, database |
| **Default** | CPU cores | Heavy computation |
| **Unconfined** | Varies | Special cases only |
