# Restrict Screenshot & Screen Recording — Complete Guide

> [!NOTE]
> **Production-ready implementations**, edge cases, Compose support, and interview talking points for banking-grade Android apps.

| Badge | Type |
| :--- | :--- |
| `FLAG_SECURE` | Core API |
| `Jetpack Compose` | UI Toolkit |
| `PCI DSS` | Compliance |
| `OWASP M2` | Security Standard |
| `Banking-Grade` | Security Level |

---

## 01 — How it works

### 🔒 FLAG_SECURE — The Core API
*   A **WindowManager flag** that marks a window as containing sensitive content.
*   When set, the system renders a **black/blank frame** instead of real content in screenshots.
*   Also blocks content from appearing in the **Recent Apps** thumbnail.
*   Prevents screen recording tools (built-in or third-party) from capturing the window.
*   Applies at the **window level** — works for entire Activity or specific Compose screens.

### ⚠️ What It Does NOT Do
*   **Cannot prevent** a second camera pointing at the screen.
*   **Cannot detect** hardware HDMI capture cards.
*   Does not block screenshots on **rooted devices** (root can bypass FLAG_SECURE).
*   Does not block recording if the **kernel is compromised**.
*   Only covers **your app's windows**, not overlays from other apps.

> [!TIP]
> **Key mental model:** `FLAG_SECURE` tells the OS compositor to treat your surface as DRM-protected content — the same mechanism used by Netflix and banking apps globally.

---

## 02 — Implementation Methods

### Method 1 — Entire Activity (Simplest)
Apply in `onCreate()` before `setContentView()`. Secures all screens in this Activity.

**Best for:** Banking apps where the ENTIRE app should be protected — payment screens, account details, transaction history.

```kotlin
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // ✅ Must be called BEFORE setContentView()
        // This secures the entire window immediately
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )

        setContentView(R.layout.activity_main)
    }

    // To remove it later (e.g., for non-sensitive screens)
    fun disableScreenSecurity() {
        window.clearFlags(
            WindowManager.LayoutParams.FLAG_SECURE
        )
    }
}
```

### Method 2 — Toggling Based on Destination (Navigation-Aware)
**Kotlin · SecurityAwareActivity.kt**
```kotlin
// Define which screens require protection
val secureDestinations = setOf(
    R.id.paymentFragment,
    R.id.accountDetailsFragment,
    R.id.transactionHistoryFragment,
    R.id.cardDetailsFragment
)

// In Activity, listen to nav destination changes
navController.addOnDestinationChangedListener { _, destination, _ ->
    if (destination.id in secureDestinations) {
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
    } else {
        window.clearFlags(
            WindowManager.LayoutParams.FLAG_SECURE
        )
    }
}
```

### Method 3 — Jetpack Compose (Per-Screen)
Wrap any sensitive Compose screen with this. `FLAG_SECURE` is set when screen appears and automatically CLEARED when it leaves composition.

**Kotlin · SecureScreen.kt**
```kotlin
/**
 * Wrap any sensitive Compose screen with this.
 * FLAG_SECURE is set when screen appears and
 * automatically CLEARED when it leaves composition.
 */
@Composable
fun SecureScreen(content: @Composable () -> Unit) {
    val context = LocalContext.current

    DisposableEffect(Unit) {
        val activity = context.findActivity()
        activity?.window?.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )

        onDispose {
            // ✅ Auto-cleared when composable leaves the tree
            activity?.window?.clearFlags(
                WindowManager.LayoutParams.FLAG_SECURE
            )
        }
    }

    content()
}

// Extension — find Activity from Context
fun Context.findActivity(): Activity? {
    var ctx = this
    while (ctx is ContextWrapper) {
        if (ctx is Activity) return ctx
        ctx = ctx.baseContext
    }
    return null
}
```

**Usage Example:**
```kotlin
@Composable
fun PaymentScreen() {
    SecureScreen {
        // Your payment UI here — fully protected
        Column {
            Text("Card: **** **** **** 4242")
            Text("Balance: ₹1,24,500")
            PaymentButton()
        }
    }
}
```

### Method 4 — ViewModel-Driven Security State
Cleaner pattern — let ViewModel control security state, not the UI layer directly.

```kotlin
class ScreenSecurityViewModel : ViewModel() {

    private val _isSecure = MutableStateFlow(false)
    val isSecure: StateFlow<Boolean> = _isSecure.asStateFlow()

    fun enableSecurity()  { _isSecure.value = true  }
    fun disableSecurity() { _isSecure.value = false }
}

// In your Composable screen
@Composable
fun AccountScreen(viewModel: AccountViewModel = hiltViewModel()) {

    val isSecure by viewModel.isSecure.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) { viewModel.enableSecurity() }

    if (isSecure) {
        SecureScreen { AccountContent(viewModel) }
    } else {
        AccountContent(viewModel)
    }
}
```

---

## 03 — Screen Recording Detection (Android 14+)

> [!WARNING]
> **New in Android 14 (API 34):** The system now notifies apps when screen recording starts. This is the first official API for detection.

### WindowInfoTracker — Official Detection API

```kotlin
class ScreenRecordingDetector @Inject constructor(
    private val activity: Activity
) {
    private val _isBeingRecorded = MutableStateFlow(false)
    val isBeingRecorded = _isBeingRecorded.asStateFlow()

    @RequiresApi(Build.VERSION_CODES.UPSIDE_DOWN_CAKE) // API 34
    fun startMonitoring(scope: CoroutineScope) {
        scope.launch {
            WindowInfoTracker
                .getOrCreate(activity)
                .windowLayoutInfo(activity)
                .collect { layoutInfo ->
                    // Check if screen content is being captured
                    val isCapturing = activity
                        .windowManager
                        .currentWindowMetrics
                        .windowInsetsController != null

                    // Alternative: use ActivityLifecycleCallbacks
                    _isBeingRecorded.value = isScreenBeingCaptured()
                }
        }
    }

    @RequiresApi(Build.VERSION_CODES.UPSIDE_DOWN_CAKE)
    private fun isScreenBeingCaptured(): Boolean {
        return activity.isScreenCaptureEnabled
    }
}
```

**When Recording is Detected — Do This:**
*   ✅ Blur or hide sensitive data on screen
*   ✅ Show a security warning overlay
*   ✅ Pause video or financial data display
*   ✅ Log the event server-side for audit
*   ✅ For high-security: terminate the session

**What You Cannot Do:**
*   ❌ Cannot **stop** the recording — OS doesn't allow it
*   ❌ Cannot detect recording on **Android < 14** reliably
*   ❌ Cannot prevent recording on **rooted devices**
*   ❌ Cannot block **hardware capture cards**

---

## 04 — Protection Comparison

| Threat Vector | FLAG_SECURE | Recording Detection | Rooted Device | Notes |
| :--- | :--- | :--- | :--- | :--- |
| System Screenshot | ✅ Blocked | — | ❌ Bypass | Black image saved |
| 3rd-party Screenshot App | ✅ Blocked | — | ❌ Bypass | App sees blank window |
| Built-in Screen Recorder | ✅ Blocked | ✅ Detected | ❌ Bypass | Black frame recorded |
| 3rd-party Screen Recorder | ✅ Blocked | ~ API 34+ only | ❌ Bypass | MediaProjection blocked |
| Recent Apps Thumbnail | ✅ Blocked | — | ❌ Bypass | Black thumbnail shown |
| ADB Screenshot | ✅ Blocked | — | ❌ Bypass | Black image via adb screencap |
| HDMI Capture Card | ❌ Cannot block | ❌ Undetectable | N/A | Hardware level — no defense |
| Rooted Device + Custom App | ❌ Bypassable | ❌ Can be hidden | ❌ Bypass | Root detection is key defense |
| Second Camera | ❌ Cannot block | ❌ Undetectable | N/A | Physical threat — no defense |

---

## 05 — Edge Cases & Gotchas

### ⚡ Timing Issue
If you call `setFlags()` **after** `setContentView()` there can be a brief flash where content is visible. Always set the flag **before** `setContentView()`.

> **Rule:** FLAG_SECURE → setContentView → UI setup

### 🪟 Dialog Windows
Dialogs are separate windows. If you show a dialog with card info, you need to apply `FLAG_SECURE` to **the dialog's window** separately, not just the Activity.

```kotlin
val dialog = AlertDialog.Builder(context).create()
dialog.show()
// Apply AFTER show() — dialog window now exists
dialog.window?.setFlags(
    WindowManager.LayoutParams.FLAG_SECURE,
    WindowManager.LayoutParams.FLAG_SECURE
)
```

### 🧪 UI Testing & Screenshots in CI
`FLAG_SECURE` blocks Espresso screenshot capture and UI testing tools. You need to **disable it in debug builds** for testing.

```kotlin
if (!BuildConfig.DEBUG) {
    window.setFlags(
        WindowManager.LayoutParams.FLAG_SECURE,
        WindowManager.LayoutParams.FLAG_SECURE
    )
}
```

### 🔗 Compose Bottom Sheet / Dialog
Compose ModalBottomSheet and Dialog create their own window. Use a custom `SecureDialog` composable that applies the flag to the dialog's window context.

```kotlin
@Composable
fun SecureDialog(
    onDismiss: () -> Unit,
    content: @Composable () -> Unit
) {
    Dialog(onDismissRequest = onDismiss) {
        // This gives us the dialog's window
        val dialogWindow = getDialogWindow()
        SideEffect {
            dialogWindow?.setFlags(
                WindowManager.LayoutParams.FLAG_SECURE,
                WindowManager.LayoutParams.FLAG_SECURE
            )
        }
        content()
    }
}
```

---

## 06 — Recommended Decision Flow

1.  **Banking / Finance App?**
    *   → Apply `FLAG_SECURE` globally to ALL screens. No exceptions.
2.  **Selective Sensitive Screens?**
    *   → Payment, Account, Card Details, Transaction History → `SecureScreen` wrapper in Compose or `SecureFragment` in View system.
3.  **Custom Dialogs Showing Card Data?**
    *   → Apply `FLAG_SECURE` specifically to `dialog.window` after `dialog.show()`.
4.  **Target API 34+?**
    *   → Also add Screen Recording Detection via `WindowInfoTracker` and respond with blur/overlay.
5.  **Debug Build?**
    *   → Conditionally disable in `BuildConfig.DEBUG` for UI testing and screenshot generation in CI/CD.

---

## 07 — Interview Q & A

### Q: How do you prevent screenshots in an Android banking app?
**A:** "I use `WindowManager.LayoutParams.FLAG_SECURE`, set before `setContentView()` in onCreate. For a banking app I apply it globally. In Compose I wrap sensitive screens with a `SecureScreen` composable using `DisposableEffect` which auto-clears the flag when the composable leaves the tree. On Android 14+ I also use the `WindowInfoTracker` API to detect screen recording and blur sensitive fields when recording is detected. I handle edge cases like dialogs needing their own flag, and disable it in debug builds so Espresso tests continue working."

### Q: Can FLAG_SECURE be bypassed? How do you defend against that?
**A:** "Yes — rooted devices can bypass it by patching the system compositor or using root-level screen capture tools. My defense is **layered**: `FLAG_SECURE` is the first layer. Root detection (checking for su binary, known root apps like Magisk, SafetyNet Attestation) is the second. If root is detected, I restrict access to sensitive features or require additional verification. I also implement server-side transaction signing so even if the UI is compromised, transactions cannot be forged. The principle is defense-in-depth — no single control should be the only protection."

### Q: How do you apply screen security selectively in a Compose-only app?
**A:** "I create a `SecureScreen` composable using `DisposableEffect(Unit)`. In the effect I get the Activity via a `findActivity()` Context extension and call `window.setFlags(FLAG_SECURE)`. In the `onDispose` lambda I clear the flag. This means the flag is set exactly while the composable is in the composition tree and automatically removed when it leaves. It's reusable, testable, and lifecycle-safe. For dialogs and `ModalBottomSheet` I handle their separate window context with `SideEffect`."

### Q: Which compliance standards require screenshot prevention?
**A:** "OWASP Mobile Security Testing Guide (MSTG) under MASVS-STORAGE-9 recommends preventing sensitive data exposure in screenshots. PCI DSS requires protection of cardholder data — a screenshot of a card number or CVV on screen violates this. RBI (Reserve Bank of India) guidelines for mobile banking also recommend preventing screen capture for sensitive operations. In practice, most banking regulators globally expect this as baseline security hygiene, even if not explicitly named in the standard."