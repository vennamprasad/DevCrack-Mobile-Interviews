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
