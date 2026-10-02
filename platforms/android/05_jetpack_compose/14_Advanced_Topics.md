## **Advanced Topics**

### 37. What is the Compose Compiler Plugin?

**Answer:**
The Compose Compiler is a Kotlin compiler plugin that transforms `@Composable` functions to enable:
- Recomposition tracking
- State observation
- Smart recomposition skipping
- Runtime optimization

**Important:** Compose Compiler version must match Kotlin version.

```kotlin
// build.gradle.kts
composeOptions {
    kotlinCompilerExtensionVersion = "1.5.3"
}
```

---

### 38. How to handle configuration changes in Compose?

**Answer:**
Compose handles configuration changes automatically through:

1. **rememberSaveable** - Survives configuration changes
2. **ViewModel** - Survives configuration changes
3. **SavedStateHandle** - In ViewModel for complex state

```kotlin
@Composable
fun ConfigurationSafeScreen(
    viewModel: MyViewModel = viewModel()
) {
    // Survives rotation
    val uiState by viewModel.state.collectAsState()

    // Also survives rotation
    var localState by rememberSaveable { mutableStateOf("") }
}
```

---

### 39. How to implement gesture handling?

**Answer:**
Use `Modifier.pointerInput` with gesture detectors.

```kotlin
@Composable
fun DraggableBox() {
    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }

    Box(
        modifier = Modifier
            .offset { IntOffset(offsetX.roundToInt(), offsetY.roundToInt()) }
            .size(100.dp)
            .background(Color.Blue)
            .pointerInput(Unit) {
                detectDragGestures { change, dragAmount ->
                    change.consume()
                    offsetX += dragAmount.x
                    offsetY += dragAmount.y
                }
            }
    )
}
```

**Available gesture detectors:**
- `detectTapGestures` - Tap, double tap, long press
- `detectDragGestures` - Drag
- `detectTransformGestures` - Pinch, zoom, rotate
- `detectHorizontalDragGestures` - Horizontal drag only

---

### 40. How to save and restore scroll position?

**Answer:**

```kotlin
@Composable
fun ScrollableList() {
    val listState = rememberLazyListState()

    // Save scroll position
    val scrollPosition = rememberSaveable(
        saver = listState.firstVisibleItemScrollOffset
    ) { mutableStateOf(0) }

    LaunchedEffect(scrollPosition.value) {
        listState.scrollToItem(scrollPosition.value)
    }

    LazyColumn(state = listState) {
        items(100) { index ->
            Text("Item $index")
        }
    }

    // Save on scroll
    DisposableEffect(Unit) {
        onDispose {
            scrollPosition.value = listState.firstVisibleItemIndex
        }
    }
}
```

---

### 41. What is Compose Multiplatform?

**Answer:**
Compose Multiplatform by JetBrains extends Jetpack Compose to support:
- Desktop (Windows, macOS, Linux)
- Web (experimental)
- iOS (alpha)

```kotlin
// Common code
@Composable
fun App() {
    MaterialTheme {
        Text("Hello from Compose Multiplatform!")
    }
}

// Android
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { App() }
    }
}

// Desktop
fun main() = application {
    Window(onCloseRequest = ::exitApplication) {
        App()
    }
}
```

---

### 42. How to implement pull-to-refresh?

**Answer:**

```kotlin
@OptIn(ExperimentalMaterialApi::class)
@Composable
fun PullToRefreshScreen() {
    var isRefreshing by remember { mutableStateOf(false) }
    val pullRefreshState = rememberPullRefreshState(
        refreshing = isRefreshing,
        onRefresh = {
            isRefreshing = true
            // Simulate refresh
            kotlinx.coroutines.GlobalScope.launch {
                delay(2000)
                isRefreshing = false
            }
        }
    )

    Box(Modifier.pullRefresh(pullRefreshState)) {
        LazyColumn {
            items(50) { index ->
                Text("Item $index", modifier = Modifier.padding(16.dp))
            }
        }

        PullRefreshIndicator(
            refreshing = isRefreshing,
            state = pullRefreshState,
            modifier = Modifier.align(Alignment.TopCenter)
        )
    }
}
```

---

### 43. How to implement forms with validation?

**Answer:**

```kotlin
@Composable
fun RegistrationForm() {
    var email by rememberSaveable { mutableStateOf("") }
    var password by rememberSaveable { mutableStateOf("") }
    var emailError by remember { mutableStateOf<String?>(null) }
    var passwordError by remember { mutableStateOf<String?>(null) }

    Column(modifier = Modifier.padding(16.dp)) {
        OutlinedTextField(
            value = email,
            onValueChange = {
                email = it
                emailError = if (Patterns.EMAIL_ADDRESS.matcher(it).matches()) {
                    null
                } else {
                    "Invalid email"
                }
            },
            label = { Text("Email") },
            isError = emailError != null,
            supportingText = { emailError?.let { Text(it) } }
        )

        OutlinedTextField(
            value = password,
            onValueChange = {
                password = it
                passwordError = if (it.length >= 8) {
                    null
                } else {
                    "Password must be at least 8 characters"
                }
            },
            label = { Text("Password") },
            visualTransformation = PasswordVisualTransformation(),
            isError = passwordError != null,
            supportingText = { passwordError?.let { Text(it) } }
        )

        Button(
            onClick = { /* Submit */ },
            enabled = emailError == null && passwordError == null
        ) {
            Text("Register")
        }
    }
}
```

---

### 44. How to migrate from View system to Compose?

**Answer:**

**Migration Strategy:**

1. **Incremental adoption** - Use ComposeView in existing screens
2. **Start with new features** - Build new screens in Compose
3. **Migrate bottom-up** - Start with leaf components
4. **Share ViewModels** - Use same ViewModels for both systems

```kotlin
// Step 1: Wrap Compose in existing Activity
class OldActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.old_layout)

        findViewById<ComposeView>(R.id.compose_section).setContent {
            NewComposeFeature()
        }
    }
}

// Step 2: Eventually migrate entire screen
class NewActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyAppTheme {
                FullComposeScreen()
            }
        }
    }
}
```

---

### 45. Best practices for Compose development?

**Answer:**

**Architecture:**
- Use MVVM or MVI pattern
- Keep composables small and focused
- Hoist state to appropriate level
- Use ViewModels for business logic

**Performance:**
- Mark data classes as @Immutable/@Stable
- Use keys in lists
- Avoid creating lambdas in composition
- Use derivedStateOf for expensive calculations

**Testing:**
- Write UI tests with ComposeTestRule
- Use semantics for testability
- Test ViewModels separately

**Code Organization:**
- Separate stateless and stateful composables
- Create reusable components
- Use preview functions extensively

```kotlin
// Good structure
@Composable
fun UserScreen(
    viewModel: UserViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    UserScreenContent(
        uiState = uiState,
        onAction = viewModel::handleAction
    )
}

@Composable
private fun UserScreenContent(
    uiState: UserUiState,
    onAction: (UserAction) -> Unit
) {
    // Stateless UI
}

@Preview
@Composable
private fun UserScreenPreview() {
    UserScreenContent(
        uiState = UserUiState.Mock,
        onAction = {}
    )
}
```
