## **Error Handling & Edge Cases**

### 64. How to handle errors in Compose?

**Answer:**

```kotlin
// 1. Error Boundary pattern
@Composable
fun ErrorBoundary(
    fallback: @Composable (Throwable) -> Unit = { DefaultErrorScreen(it) },
    content: @Composable () -> Unit
) {
    var error by remember { mutableStateOf<Throwable?>(null) }

    if (error != null) {
        fallback(error!!)
    } else {
        try {
            content()
        } catch (e: Exception) {
            error = e
        }
    }
}

// Usage
ErrorBoundary {
    MyScreen()
}

// 2. With ViewModel
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val exception: Throwable) : UiState<Nothing>()
}

@Composable
fun DataScreen(viewModel: DataViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    when (val state = uiState) {
        is UiState.Loading -> LoadingIndicator()
        is UiState.Success -> ContentView(state.data)
        is UiState.Error -> ErrorView(
            error = state.exception,
            onRetry = { viewModel.retry() }
        )
    }
}

// 3. Snackbar for non-critical errors
@Composable
fun ScreenWithSnackbar() {
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) {
        // Handle error
        LaunchedEffect(errorState) {
            errorState?.let { error ->
                scope.launch {
                    snackbarHostState.showSnackbar(
                        message = error.message ?: "An error occurred",
                        actionLabel = "Retry"
                    )
                }
            }
        }
    }
}
```

---

### 65. How to handle back press in Compose?

**Answer:**

```kotlin
@Composable
fun BackHandlerExample() {
    var showDialog by remember { mutableStateOf(false) }

    // Intercept back press
    BackHandler(enabled = showDialog) {
        showDialog = false
    }

    if (showDialog) {
        AlertDialog(
            onDismissRequest = { showDialog = false },
            title = { Text("Confirm") },
            text = { Text("Are you sure?") },
            confirmButton = {
                Button(onClick = { showDialog = false }) {
                    Text("Yes")
                }
            }
        )
    }
}

// Multiple BackHandlers (last one wins)
@Composable
fun NestedBackHandlers() {
    var step by remember { mutableStateOf(1) }

    BackHandler(enabled = step > 1) {
        step--
    }

    when (step) {
        1 -> Step1(onNext = { step = 2 })
        2 -> Step2(onNext = { step = 3 })
        3 -> Step3()
    }
}

// With NavController
@Composable
fun ScreenWithNavigation(navController: NavController) {
    BackHandler {
        // Custom back behavior
        if (hasUnsavedChanges) {
            showConfirmDialog = true
        } else {
            navController.popBackStack()
        }
    }
}
```

---

### 66. How to handle configuration changes properly?

**Answer:**

```kotlin
// 1. Use ViewModel for data
class MyViewModel : ViewModel() {
    private val _data = MutableStateFlow<List<Item>>(emptyList())
    val data = _data.asStateFlow()

    // Survives configuration changes
}

// 2. Use rememberSaveable for UI state
@Composable
fun ConfigSafeScreen() {
    // Lost on rotation
    var tempState by remember { mutableStateOf("") }

    // Survives rotation
    var savedState by rememberSaveable { mutableStateOf("") }

    // Survives rotation (custom objects)
    var customState by rememberSaveable(stateSaver = CustomStateSaver) {
        mutableStateOf(CustomObject())
    }
}

// 3. Custom Saver
data class SearchFilters(
    val category: String = "",
    val minPrice: Int = 0,
    val maxPrice: Int = 1000
)

val SearchFiltersSaver = Saver<SearchFilters, List<Any>>(
    save = { listOf(it.category, it.minPrice, it.maxPrice) },
    restore = {
        SearchFilters(
            category = it[0] as String,
            minPrice = it[1] as Int,
            maxPrice = it[2] as Int
        )
    }
)

@Composable
fun SearchScreen() {
    var filters by rememberSaveable(stateSaver = SearchFiltersSaver) {
        mutableStateOf(SearchFilters())
    }
}

// 4. Handle orientation-specific layouts
@Composable
fun AdaptiveLayout() {
    val configuration = LocalConfiguration.current

    when (configuration.orientation) {
        Configuration.ORIENTATION_LANDSCAPE -> {
            Row { /* Landscape layout */ }
        }
        else -> {
            Column { /* Portrait layout */ }
        }
    }
}
```
