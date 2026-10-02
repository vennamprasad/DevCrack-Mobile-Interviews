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
