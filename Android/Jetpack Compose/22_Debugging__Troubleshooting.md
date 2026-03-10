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
