## **Animations**

### 26. How to animate values in Compose?

**Answer:**
Use `animate*AsState` for simple animations.

```kotlin
@Composable
fun AnimatedBox() {
    var expanded by remember { mutableStateOf(false) }

    val size by animateDpAsState(
        targetValue = if (expanded) 200.dp else 100.dp,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioMediumBouncy,
            stiffness = Spring.StiffnessLow
        )
    )

    Box(
        modifier = Modifier
            .size(size)
            .background(Color.Blue)
            .clickable { expanded = !expanded }
    )
}
```

**Available animate functions:**
- `animateDpAsState`
- `animateColorAsState`
- `animateFloatAsState`
- `animateIntAsState`

---

### 27. What is `AnimatedVisibility` and how to use it?

**Answer:**
`AnimatedVisibility` animates the appearance and disappearance of content.

```kotlin
@Composable
fun AnimatedContent() {
    var visible by remember { mutableStateOf(false) }

    Column {
        Button(onClick = { visible = !visible }) {
            Text("Toggle")
        }

        AnimatedVisibility(
            visible = visible,
            enter = fadeIn() + slideInVertically(),
            exit = fadeOut() + slideOutVertically()
        ) {
            Text("I'm animated!")
        }
    }
}
```

---

### 28. How to create complex animations with `updateTransition`?

**Answer:**
`updateTransition` coordinates multiple animated values.

```kotlin
@Composable
fun MultiPropertyAnimation() {
    var selected by remember { mutableStateOf(false) }
    val transition = updateTransition(selected, label = "selected")

    val size by transition.animateDp(label = "size") { isSelected ->
        if (isSelected) 150.dp else 100.dp
    }

    val color by transition.animateColor(label = "color") { isSelected ->
        if (isSelected) Color.Blue else Color.Gray
    }

    Box(
        modifier = Modifier
            .size(size)
            .background(color)
            .clickable { selected = !selected }
    )
}
```
