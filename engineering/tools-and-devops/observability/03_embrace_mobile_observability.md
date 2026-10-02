# 🛡️ Embrace.io: Mobile-Native Observability & ANR Forensics

> **A deep dive into mobile-first telemetry: 100% session capture, solving mystery ANRs, user journey timeline reconstruction, and NDK native crash unwinding.**

---

## 📌 Executive Summary

While traditional APM tools (like Datadog, New Relic) were born on backend servers and adapted for mobile, **Embrace.io** was engineered from day one exclusively for iOS and Android. 

Rather than relying on sampling rates or only logging events when an uncaught exception occurs, Embrace records **100% of user sessions**. This provides complete contextual timelines (network calls, memory warnings, breadcrumbs, view lifecycles, and UI thread freezes) that explain *why* an issue occurred even if the OS abruptly killed the app (e.g., OOM or ANR).

---

## 🏗️ Core Architecture: 100% Session Capture vs. Sampling

```
Traditional APM (Sampling / Crash-Only):
[ User Session ] ──(Sample Rate 10%)──> [ Dropped ]
[ User Session ] ──(No Crash)─────────> [ Dropped ]
[ User Session ] ──(Crash!)───────────> [ Stack Trace Only (No Context) ]

Embrace.io (100% Deterministic Capture):
[ User Session ] ──(Local Ring Buffer)──> [ Session Timeline Stored ]
                                                 │
      ┌──────────────────────────────────────────┴─────────────────────────┐
      │ • View transitions (Compose / SwiftUI)                             │
      │ • Main thread blockages & unresponsiveness (>100ms)                │
      │ • Every HTTP request, latency, status code, and payload size        │
      │ • Memory warnings & thermal state throttle events                   │
      │ • Custom breadcrumbs & user interaction taps                       │
      └────────────────────────────────────────────────────────────────────┘
```

### Key Differences in Production

| Dimension | Datadog / New Relic | Firebase Crashlytics | Embrace.io |
| :--- | :--- | :--- | :--- |
| **Session Model** | Sampled RUM sessions (cost control) | Crash & Non-fatal reports only | **100% session capture** with offline disk buffering |
| **ANR Forensics** | Watchdog polling (captures stack) | Android ExitInfo / 5-second trace | **Continuous sampling of UI thread** (identifies what stalled the main thread prior to the ANR) |
| **Out-of-Memory (OOM)** | Inferred from sudden session termination | Inferred | **Deterministic OOM detection** via memory telemetry before OS SIGKILL |
| **Network Telemetry** | Interceptor spans | OkHttp / URLSession metrics | Automatic network body size, error rates, and connection stalls |

---

## 🔬 Solving the "Mystery ANR" (Application Not Responding)

In Android, an ANR is triggered when:
1. The app does not respond to an input event (e.g., key press or screen touch) within **5 seconds**.
2. A `BroadcastReceiver` does not finish executing within **10 seconds** (foreground) or **60 seconds** (background).

### Why Standard ANR Reports Fail
Google Play Console and standard crash reporters only take a **single snapshot** of the stack trace at the exact moment the ANR dialog pops up. 
Often, this snapshot shows an innocent method:
```text
"main" prio=5 tid=1 Native
  at android.os.MessageQueue.nativePollOnce(Native Method)
  at android.os.MessageQueue.next(MessageQueue.java:335)
  at android.os.Looper.loop(Looper.java:206)
```
This tells the engineer **nothing** about what locked the main thread for the previous 4.9 seconds!

### How Embrace Solves It: Thread Sampler
Embrace runs a background watchdog that samples the main thread periodically (e.g., every 100ms) whenever the main thread is unresponsive:
1. It records the call tree over time (e.g., Disk I/O on main thread during SharedPreferences read).
2. It detects **Binder IPC deadlocks** where the app was waiting for a system service (e.g., `LocationManager` or `AudioManager`).
3. It visualizes the ANR as an **interactive flame graph** showing the percentage of time spent in each blocking call leading up to the freeze.

---

## 💻 Implementation & Production Setup

### Android (Kotlin) Implementation

```kotlin
// build.gradle.kts
plugins {
    id("io.embrace.swazzler") version "6.0.0"
}

dependencies {
    implementation("io.embrace:embrace-android-sdk:6.0.0")
}
```

```kotlin
// Application class
class MobileApp : Application() {
    override fun onCreate() {
        super.onCreate()
        
        // Initialize Embrace as early as possible in Application.onCreate
        Embrace.getInstance().start(this)
        
        // Set user context
        Embrace.getInstance().setUserIdentifier("user_849204")
        Embrace.getInstance().addUserPersona("prime_subscriber")
        
        // Add custom breadcrumbs
        Embrace.getInstance().addBreadcrumb("Checkout Flow Initiated")
    }
}

// Measuring custom critical user flows (e.g., Add to Cart -> Order Placed)
class CheckoutViewModel : ViewModel() {
    fun startCheckout() {
        // Start a tracked moment
        Embrace.getInstance().startMoment("checkout_latency")
    }

    fun onCheckoutSuccess() {
        // End the tracked moment with custom properties
        Embrace.getInstance().endMoment("checkout_latency", mapOf("payment_type" to "apple_pay"))
    }

    fun onCheckoutFailed(error: Throwable) {
        Embrace.getInstance().recordError(
            error, 
            mapOf("step" to "stripe_payment_intent"),
            true // Allow crash-free session calculation adjustment
        )
    }
}
```

### iOS (Swift) Implementation

```swift
import UIKit
import EmbraceIO

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        // Start Embrace immediately
        do {
            try Embrace.client?.start()
        } catch {
            print("Failed to start Embrace: \(error)")
        }
        
        return true
    }
}

// Logging custom views and network breadcrumbs
class ProductDetailViewController: UIViewController {
    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        Embrace.client?.addBreadcrumb(name: "ProductDetail_Opened")
    }
}
```

---

## 📊 Battery & Performance Footprint Optimization

Capturing 100% of user sessions sounds computationally expensive. How does Embrace prevent draining battery or causing jank?

1. **In-Memory Ring Buffer**: Telemetry is written into a zero-allocation circular buffer in native memory (C/C++).
2. **Batch Compression & Upload**: Logs and metrics are compressed via Zstandard (`zstd`) and flushed to disk. They are uploaded:
   - When the app transitions to the background (`onStop` / `didEnterBackground`).
   - At the beginning of the subsequent app launch.
3. **No Network Overhead on App Launch**: Launch-critical metrics are buffered locally and deferred until background network queues have settled.

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How do you detect and fix an Out-Of-Memory (OOM) crash when Android's Low Memory Killer (LMK) sends a SIGKILL that bypasses all Java/Kotlin try-catch blocks?"
* **Answer**: The OS LMK terminates processes with `SIGKILL` (signal 9), which cannot be caught by any language-level uncaught exception handler or signal handler.
* **Architecture Solution**:
  1. Record continuous memory state markers (`ActivityManager.getMemoryInfo()`, device available RAM, JVM heap usage, low-memory trim callbacks `onTrimMemory(TRIM_MEMORY_RUNNING_CRITICAL)`) to a small memory-mapped file (`mmap`).
  2. On the next application launch, if the app did not shut down cleanly via normal lifecycle callbacks and the last recorded memory marker indicated critical memory pressure, the session is classified as an **OOM Termination**.
  3. Inspect the session timeline to find high bitmap allocations, retained fragment/activity leaks (e.g., LeakCanary), or unconstrained cache sizes.

### Q2: "Why choose Embrace over Datadog for an enterprise mobile application?"
* **Trade-off Analysis**:
  - Choose **Datadog** if your organization already uses Datadog for backend Kubernetes/APM and demands unified W3C distributed trace correlation from the mobile screen all the way to backend PostgreSQL queries.
  - Choose **Embrace** if your primary challenge is mobile-specific user experience bugs: mystery ANRs, cold-start bottlenecks, OOM crashes, and non-fatal session freezes that traditional APM sampling misses.
