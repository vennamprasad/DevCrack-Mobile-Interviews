# 🌊 Kotlin Flow Fundamentals: Cold Streams, Hot Streams & Flow Builders

> **Mastering reactive asynchronous streams in Kotlin: Cold Flows, Hot State, Backpressure, Exception Transparency, and Android Lifecycle Safety.**

---

## 📌 Executive Summary

Kotlin **Flow** is a reactive asynchronous stream library built on top of Kotlin Coroutines. Unlike RxJava, which required complex operators, thread-pool schedulers, and disposable disposals, Kotlin Flow leverages **suspending functions** to provide sequential, non-blocking, and backpressure-resilient data streams.

---

## ❄️ Cold Streams vs. 🔥 Hot Streams

Understanding the difference between Cold and Hot streams is the single most tested concept in Kotlin concurrency interviews:

```
Cold Flow (Lazy / On-Demand):
[ Producer: flow { ... } ]
            │
(No code runs yet!)
            │
            ▼
[ Consumer 1 calls .collect() ] ──> Starts execution from beginning for Consumer 1
[ Consumer 2 calls .collect() ] ──> Starts independent execution for Consumer 2

Hot Flow (StateFlow / SharedFlow):
[ Producer ] ──> (Emits continuously regardless of active collectors)
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
[ Subscriber 1 ]               [ Subscriber 2 ]
(Receives broadcast deltas)     (Receives broadcast deltas)
```

| Dimension | Cold Flow (`Flow<T>`) | Hot Flow (`StateFlow<T>`, `SharedFlow<T>`) |
| :--- | :--- | :--- |
| **Execution Trigger** | Executes **only when collected** (`.collect()`). | Active independently of whether there are subscribers. |
| **State Storage** | Does not store state. | `StateFlow` stores latest value; `SharedFlow` stores replay buffer. |
| **Multiple Collectors** | Each collector runs a separate producer execution block. | Broadcasts values to all active collectors simultaneously. |
| **Unicast vs Multicast** | Unicast (1 producer to 1 consumer). | Multicast (1 producer to many consumers). |
| **Typical Use Case** | Room Database queries, Network polling requests, File reading. | UI ViewState in ViewModel, One-off Navigation / Snackbar events. |

---

## 🛠️ Flow Builders & Creation Patterns

### 1. `flow { ... }` (Standard Builder)
```kotlin
fun fetchStockPrices(symbol: String): Flow<Double> = flow {
    while (true) {
        val price = api.getLatestPrice(symbol) // Suspending network call
        emit(price)                            // Emits value to collector
        delay(2000)                            // Non-blocking delay
    }
}
```

### 2. `flowOf(...)` and `.asFlow()`
```kotlin
val staticNumbersFlow = flowOf(1, 2, 3, 4, 5)

val listFlow = listOf("Apple", "Banana", "Cherry").asFlow()
```

### 3. `channelFlow { ... }` (Concurrent Production)
When you need to emit values from **multiple coroutines concurrently**, the standard `flow {}` builder throws an `IllegalStateException` because it enforces sequential emissions. Use `channelFlow`:

```kotlin
fun listenToMultipleSensors(): Flow<SensorData> = channelFlow {
    // Launch child coroutine for Accelerometer
    launch {
        accelerometer.collect { send(SensorData.Accel(it)) }
    }
    // Launch child coroutine for Gyroscope
    launch {
        gyroscope.collect { send(SensorData.Gyro(it)) }
    }
}
```

---

## 🛡️ Context Preservation & Exception Transparency

Flow enforces two strict architectural rules:

### 1. Context Preservation (`flowOn`)
You cannot change the CoroutineContext inside a `flow {}` builder using `withContext()`:
```kotlin
// ❌ COMPILE ERROR / RUNTIME CRASH: Violates Context Preservation
fun badFlow() = flow {
    withContext(Dispatchers.IO) {
        emit(fetchData()) // IllegalStateException: Flow invariant is violated
    }
}

// ✅ CORRECT: Use flowOn() operator
fun goodFlow(): Flow<Data> = flow {
    emit(fetchData()) // Runs on Dispatchers.IO
}.flowOn(Dispatchers.IO) // Changes the upstream dispatcher only!
```

### 2. Exception Transparency (`catch`)
Upstream errors must be caught using the `.catch` operator, not by wrapping `emit()` in a try-catch block:

```kotlin
repository.observeUserData()
    .flowOn(Dispatchers.IO)
    .catch { error ->
        emit(UserData.EmptyFallback(error.message)) // Emit fallback or log error
    }
    .collect { data ->
        updateUI(data)
    }
```

---

## 📱 Android Lifecycle-Safe Collection

Collecting flows naively inside `lifecycleScope.launch` in Android Activities or Fragments is a dangerous memory leak and battery drain:
- Even when the app is in the background (`onStop`), `lifecycleScope.launch` keeps collecting data!
- If the flow is observing location or a camera stream, it drains battery while the user isn't even looking at the screen.

### The Solution: `repeatOnLifecycle`

```kotlin
class UserProfileActivity : AppCompatActivity() {
    private val viewModel: UserViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        lifecycleScope.launch {
            // repeatOnLifecycle suspends when lifecycle is below STARTED (app backgrounded)
            // and automatically restarts collection when lifecycle enters STARTED (app foregrounded)
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { state ->
                    renderUi(state)
                }
            }
        }
    }
}
```

In Jetpack Compose:
```kotlin
@Composable
fun UserProfileScreen(viewModel: UserViewModel) {
    // collectAsStateWithLifecycle is lifecycle-aware by default!
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    
    ProfileContent(uiState)
}
```
