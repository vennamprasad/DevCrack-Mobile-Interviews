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
