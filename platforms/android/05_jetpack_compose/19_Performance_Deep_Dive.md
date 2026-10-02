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
