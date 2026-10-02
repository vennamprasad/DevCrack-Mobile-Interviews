# 🐶 Datadog Mobile Observability & RUM Mastery

> **The definitive Senior & Staff Mobile Engineer guide to Real User Monitoring (RUM), Distributed Tracing (Mobile ↔ Backend), Mobile Vitals, and Session Replay.**

![Datadog](https://img.shields.io/badge/Platform-Datadog_RUM-632CA6?style=for-the-badge&logo=datadog&logoColor=white)
![Observability](https://img.shields.io/badge/Discipline-Full_Stack_Observability-blue?style=for-the-badge)
![DistributedTracing](https://img.shields.io/badge/APM-W3C_Trace_Context-green?style=for-the-badge)
![Level](https://img.shields.io/badge/Target-Senior_%2F_Staff_%2F_Architect-purple?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Why Datadog for Mobile?](#1-why-datadog-for-mobile)
- [2. The 4 Pillars of Mobile Observability](#2-the-4-pillars-of-mobile-observability)
- [3. Distributed Tracing: Linking Mobile to Backend Spans](#3-distributed-tracing-linking-mobile-to-backend-spans)
- [4. Android SDK Implementation](#4-android-sdk-implementation)
- [5. iOS SDK Implementation (Swift)](#5-ios-sdk-implementation-swift)
- [6. Mobile Vitals: Slow Frames, Frozen Frames & App Launch](#6-mobile-vitals-slow-frames-frozen-frames--app-launch)
- [7. Privacy, Compliance & PII Masking](#7-privacy-compliance--pii-masking)
- [8. CI/CD Deobfuscation (R8 & dSYM)](#8-cicd-deobfuscation-r8--dsym)
- [9. Datadog vs Firebase vs Sentry Decision Matrix](#9-datadog-vs-firebase-vs-sentry-decision-matrix)
- [10. Staff Interview Scenarios & Talking Points](#10-staff-interview-scenarios--talking-points)

---

## 1. Why Datadog for Mobile?

In modern microservice architectures, mobile apps are the **entry point** to distributed backend graphs. When a checkout fails or loads slowly, traditional crash reporters (like Firebase Crashlytics) only report fatal unhandled exceptions, leaving silent network delays, dropped frames, and backend 500 errors invisible.

**Datadog Mobile RUM (Real User Monitoring)** provides:
- **Full-Journey Visibility:** Correlates every tap, scroll, screen transition, network request, and crash into a unified session timeline.
- **Distributed APM Tracing:** Automatically propagates trace headers so backend server spans are tied to the exact mobile button click that initiated them.
- **Session Replay:** Pixel-accurate, PII-sanitized visual replays of user actions leading up to a bug.

---

## 2. The 4 Pillars of Mobile Observability

```
┌─────────────────────────────────────────────────────────────┐
│                     1. Mobile RUM                           │
│  - User sessions, screen view durations, custom user actions│
│  - Taps, swipes, navigation flow drop-offs                  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    2. Mobile Vitals                         │
│  - Cold Start (TTID/TTFD), Warm Start, Hot Start            │
│  - Slow Frames (> 16.6ms), Frozen Frames (> 700ms)          │
│  - CPU Churn, Memory Usage (OOM warnings), Battery drain   │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│               3. Crash & Error Tracking                     │
│  - JVM crashes, Native NDK (tombstone) segmentation faults  │
│  - iOS fatal Mach exceptions & SIGSEGV signals              │
│  - Automatic deobfuscation (R8/ProGuard) & dSYM symbolication│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│           4. Distributed Tracing (APM Link)                 │
│  - Injects W3C Trace Context (traceparent / tracestate)     │
│  - Connects client OkHttp/URLSession calls to cloud spans   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Distributed Tracing: Linking Mobile to Backend Spans

The key technical advantage of Datadog is injecting **W3C Trace Context headers** into outbound HTTP requests:

```
[Android Client Tap: "Pay Now"]
   │
   │  Headers injected:
   │  x-datadog-trace-id: 1234567890
   │  x-datadog-parent-id: 9876543210
   │  traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
   ▼
[API Gateway] ──► [Order Service] ──► [Payment Service] ──► [Postgres DB]
   (20ms)             (45ms)             (3,400ms - slow!)        (10ms)
```

In the Datadog dashboard, an engineer investigating why a user experienced a 3.5-second freeze immediately sees that **3,400ms was spent waiting inside the downstream Payment Service**, not the mobile device!

---

## 4. Android SDK Implementation

### Step 1: Dependencies (`build.gradle.kts`)
```kotlin
dependencies {
    implementation("com.datadoghq:dd-sdk-android-rum:2.14.0")
    implementation("com.datadoghq:dd-sdk-android-okhttp:2.14.0")
    implementation("com.datadoghq:dd-sdk-android-session-replay:2.14.0")
}
```

### Step 2: Initialization (`Application.onCreate`)
```kotlin
import android.app.Application
import com.datadog.android.Datadog
import com.datadog.android.core.configuration.Configuration
import com.datadog.android.core.configuration.Credentials
import com.datadog.android.privacy.TrackingConsent
import com.datadog.android.rum.Rum
import com.datadog.android.rum.RumConfiguration
import com.datadog.android.rum.tracking.ActivityViewTrackingStrategy

class MobileApp : Application() {
    override fun onCreate() {
        super.onCreate()

        // 1. Credentials
        val credentials = Credentials(
            clientToken = BuildConfig.DATADOG_CLIENT_TOKEN,
            env = BuildConfig.BUILD_TYPE, // "staging" or "release"
            variant = BuildConfig.FLAVOR
        )

        // 2. Global Core Configuration
        val config = Configuration.Builder(
            crashReportsEnabled = true // Catches JVM & NDK crashes
        ).build()

        Datadog.initialize(this, credentials, config, TrackingConsent.GRANTED)

        // 3. Configure RUM
        val rumConfig = RumConfiguration.Builder(applicationId = BuildConfig.DATADOG_APP_ID)
            .trackUserInteractions() // Auto-captures Button taps & List clicks
            .useViewTrackingStrategy(ActivityViewTrackingStrategy(trackExtras = false))
            .trackLongTasks(durationThresholdMs = 100L) // Flags UI blocks > 100ms
            .build()

        Rum.enable(rumConfig)
    }
}
```

### Step 3: OkHttp Distributed Tracing Interceptor
```kotlin
import com.datadog.android.okhttp.DatadogInterceptor
import com.datadog.android.okhttp.trace.TracingInterceptor
import okhttp3.OkHttpClient

val okHttpClient = OkHttpClient.Builder()
    // Injects W3C & Datadog headers only to verified first-party API domains
    .addInterceptor(
        DatadogInterceptor(
            tracedHosts = listOf("api.devcrack.com", "gateway.devcrack.com")
        )
    )
    .addNetworkInterceptor(
        TracingInterceptor(
            tracedHosts = listOf("api.devcrack.com", "gateway.devcrack.com")
        )
    )
    .build()
```

---

## 5. iOS SDK Implementation (Swift)

### Initialization (`AppDelegate.swift`)
```swift
import DatadogCore
import DatadogRUM
import DatadogTrace

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        // 1. Initialize Datadog Core
        Datadog.initialize(
            with: Datadog.Configuration(
                clientToken: "pub_token_here",
                env: "production"
            ),
            trackingConsent: .granted
        )

        // 2. Enable RUM
        RUM.enable(
            with: RUM.Configuration(
                applicationID: "app_id_here",
                uiKitViewsPredicate: DefaultUIKitRUMViewsPredicate(),
                uiKitActionsPredicate: DefaultUIKitRUMActionsPredicate()
            )
        )

        // 3. Enable URLSession Distributed Tracing
        Trace.enable(
            with: Trace.Configuration(
                networkInfoEnabled: true
            )
        )

        return true
    }
}
```

---

## 6. Mobile Vitals: Slow Frames, Frozen Frames & App Launch

Datadog benchmarks device health against Google Play Console & Apple Store thresholds:

| Vital | Threshold | Detection Mechanism |
| :--- | :--- | :--- |
| **Cold Start (TTID)** | Target: < 2,000ms | Measured from process spawn until first frame presentation (`Activity.onResume()` + draw pass). |
| **Time to Full Display (TTFD)** | Target: < 3,500ms | Triggered explicitly in code when feed/content renders via `GlobalRumMonitor.get().reportFullyDrawn()`. |
| **Slow Frame** | Duration > 16.6ms | Frame took longer than one refresh cycle (60 FPS). |
| **Frozen Frame** | Duration > 700ms | Extreme user-perceptible freeze where the app fails to accept inputs. |
| **Long Tasks** | Main thread > 100ms | Captured via `Looper.setMessageLogging()` printer inspection on Android. |

---

## 7. Privacy, Compliance & PII Masking

Enterprise mobile apps (FinTech, Healthcare) must comply with GDPR, HIPAA, and PCI-DSS.

Datadog Session Replay supports three privacy levels:
1. **`ALLOW`**: Records all elements on the screen. (Never use in production).
2. **`MASK_USER_INPUT` (Default)**: Automatically masks `EditText`, `TextField`, inputs, and sensitive form elements with asterisks (`***`).
3. **`MASK_ALL`**: Overlays solid gray placeholder blocks over all UI text and images, recording only the geometry and animations.

In Jetpack Compose or SwiftUI, engineers explicitly mask views:
```kotlin
// Mask sensitive account balance
Text(
    text = "$54,230.00",
    modifier = Modifier.datadogSessionReplayMask()
)
```

---

## 8. CI/CD Deobfuscation (R8 & dSYM)

When uploading release builds to production, stack traces are obfuscated (`com.app.a.b.c()`).

### Fastlane Action (`Fastfile`)
```ruby
lane :upload_datadog_mappings do
  # Upload Android ProGuard/R8 mapping file
  sh("npx @datadog/datadog-ci sourcemaps upload ./app/build/outputs/mapping/release/mapping.txt \
      --service com.devcrack.app \
      --release-version #{get_version_name} \
      --minified-path ./app/build/outputs/apk/release/")

  # Upload iOS dSYM symbols
  datadog_upload_dsym(
    api_key: ENV["DATADOG_API_KEY"],
    dsym_path: "./build/MobileApp.app.dSYM.zip"
  )
end
```

---

## 9. Datadog vs Firebase vs Sentry Decision Matrix

| Dimension | Firebase Crashlytics | Sentry | Datadog Mobile RUM |
| :--- | :--- | :--- | :--- |
| **Core Architecture** | Mobile crash reporter | Developer error & performance platform | Enterprise full-stack observability platform |
| **Distributed APM Tracing** | ❌ None | ⚠️ Partial backend trace correlation | ✅ Full W3C OpenTelemetry trace propagation |
| **Session Replay** | ❌ None | ✅ Good | ✅ High-performance, granular PII masking |
| **Mobile Vitals** | ⚠️ Basic (Firebase Perf) | ✅ Good | ✅ Advanced (Frozen frames, ANRs, battery, memory) |
| **Pricing Model** | Free (Google Cloud) | Per-event / developer seats | Per-session / Monthly Active Users (MAU) |
| **Best Fit** | Early-stage apps & startups | Mid-sized product teams | Enterprise organizations with complex microservices |

---

## 10. Staff Interview Scenarios & Talking Points

### Scenario 1: "How do you trace an API latency issue from mobile to the backend?"
> **Staff Answer:** "We configure the Datadog OkHttp interceptor with first-party host filters (`tracedHosts`). When the user taps a button, Datadog generates an OpenTelemetry-compliant `traceparent` header containing a unique Trace ID and Span ID. The API Gateway forwards these headers across downstream microservices. If an API request stalls, we jump directly from the mobile RUM session into the backend APM flame graph, pinpointing the slow microservice or SQL query."

### Scenario 2: "How do you ensure the Datadog SDK doesn't drain the device battery or cause memory pressure?"
> **Staff Answer:** "The Datadog SDK writes telemetry to an encrypted, ring-buffered SQLite store on local disk. It does not perform immediate network calls per event. Instead, it uploads data in opportunistic batches, throttling back uploads when the OS enters Low Power / Battery Saver mode or when the radio state is on metered cellular networks."
