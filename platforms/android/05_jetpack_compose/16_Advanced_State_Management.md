## **Advanced State Management**

### 49. What is `produceState` and when to use it?

**Answer:**
`produceState` converts non-Compose state sources into Compose State.

```kotlin
@Composable
fun LoadData(userId: String): State<Result<User>> {
    return produceState<Result<User>>(
        initialValue = Result.Loading,
        key1 = userId
    ) {
        value = Result.Loading
        try {
            val user = repository.getUser(userId)
            value = Result.Success(user)
        } catch (e: Exception) {
            value = Result.Error(e)
        }
    }
}

@Composable
fun UserScreen(userId: String) {
    val userResult by loadData(userId)

    when (userResult) {
        is Result.Loading -> LoadingIndicator()
        is Result.Success -> UserContent(userResult.data)
        is Result.Error -> ErrorMessage(userResult.error)
    }
}
```

**Use cases:**
- Converting callbacks to State
- Polling/streaming data
- Complex async operations

---

### 50. What is `rememberUpdatedState` and why is it important?

**Answer:**
`rememberUpdatedState` creates a State that always has the latest value, useful in long-running effects.

```kotlin
@Composable
fun Timer(onTimeout: () -> Unit) {
    // Capture latest callback
    val currentOnTimeout by rememberUpdatedState(onTimeout)

    LaunchedEffect(Unit) {
        delay(5000)
        // Always calls the latest onTimeout, even if it changed
        currentOnTimeout()
    }
}

// Usage
var message by remember { mutableStateOf("Initial") }
Timer(onTimeout = {
    // This lambda may change, but timer uses latest version
    println(message)
})
```

**Without rememberUpdatedState:**
```kotlin
// ❌ Captures old callback
LaunchedEffect(Unit) {
    delay(5000)
    onTimeout() // May be stale
}
```

---

### 51. How to share state between multiple composables at different levels?

**Answer:**
Multiple approaches:

**1. State Hoisting (Recommended)**
```kotlin
@Composable
fun ParentScreen() {
    var sharedState by remember { mutableStateOf("") }

    ChildA(sharedState) { sharedState = it }
    ChildB(sharedState)
}
```

**2. ViewModel (For business logic)**
```kotlin
@Composable
fun Screen(viewModel: SharedViewModel = viewModel()) {
    val sharedState by viewModel.state.collectAsState()

    ChildA(sharedState) { viewModel.updateState(it) }
    ChildB(sharedState)
}
```

**3. CompositionLocal (For deep trees)**
```kotlin
val LocalSharedState = compositionLocalOf { mutableStateOf("") }

@Composable
fun Parent() {
    val state = remember { mutableStateOf("") }

    CompositionLocalProvider(LocalSharedState provides state) {
        DeepChild() // Can access state anywhere
    }
}
```

---

### 52. What are State Holders and why use them?

**Answer:**
State holders are classes that manage state and business logic for composables.

```kotlin
// State Holder
class SearchState(
    initialQuery: String = "",
    private val searchRepository: SearchRepository
) {
    var query by mutableStateOf(initialQuery)
        private set

    var results by mutableStateOf<List<Result>>(emptyList())
        private set

    var isLoading by mutableStateOf(false)
        private set

    fun updateQuery(newQuery: String) {
        query = newQuery
        search()
    }

    private fun search() {
        isLoading = true
        // Perform search
    }
}

@Composable
fun rememberSearchState(
    initialQuery: String = "",
    searchRepository: SearchRepository
): SearchState {
    return remember(searchRepository) {
        SearchState(initialQuery, searchRepository)
    }
}

@Composable
fun SearchScreen() {
    val searchState = rememberSearchState(
        searchRepository = LocalSearchRepository.current
    )

    SearchContent(
        query = searchState.query,
        results = searchState.results,
        isLoading = searchState.isLoading,
        onQueryChange = searchState::updateQuery
    )
}
```

**Benefits:**
- Encapsulates logic
- Reusable
- Testable
- Survives recomposition
