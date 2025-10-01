# Jetpack Compose — Interview Questions (Basic & Advanced)

Below are concise interview questions and answers covering basic to advanced Jetpack Compose concepts, with short code examples where helpful. At least 30 items are included.

1. What is Jetpack Compose?
**Answer:** 
A modern declarative UI toolkit for Android that uses composable functions to describe UI. It replaces imperative View-based UI with a reactive model.

2. What is a @Composable function?
**Answer:** 
A function annotated with @Composable that can emit UI. It can call other composables and is managed by the Compose runtime.
Example:
```kotlin
@Composable
fun Greeting(name: String) {
    Text("Hello, $name!")
}
```

3. What is “state” in Compose?
**Answer:** 
State is data that, when changed, triggers recomposition of affected composables. Common types: mutableStateOf, MutableStateFlow used with collectAsState().

4. What is remember and rememberSaveable?
**Answer:** 
remember retains a value across recompositions. rememberSaveable retains across recompositions and process death (using Parcelable or saved instance mechanisms).
```kotlin
val count = remember { mutableStateOf(0) }
val text = rememberSaveable { mutableStateOf("") }
```

5. What is recomposition?
- The process where Compose re-executes composable functions to update UI when observed state changes. Compose tries to minimize work by skipping unaffected parts.

6. What are side-effect APIs? (LaunchedEffect, SideEffect, DisposableEffect)
- APIs for interacting with side effects:
    - LaunchedEffect: runs suspend work scoped to composition.
    - DisposableEffect: acquire/cleanup resources on enter/leave.
    - SideEffect: run after successful composition for non-suspending work.

Example:
```kotlin
LaunchedEffect(key1 = userId) {
    viewModel.load(userId)
}
```

7. What is state hoisting?
- Pattern of moving state up to a common owner (typically a parent) and passing it down via parameters and change callbacks, enabling single-source-of-truth.

8. How do you create a stateless composable?
- Accept state via parameters and emit events via callbacks rather than holding internal state.

9. What is MutableState and snapshot system?
- mutableStateOf creates an observable state. Compose uses a snapshot system for consistent reads/writes across threads and to drive recomposition.

10. How does Compose interoperate with existing Views?
- Use AndroidView to host a traditional View inside Compose, or ComposeView to embed Compose in an XML layout.
```kotlin
AndroidView(factory = { context ->
    TextView(context).apply { text = "From View" }
})
```

11. What are Modifiers?
- A fluent API to decorate or augment composables (layout, draw, input). They are immutable and can be chained.

12. Explain layout primitives Row, Column, and Box.
- Row: places children horizontally; Column: vertically; Box: overlays children. Use modifiers for sizing and alignment.

13. What are Lazy layouts?
- LazyColumn and LazyRow render only visible items, similar to RecyclerView. Use items{} for lists.
```kotlin
LazyColumn {
    items(itemsList) { item -> Text(item) }
}
```

14. How to handle lists with stable keys?
- Provide key parameter to items to maintain item identity and optimize animations.
```kotlin
items(itemsList, key = { it.id }) { item -> ... }
```

15. What is Compose Navigation?
- Jetpack Navigation Compose provides navigation APIs for composables, including NavHost and NavController.

16. How to integrate ViewModel with Compose?
- Use viewModel() or hiltViewModel() in composables and expose UI state as StateFlow/LiveData and collect with collectAsState() or observeAsState().
```kotlin
val vm: MyViewModel = viewModel()
val uiState by vm.state.collectAsState()
```

17. What is collectAsState()?
- Converts a Flow/StateFlow into Compose State<T> to observe in composables and trigger recomposition.

18. How do you animate values in Compose?
- Use animate*AsState for simple animations, updateTransition for complex multi-property animations, and AnimatedVisibility for enter/exit.
```kotlin
val size by animateDpAsState(if (expanded) 200.dp else 100.dp)
Box(modifier = Modifier.size(size)) { ... }
```

19. What is derivedStateOf?
- Creates a memoized dependent state derived from other states to avoid unnecessary recalculations and recompositions.
```kotlin
val derived = remember { derivedStateOf { items.filter { it.active } } }
```

20. What is snapshotFlow?
- Bridges Compose state reads into a Flow for use with coroutines (e.g., for debouncing).
```kotlin
val flow = snapshotFlow { query }
```

21. Explain CompositionLocal and theming.
- CompositionLocal provides implicit scoped data (like a dependency injection within composition). Used by MaterialTheme to supply colors/typography.
```kotlin
val LocalUser = compositionLocalOf<User?> { null }
```

22. How does Compose handle accessibility and semantics?
- Use Modifier.semantics and Compose's semantic properties; testing and TalkBack integration rely on these.

23. What are tools for Compose debugging and previews?
- Android Studio provides @Preview, the Layout Inspector, and recomposition counts. Use @Preview to render composables in the IDE.

24. How to test Compose UI?
- Use createComposeRule(), setContent { ... }, semantics, and compose testing APIs (onNodeWithText, performClick, etc.).
```kotlin
@get:Rule val composeTestRule = createComposeRule()
composeTestRule.setContent { MyComposable() }
composeTestRule.onNodeWithText("Hello").assertExists()
```

25. What is the difference between LaunchedEffect and rememberCoroutineScope?
- LaunchedEffect launches a coroutine tied to a key and cancels when key changes or leaves composition. rememberCoroutineScope provides a coroutine scope tied to composition lifecycle for ad-hoc coroutines.

26. What is DisposableEffect used for?
- Acquire resources and provide a cleanup when the key or composition leaves (e.g., register/unregister listeners).
```kotlin
DisposableEffect(key1 = lifecycleOwner) {
    val cb = ...
    onDispose { /* cleanup */ }
}
```

27. How to optimize performance (recomposition)?
- Hoist state, use remember/derivedStateOf, make composables small and stable, use keys for lists, avoid passing new object instances on each recomposition, and use SnapshotStateList/Map for stable collections.

28. What are stability and @Stable / @Immutable annotations?
- Compose uses stability of types to determine recomposition behavior. Marking data classes @Immutable or functions/objects as @Stable helps the compiler optimize.

29. How to handle gestures (tap, drag, scroll)?
- Use Modifier.pointerInput with detectTapGestures, dragGestureFilter (legacy), or higher-level modifiers like draggable and scrollable. For complex pointer handling, implement awaitPointerEventScope.
```kotlin
Modifier.pointerInput(Unit) {
    detectTapGestures { offset -> /* handle tap */ }
}
```

30. How to implement navigation with arguments?
- Use NavHost routes with placeholders and navBackStackEntry arguments; pass and retrieve via navController.navigate("screen/$id") and backStackEntry.arguments.

31. What is Compose Multiplatform (Compose for Desktop/Web)?
- Jetpack Compose's declarative model has been adapted for desktop/web via Compose Multiplatform by JetBrains, enabling shared UI code on other targets.

32. Explain recomposition scope and skipping.
- Compose divides UI into scopes; when state changes, only scopes that read that state are recomposed. Skipping avoids re-executing composables whose parameters and observed state haven't changed.

33. How do you save UI state across process death?
- Use rememberSaveable for simple types or saveable state holders; for complex persistent state use ViewModel + SavedStateHandle.

34. How to handle side effects when leaving composition?
- Use DisposableEffect to run cleanup in onDispose block when composition leaves or key changes.

35. What is the Compose Compiler Plugin and its role?
- The compiler plugin transforms @Composable functions to runtime-managed code, enabling the composition model, recomposition, and optimizations. Keep plugin and Kotlin compiler versions compatible.

36. How to do Compose <-> View event bridging?
- Expose callbacks in Views and invoke them from AndroidView, or use ComposeView.setContent to host composables and wire listeners.

37. How to support theming and dark mode?
- Use MaterialTheme (Material 2 or Material 3), provide light/dark color schemes, and dynamically switch based on isSystemInDarkTheme() or user preference.

38. How to implement forms and input validation?
- Hold input values in state (rememberSaveable or ViewModel), validate on change or submit, use TextField and visual error indicators. Keep validation logic in ViewModel for testability.

39. How to profile Compose apps?
- Use Android Studio Profiler, Layout Inspector for recomposition counts, and System Trace. Look for excessive recompositions or memory leaks.

40. Common migration tips from View system to Compose?
- Start with small screens, embed Compose via ComposeView, hoist business logic to ViewModel, avoid one-to-one translation; embrace composable patterns and state hoisting.

Summary: Focus on state management, recomposition, side-effect APIs, modifiers/layouts, lists/keys, animations, navigation, interop, performance optimization, and testing. Small, well-scoped composables and single-source-of-truth state make Compose apps robust and performant.