## **Flow & Channels**

### Q33. What is Flow in Kotlin?

**Answer:**
Flow is a cold asynchronous stream that emits values sequentially.

```kotlin
// Create Flow
fun numbersFlow(): Flow<Int> = flow {
    for (i in 1..5) {
        delay(100)
        emit(i) // Emit values
    }
}

// Collect Flow
suspend fun example() {
    numbersFlow().collect { value ->
        println(value) // 1, 2, 3, 4, 5
    }
}

// Flow builders
val flow1 = flowOf(1, 2, 3) // From values
val flow2 = listOf(1, 2, 3).asFlow() // From collection
val flow3 = flow { emit(1) } // Custom

// Flow is cold - doesn't run until collected
val numbers = flow {
    println("Flow started")
    emit(1)
}
// "Flow started" not printed yet

numbers.collect { println(it) }
// Now "Flow started" prints, then 1
```

---

### Q34. What is the difference between cold and hot streams?

**Answer:**

**Cold Streams (Flow):**
```kotlin
// Each collector gets own execution
val coldFlow = flow {
    println("Flow started")
    emit(1)
    emit(2)
}

// First collector
coldFlow.collect { println("Collector 1: $it") }
// Output:
// Flow started
// Collector 1: 1
// Collector 1: 2

// Second collector (starts from beginning)
coldFlow.collect { println("Collector 2: $it") }
// Output:
// Flow started (again!)
// Collector 2: 1
// Collector 2: 2
```

**Hot Streams (SharedFlow, StateFlow, Channel):**
```kotlin
// SharedFlow - hot stream
val hotFlow = MutableSharedFlow<Int>()

// Emit values
scope.launch {
    hotFlow.emit(1)
    hotFlow.emit(2)
}

// Collectors share same stream
scope.launch {
    hotFlow.collect { println("Collector 1: $it") }
}

scope.launch {
    hotFlow.collect { println("Collector 2: $it") }
}
// Both collectors receive same values
```

| Feature | Cold (Flow) | Hot (SharedFlow/StateFlow) |
|---------|-------------|----------------------------|
| **Execution** | Per collector | Shared |
| **Start** | On collect | Immediately |
| **Values** | All from start | Only new values |
| **Use case** | API calls, DB queries | Events, state |

---

### Q35. What is StateFlow vs SharedFlow?

**Answer:**

**StateFlow:**
```kotlin
// Always has a value
val _state = MutableStateFlow(0)
val state: StateFlow<Int> = _state.asStateFlow()

// Update
_state.value = 1
_state.update { it + 1 }

// Collect (always gets current value)
state.collect { value ->
    println(value) // Immediately prints current value, then updates
}

// Properties
state.value // Get current value synchronously
```

**SharedFlow:**
```kotlin
// May not have initial value
val _events = MutableSharedFlow<Event>(
    replay = 1, // Cache last N values
    extraBufferCapacity = 10, // Buffer for slow collectors
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)
val events: SharedFlow<Event> = _events.asSharedFlow()

// Emit
_events.emit(Event.Click)
_events.tryEmit(Event.Click) // Non-suspending

// Collect
events.collect { event ->
    handleEvent(event)
}
```

**Comparison:**
```kotlin
// StateFlow - for state
class ViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState.Loading)
    val uiState = _uiState.asStateFlow()

    fun loadData() {
        _uiState.value = UiState.Success(data)
    }
}

// SharedFlow - for events
class ViewModel : ViewModel() {
    private val _events = MutableSharedFlow<Event>()
    val events = _events.asSharedFlow()

    fun onClick() {
        viewModelScope.launch {
            _events.emit(Event.Navigate)
        }
    }
}
```

| Feature | StateFlow | SharedFlow |
|---------|-----------|------------|
| **Initial value** | Required | Optional |
| **Replay** | Always 1 | Configurable |
| **Current value** | Yes (.value) | No |
| **Use case** | UI state | One-time events |
| **Conflation** | Yes | Configurable |

---

### Q36. What are Flow operators?

**Answer:**

**Transformation:**
```kotlin
val numbers = flowOf(1, 2, 3, 4, 5)

// map
numbers.map { it * 2 }
    .collect { println(it) } // 2, 4, 6, 8, 10

// filter
numbers.filter { it % 2 == 0 }
    .collect { println(it) } // 2, 4

// transform - custom transformation
numbers.transform { value ->
    emit(value)
    emit(value * 2)
}.collect { println(it) } // 1, 2, 2, 4, 3, 6, ...
```

**Intermediate operators:**
```kotlin
// take - limit number of values
numbers.take(3).collect { println(it) } // 1, 2, 3

// drop - skip first N values
numbers.drop(2).collect { println(it) } // 3, 4, 5

// debounce - emit only after quiet period
searchQuery
    .debounce(300)
    .collect { query ->
        search(query)
    }

// distinctUntilChanged - skip consecutive duplicates
flow { emit(1); emit(1); emit(2); emit(2) }
    .distinctUntilChanged()
    .collect { println(it) } // 1, 2

// onEach - perform action on each value
numbers
    .onEach { println("Processing $it") }
    .collect()
```

**Terminal operators:**
```kotlin
// collect - consume values
numbers.collect { value -> }

// first - get first value
val first = numbers.first()

// toList - collect to list
val list = numbers.toList()

// reduce - accumulate
val sum = numbers.reduce { acc, value -> acc + value }

// fold - accumulate with initial
val sum2 = numbers.fold(0) { acc, value -> acc + value }
```

**Exception handling:**
```kotlin
flow {
    emit(1)
    throw Exception("Error")
}
    .catch { e ->
        println("Caught: ${e.message}")
        emit(0) // Can emit recovery value
    }
    .collect { println(it) }

// onCompletion
numbers
    .onCompletion { cause ->
        if (cause != null) {
            println("Flow completed with error: $cause")
        } else {
            println("Flow completed successfully")
        }
    }
    .collect()
```

---

### Q37. What are flatMap operators in Flow?

**Answer:**

**flatMapConcat** - Sequential:
```kotlin
// Process flows sequentially
flowOf(1, 2, 3)
    .flatMapConcat { value ->
        flow {
            emit("$value-a")
            delay(100)
            emit("$value-b")
        }
    }
    .collect { println(it) }
// Output: 1-a, 1-b, 2-a, 2-b, 3-a, 3-b
```

**flatMapMerge** - Concurrent:
```kotlin
// Process flows concurrently
flowOf(1, 2, 3)
    .flatMapMerge(concurrency = 2) { value ->
        flow {
            emit("$value-a")
            delay(100)
            emit("$value-b")
        }
    }
    .collect { println(it) }
// Output: 1-a, 2-a, 1-b, 2-b, 3-a, 3-b (interleaved)
```

**flatMapLatest** - Cancel previous:
```kotlin
// Cancel previous flow when new value arrives
searchQuery
    .flatMapLatest { query ->
        searchDatabase(query)
    }
    .collect { results ->
        updateUI(results)
    }
// If new query arrives, previous search is cancelled
```

**Real-world examples:**
```kotlin
// Sequential API calls
fun getUsers(): Flow<User> = flow {
    val userIds = getUserIds()
    userIds
        .asFlow()
        .flatMapConcat { id ->
            getUserDetails(id)
        }
        .collect { emit(it) }
}

// Parallel API calls
fun getUsersParallel(): Flow<User> =
    getUserIds()
        .asFlow()
        .flatMapMerge(concurrency = 5) { id ->
            getUserDetails(id)
        }

// Search with cancellation
val searchResults = searchQuery
    .debounce(300)
    .flatMapLatest { query ->
        searchApi(query)
    }
```

---

### Q38. What are Channels and when to use them?

**Answer:**
Channels are hot streams for communication between coroutines (like queues).

```kotlin
// Create channel
val channel = Channel<Int>()

// Producer
launch {
    for (i in 1..5) {
        channel.send(i)
        delay(100)
    }
    channel.close() // Signal completion
}

// Consumer
launch {
    for (value in channel) {
        println(value)
    }
}

// Channel types
val unlimited = Channel<Int>(Channel.UNLIMITED) // Unbounded
val buffered = Channel<Int>(10) // Buffer of 10
val rendezvous = Channel<Int>() // No buffer (default)
val conflated = Channel<Int>(Channel.CONFLATED) // Keeps only latest

// Produce/consume pattern
fun produceNumbers() = produce {
    repeat(5) { send(it) }
}

suspend fun consumeNumbers() {
    produceNumbers().consumeEach { value ->
        println(value)
    }
}

// Use cases:
// 1. Producer-consumer pattern
val workChannel = Channel<Work>()

// Multiple producers
repeat(5) { workerId ->
    launch {
        generateWork(workerId).forEach { work ->
            workChannel.send(work)
        }
    }
}

// Multiple consumers
repeat(3) { consumerId ->
    launch {
        for (work in workChannel) {
            processWork(consumerId, work)
        }
    }
}

// 2. Pipeline
fun CoroutineScope.produceSquares() = produce {
    repeat(5) { send(it * it) }
}

fun CoroutineScope.processSquares(
    input: ReceiveChannel<Int>
) = produce {
    for (value in input) {
        send(value * 2)
    }
}

val squares = produceSquares()
val processed = processSquares(squares)
processed.consumeEach { println(it) }
```

**Flow vs Channel:**

| Feature | Flow | Channel |
|---------|------|---------|
| **Type** | Cold | Hot |
| **Start** | On collect | Immediately |
| **Collectors** | Multiple (independent) | Multiple (shared) |
| **Use case** | Streams, transformations | Communication, queues |
