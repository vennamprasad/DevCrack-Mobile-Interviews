## **Theming & Material Design**

### 24. How to implement theming in Compose?

**Answer:**
Use `MaterialTheme` to define colors, typography, and shapes.

```kotlin
private val LightColorScheme = lightColorScheme(
    primary = Purple500,
    secondary = Teal200,
    background = Color.White
)

private val DarkColorScheme = darkColorScheme(
    primary = Purple200,
    secondary = Teal200,
    background = Color.Black
)

@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

---

### 25. What is `CompositionLocal` and when to use it?

**Answer:**
`CompositionLocal` provides implicit dependency injection through the composition tree.

```kotlin
val LocalUser = compositionLocalOf<User?> { null }

@Composable
fun App() {
    CompositionLocalProvider(LocalUser provides currentUser) {
        MainScreen() // Can access LocalUser
    }
}

@Composable
fun ProfileButton() {
    val user = LocalUser.current // Access provided value
    Text("Hi, ${user?.name}")
}
```

**Common built-in CompositionLocals:**
- `LocalContext` - Android Context
- `LocalConfiguration` - Device configuration
- `LocalDensity` - Screen density
