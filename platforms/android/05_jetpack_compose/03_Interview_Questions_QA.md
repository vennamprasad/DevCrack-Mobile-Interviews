## 🧩 Interview Questions (Q&A)

### 1. What is Jetpack Compose?

**Answer:**
Jetpack Compose is Android's modern declarative UI toolkit that simplifies and accelerates UI development. Instead of imperative XML layouts (finding views, setting properties), you describe your UI using Kotlin functions that transform data into UI hierarchy.

**Key Benefits:**
- **Less Code:** No XML, no boilerplates (Adapters, ViewHolders).
- **Intuitive:** Single language (Kotlin) for Logic and UI.
- **Accelerated Development:** Live Preview and Interactive Mode in Android Studio.
- **Powerful:** Built-in support for Material Design, Dark Theme, and Animations.

---

### 2. What is a @Composable function?

**Answer:**
A function annotated with `@Composable` that describes a piece of UI. It tells the Compose compiler that this function is intended to convert data into a UI tree.

*   **Idempotent:** Should produce the same result for the same inputs.
*   **Side-effect free:** Should not modify global state or perform I/O directly (use Side Effect APIs instead).
*   **Restartable:** Can be re-executed by the runtime when state changes.

```kotlin
@Composable
fun Greeting(name: String) {
    Text(
        text = "Hello, $name!",
        style = MaterialTheme.typography.body1
    )
}
```

---

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
