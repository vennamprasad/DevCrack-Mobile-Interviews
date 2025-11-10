# Jetpack Compose Interview Questions & Answers

A comprehensive guide covering basic to advanced Jetpack Compose concepts with clear explanations and code examples.

---

## **Basics**

### 1. What is Jetpack Compose?

**Answer:**
Jetpack Compose is Android's modern declarative UI toolkit that simplifies and accelerates UI development. Instead of imperative XML layouts, you describe your UI using Kotlin functions.

**Key Benefits:**
- Less boilerplate code
- Built-in Material Design components
- Reactive programming model
- Better performance through smart recomposition
- Easy integration with existing Views

```kotlin
@Composable
fun WelcomeScreen() {
    Text(text = "Hello Compose!")
}
```

---

### 2. What is a @Composable function?

**Answer:**
A function annotated with `@Composable` that describes a piece of UI. These functions can:
- Emit UI elements
- Call other composable functions
- Be managed by the Compose runtime for recomposition

```kotlin
@Composable
fun Greeting(name: String) {
    Text(
        text = "Hello, $name!",
        style = MaterialTheme.typography.h5
    )
}
```

**Important Rules:**
- Must be called from another composable or composition context
- Cannot return values (void/Unit)
- Can be called conditionally or in loops

---

### 3. What is State in Compose?

**Answer:**
State is any value that can change over time. When state changes, Compose automatically recomposes (re-executes) the UI that depends on that state.

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Column {
        Text("Count: $count")
        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}
```

**State Types:**
- `mutableStateOf()` - Basic observable state
- `StateFlow` - For ViewModels
- `LiveData` - Legacy support
- `MutableState<T>` - Generic state holder

---

### 4. What is the difference between `remember` and `rememberSaveable`?

**Answer:**

| Feature | remember | rememberSaveable |
|---------|----------|------------------|
| **Survives recomposition** | ✅ Yes | ✅ Yes |
| **Survives configuration changes** | ❌ No | ✅ Yes |
| **Survives process death** | ❌ No | ✅ Yes |
| **Requires Parcelable** | ❌ No | ✅ Yes (for custom types) |

```kotlin
@Composable
fun Example() {
    // Lost on rotation
    var tempCount by remember { mutableStateOf(0) }

    // Survives rotation and process death
    var savedCount by rememberSaveable { mutableStateOf(0) }
}
```

---

### 5. What is Recomposition?

**Answer:**
Recomposition is the process where Compose re-executes composable functions when their observed state changes. It's **intelligent** - only affected composables recompose, not the entire tree.

**Recomposition Principles:**
- Happens automatically when state changes
- Can occur in any order
- Can be skipped if inputs haven't changed
- Should be side-effect free

```kotlin
@Composable
fun RecompositionExample() {
    var count by remember { mutableStateOf(0) }

    // Only recomposes when count changes
    Text("Count: $count")

    // Never recomposes
    Text("Static text")
}
```

---

## **State Management**

### 6. What is State Hoisting?

**Answer:**
State hoisting is a pattern where you move state to a composable's caller to make the composable stateless. This enables:
- Single source of truth
- Reusability
- Easier testing

```kotlin
// ❌ Stateful (not reusable)
@Composable
fun SearchBar() {
    var query by remember { mutableStateOf("") }
    TextField(value = query, onValueChange = { query = it })
}

// ✅ Stateless (reusable)
@Composable
fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit
) {
    TextField(value = query, onValueChange = onQueryChange)
}
```

---

### 7. How to create a stateless composable?

**Answer:**
Accept state via parameters and emit events via callbacks instead of holding internal state.

```kotlin
@Composable
fun CheckboxWithLabel(
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
    label: String
) {
    Row(
        modifier = Modifier.clickable { onCheckedChange(!checked) }
    ) {
        Checkbox(checked = checked, onCheckedChange = onCheckedChange)
        Text(text = label)
    }
}
```

---

### 8. What is `derivedStateOf` and when should you use it?

**Answer:**
`derivedStateOf` creates a computed state that only recomposes when the calculation result changes, not when inputs change.

**Use when:**
- You have expensive calculations based on state
- You want to avoid unnecessary recompositions

```kotlin
@Composable
fun MessageList(messages: List<Message>) {
    val listState = rememberLazyListState()

    // Only recomposes when result changes (not on every scroll)
    val showButton by remember {
        derivedStateOf {
            listState.firstVisibleItemIndex > 0
        }
    }

    if (showButton) {
        FloatingActionButton(onClick = { /* scroll to top */ }) {
            Icon(Icons.Default.ArrowUpward, "Scroll to top")
        }
    }
}
```

---

### 9. What is `snapshotFlow` and how is it used?

**Answer:**
`snapshotFlow` converts Compose state reads into a Kotlin Flow, allowing you to use Flow operators like `debounce`, `filter`, etc.

```kotlin
@Composable
fun SearchScreen() {
    var query by remember { mutableStateOf("") }

    LaunchedEffect(Unit) {
        snapshotFlow { query }
            .debounce(300)
            .filter { it.length >= 3 }
            .collect { searchQuery ->
                // Perform search
            }
    }
}
```

---

## **Side Effects**

### 10. What are Side Effects in Compose?

**Answer:**
Side effects are operations that happen outside the scope of a composable function, such as:
- Launching coroutines
- Updating external state
- Registering callbacks
- Analytics tracking

**Side Effect APIs:**
- `LaunchedEffect` - For coroutines
- `DisposableEffect` - For cleanup
- `SideEffect` - For non-suspending side effects
- `rememberCoroutineScope` - For event-driven coroutines

---

### 11. Explain `LaunchedEffect` with examples.

**Answer:**
`LaunchedEffect` runs a suspend block when the composable enters composition and cancels it when keys change or composition leaves.

```kotlin
@Composable
fun UserProfile(userId: String) {
    var user by remember { mutableStateOf<User?>(null) }

    // Runs when userId changes
    LaunchedEffect(userId) {
        user = repository.getUser(userId)
    }

    user?.let { UserCard(it) }
}
```

**Key Points:**
- Takes one or more keys
- Relaunches when any key changes
- Automatically cancels on composition exit

---

### 12. What is `DisposableEffect` used for?

**Answer:**
`DisposableEffect` is used for side effects that require cleanup (like registering/unregistering listeners).

```kotlin
@Composable
fun LocationTracker() {
    val context = LocalContext.current

    DisposableEffect(Unit) {
        val locationManager = context.getSystemService(LocationManager::class.java)
        val listener = LocationListener { location ->
            // Handle location
        }

        locationManager.requestLocationUpdates(
            LocationManager.GPS_PROVIDER,
            1000L,
            10f,
            listener
        )

        onDispose {
            locationManager.removeUpdates(listener)
        }
    }
}
```

---

### 13. What is the difference between `LaunchedEffect` and `rememberCoroutineScope`?

**Answer:**

| Feature | LaunchedEffect | rememberCoroutineScope |
|---------|----------------|------------------------|
| **When it runs** | Automatically on composition | Manually triggered |
| **Use case** | Key-based effects | Event-driven actions |
| **Lifecycle** | Tied to keys | Tied to composition |

```kotlin
@Composable
fun Example() {
    val scope = rememberCoroutineScope()

    // Auto-runs on composition
    LaunchedEffect(Unit) {
        delay(1000)
        println("Auto-triggered")
    }

    // Only runs on button click
    Button(
        onClick = {
            scope.launch {
                delay(1000)
                println("Manually triggered")
            }
        }
    ) {
        Text("Click Me")
    }
}
```

---

### 14. What is `SideEffect` and when to use it?

**Answer:**
`SideEffect` runs after every successful recomposition for non-suspending side effects.

```kotlin
@Composable
fun AnalyticsScreen(screenName: String) {
    SideEffect {
        // Logs every time screenName changes
        analytics.logScreenView(screenName)
    }
}
```

**Use cases:**
- Analytics tracking
- Updating non-Compose objects
- Publishing state to external observers

---

## **Layout & UI**

### 15. What are Modifiers in Compose?

**Answer:**
Modifiers are used to decorate or configure composables. They are:
- **Immutable** - each modification creates a new Modifier
- **Chainable** - order matters
- **Reusable** - can be stored and reused

```kotlin
@Composable
fun ModifierExample() {
    Text(
        text = "Hello",
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .background(Color.Blue)
            .clickable { /* action */ }
    )
}
```

**Common Modifiers:**
- Layout: `size`, `padding`, `fillMaxWidth`, `weight`
- Drawing: `background`, `border`, `clip`, `shadow`
- Interaction: `clickable`, `draggable`, `scrollable`

---

### 16. Explain `Row`, `Column`, and `Box` layouts.

**Answer:**

**Row** - Horizontal layout
```kotlin
Row(
    modifier = Modifier.fillMaxWidth(),
    horizontalArrangement = Arrangement.SpaceBetween,
    verticalAlignment = Alignment.CenterVertically
) {
    Text("Left")
    Text("Right")
}
```

**Column** - Vertical layout
```kotlin
Column(
    modifier = Modifier.fillMaxHeight(),
    verticalArrangement = Arrangement.SpaceEvenly,
    horizontalAlignment = Alignment.CenterHorizontally
) {
    Text("Top")
    Text("Bottom")
}
```

**Box** - Stack/Overlay layout
```kotlin
Box(modifier = Modifier.size(200.dp)) {
    Image(...)
    Text(
        "Overlay Text",
        modifier = Modifier.align(Alignment.BottomCenter)
    )
}
```

---

### 17. What are Lazy Composables? How do they work?

**Answer:**
Lazy composables (`LazyColumn`, `LazyRow`, `LazyVerticalGrid`) render only visible items, similar to RecyclerView.

```kotlin
@Composable
fun MessageList(messages: List<Message>) {
    LazyColumn {
        items(
            items = messages,
            key = { it.id } // Important for optimization
        ) { message ->
            MessageItem(message)
        }
    }
}
```

**Benefits:**
- Efficient memory usage
- Smooth scrolling
- Built-in scroll state
- No adapter needed

---

### 18. Why are keys important in Lazy lists?

**Answer:**
Keys help Compose identify items across recompositions, enabling:
- Proper animations
- State preservation
- Performance optimization

```kotlin
LazyColumn {
    // ❌ Without key - poor performance
    items(users) { user ->
        UserCard(user)
    }

    // ✅ With key - optimized
    items(users, key = { it.id }) { user ->
        UserCard(user)
    }
}
```

---

### 19. How to create custom layouts in Compose?

**Answer:**
Use the `Layout` composable to create custom layouts with full control over measurement and placement.

```kotlin
@Composable
fun CustomLayout(
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Layout(
        modifier = modifier,
        content = content
    ) { measurables, constraints ->
        // Measure children
        val placeables = measurables.map { it.measure(constraints) }

        // Calculate layout size
        val width = placeables.maxOf { it.width }
        val height = placeables.sumOf { it.height }

        // Place children
        layout(width, height) {
            var yPosition = 0
            placeables.forEach { placeable ->
                placeable.placeRelative(0, yPosition)
                yPosition += placeable.height
            }
        }
    }
}
```

---

## **Navigation**

### 20. How does Navigation work in Compose?

**Answer:**
Compose Navigation uses `NavHost` and `NavController` to navigate between composable screens.

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(onNavigateToDetail = { id ->
                navController.navigate("detail/$id")
            })
        }
        composable(
            route = "detail/{id}",
            arguments = listOf(navArgument("id") { type = NavType.IntType })
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getInt("id")
            DetailScreen(id = id)
        }
    }
}
```

---

### 21. How to pass arguments in Compose Navigation?

**Answer:**
Use route placeholders and navArguments.

```kotlin
// Define route with argument
composable(
    route = "profile/{userId}",
    arguments = listOf(
        navArgument("userId") {
            type = NavType.StringType
            nullable = false
        }
    )
) { backStackEntry ->
    val userId = backStackEntry.arguments?.getString("userId")
    ProfileScreen(userId = userId!!)
}

// Navigate with argument
navController.navigate("profile/$userId")
```

**For complex objects, use:**
- JSON serialization
- Shared ViewModel
- SavedStateHandle

---

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

---

## **Theming & Material Design**

### 24. How to implement theming in Compose?

**Answer:**
Use `MaterialTheme` to define colors, typography, and shapes.

```kotlin
private val LightColorScheme = lightColorScheme(
    primary = Purple500,
    secondary = Teal200,
    background = Color.White
)

private val DarkColorScheme = darkColorScheme(
    primary = Purple200,
    secondary = Teal200,
    background = Color.Black
)

@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

---

### 25. What is `CompositionLocal` and when to use it?

**Answer:**
`CompositionLocal` provides implicit dependency injection through the composition tree.

```kotlin
val LocalUser = compositionLocalOf<User?> { null }

@Composable
fun App() {
    CompositionLocalProvider(LocalUser provides currentUser) {
        MainScreen() // Can access LocalUser
    }
}

@Composable
fun ProfileButton() {
    val user = LocalUser.current // Access provided value
    Text("Hi, ${user?.name}")
}
```

**Common built-in CompositionLocals:**
- `LocalContext` - Android Context
- `LocalConfiguration` - Device configuration
- `LocalDensity` - Screen density

---

## **Animations**

### 26. How to animate values in Compose?

**Answer:**
Use `animate*AsState` for simple animations.

```kotlin
@Composable
fun AnimatedBox() {
    var expanded by remember { mutableStateOf(false) }

    val size by animateDpAsState(
        targetValue = if (expanded) 200.dp else 100.dp,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        )
    )

    Box(
        modifier = Modifier
            .size(size)
            .background(Color.Blue)
            .clickable { expanded = !expanded }
    )
}
```

**Available animate functions:**
- `animateDpAsState`
- `animateColorAsState`
- `animateFloatAsState`
- `animateIntAsState`

---

### 27. What is `AnimatedVisibility` and how to use it?

**Answer:**
`AnimatedVisibility` animates the appearance and disappearance of content.

```kotlin
@Composable
fun AnimatedContent() {
    var visible by remember { mutableStateOf(false) }

    Column {
        Button(onClick = { visible = !visible }) {
            Text("Toggle")
        }

        AnimatedVisibility(
            visible = visible,
            enter = fadeIn() + slideInVertically(),
            exit = fadeOut() + slideOutVertically()
        ) {
            Text("I'm animated!")
        }
    }
}
```

---

### 28. How to create complex animations with `updateTransition`?

**Answer:**
`updateTransition` coordinates multiple animated values.

```kotlin
@Composable
fun MultiPropertyAnimation() {
    var selected by remember { mutableStateOf(false) }
    val transition = updateTransition(selected, label = "selected")

    val size by transition.animateDp(label = "size") { isSelected ->
        if (isSelected) 150.dp else 100.dp
    }

    val color by transition.animateColor(label = "color") { isSelected ->
        if (isSelected) Color.Blue else Color.Gray
    }

    Box(
        modifier = Modifier
            .size(size)
            .background(color)
            .clickable { selected = !selected }
    )
}
```

---

## **Performance & Optimization**

### 29. How to optimize recomposition?

**Answer:**

**Best Practices:**

1. **Hoist state properly**
```kotlin
// ❌ Bad - entire screen recomposes
@Composable
fun Screen() {
    var query by remember { mutableStateOf("") }
    Column {
        SearchBar(query) { query = it }
        ResultsList(query)
    }
}

// ✅ Good - only SearchBar recomposes
@Composable
fun Screen() {
    Column {
        var query by remember { mutableStateOf("") }
        SearchBar(query) { query = it }
        ResultsList(query)
    }
}
```

2. **Use stable parameters**
```kotlin
// ❌ Creates new lambda every recomposition
@Composable
fun List() {
    items.forEach { item ->
        Item(onClick = { handleClick(item) })
    }
}

// ✅ Stable lambda
@Composable
fun List() {
    val onClick = remember { { item: Item -> handleClick(item) } }
    items.forEach { item ->
        Item(onClick = { onClick(item) })
    }
}
```

3. **Use keys in lists**
4. **Mark data classes as @Immutable or @Stable**
5. **Use derivedStateOf for expensive calculations**

---

### 30. What are `@Stable` and `@Immutable` annotations?

**Answer:**
These annotations help the Compose compiler optimize recomposition.

**@Immutable** - Values never change after construction
```kotlin
@Immutable
data class User(val id: Int, val name: String)
```

**@Stable** - Values may change, but Compose will be notified
```kotlin
@Stable
class ViewModel {
    var state by mutableStateOf(State())
}
```

**Effects:**
- Compose can skip recomposition if parameters haven't changed
- Better performance in lists
- Reduced unnecessary renders

---

### 31. How to debug performance issues in Compose?

**Answer:**

**Tools:**

1. **Layout Inspector** - Shows recomposition counts
2. **Compose Compiler Metrics** - Generate reports
```kotlin
// build.gradle.kts
tasks.withType<KotlinCompile>().configureEach {
    kotlinOptions {
        freeCompilerArgs += listOf(
            "-P", "plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=..."
        )
    }
}
```

3. **Recomposition Highlighting**
```kotlin
@Composable
fun DebugComposable() {
    val count = remember { mutableStateOf(0) }

    SideEffect {
        count.value++
        println("Recomposed ${count.value} times")
    }
}
```

---

## **Testing**

### 32. How to test Compose UI?

**Answer:**
Use `createComposeRule()` and Compose testing APIs.

```kotlin
class LoginScreenTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun testLogin() {
        composeTestRule.setContent {
            LoginScreen()
        }

        // Find and interact with nodes
        composeTestRule
            .onNodeWithText("Email")
            .performTextInput("test@example.com")

        composeTestRule
            .onNodeWithText("Password")
            .performTextInput("password123")

        composeTestRule
            .onNodeWithText("Login")
            .performClick()

        // Assert
        composeTestRule
            .onNodeWithText("Welcome!")
            .assertIsDisplayed()
    }
}
```

---

### 33. How to test ViewModel with Compose?

**Answer:**

```kotlin
@Test
fun testViewModelIntegration() {
    val viewModel = HomeViewModel()

    composeTestRule.setContent {
        HomeScreen(viewModel = viewModel)
    }

    // Trigger action
    composeTestRule
        .onNodeWithText("Load Data")
        .performClick()

    // Wait for async operation
    composeTestRule.waitUntil(timeoutMillis = 5000) {
        viewModel.uiState.value.isLoading == false
    }

    // Assert
    composeTestRule
        .onNodeWithText("Data loaded")
        .assertExists()
}
```

---

### 34. What are Semantics in Compose testing?

**Answer:**
Semantics provide metadata about UI elements for testing and accessibility.

```kotlin
@Composable
fun TestableButton() {
    Button(
        onClick = { },
        modifier = Modifier.semantics {
            contentDescription = "Submit button"
            testTag = "submit_btn"
        }
    ) {
        Text("Submit")
    }
}

// In test
composeTestRule
    .onNodeWithTag("submit_btn")
    .performClick()
```

---

## **Interoperability**

### 35. How to use Android Views in Compose?

**Answer:**
Use `AndroidView` composable.

```kotlin
@Composable
fun WebViewComposable(url: String) {
    AndroidView(
        factory = { context ->
            WebView(context).apply {
                settings.javaScriptEnabled = true
                loadUrl(url)
            }
        },
        update = { webView ->
            webView.loadUrl(url)
        }
    )
}
```

---

### 36. How to use Compose in existing View-based apps?

**Answer:**
Use `ComposeView` in XML layouts.

```xml
<!-- layout.xml -->
<androidx.compose.ui.platform.ComposeView
    android:id="@+id/compose_view"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />
```

```kotlin
// In Activity/Fragment
binding.composeView.setContent {
    MyAppTheme {
        GreetingScreen()
    }
}
```

---

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

---

---

## **Memory Management & Lifecycle**

### 46. What happens to composables when they leave composition?

**Answer:**
When a composable leaves composition (removed from UI tree):
- All `remember` values are forgotten
- `LaunchedEffect` coroutines are cancelled
- `DisposableEffect` calls `onDispose`
- State is lost unless stored in ViewModel or rememberSaveable

```kotlin
@Composable
fun ConditionalContent(show: Boolean) {
    if (show) {
        // When show becomes false, all state here is lost
        var count by remember { mutableStateOf(0) }

        DisposableEffect(Unit) {
            println("Entered composition")
            onDispose {
                println("Left composition - cleanup")
            }
        }
    }
}
```

---

### 47. How does Compose handle memory leaks?

**Answer:**
Compose prevents memory leaks through:

1. **Automatic cancellation** - Coroutines auto-cancel when composable leaves
2. **Weak references** - Internal use of weak references
3. **DisposableEffect** - For manual cleanup

```kotlin
@Composable
fun LeakSafeComposable() {
    val context = LocalContext.current

    // ❌ Potential leak - listener never removed
    LaunchedEffect(Unit) {
        val listener = object : SomeListener {
            override fun onEvent() {
                // Holds reference to context
            }
        }
        someManager.addListener(listener)
    }

    // ✅ Leak-safe with cleanup
    DisposableEffect(Unit) {
        val listener = object : SomeListener {
            override fun onEvent() { }
        }
        someManager.addListener(listener)

        onDispose {
            someManager.removeListener(listener)
        }
    }
}
```

---

### 48. What is the lifecycle of a composable?

**Answer:**
Composables have three lifecycle phases:

1. **Enter** - Initial composition
2. **Recompose** - State changes trigger re-execution
3. **Leave** - Removed from composition

```kotlin
@Composable
fun LifecycleAware() {
    // Enter: Runs on first composition
    val state = remember { mutableStateOf(0) }

    // Enter: Runs once
    LaunchedEffect(Unit) {
        println("Entered composition")
    }

    // Recompose: Runs on every recomposition
    SideEffect {
        println("Recomposed")
    }

    // Leave: Runs when leaving
    DisposableEffect(Unit) {
        onDispose {
            println("Leaving composition")
        }
    }
}
```

---

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

---

## **Advanced UI & Layouts**

### 53. What is `SubcomposeLayout` and when to use it?

**Answer:**
`SubcomposeLayout` allows measuring one composable before laying out another, enabling dynamic layouts.

```kotlin
@Composable
fun AdaptiveLayout(
    header: @Composable () -> Unit,
    content: @Composable (headerHeight: Dp) -> Unit
) {
    SubcomposeLayout { constraints ->
        // Measure header first
        val headerPlaceables = subcompose("header", header)
            .map { it.measure(constraints) }

        val headerHeight = headerPlaceables.maxOfOrNull { it.height } ?: 0

        // Use header height for content
        val contentPlaceables = subcompose("content") {
            content(headerHeight.toDp())
        }.map { it.measure(constraints) }

        layout(constraints.maxWidth, constraints.maxHeight) {
            var y = 0
            headerPlaceables.forEach {
                it.placeRelative(0, y)
                y += it.height
            }
            contentPlaceables.forEach {
                it.placeRelative(0, y)
            }
        }
    }
}
```

**Use cases:**
- Dependent layouts
- Adaptive UIs
- Complex measurement requirements

---

### 54. How to implement a custom Modifier?

**Answer:**
Create custom modifiers using `Modifier.then()` or composed modifiers.

```kotlin
// Simple modifier
fun Modifier.dashedBorder(
    color: Color,
    strokeWidth: Dp = 1.dp,
    dashLength: Dp = 4.dp,
    gapLength: Dp = 4.dp
) = this.then(
    DrawModifier(color, strokeWidth, dashLength, gapLength)
)

private data class DrawModifier(
    val color: Color,
    val strokeWidth: Dp,
    val dashLength: Dp,
    val gapLength: Dp
) : DrawModifier {
    override fun ContentDrawScope.draw() {
        drawContent()

        val stroke = Stroke(
            width = strokeWidth.toPx(),
            pathEffect = PathEffect.dashPathEffect(
                floatArrayOf(dashLength.toPx(), gapLength.toPx())
            )
        )

        drawRect(
            color = color,
            style = stroke
        )
    }
}

// Composed modifier (with state)
fun Modifier.shimmer(): Modifier = composed {
    var targetValue by remember { mutableStateOf(0f) }

    val shimmerAnimation by animateFloatAsState(
        targetValue = targetValue,
        animationSpec = infiniteRepeatable(
            animation = tween(1000),
            repeatMode = RepeatMode.Reverse
        )
    )

    LaunchedEffect(Unit) {
        targetValue = 1f
    }

    this.drawWithContent {
        drawContent()
        drawRect(
            brush = Brush.linearGradient(
                colors = listOf(
                    Color.Gray.copy(alpha = 0.3f),
                    Color.White.copy(alpha = 0.5f),
                    Color.Gray.copy(alpha = 0.3f)
                ),
                start = Offset(size.width * shimmerAnimation, 0f),
                end = Offset(size.width * (shimmerAnimation + 0.3f), size.height)
            )
        )
    }
}

// Usage
Box(modifier = Modifier.size(200.dp).shimmer())
```

---

### 55. How to implement Swipe-to-Dismiss?

**Answer:**

```kotlin
@OptIn(ExperimentalMaterialApi::class)
@Composable
fun SwipeToDeleteItem(
    item: Item,
    onDelete: (Item) -> Unit
) {
    val dismissState = rememberDismissState(
        confirmStateChange = { dismissValue ->
            if (dismissValue == DismissValue.DismissedToStart) {
                onDelete(item)
                true
            } else {
                false
            }
        }
    )

    SwipeToDismiss(
        state = dismissState,
        directions = setOf(DismissDirection.EndToStart),
        background = {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(Color.Red),
                contentAlignment = Alignment.CenterEnd
            ) {
                Icon(
                    Icons.Default.Delete,
                    contentDescription = "Delete",
                    tint = Color.White,
                    modifier = Modifier.padding(16.dp)
                )
            }
        },
        dismissContent = {
            ItemCard(item)
        }
    )
}
```

---

### 56. How to implement Drag and Drop in Compose?

**Answer:**

```kotlin
@Composable
fun DragAndDropList() {
    var items by remember { mutableStateOf(listOf("A", "B", "C", "D")) }
    var draggedItem by remember { mutableStateOf<String?>(null) }

    LazyColumn {
        itemsIndexed(items, key = { _, item -> item }) { index, item ->
            DraggableItem(
                item = item,
                isDragging = draggedItem == item,
                onDragStart = { draggedItem = item },
                onDragEnd = { draggedItem = null },
                onDrop = { droppedOn ->
                    val fromIndex = items.indexOf(item)
                    val toIndex = items.indexOf(droppedOn)
                    items = items.toMutableList().apply {
                        add(toIndex, removeAt(fromIndex))
                    }
                }
            )
        }
    }
}

@Composable
fun DraggableItem(
    item: String,
    isDragging: Boolean,
    onDragStart: () -> Unit,
    onDragEnd: () -> Unit,
    onDrop: (String) -> Unit
) {
    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }

    Box(
        modifier = Modifier
            .offset { IntOffset(offsetX.roundToInt(), offsetY.roundToInt()) }
            .alpha(if (isDragging) 0.5f else 1f)
            .pointerInput(Unit) {
                detectDragGestures(
                    onDragStart = { onDragStart() },
                    onDragEnd = {
                        offsetX = 0f
                        offsetY = 0f
                        onDragEnd()
                    },
                    onDrag = { change, dragAmount ->
                        change.consume()
                        offsetX += dragAmount.x
                        offsetY += dragAmount.y
                    }
                )
            }
    ) {
        Text(item, modifier = Modifier.padding(16.dp))
    }
}
```

---

## **Advanced Navigation**

### 57. How to implement nested navigation?

**Answer:**

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController, startDestination = "main") {
        composable("main") {
            MainScreen(
                onNavigateToProfile = { navController.navigate("profile") }
            )
        }

        // Nested navigation graph
        navigation(startDestination = "profile/details", route = "profile") {
            composable("profile/details") {
                ProfileDetailsScreen(
                    onNavigateToSettings = {
                        navController.navigate("profile/settings")
                    }
                )
            }
            composable("profile/settings") {
                SettingsScreen()
            }
        }
    }
}
```

---

### 58. How to handle deep links in Compose Navigation?

**Answer:**

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController, startDestination = "home") {
        composable(
            route = "product/{productId}",
            arguments = listOf(
                navArgument("productId") { type = NavType.IntType }
            ),
            deepLinks = listOf(
                navDeepLink {
                    uriPattern = "myapp://product/{productId}"
                    action = Intent.ACTION_VIEW
                },
                navDeepLink {
                    uriPattern = "https://myapp.com/product/{productId}"
                }
            )
        ) { backStackEntry ->
            val productId = backStackEntry.arguments?.getInt("productId")
            ProductScreen(productId)
        }
    }
}

// In AndroidManifest.xml
/*
<activity>
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="myapp" android:host="product" />
        <data android:scheme="https" android:host="myapp.com" />
    </intent-filter>
</activity>
*/
```

---

### 59. How to implement bottom navigation with multiple back stacks?

**Answer:**

```kotlin
@Composable
fun MainScreen() {
    val navController = rememberNavController()
    var selectedTab by rememberSaveable { mutableStateOf(0) }

    Scaffold(
        bottomBar = {
            NavigationBar {
                BottomNavItem.values().forEachIndexed { index, item ->
                    NavigationBarItem(
                        selected = selectedTab == index,
                        onClick = {
                            selectedTab = index
                            navController.navigate(item.route) {
                                // Pop to start destination
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                // Avoid multiple copies
                                launchSingleTop = true
                                // Restore state
                                restoreState = true
                            }
                        },
                        icon = { Icon(item.icon, item.label) },
                        label = { Text(item.label) }
                    )
                }
            }
        }
    ) { padding ->
        NavHost(
            navController,
            startDestination = BottomNavItem.Home.route,
            modifier = Modifier.padding(padding)
        ) {
            composable(BottomNavItem.Home.route) { HomeScreen() }
            composable(BottomNavItem.Search.route) { SearchScreen() }
            composable(BottomNavItem.Profile.route) { ProfileScreen() }
        }
    }
}

enum class BottomNavItem(val route: String, val icon: ImageVector, val label: String) {
    Home("home", Icons.Default.Home, "Home"),
    Search("search", Icons.Default.Search, "Search"),
    Profile("profile", Icons.Default.Person, "Profile")
}
```

---

## **Performance Deep Dive**

### 60. What causes unnecessary recomposition and how to find it?

**Answer:**

**Common Causes:**
1. Unstable parameters
2. Creating new objects in composition
3. Lambda recreation
4. Reading state unnecessarily

**Detection Tools:**

```kotlin
// 1. Use Layout Inspector
// Android Studio → Tools → Layout Inspector → Enable "Show Recomposition Counts"

// 2. Manual logging
@Composable
fun TrackedComposable() {
    val recompositionCount = remember { mutableStateOf(0) }

    SideEffect {
        recompositionCount.value++
        Log.d("Recomposition", "Count: ${recompositionCount.value}")
    }
}

// 3. Composition tracing
@Composable
fun MyScreen() {
    CompositionLocalProvider(
        LocalInspectionMode provides true
    ) {
        // Your content
    }
}
```

**Fixing unstable parameters:**
```kotlin
// ❌ Unstable - List is not stable
@Composable
fun ItemList(items: List<Item>) { }

// ✅ Stable - Use ImmutableList or mark as Stable
@Composable
fun ItemList(items: ImmutableList<Item>) { }

// Or use kotlinx.collections.immutable
implementation("org.jetbrains.kotlinx:kotlinx-collections-immutable:0.3.5")

@Composable
fun ItemList(items: ImmutableList<Item>) { }
```

---

### 61. How to optimize LazyColumn performance?

**Answer:**

```kotlin
@Composable
fun OptimizedList(items: List<Item>) {
    LazyColumn(
        // 1. Use keys for stable item identity
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(
            items = items,
            key = { item -> item.id }, // Essential!
            contentType = { item -> item.type } // Optional: for different item types
        ) { item ->
            // 2. Keep items small and focused
            ItemCard(item)
        }
    }
}

@Composable
fun ItemCard(item: Item) {
    // 3. Use remember for expensive calculations
    val formattedDate = remember(item.timestamp) {
        formatDate(item.timestamp)
    }

    // 4. Avoid creating lambdas
    val onClick = remember { { handleClick(item.id) } }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
    ) {
        // 5. Use Text instead of TextView
        Text(item.title)
        Text(formattedDate)
    }
}

// 6. For images, use Coil with proper caching
@Composable
fun ImageItem(url: String) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(url)
            .memoryCacheKey(url)
            .diskCacheKey(url)
            .crossfade(true)
            .build(),
        contentDescription = null,
        modifier = Modifier.size(100.dp)
    )
}
```

---

### 62. What is Composition Local resolution and its performance impact?

**Answer:**

CompositionLocal allows passing data through composition tree without explicit parameters.

**Performance Considerations:**

```kotlin
// ❌ Creates recomposition on every change
val LocalConfig = compositionLocalOf { Config() }

// ✅ Better - static
val LocalConfig = staticCompositionLocalOf { Config() }

@Composable
fun Parent() {
    // Changes to config recompose all consumers
    val config = remember { mutableStateOf(Config()) }

    CompositionLocalProvider(LocalConfig provides config.value) {
        Child() // Recomposes when config changes
    }
}

// Performance tip: Split into multiple CompositionLocals
val LocalTheme = staticCompositionLocalOf { Theme.Light }
val LocalUser = compositionLocalOf<User?> { null }

// Only components using LocalUser recompose when user changes
```

**When to use staticCompositionLocalOf:**
- Value rarely/never changes (theme, resources)
- Avoid tracking recomposition

**When to use compositionLocalOf:**
- Value changes and consumers should recompose

---

### 63. How does Compose Compiler optimize code?

**Answer:**

The Compose Compiler performs several optimizations:

**1. Skippable Functions**
```kotlin
// Skippable if parameters are stable
@Composable
fun UserCard(user: User) { // Skipped if user hasn't changed
    Text(user.name)
}

// Non-skippable due to unstable parameter
@Composable
fun UserList(users: List<User>) { // Always recomposes
    // ...
}
```

**2. Restartable Functions**
```kotlin
// Compiler adds restart groups
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    Button(onClick = { count++ }) {
        Text("$count") // Only this recomposes
    }
}
```

**3. Comparison Propagation**
```kotlin
@Composable
fun Display(value: Int) { // Compiler inserts equality check
    if (currentValue != value) {
        // Recompose
    }
}
```

**View optimization reports:**
```gradle
// build.gradle.kts
android {
    kotlinOptions {
        freeCompilerArgs += listOf(
            "-P",
            "plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=" +
                    project.buildDir.absolutePath + "/compose_metrics"
        )
        freeCompilerArgs += listOf(
            "-P",
            "plugin:androidx.compose.compiler.plugins.kotlin:metricsDestination=" +
                    project.buildDir.absolutePath + "/compose_metrics"
        )
    }
}
```

---

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

---

## **Real-World Scenarios**

### 67. How to implement infinite scrolling/pagination?

**Answer:**

```kotlin
@Composable
fun PaginatedList(viewModel: PaginatedViewModel = viewModel()) {
    val items by viewModel.items.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val listState = rememberLazyListState()

    // Detect scroll to end
    LaunchedEffect(listState) {
        snapshotFlow { listState.layoutInfo.visibleItemsInfo.lastOrNull() }
            .collect { lastVisible ->
                lastVisible?.let {
                    val totalItems = listState.layoutInfo.totalItemsCount
                    if (it.index >= totalItems - 3 && !isLoading) {
                        viewModel.loadMore()
                    }
                }
            }
    }

    LazyColumn(state = listState) {
        items(items, key = { it.id }) { item ->
            ItemCard(item)
        }

        if (isLoading) {
            item {
                Box(
                    modifier = Modifier.fillMaxWidth(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
        }
    }
}

// ViewModel
class PaginatedViewModel : ViewModel() {
    private val _items = MutableStateFlow<List<Item>>(emptyList())
    val items = _items.asStateFlow()

    private val _isLoading = MutableStateFlow(false)
    val isLoading = _isLoading.asStateFlow()

    private var currentPage = 0

    init {
        loadMore()
    }

    fun loadMore() {
        if (_isLoading.value) return

        viewModelScope.launch {
            _isLoading.value = true
            try {
                val newItems = repository.getItems(page = currentPage, pageSize = 20)
                _items.value = _items.value + newItems
                currentPage++
            } finally {
                _isLoading.value = false
            }
        }
    }
}
```

---

### 68. How to implement search with debounce?

**Answer:**

```kotlin
@Composable
fun SearchScreen(viewModel: SearchViewModel = viewModel()) {
    var query by remember { mutableStateOf("") }
    val searchResults by viewModel.searchResults.collectAsState()
    val isSearching by viewModel.isSearching.collectAsState()

    // Debounced search
    LaunchedEffect(query) {
        snapshotFlow { query }
            .debounce(300)
            .filter { it.length >= 3 }
            .collectLatest { searchQuery ->
                viewModel.search(searchQuery)
            }
    }

    Column {
        SearchBar(
            query = query,
            onQueryChange = { query = it },
            onClear = { query = "" }
        )

        when {
            isSearching -> LoadingIndicator()
            query.length < 3 -> Text("Type at least 3 characters")
            searchResults.isEmpty() -> Text("No results")
            else -> SearchResults(searchResults)
        }
    }
}

// Alternative: Using produceState
@Composable
fun SearchWithProduceState(query: String): State<List<Result>> {
    return produceState<List<Result>>(
        initialValue = emptyList(),
        key1 = query
    ) {
        if (query.length >= 3) {
            delay(300) // Debounce
            value = repository.search(query)
        }
    }
}
```

---

### 69. How to implement multi-selection in lists?

**Answer:**

```kotlin
@Composable
fun MultiSelectList() {
    var items by remember { mutableStateOf(generateItems()) }
    var selectedIds by remember { mutableStateOf(setOf<Int>()) }
    var isSelectionMode by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            if (isSelectionMode) {
                TopAppBar(
                    title = { Text("${selectedIds.size} selected") },
                    navigationIcon = {
                        IconButton(onClick = {
                            isSelectionMode = false
                            selectedIds = emptySet()
                        }) {
                            Icon(Icons.Default.Close, "Close")
                        }
                    },
                    actions = {
                        IconButton(onClick = {
                            // Delete selected
                            items = items.filter { it.id !in selectedIds }
                            isSelectionMode = false
                            selectedIds = emptySet()
                        }) {
                            Icon(Icons.Default.Delete, "Delete")
                        }
                    }
                )
            }
        }
    ) { padding ->
        LazyColumn(modifier = Modifier.padding(padding)) {
            items(items, key = { it.id }) { item ->
                SelectableItem(
                    item = item,
                    isSelected = item.id in selectedIds,
                    isSelectionMode = isSelectionMode,
                    onShortClick = {
                        if (isSelectionMode) {
                            toggleSelection(item.id, selectedIds) { selectedIds = it }
                        } else {
                            // Normal click action
                        }
                    },
                    onLongClick = {
                        if (!isSelectionMode) {
                            isSelectionMode = true
                            selectedIds = setOf(item.id)
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun SelectableItem(
    item: Item,
    isSelected: Boolean,
    isSelectionMode: Boolean,
    onShortClick: () -> Unit,
    onLongClick: () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(if (isSelected) Color.LightGray else Color.White)
            .combinedClickable(
                onClick = onShortClick,
                onLongClick = onLongClick
            )
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (isSelectionMode) {
            Checkbox(
                checked = isSelected,
                onCheckedChange = { onShortClick() }
            )
        }
        Text(item.title, modifier = Modifier.padding(start = 8.dp))
    }
}

fun toggleSelection(
    id: Int,
    currentSelection: Set<Int>,
    onUpdate: (Set<Int>) -> Unit
) {
    onUpdate(
        if (id in currentSelection) {
            currentSelection - id
        } else {
            currentSelection + id
        }
    )
}
```

---

### 70. How to implement image picker in Compose?

**Answer:**

```kotlin
@Composable
fun ImagePickerScreen() {
    var imageUri by remember { mutableStateOf<Uri?>(null) }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        imageUri = uri
    }

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        imageUri?.let { uri ->
            AsyncImage(
                model = uri,
                contentDescription = null,
                modifier = Modifier.size(300.dp)
            )
        }

        Button(onClick = { launcher.launch("image/*") }) {
            Text("Pick Image")
        }
    }
}

// Multiple images
@Composable
fun MultipleImagePicker() {
    var imageUris by remember { mutableStateOf<List<Uri>>(emptyList()) }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetMultipleContents()
    ) { uris: List<Uri> ->
        imageUris = uris
    }

    Column {
        Button(onClick = { launcher.launch("image/*") }) {
            Text("Pick Images")
        }

        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
            contentPadding = PaddingValues(8.dp)
        ) {
            items(imageUris) { uri ->
                AsyncImage(
                    model = uri,
                    contentDescription = null,
                    modifier = Modifier
                        .size(100.dp)
                        .padding(4.dp)
                )
            }
        }
    }
}

// Camera capture
@Composable
fun CameraCapture() {
    val context = LocalContext.current
    var imageUri by remember { mutableStateOf<Uri?>(null) }
    var capturedImageUri by remember { mutableStateOf<Uri?>(null) }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicture()
    ) { success ->
        if (success) {
            capturedImageUri = imageUri
        }
    }

    Column {
        Button(onClick = {
            // Create temp file
            val photoFile = File.createTempFile(
                "IMG_",
                ".jpg",
                context.cacheDir
            )
            imageUri = FileProvider.getUriForFile(
                context,
                "${context.packageName}.provider",
                photoFile
            )
            launcher.launch(imageUri!!)
        }) {
            Text("Take Photo")
        }

        capturedImageUri?.let { uri ->
            AsyncImage(
                model = uri,
                contentDescription = null,
                modifier = Modifier.size(300.dp)
            )
        }
    }
}
```

---

## **Debugging & Troubleshooting**

### 71. Common Compose issues and solutions

**Answer:**

**Issue 1: Recomposition happening too often**
```kotlin
// Problem
@Composable
fun BadExample(items: List<String>) {
    // Creates new lambda on every recomposition
    items.forEach { item ->
        Button(onClick = { handleClick(item) }) {
            Text(item)
        }
    }
}

// Solution
@Composable
fun GoodExample(items: List<String>) {
    items.forEach { item ->
        val onClick = remember(item) { { handleClick(item) } }
        Button(onClick = onClick) {
            Text(item)
        }
    }
}
```

**Issue 2: State not updating**
```kotlin
// Problem - Mutating state directly
val list = remember { mutableStateListOf(1, 2, 3) }
list.add(4) // UI doesn't update if list reference doesn't change

// Solution - Create new instance or use mutableStateListOf
val list = remember { mutableStateListOf(1, 2, 3) }
list.add(4) // This works with mutableStateListOf

// Or
var list by remember { mutableStateOf(listOf(1, 2, 3)) }
list = list + 4 // Creates new list, triggers recomposition
```

**Issue 3: LaunchedEffect runs multiple times**
```kotlin
// Problem - Wrong key
LaunchedEffect(true) { // Runs on every recomposition
    loadData()
}

// Solution - Use proper key
LaunchedEffect(Unit) { // Runs once
    loadData()
}

LaunchedEffect(userId) { // Runs when userId changes
    loadData(userId)
}
```

**Issue 4: Remember not working after rotation**
```kotlin
// Problem
var state by remember { mutableStateOf("") } // Lost on rotation

// Solution
var state by rememberSaveable { mutableStateOf("") } // Survives rotation
```

**Issue 5: Composable not recomposing when expected**
```kotlin
// Problem - Reading state outside composition
@Composable
fun BadExample(viewModel: VM) {
    val value = viewModel.state.value // Read once, never updates
    Text(value)
}

// Solution - Collect as State
@Composable
fun GoodExample(viewModel: VM) {
    val value by viewModel.state.collectAsState()
    Text(value)
}
```

---

### 72. How to debug Compose with Android Studio?

**Answer:**

**1. Layout Inspector**
```
Tools → Layout Inspector
- View composition tree
- See recomposition counts
- Inspect modifier chain
- View CompositionLocal values
```

**2. Enable Compose debugging**
```kotlin
// build.gradle.kts
android {
    buildFeatures {
        compose = true
    }

    kotlinOptions {
        // Enable compose metrics
        freeCompilerArgs += listOf(
            "-P",
            "plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=" +
                "${project.buildDir}/compose_reports"
        )
    }
}
```

**3. Logging recompositions**
```kotlin
class Ref(var value: Int)

@Composable
inline fun LogCompositions(tag: String) {
    val ref = remember { Ref(0) }
    SideEffect {
        ref.value++
        Log.d("Compose", "$tag: ${ref.value} compositions")
    }
}

@Composable
fun MyScreen() {
    LogCompositions("MyScreen")
    // Your content
}
```

**4. Compose Profiler (experimental)**
```
// Track composition performance
androidx.compose.runtime.Recomposer.current().apply {
    // Enable tracking
}
```

---

### 73. What are the limitations of Jetpack Compose?

**Answer:**

**Current Limitations:**

1. **Learning Curve**
   - Declarative paradigm shift
   - New mental model
   - Different debugging approach

2. **Performance Considerations**
   - Initial composition overhead
   - Recomposition cost for complex UIs
   - Memory usage higher than Views initially

3. **Tooling**
   - Preview limitations (no animations, limited interactions)
   - Debugging harder than XML
   - Less mature IDE support compared to Views

4. **Library Support**
   - Some View libraries don't have Compose equivalents
   - AndroidView needed for legacy components

5. **Platform Features**
   - Some Android features easier in Views
   - WebView, Camera, Maps need AndroidView wrapper

6. **File Size**
   - Adds ~2MB to APK
   - Runtime + compiler dependencies

**Workarounds:**
```kotlin
// Use AndroidView for unsupported features
@Composable
fun CustomView() {
    AndroidView(
        factory = { context ->
            // Traditional View
            CustomAndroidView(context)
        }
    )
}

// Split modules to reduce APK size
// Only include Compose in modules that need it
```

---

## **Architecture & Best Practices**

### 74. What is the recommended architecture for Compose apps?

**Answer:**

**Recommended: MVVM with UDF (Unidirectional Data Flow)**

```kotlin
// 1. UI State
data class HomeUiState(
    val isLoading: Boolean = false,
    val items: List<Item> = emptyList(),
    val error: String? = null,
    val selectedFilter: Filter = Filter.ALL
)

// 2. UI Events
sealed class HomeUiEvent {
    data class FilterChanged(val filter: Filter) : HomeUiEvent()
    object Refresh : HomeUiEvent()
    data class ItemClicked(val itemId: Int) : HomeUiEvent()
}

// 3. ViewModel
class HomeViewModel(
    private val repository: ItemRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    fun onEvent(event: HomeUiEvent) {
        when (event) {
            is HomeUiEvent.FilterChanged -> updateFilter(event.filter)
            is HomeUiEvent.Refresh -> refresh()
            is HomeUiEvent.ItemClicked -> navigateToDetail(event.itemId)
        }
    }

    private fun updateFilter(filter: Filter) {
        _uiState.update { it.copy(selectedFilter = filter) }
        loadItems()
    }

    private fun loadItems() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val items = repository.getItems(_uiState.value.selectedFilter)
                _uiState.update { it.copy(items = items, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(error = e.message, isLoading = false)
                }
            }
        }
    }
}

// 4. Composable (Stateless)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel(),
    onNavigateToDetail: (Int) -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()

    HomeScreenContent(
        uiState = uiState,
        onEvent = viewModel::onEvent
    )
}

@Composable
private fun HomeScreenContent(
    uiState: HomeUiState,
    onEvent: (HomeUiEvent) -> Unit
) {
    Column {
        FilterChips(
            selectedFilter = uiState.selectedFilter,
            onFilterChange = { onEvent(HomeUiEvent.FilterChanged(it)) }
        )

        when {
            uiState.isLoading -> LoadingIndicator()
            uiState.error != null -> ErrorMessage(uiState.error)
            else -> ItemList(
                items = uiState.items,
                onItemClick = { onEvent(HomeUiEvent.ItemClicked(it)) }
            )
        }
    }
}
```

**Key Principles:**
1. **Single source of truth** - State in ViewModel
2. **Unidirectional data flow** - Events up, State down
3. **Separation of concerns** - UI logic vs Business logic
4. **Testability** - ViewModels easily testable

---

### 75. Best practices for production Compose apps?

**Answer:**

**1. State Management**
```kotlin
// ✅ DO: Hoist state to appropriate level
@Composable
fun Screen() {
    var sharedState by remember { mutableStateOf("") }
    ComponentA(sharedState) { sharedState = it }
    ComponentB(sharedState)
}

// ❌ DON'T: Keep state in multiple places
@Composable
fun BadScreen() {
    ComponentA() // Has its own state
    ComponentB() // Has duplicate state
}
```

**2. Composable Design**
```kotlin
// ✅ DO: Keep composables small and focused
@Composable
fun UserCard(user: User) {
    Card {
        UserAvatar(user.avatarUrl)
        UserInfo(user.name, user.email)
    }
}

// ❌ DON'T: Create god composables
@Composable
fun GiantScreen() {
    // 500 lines of code
}
```

**3. Performance**
```kotlin
// ✅ DO: Use keys in lists
LazyColumn {
    items(items, key = { it.id }) { item ->
        ItemCard(item)
    }
}

// ❌ DON'T: Skip keys
LazyColumn {
    items(items) { item -> // No key
        ItemCard(item)
    }
}
```

**4. Side Effects**
```kotlin
// ✅ DO: Use appropriate effect APIs
@Composable
fun Screen(userId: String) {
    LaunchedEffect(userId) {
        loadUser(userId)
    }
}

// ❌ DON'T: Perform side effects in composition
@Composable
fun BadScreen(userId: String) {
    loadUser(userId) // Runs on every recomposition!
}
```

**5. Testing**
```kotlin
// ✅ DO: Write tests
@Test
fun testUserScreen() {
    composeTestRule.setContent {
        UserScreen(user = testUser)
    }

    composeTestRule
        .onNodeWithText(testUser.name)
        .assertExists()
}
```

**6. Previews**
```kotlin
// ✅ DO: Create multiple previews
@Preview(name = "Light Mode")
@Preview(name = "Dark Mode", uiMode = Configuration.UI_MODE_NIGHT_YES)
@Preview(name = "Large Font", fontScale = 2f)
@Composable
fun UserCardPreview() {
    MyTheme {
        UserCard(sampleUser)
    }
}
```

**7. Modularization**
```kotlin
// Separate into modules
:feature:home
:feature:profile
:core:ui (shared components)
:core:design-system (theme, colors, typography)
```

**8. Accessibility**
```kotlin
// ✅ DO: Add semantics
Text(
    "Close",
    modifier = Modifier.semantics {
        contentDescription = "Close dialog"
        role = Role.Button
    }
)
```

**9. Error Handling**
```kotlin
// ✅ DO: Handle all states
when (uiState) {
    is Loading -> LoadingState()
    is Success -> SuccessState(uiState.data)
    is Error -> ErrorState(uiState.error)
    is Empty -> EmptyState()
}
```

**10. Documentation**
```kotlin
/**
 * Displays a user profile card with avatar and information.
 *
 * @param user The user data to display
 * @param onEditClick Callback when edit button is clicked
 * @param modifier Modifier to be applied to the card
 */
@Composable
fun UserProfileCard(
    user: User,
    onEditClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    // Implementation
}
```

---

## Summary

**Key Concepts to Master:**
- **State Management** - remember, rememberSaveable, StateFlow, derivedStateOf, produceState
- **Recomposition** - How and when it happens, optimization techniques
- **Side Effects** - LaunchedEffect, DisposableEffect, rememberCoroutineScope, SideEffect
- **Layouts** - Row, Column, Box, Lazy composables, custom layouts
- **Modifiers** - Order matters, chainable, immutable, custom modifiers
- **Navigation** - NavHost, NavController, arguments, deep links, nested navigation
- **Performance** - Optimization techniques, @Stable/@Immutable, profiling
- **Testing** - ComposeTestRule, semantics, integration tests
- **Interop** - AndroidView, ComposeView
- **Memory** - Lifecycle, cleanup, preventing leaks
- **Advanced** - SubcomposeLayout, custom modifiers, complex animations
- **Real-world** - Pagination, search, multi-select, image picker
- **Architecture** - MVVM with UDF, clean architecture
- **Best Practices** - Code organization, accessibility, documentation

**Interview Tips:**
1. Always explain with code examples
2. Mention real-world use cases
3. Discuss trade-offs and alternatives
4. Know performance implications
5. Understand the "why" not just the "how"
6. Be ready to debug issues live
7. Demonstrate testing knowledge

**Resources:**
- Official Compose Documentation
- Compose Performance Guidelines
- Android Developers Blog
- Compose Compiler Metrics
- Layout Inspector
- Compose Pathways (training)
