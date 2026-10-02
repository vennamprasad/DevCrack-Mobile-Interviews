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
