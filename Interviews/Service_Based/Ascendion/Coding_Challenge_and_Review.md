# 🧪 45-Minute Senior Android Live Technical Interview Kit
> **Role:** Senior Android Engineer (L4 / Lead Level)  
> **Company Context:** Ascendion (Client-Facing Enterprise Digital Engineering)  
> **Total Time:** 45 Minutes Timeboxed  
> **Format:** 
> - **Part 1 (15 Mins):** Code Review & Bug Hunting (PR Review Scenario)  
> - **Part 2 (20 Mins):** Live Coding / Refactoring (Debounced Search + Offline-First Flow)  
> - **Part 3 (10 Mins):** Architectural Stress-Testing & Testing Fire-Drill  
> 
> *(Interviewer Note: Candidate receives problem prompts from Section A; keep Section B Solution & Evaluation Keys for yourself.)*

![Ascendion](https://img.shields.io/badge/Ascendion-Interview_Kit-00B4D8?style=for-the-badge)
![Time](https://img.shields.io/badge/Duration-45_Minutes-orange?style=for-the-badge)
![Senior Android](https://img.shields.io/badge/Level-Senior_%2F_Staff-3DDC84?style=for-the-badge&logo=android)

---

## ⏱️ 45-Minute Stepwise Interview Master Schedule

```
00:00 - 02:00 (02 min) | Brief Intro & Instructions
02:00 - 15:00 (13 min) | Phase 1: Live Code Review & Anti-Pattern Detection
15:00 - 35:00 (20 min) | Phase 2: Live Coding - Debounced Search & Offline Flow
35:00 - 42:00 (07 min) | Phase 3: Architecture Stress-Test & Unit Testing Fire-Drill
42:00 - 45:00 (03 min) | Phase 4: Candidate Q&A & Interview Wrap-Up
```

---

# 🧩 Phase 1: Live Code Review & Anti-Pattern Detection (15 Mins)

### 📋 Section A: Candidate Problem Prompt (Share with Candidate)

> *"You are conducting a Senior Code Review on a Pull Request. The feature fetches user data, updates an active tracking indicator, and automatically navigates home after a 10-second timer.*  
> *Review the code below. Point out any bugs, memory leaks, performance traps, or architectural flaws. Tell me what causes them and how you'd fix them."*

```kotlin
class UserProfileViewModel @Inject constructor(
    private val userRepository: UserRepository,
    private val analyticsTracker: AnalyticsTracker
) : ViewModel() {

    var userState: User? = null
    val isTracking = MutableStateFlow(false)

    fun fetchUserData(userId: String) {
        GlobalScope.launch {
            try {
                val data = userRepository.getUser(userId) // Remote network call
                userState = data
            } catch (e: Exception) {
                println("Error: ${e.message}")
            }
        }
    }

    fun startPeriodicSync() {
        viewModelScope.launch(Dispatchers.IO) {
            while (true) {
                delay(5000)
                val status = userRepository.checkStatus()
                withContext(Dispatchers.Main) {
                    isTracking.value = status
                }
            }
        }
    }
}

@Composable
fun UserProfileScreen(
    userId: String,
    viewModel: UserProfileViewModel,
    onNavigateHome: () -> Unit
) {
    var renderCount by remember { mutableStateOf(0) }
    renderCount++ // Track recompositions

    LaunchedEffect(Unit) {
        viewModel.fetchUserData(userId)
    }

    LaunchedEffect(Unit) {
        delay(10000)
        onNavigateHome()
    }

    val tracking by viewModel.isTracking.collectAsState()

    Column(modifier = Modifier.fillMaxSize()) {
        Text("Profile for User: $userId")
        Text("Renders: $renderCount")

        val user = viewModel.userState
        if (user != null) {
            Text("Name: ${user.name}")
            Text("Email: ${user.email}")
        } else {
            CircularProgressIndicator()
        }

        if (tracking) {
            Text("Status: Active")
        }
    }
}
```

---

### 🔍 Section B: Interviewer Answer Key (Phase 1)

| # | Bug | Root Cause | Impact | Fix |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Infinite Recomposition Loop** | `renderCount++` mutates Compose `State` directly in the Composable body during composition. | 100% CPU lockup, UI freeze / ANR. | Remove mutation from body; use `SideEffect` or profile externally. |
| **2** | **Coroutine Scope Leak** | `GlobalScope.launch` does not cancel when ViewModel is cleared. | Memory leak, waste of network/battery. | Use `viewModelScope.launch`. |
| **3** | **Stale Closure in Navigation Timer** | `LaunchedEffect(Unit)` captures `onNavigateHome` in its closure over a 10s delay. | If parent recomposes, triggers outdated navigation callback. | Wrap with `val currentOnNavigateHome by rememberUpdatedState(onNavigateHome)`. |
| **4** | **Unobservable State Property** | `var userState: User? = null` is a plain Kotlin property. | Compose cannot track mutations. Screen remains stuck in `CircularProgressIndicator` forever. | Use `MutableStateFlow<UiState>` + `collectAsStateWithLifecycle()`. |
| **5** | **Volatile Key in `LaunchedEffect`** | Passed `Unit` instead of `userId`. | Screen does not reload if `userId` changes (e.g. clicking different profile). | Change key to `LaunchedEffect(userId)`. |
| **6** | **Cancellation Ignored in While Loop** | `while (true)` with `isTracking.value = status` using redundant `withContext(Dispatchers.Main)`. | `StateFlow` is thread-safe; `withContext(Main)` is redundant. Loop should use `while (isActive)`. | Use `while (isActive)` without manual dispatch switching. |

---

# 💻 Phase 2: Live Coding - Debounced Search & Offline Flow (20 Mins)

### 📋 Section A: Candidate Problem Prompt (Share with Candidate)

> *"In enterprise apps, search fields often suffer from race conditions, redundant network calls, and sluggish offline performance.*  
> *Implement a `SearchViewModel` and its reactive pipeline that satisfies these requirements:*  
> 1. *Accepts a user query stream as they type.*  
> 2. *Debounces input by 300ms to avoid spamming the backend.*  
> 3. *Ignores duplicate consecutive queries.*  
> 4. *Cancels any previous in-flight network request if the user types a new character (`flatMapLatest`).*  
> 5. *Emits a clear sealed UI state: `Idle`, `Loading`, `Success(List<Product>)`, `Empty`, `Error(message)`.*  
> 6. *Queries local Room database cache before hitting remote API.*"

---

### 🔍 Section B: Interviewer Solution & Code Standard (Phase 2)

```kotlin
// 1. Clean UI State Modeling
sealed interface SearchUiState {
    object Idle : SearchUiState
    object Loading : SearchUiState
    data class Success(val products: List<Product>) : SearchUiState
    object Empty : SearchUiState
    data class Error(val message: String) : SearchUiState
}

// 2. ViewModel Implementation
@HiltViewModel
class SearchViewModel @Inject constructor(
    private val searchRepository: SearchRepository
) : ViewModel() {

    private val searchQuery = MutableStateFlow("")

    @OptIn(FlowPreview::class, ExperimentalCoroutinesApi::class)
    val uiState: StateFlow<SearchUiState> = searchQuery
        .debounce(300L) // Wait 300ms pause in typing
        .map { it.trim() }
        .distinctUntilChanged() // Ignore duplicate keystrokes
        .flatMapLatest { query ->
            if (query.isBlank()) {
                flowOf(SearchUiState.Idle)
            } else {
                searchRepository.searchProducts(query)
                    .map { products ->
                        if (products.isEmpty()) SearchUiState.Empty
                        else SearchUiState.Success(products)
                    }
                    .catch { e -> emit(SearchUiState.Error(e.localizedMessage ?: "Network failed")) }
                    .onStart { emit(SearchUiState.Loading) }
            }
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000L), // Survives 5s config changes
            initialValue = SearchUiState.Idle
        )

    fun onQueryChanged(newQuery: String) {
        searchQuery.value = newQuery
    }
}

// 3. Offline-First Repository Pattern
class DefaultSearchRepository @Inject constructor(
    private val productDao: ProductDao,
    private val apiService: SearchApiService
) : SearchRepository {

    override fun searchProducts(query: String): Flow<List<Product>> = flow {
        // Step 1: Emit local cached data immediately for instant response
        val cached = productDao.searchCachedProducts("%$query%")
        if (cached.isNotEmpty()) {
            emit(cached.map { it.toDomain() })
        }

        // Step 2: Fetch fresh data from network
        val remote = apiService.search(query)
        
        // Step 3: Cache into Room & emit latest results
        productDao.insertAll(remote.map { it.toEntity() })
        emit(remote.map { it.toDomain() })
    }.flowOn(Dispatchers.IO)
}
```

### What to Look For (Evaluation Bar):
- ✅ Uses `flatMapLatest`: Cancels previous search request when a new character is emitted. (If they use `flatMapMerge` or `map`, ask: *"What happens if query 'A' takes 2 seconds and query 'AB' takes 100ms?"* $\rightarrow$ Race condition!).
- ✅ Uses `SharingStarted.WhileSubscribed(5000L)`: Proactively explains that 5000ms keeps the upstream Flow alive during Activity rotation/recreation without wasting background resources.
- ✅ Uses `flowOn(Dispatchers.IO)`: Correctly shifts disk/network I/O off the main thread.

---

# ⚡ Phase 3: Architectural Stress-Testing & Testing Fire-Drill (10 Mins)

Ask the candidate 2 or 3 rapid-fire architectural questions to test their real-world experience:

### Question 1: Unit Testing Coroutines & Turbine
> *"How would you unit-test this `SearchViewModel`? Why does `runTest` matter, and how do you handle the 300ms debounce during testing without using `Thread.sleep()`?"*

#### Expected Senior Answer:
- Use `runTest` from `kotlinx-coroutines-test`. It uses virtual time (`TestCoroutineScheduler`), allowing the 300ms debounce to skip forward instantaneously via `advanceTimeBy(300)` or `advanceUntilIdle()`.
- Replace `Dispatchers.Main` using `Dispatchers.setMain(StandardTestDispatcher())`.
- Use **Turbine** (`uiState.test { ... }`) to assert sequential emissions: `awaitItem()` $\rightarrow$ `Loading` $\rightarrow$ `Success`.

```kotlin
@Test
fun `when query typed, emits loading then success after debounce`() = runTest {
    val repository = FakeSearchRepository()
    val viewModel = SearchViewModel(repository)

    viewModel.uiState.test {
        assertEquals(SearchUiState.Idle, awaitItem())

        viewModel.onQueryChanged("Shoes")
        advanceTimeBy(301L) // Fast-forward virtual time past debounce

        assertEquals(SearchUiState.Loading, awaitItem())
        val successState = awaitItem() as SearchUiState.Success
        assertEquals(2, successState.products.size)
    }
}
```

---

### Question 2: Multi-Module Architecture & Dependency Rules
> *"In a multi-module enterprise app with 40+ Gradle modules, where should the `ProductDao`, `SearchRepository`, and `SearchViewModel` reside? How do you prevent `:feature:cart` from circularly depending on `:feature:search`?"*

```mermaid
graph TD
    A[:feature:search] --> B[:core:domain (UseCases & Interfaces)]
    C[:feature:cart] --> B
    D[:core:database (Room & DAOs)] --> B
    E[:core:network (Retrofit)] --> B
    F[:app (Hilt Dependency Container)] --> A
    F --> C
    F --> D
    F --> E
```

#### Expected Senior Answer:
- Features should **never directly depend on each other** (feature-to-feature dependency leads to circular dependencies and monolithic build bottlenecks).
- **Core-Domain Module:** Holds pure Kotlin data models and repository interfaces (`SearchRepository`).
- **Core-Data/Database Module:** Implements `SearchRepositoryImpl`, Room entities, and DAOs.
- **Navigation / Inter-Module Communication:** Handled via deep links, Compose destination routing interfaces, or an aggregator `:app` module wire-up.

---

# 📊 Phase 4: Candidate Scoring Rubric (45-Min Evaluation)

| Metric | 1 - Strong No Hire | 2 - No Hire | 3 - Hire (Senior L4) | 4 - Strong Hire (Staff/Lead) |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Code Review** (15 Mins) | Found $\le 2$ obvious bugs. Could not explain why `renderCount++` locks UI or how `rememberUpdatedState` works. | Found 3 bugs. Needed strong hints on stale closure or Compose state tracking. | Found 4–5 bugs quickly. Explained root cause and wrote clean refactored fix. | Spotted all 6 bugs immediately. Addressed snapshot state internals and lifecycle collection. |
| **Phase 2: Live Coding** (20 Mins) | Struggled with Coroutines syntax. Blocked main thread or created race conditions with nested launches. | Wrote search logic but missed `flatMapLatest` (race condition) or `debounce`. | Wrote complete reactive pipeline with `debounce`, `flatMapLatest`, and UDF state. | Flawlessly implemented reactive pipeline + offline-first Room cache + `SharingStarted.WhileSubscribed(5000)`. |
| **Phase 3: Testing & Architecture** (10 Mins) | Cannot explain how to unit-test Coroutines or virtual time advancement. | Knows Mockito, but unclear on `StandardTestDispatcher`, `Turbine`, or multi-module rules. | Explains `runTest`, `advanceTimeBy`, and clean multi-module decoupling. | Authoritatively details virtual time scheduling, Turbine assertions, and API boundary inversion. |

---

## 📝 45-Minute Quick Decision Sheet

```markdown
Candidate Name: _______________________    Date: ______________
Interviewer:    _______________________    Time: 45 Minutes

Final Recommendation: 
[ ] Strong Hire (L4+/Lead)   [ ] Hire (Senior L4)   [ ] No Hire   [ ] Strong No Hire

Scores:
- Phase 1 (Code Review):     [ ] / 4
- Phase 2 (Live Coding):     [ ] / 4
- Phase 3 (Architecture):    [ ] / 4
- Communication & Polish:    [ ] / 4

Key Takeaway / Hiring Rationale:
_________________________________________________________________________
_________________________________________________________________________
```
