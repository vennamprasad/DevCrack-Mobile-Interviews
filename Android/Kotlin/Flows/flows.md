# Kotlin Flows

Kotlin Flows are a part of Kotlin Coroutines and provide a way to handle streams of asynchronous data.

## Key Concepts

- **Flow**: Represents a cold asynchronous stream of values.
- **Cold Stream**: The flow does not emit data until it is collected.
- **Operators**: Functions like `map`, `filter`, `take`, etc., to transform flows.
- **Collector**: Consumes the values emitted by the flow.

## Basic Example

```kotlin
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.runBlocking

fun simpleFlow(): Flow<Int> = flow {
    for (i in 1..3) {
        emit(i)
    }
}

fun main() = runBlocking {
    simpleFlow().collect { value ->
        println(value)
    }
}
```

## Common Operators

- `map { }` – Transform each value.
- `filter { }` – Filter values.
- `take(n)` – Take first n values.
- `collect { }` – Terminal operator to receive values.

## Use Cases

- Asynchronous data streams (e.g., network responses, database updates)
- Reactive UI updates
- Event handling

## Common Interview Questions on Kotlin Flows (with Answers)

1. **What is the difference between Flow and LiveData?**  
    *Flow is a cold asynchronous stream from Kotlin Coroutines, suitable for both UI and non-UI layers, and supports operators and backpressure. LiveData is lifecycle-aware, designed for UI, and does not support operators or backpressure.*

2. **How does Flow handle backpressure?**  
    *Flow is cold and suspends the producer if the consumer is slow, naturally handling backpressure by suspending emission until the collector is ready.*

3. **Explain cold vs hot streams in the context of Flow.**  
    *Cold streams (like Flow) start emitting values only when collected, and each collector gets its own emissions. Hot streams (like SharedFlow, StateFlow) emit values regardless of collectors, and multiple collectors share emissions.*

4. **What are some common Flow operators and their use cases?**  
    *Operators like `map`, `filter`, `take`, `flatMapConcat`, and `debounce` are used to transform, filter, limit, combine, or debounce emissions from a Flow.*

5. **How do you handle exceptions in a Flow?**  
    *Use the `catch` operator to handle exceptions upstream, or try-catch blocks inside the flow builder for emission errors.*

6. **What is the difference between `flow`, `channelFlow`, and `stateFlow`?**  
    - `flow`: Basic cold stream builder.
    - `channelFlow`: Allows concurrent emissions from multiple coroutines.
    - `stateFlow`: Hot, state-holder observable flow, always has a current value.

7. **How can you combine multiple flows?**  
    *Use operators like `zip`, `combine`, or `flatMapMerge` to merge or combine emissions from multiple flows.*

8. **How does Flow cancellation work?**  
    *Flow is cancellable; if the coroutine collecting the flow is cancelled, the flow stops emitting and cleans up resources.*

9. **What is the role of `collect` in Flow?**  
    *`collect` is a terminal operator that triggers the flow to start emitting values and processes each emitted value.*

10. **How do you test Flows in unit tests?**  
     *Use libraries like Turbine or run test coroutines with `runBlockingTest` to collect and assert emissions from a Flow.*
    ## Sample Code Interview Snippets (with Answers)

    ### 1. Collecting Flow Values

    **Question:** How do you collect values from a Flow and print them?

    ```kotlin
    val numbers = flowOf(1, 2, 3)
    numbers.collect { value ->
        println(value)
    }
    ```
    *This collects and prints each value emitted by the flow.*

    ---

    ### 2. Using Flow Operators

    **Question:** How do you use `map` and `filter` operators on a Flow?

    ```kotlin
    val flow = flowOf(1, 2, 3, 4, 5)
    flow
        .filter { it % 2 == 0 }
        .map { it * it }
        .collect { println(it) }
    ```
    *This filters even numbers and prints their squares.*

    ---

    ### 3. Exception Handling in Flows

    **Question:** How do you handle exceptions in a Flow?

    ```kotlin
    flow {
        emit(1)
        throw RuntimeException("Error!")
    }.catch { e ->
        emit(-1)
    }.collect { println(it) }
    ```
    *This emits 1, then catches the exception and emits -1.*

    ---

    ### 4. Combining Flows

    **Question:** How do you combine two flows?

    ```kotlin
    val flow1 = flowOf(1, 2)
    val flow2 = flowOf("A", "B")
    flow1.zip(flow2) { a, b -> "$a$b" }
        .collect { println(it) }
    ```
    *This combines emissions to print "1A" and "2B".*

    ---

    ### 5. Using StateFlow

    **Question:** How do you use StateFlow to hold and observe state?

    ```kotlin
    val stateFlow = MutableStateFlow(0)
    stateFlow.value = 5
    stateFlow.collect { println(it) }
    ```
    *This holds a state and emits updates to collectors.*

## Resources

- [Kotlin Flow Documentation](https://kotlinlang.org/docs/flow.html)
- [Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)

---

# Real-World Problems & Solutions with Flows

## **1. StateFlow vs SharedFlow vs Flow - When to Use What**

### **Flow (Cold Stream)**
**Use Case**: One-time operations, API calls, database queries

```kotlin
class UserRepository {
    // Returns fresh data each time it's collected
    fun getUser(id: String): Flow<User> = flow {
        val user = api.fetchUser(id)
        emit(user)
    }
}

// Each collector gets a NEW API call
viewModelScope.launch {
    repository.getUser("123").collect { user ->
        println("Collector 1: $user")
    }
}

viewModelScope.launch {
    repository.getUser("123").collect { user ->
        println("Collector 2: $user")  // Separate API call!
    }
}
```

### **StateFlow (Hot Stream with State)**
**Use Case**: UI state, configuration, single source of truth

```kotlin
class UserViewModel : ViewModel() {
    private val _userState = MutableStateFlow<UserState>(UserState.Loading)
    val userState: StateFlow<UserState> = _userState.asStateFlow()

    fun loadUser(id: String) {
        viewModelScope.launch {
            _userState.value = UserState.Loading
            try {
                val user = repository.fetchUser(id)
                _userState.value = UserState.Success(user)
            } catch (e: Exception) {
                _userState.value = UserState.Error(e.message)
            }
        }
    }
}

// In Activity/Fragment
lifecycleScope.launch {
    viewModel.userState.collect { state ->
        when (state) {
            is UserState.Loading -> showLoading()
            is UserState.Success -> showUser(state.user)
            is UserState.Error -> showError(state.message)
        }
    }
}
```

**Key Features**:
- Always has a current value (`.value`)
- New collectors immediately get the latest value
- Conflates updates (skips intermediate values if collector is slow)
- Perfect for UI state

### **SharedFlow (Hot Stream for Events)**
**Use Case**: Events, notifications, one-time actions

```kotlin
class EventViewModel : ViewModel() {
    private val _navigationEvents = MutableSharedFlow<NavigationEvent>()
    val navigationEvents = _navigationEvents.asSharedFlow()

    fun onLoginSuccess() {
        viewModelScope.launch {
            _navigationEvents.emit(NavigationEvent.GoToHome)
        }
    }
}

// Collectors only receive NEW events (no replay by default)
lifecycleScope.launch {
    viewModel.navigationEvents.collect { event ->
        when (event) {
            is NavigationEvent.GoToHome -> navigateToHome()
            is NavigationEvent.ShowError -> showErrorDialog()
        }
    }
}
```

**Key Features**:
- No initial value
- Can configure replay (buffer past events)
- Doesn't skip values (unless buffer is full)
- Perfect for one-time events

**Comparison Table**:
| Feature | Flow | StateFlow | SharedFlow |
|---------|------|-----------|------------|
| Hot/Cold | Cold | Hot | Hot |
| Initial Value | No | Yes | Optional (replay) |
| Multiple Collectors | Independent streams | Share same stream | Share same stream |
| Conflation | No | Yes | Configurable |
| Use Case | API calls | UI state | Events |

---

## **2. Search with Debouncing (Real-Time Search)**

### **Problem**: Don't want to search on every keystroke

```kotlin
class SearchViewModel : ViewModel() {
    private val _searchQuery = MutableStateFlow("")

    val searchResults: StateFlow<List<Result>> = _searchQuery
        .debounce(300)  // Wait 300ms after user stops typing
        .filter { it.length >= 3 }  // Only search if 3+ characters
        .distinctUntilChanged()  // Don't search if query hasn't changed
        .flatMapLatest { query ->
            searchRepository.search(query)
                .catch { emit(emptyList()) }  // Handle errors gracefully
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    fun onSearchQueryChanged(query: String) {
        _searchQuery.value = query
    }
}

// In UI
class SearchActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        searchEditText.addTextChangedListener { text ->
            viewModel.onSearchQueryChanged(text.toString())
        }

        lifecycleScope.launch {
            viewModel.searchResults.collect { results ->
                adapter.submitList(results)
            }
        }
    }
}
```

**Why It Works**:
- `debounce(300)`: Waits 300ms after last emission
- `filter`: Prevents unnecessary API calls for short queries
- `distinctUntilChanged`: Avoids duplicate searches
- `flatMapLatest`: Cancels previous search if new one starts
- `catch`: Handles errors without breaking the flow

---

## **3. Pagination with Flows**

### **Problem**: Load items incrementally as user scrolls

```kotlin
class PaginatedRepository {
    private var currentPage = 0
    private val _items = mutableListOf<Item>()

    fun getItems(): Flow<PagingState<Item>> = flow {
        emit(PagingState.Loading)

        try {
            val newItems = api.fetchItems(page = currentPage, pageSize = 20)
            _items.addAll(newItems)
            currentPage++

            emit(PagingState.Success(
                items = _items.toList(),
                hasMore = newItems.size == 20
            ))
        } catch (e: Exception) {
            emit(PagingState.Error(e.message ?: "Unknown error"))
        }
    }

    fun reset() {
        currentPage = 0
        _items.clear()
    }
}

class FeedViewModel : ViewModel() {
    private val _feedState = MutableStateFlow<PagingState<Item>>(PagingState.Initial)
    val feedState = _feedState.asStateFlow()

    fun loadMore() {
        viewModelScope.launch {
            repository.getItems().collect { state ->
                _feedState.value = state
            }
        }
    }

    fun refresh() {
        repository.reset()
        loadMore()
    }
}

sealed class PagingState<out T> {
    object Initial : PagingState<Nothing>()
    object Loading : PagingState<Nothing>()
    data class Success<T>(val items: List<T>, val hasMore: Boolean) : PagingState<T>()
    data class Error(val message: String) : PagingState<Nothing>()
}
```

---

## **4. Offline-First Architecture (Network + Cache Pattern)**

### **Problem**: Show cached data immediately, update from network in background

```kotlin
class ArticleRepository(
    private val api: ArticleApi,
    private val database: ArticleDao
) {
    // Single source of truth pattern
    fun getArticle(id: String): Flow<Resource<Article>> = flow {
        // First, emit cached data
        emit(Resource.Loading(data = database.getArticle(id)))

        try {
            // Fetch fresh data from network
            val freshArticle = api.fetchArticle(id)

            // Update cache
            database.insertArticle(freshArticle)

            // Emit fresh data (database will emit through Room's Flow)
        } catch (e: IOException) {
            // Network error - emit error but keep showing cached data
            emit(Resource.Error(
                message = "Network error",
                data = database.getArticle(id)
            ))
        }
    }.flatMapLatest {
        // Observe database for any updates
        database.observeArticle(id).map { article ->
            Resource.Success(article)
        }
    }

    // For list of articles
    fun getArticles(): Flow<Resource<List<Article>>> = flow {
        emit(Resource.Loading(data = database.getAllArticles()))

        try {
            val freshArticles = api.fetchArticles()
            database.insertArticles(freshArticles)
        } catch (e: IOException) {
            emit(Resource.Error(
                message = "Cannot fetch fresh data",
                data = database.getAllArticles()
            ))
        }
    }.flatMapLatest {
        database.observeAllArticles().map { articles ->
            Resource.Success(articles)
        }
    }
}

sealed class Resource<T>(
    val data: T? = null,
    val message: String? = null
) {
    class Success<T>(data: T) : Resource<T>(data)
    class Loading<T>(data: T? = null) : Resource<T>(data)
    class Error<T>(message: String, data: T? = null) : Resource<T>(data, message)
}

// Usage in ViewModel
class ArticleViewModel : ViewModel() {
    fun loadArticle(id: String) {
        viewModelScope.launch {
            repository.getArticle(id).collect { resource ->
                when (resource) {
                    is Resource.Loading -> {
                        _uiState.value = UiState.Loading(resource.data)
                    }
                    is Resource.Success -> {
                        _uiState.value = UiState.Success(resource.data!!)
                    }
                    is Resource.Error -> {
                        _uiState.value = UiState.Error(
                            message = resource.message!!,
                            cachedData = resource.data
                        )
                    }
                }
            }
        }
    }
}
```

---

## **5. Combining Multiple Flows**

### **Problem**: Need data from multiple sources

**Using `combine` (waits for all flows)**:
```kotlin
class DashboardViewModel : ViewModel() {
    private val userFlow = repository.observeUser()
    private val notificationsFlow = repository.observeNotifications()
    private val settingsFlow = repository.observeSettings()

    val dashboardState = combine(
        userFlow,
        notificationsFlow,
        settingsFlow
    ) { user, notifications, settings ->
        DashboardState(
            user = user,
            unreadCount = notifications.count { !it.isRead },
            isDarkMode = settings.isDarkMode
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = DashboardState.Loading
    )
}
```

**Using `zip` (pairs emissions)**:
```kotlin
val flow1 = flowOf(1, 2, 3)
val flow2 = flowOf("A", "B", "C")

flow1.zip(flow2) { num, letter ->
    "$num$letter"
}.collect { println(it) }
// Output: 1A, 2B, 3C
```

**Using `merge` (merges all emissions)**:
```kotlin
val localFlow = database.observeArticles()
val remoteFlow = api.fetchArticlesFlow()

merge(localFlow, remoteFlow)
    .collect { articles ->
        updateUI(articles)
    }
```

---

## **6. Error Handling and Retry with Flows**

### **Problem**: Network calls fail, need retry logic

```kotlin
class NetworkRepository {
    fun fetchDataWithRetry(): Flow<Result<Data>> = flow {
        emit(Result.Loading)

        val data = api.fetchData()
        emit(Result.Success(data))
    }
    .retry(3) { cause ->
        // Only retry on IO exceptions, with delay
        (cause is IOException).also { shouldRetry ->
            if (shouldRetry) delay(1000)
        }
    }
    .catch { exception ->
        emit(Result.Error(exception.message ?: "Unknown error"))
    }

    // Advanced retry with exponential backoff
    fun fetchDataWithExponentialBackoff(): Flow<Data> = flow {
        api.fetchData()
    }.retryWhen { cause, attempt ->
        if (cause is IOException && attempt < 3) {
            delay(1000 * 2.0.pow(attempt.toInt()).toLong())
            true
        } else {
            false
        }
    }
}

// Usage
viewModelScope.launch {
    repository.fetchDataWithRetry().collect { result ->
        when (result) {
            is Result.Loading -> showLoading()
            is Result.Success -> showData(result.data)
            is Result.Error -> showError(result.message)
        }
    }
}
```

**Custom Retry Operator**:
```kotlin
fun <T> Flow<T>.retryWithBackoff(
    maxRetries: Int = 3,
    initialDelay: Long = 1000L,
    maxDelay: Long = 10000L,
    factor: Double = 2.0
): Flow<T> = retryWhen { cause, attempt ->
    if (cause is IOException && attempt < maxRetries) {
        val delay = (initialDelay * factor.pow(attempt.toInt()))
            .toLong()
            .coerceAtMost(maxDelay)
        delay(delay)
        true
    } else {
        false
    }
}

// Usage
fun getUser(): Flow<User> = flow {
    emit(api.fetchUser())
}.retryWithBackoff()
```

---

## **7. Converting Callbacks to Flows**

### **Problem**: Legacy callback APIs need to work with Flows

**Using `callbackFlow`**:
```kotlin
class LocationRepository(private val locationManager: LocationManager) {

    fun observeLocation(): Flow<Location> = callbackFlow {
        val callback = object : LocationListener {
            override fun onLocationChanged(location: Location) {
                trySend(location)  // Send to flow
            }

            override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}
            override fun onProviderEnabled(provider: String) {}
            override fun onProviderDisabled(provider: String) {
                close(Exception("Location provider disabled"))
            }
        }

        // Register callback
        locationManager.requestLocationUpdates(
            LocationManager.GPS_PROVIDER,
            1000L,
            10f,
            callback
        )

        // Cleanup when flow is canceled
        awaitClose {
            locationManager.removeUpdates(callback)
        }
    }
}

// Firebase Firestore example
fun observeDocument(docId: String): Flow<Document> = callbackFlow {
    val listener = firestore.collection("docs")
        .document(docId)
        .addSnapshotListener { snapshot, error ->
            if (error != null) {
                close(error)
                return@addSnapshotListener
            }

            snapshot?.let { trySend(it.toObject(Document::class.java)!!) }
        }

    awaitClose { listener.remove() }
}
```

---

## **8. Testing Flows**

### **Problem**: How to test asynchronous flows

**Using Turbine Library**:
```kotlin
@Test
fun `test search flow emits correct results`() = runTest {
    val viewModel = SearchViewModel(fakeRepository)

    viewModel.searchResults.test {
        // Initial state
        assertEquals(emptyList(), awaitItem())

        // Trigger search
        viewModel.onSearchQueryChanged("kotlin")

        // Skip intermediate emissions if any
        // Then assert final result
        assertEquals(listOf("Kotlin Coroutines", "Kotlin Flows"), awaitItem())

        cancelAndIgnoreRemainingEvents()
    }
}
```

**Without Turbine**:
```kotlin
@Test
fun `test flow emissions`() = runTest {
    val flow = flow {
        emit(1)
        delay(100)
        emit(2)
        delay(100)
        emit(3)
    }

    val results = mutableListOf<Int>()
    flow.toList(results)

    assertEquals(listOf(1, 2, 3), results)
}

@Test
fun `test StateFlow updates`() = runTest {
    val viewModel = MyViewModel(fakeRepository)

    val job = launch {
        viewModel.uiState.collect {
            // Assertions here
        }
    }

    viewModel.loadData()

    advanceUntilIdle()  // Advance virtual time

    assertEquals(UiState.Success, viewModel.uiState.value)

    job.cancel()
}
```

---

## **9. Advanced Flow Operators in Real Scenarios**

### **flatMapConcat** (Sequential processing)
```kotlin
// Process users one by one, in order
fun processUsers(userIds: List<String>): Flow<User> {
    return userIds.asFlow()
        .flatMapConcat { id ->
            flow { emit(api.fetchUser(id)) }
        }
}
```

### **flatMapMerge** (Parallel processing)
```kotlin
// Process multiple users concurrently
fun processUsersInParallel(userIds: List<String>): Flow<User> {
    return userIds.asFlow()
        .flatMapMerge(concurrency = 3) { id ->
            flow { emit(api.fetchUser(id)) }
        }
}
```

### **transformLatest** (Cancel previous when new arrives)
```kotlin
fun searchWithTransformLatest(query: String): Flow<List<Result>> {
    return flowOf(query)
        .transformLatest { q ->
            emit(emptyList())  // Clear previous results
            delay(300)
            emit(api.search(q))
        }
}
```

### **scan** (Accumulate emissions)
```kotlin
// Calculate running total of cart items
fun cartTotal(items: Flow<Item>): Flow<Double> {
    return items
        .map { it.price }
        .scan(0.0) { total, price -> total + price }
}
```

### **buffer** (Handle backpressure)
```kotlin
fun processLargeDataset(): Flow<Data> = flow {
    repeat(100) {
        emit(fetchData(it))
    }
}
.buffer(capacity = 10)  // Buffer up to 10 items
.map { processData(it) }  // Slow processing
```

---

## **10. Real-World Production Patterns**

### **Pattern 1: Loading States with Flows**
```kotlin
sealed class UiState<out T> {
    object Idle : UiState<Nothing>()
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}

class NewsViewModel : ViewModel() {
    private val _newsState = MutableStateFlow<UiState<List<News>>>(UiState.Idle)
    val newsState = _newsState.asStateFlow()

    fun loadNews() {
        viewModelScope.launch {
            _newsState.value = UiState.Loading

            repository.getNews()
                .catch { e ->
                    _newsState.value = UiState.Error(e.message ?: "Unknown error")
                }
                .collect { news ->
                    _newsState.value = UiState.Success(news)
                }
        }
    }
}
```

### **Pattern 2: One-Time Events with SharedFlow**
```kotlin
class CheckoutViewModel : ViewModel() {
    private val _checkoutEvents = MutableSharedFlow<CheckoutEvent>()
    val checkoutEvents = _checkoutEvents.asSharedFlow()

    fun processPayment() {
        viewModelScope.launch {
            try {
                val result = paymentRepository.charge()
                _checkoutEvents.emit(CheckoutEvent.PaymentSuccess(result))
            } catch (e: Exception) {
                _checkoutEvents.emit(CheckoutEvent.PaymentFailed(e.message))
            }
        }
    }
}

sealed class CheckoutEvent {
    data class PaymentSuccess(val orderId: String) : CheckoutEvent()
    data class PaymentFailed(val error: String?) : CheckoutEvent()
}
```

### **Pattern 3: Form Validation with Flows**
```kotlin
class LoginViewModel : ViewModel() {
    val email = MutableStateFlow("")
    val password = MutableStateFlow("")

    val isLoginEnabled: StateFlow<Boolean> = combine(
        email,
        password
    ) { email, password ->
        email.isValidEmail() && password.length >= 8
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = false
    )

    val emailError: StateFlow<String?> = email
        .debounce(500)
        .map { if (it.isNotEmpty() && !it.isValidEmail()) "Invalid email" else null }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)
}
```

---

## **Common Interview Scenarios**

### **Scenario 1**: Implement a real-time chat message flow
```kotlin
class ChatRepository {
    fun observeMessages(chatId: String): Flow<List<Message>> = callbackFlow {
        val listener = firestore.collection("chats")
            .document(chatId)
            .collection("messages")
            .orderBy("timestamp")
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    close(error)
                    return@addSnapshotListener
                }

                val messages = snapshot?.documents?.map { it.toObject(Message::class.java)!! }
                    ?: emptyList()
                trySend(messages)
            }

        awaitClose { listener.remove() }
    }
}
```

### **Scenario 2**: Handle multiple data sources (remote + local + cache)
```kotlin
fun getArticles(): Flow<List<Article>> = channelFlow {
    // Emit from memory cache immediately
    memoryCache.get()?.let { send(it) }

    // Then emit from database
    launch {
        database.getArticles().collect { send(it) }
    }

    // Finally fetch from network
    launch {
        try {
            val fresh = api.fetchArticles()
            database.saveArticles(fresh)
            memoryCache.save(fresh)
            send(fresh)
        } catch (e: Exception) {
            // Already sent cached data
        }
    }
}
```

### **Scenario 3**: Implement infinite scroll pagination
```kotlin
class PagingViewModel : ViewModel() {
    private val _pagingFlow = MutableStateFlow(PagingData(items = emptyList(), page = 0))

    val items: StateFlow<List<Item>> = _pagingFlow
        .flatMapLatest { pagingData ->
            flow {
                emit(pagingData.items)

                if (!pagingData.isLoading) {
                    val newItems = repository.fetchPage(pagingData.page)
                    emit(pagingData.items + newItems)
                }
            }
        }
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun loadMore() {
        val current = _pagingFlow.value
        _pagingFlow.value = current.copy(page = current.page + 1, isLoading = true)
    }
}
```

---

## **Key Takeaways for Production**

1. **Use StateFlow for UI state**, SharedFlow for events
2. **Debounce user input** to avoid excessive API calls
3. **Implement offline-first** with cache + network patterns
4. **Handle errors gracefully** with `catch` and `retry`
5. **Convert callbacks to flows** using `callbackFlow`
6. **Test flows** with Turbine or manual collection
7. **Use `flatMapLatest`** for cancellable operations (like search)
8. **Combine flows** when multiple data sources needed
9. **Use `stateIn`** to convert cold flows to hot StateFlows
10. **Always cleanup** in `awaitClose` when using `callbackFlow`