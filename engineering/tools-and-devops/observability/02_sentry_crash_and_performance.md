# 🚨 Sentry Error Tracking & Mobile Performance Monitoring

> **Developer-first crash reporting, ANR watchdog detection, breadcrumbs, distributed tracing, and real-time release health.**

![Sentry](https://img.shields.io/badge/Platform-Sentry_Mobile-362D59?style=for-the-badge&logo=sentry&logoColor=white)
![ErrorTracking](https://img.shields.io/badge/Focus-Crash_&_ANRs-red?style=for-the-badge)
![Performance](https://img.shields.io/badge/Performance-Transaction_Spans-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Core Concepts: Errors, Events & Breadcrumbs](#1-core-concepts-errors-events--breadcrumbs)
- [2. ANR (Application Not Responding) Watchdog](#2-anr-watchdog-architecture)
- [3. Android Implementation & Timber Integration](#3-android-implementation)
- [4. Performance Monitoring: Transactions & Spans](#4-performance-monitoring-transactions--spans)
- [5. Sentry vs Datadog vs Crashlytics](#5-sentry-vs-datadog-vs-crashlytics)

---

## 1. Core Concepts: Errors, Events & Breadcrumbs

Unlike generic analytics platforms, **Sentry** focuses on actionable developer diagnostics:
- **Breadcrumbs:** A trail of user interactions (taps, screen navigations, network responses, lifecycle changes) that occurred immediately before a crash.
- **Fingerprinting:** Groups identical root causes together even when line numbers shift due to app updates.
- **Release Health:** Real-time percentage of crash-free users and crash-free sessions per app version.

---

## 2. ANR Watchdog Architecture

An **ANR (Application Not Responding)** occurs when the UI Main thread is blocked for > 5,000ms.

Sentry runs an internal daemon watchdog thread:
```kotlin
// Conceptual Watchdog Thread
class ANRWatchdog(private val timeoutMs: Long = 5000L) : Thread() {
    private var tick = 0
    private val handler = Handler(Looper.getMainLooper())

    override fun run() {
        while (!isInterrupted) {
            val lastTick = tick
            handler.post { tick++ }
            sleep(timeoutMs)

            // If main thread didn't increment tick within timeoutMs -> ANR!
            if (tick == lastTick) {
                val mainThreadStack = Looper.getMainLooper().thread.stackTrace
                Sentry.captureException(ApplicationNotRespondingException(mainThreadStack))
            }
        }
    }
}
```

---

## 3. Android Implementation

### Step 1: Gradle Dependency (`build.gradle.kts`)
```kotlin
plugins {
    id("io.sentry.android.gradle") version "4.14.0"
}

dependencies {
    implementation("io.sentry:sentry-android:7.14.0")
    implementation("io.sentry:sentry-android-timber:7.14.0")
}
```

### Step 2: Initialize (`AndroidManifest.xml`)
Sentry uses AndroidX Startup to initialize automatically:
```xml
<application>
    <meta-data android:name="io.sentry.dsn" android:value="https://your_dsn@sentry.io/12345" />
    <meta-data android:name="io.sentry.traces.sample-rate" android:value="0.2" /> <!-- 20% of sessions traced -->
    <meta-data android:name="io.sentry.anr.enable" android:value="true" />
</application>
```

---

## 4. Performance Monitoring: Transactions & Spans

Measure critical custom operations:
```kotlin
import io.sentry.Sentry

fun processCheckout() {
    val transaction = Sentry.startTransaction("checkout_flow", "task")
    try {
        val span = transaction.startChild("validate_cart", "validating local state")
        validateCart()
        span.finish()

        val paymentSpan = transaction.startChild("charge_card", "network call")
        executePayment()
        paymentSpan.finish()
    } catch (e: Exception) {
        transaction.throwable = e
        transaction.finish(SpanStatus.INTERNAL_ERROR)
        throw e
    }
    transaction.finish(SpanStatus.OK)
}
```
