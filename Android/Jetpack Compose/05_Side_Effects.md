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
