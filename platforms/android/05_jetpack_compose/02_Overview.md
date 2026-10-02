## ✅ Overview

**Jetpack Compose** is Android's modern toolkit for building native UI. It simplifies and accelerates UI development on Android with less code, powerful tools, and intuitive Kotlin APIs.

### **Why Compose?**
*   **Declarative:** You describe your UI state, and Compose takes care of updating it.
*   **Compatible:** It interoperates with your existing View-based app.
*   **Kotlin-First:** Built with the benefits of Kotlin (Coroutines, Type Safety).

### **Sample Component**

```kotlin
@Composable
fun WelcomeScreen() {
    var show by remember { mutableStateOf(true) }
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        if (show) {
            Text(text = "Hello Compose!", style = MaterialTheme.typography.h5)
        }
        Button(onClick = { show = !show }) {
            Text("Toggle")
        }
    }
}
```
