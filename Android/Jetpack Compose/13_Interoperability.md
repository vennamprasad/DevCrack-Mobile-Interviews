## **Interoperability**

### 35. How to use Android Views in Compose?

**Answer:**
Use `AndroidView` composable.

```kotlin
@Composable
fun WebViewComposable(url: String) {
    AndroidView(
        factory = { context ->
            WebView(context).apply {
                settings.javaScriptEnabled = true
                loadUrl(url)
            }
        },
        update = { webView ->
            webView.loadUrl(url)
        }
    )
}
```

---

### 36. How to use Compose in existing View-based apps?

**Answer:**
Use `ComposeView` in XML layouts.

```xml
<!-- layout.xml -->
<androidx.compose.ui.platform.ComposeView
    android:id="@+id/compose_view"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />
```

```kotlin
// In Activity/Fragment
binding.composeView.setContent {
    MyAppTheme {
        GreetingScreen()
    }
}
```
