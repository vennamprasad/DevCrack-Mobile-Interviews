## **ViewModel Integration**

### 22. How to integrate ViewModel with Compose?

**Answer:**
Use `viewModel()` or `hiltViewModel()` to obtain ViewModel instances and observe state.

```kotlin
class HomeViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            // Load data
        }
    }
}

@Composable
fun HomeScreen(viewModel: HomeViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.loadData()
    }

    when {
        uiState.isLoading -> LoadingIndicator()
        uiState.error != null -> ErrorMessage(uiState.error)
        else -> ContentView(uiState.data)
    }
}
```

---

### 23. What is `collectAsState()` and `collectAsStateWithLifecycle()`?

**Answer:**

**collectAsState()** - Collects Flow and converts to Compose State
```kotlin
val uiState by viewModel.stateFlow.collectAsState()
```

**collectAsStateWithLifecycle()** - Lifecycle-aware collection (stops when app is backgrounded)
```kotlin
val uiState by viewModel.stateFlow.collectAsStateWithLifecycle()
```

**Use `collectAsStateWithLifecycle()` to:**
- Save battery
- Prevent unnecessary network calls
- Avoid crashes when app is not visible
