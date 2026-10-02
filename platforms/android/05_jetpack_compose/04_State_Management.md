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
