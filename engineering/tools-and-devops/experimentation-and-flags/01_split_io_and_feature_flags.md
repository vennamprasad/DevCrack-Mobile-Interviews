# 🎛️ Split.io & Enterprise Feature Flagging

> **Progressive delivery, targeted rollouts, instant kill switches, offline flag evaluation, and mobile SDK architecture with Split.io and LaunchDarkly.**

![SplitIO](https://img.shields.io/badge/Platform-Split.io-00A4E4?style=for-the-badge&logoColor=white)
![FeatureFlags](https://img.shields.io/badge/Pattern-Feature_Flags-blue?style=for-the-badge)
![Safety](https://img.shields.io/badge/Safety-Kill_Switch-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Why Feature Flags in Mobile Apps?](#1-why-feature-flags-in-mobile-apps)
- [2. Split.io Architecture: Local vs Remote Evaluation](#2-splitio-architecture-local-vs-remote-evaluation)
- [3. Android SDK Implementation](#3-android-sdk-implementation)
- [4. The Instant "Kill Switch" Pattern](#4-the-instant-kill-switch-pattern)
- [5. Offline Caching & Cold-Start Latency](#5-offline-caching--cold-start-latency)
- [6. Split.io vs LaunchDarkly Comparison](#6-splitio-vs-launchdarkly-comparison)
- [7. Staff Interview Questions & Answers](#7-staff-interview-questions--answers)

---

## 1. Why Feature Flags in Mobile Apps?

In web development, deploying a fix takes minutes. In mobile development:
- **App Store Review Delays:** Apple & Google reviews take 12–48 hours.
- **User Adoption Lag:** Users take weeks or months to update apps.

**Feature Flags decouple Deployment from Release.** Code is deployed dark to production, and features are toggled on, rolled out gradually (1% -> 5% -> 25% -> 100%), or instantly turned off with a **Kill Switch** without releasing a new binary!

---

## 2. Split.io Architecture: Local vs Remote Evaluation

A major pitfall in mobile is blocking the app's startup waiting for a feature flag server.

Split.io solves this using **Local In-Memory Evaluation**:
1. **Background Polling / SSE (Server-Sent Events):** The Split SDK synchronizes feature flag definitions ("splits") in the background and saves them in local SQLite cache.
2. **Instant Sub-Millisecond Evaluation:** When your code requests `getTreatment("checkout_v2")`, the evaluation happens **locally in memory in < 1ms** using user targeting rules—no HTTP network roundtrip!

```
[App Launch] ──► Reads cached splits from disk (Instant)
     │
     └──► Background SSE Streaming ──► Receives flag updates in real time
```

---

## 3. Android SDK Implementation

### Step 1: Initialize Split Client (`Application.onCreate`)
```kotlin
import io.split.android.client.SplitClient
import io.split.android.client.SplitClientConfig
import io.split.android.client.SplitFactoryBuilder

class MobileApp : Application() {
    companion object {
        lateinit var splitClient: SplitClient
    }

    override fun onCreate() {
        super.onCreate()

        val config = SplitClientConfig.builder()
            .synchronizeInBackground(true) // Updates cache in background
            .build()

        val splitFactory = SplitFactoryBuilder.build(
            BuildConfig.SPLIT_API_KEY,
            Key(userId), // Unique user ID for deterministic bucket assignment
            config,
            this
        )

        splitClient = splitFactory.client()
    }
}
```

### Step 2: Evaluating a Flag in Code
```kotlin
fun renderPaymentButton() {
    val treatment = MobileApp.splitClient.getTreatment("new_payment_flow")

    when (treatment) {
        "on" -> {
            // Show new Apple Pay / Google Pay Flow
            showModernPaymentSheet()
        }
        "off" -> {
            // Fallback to legacy credit card form
            showLegacyCreditCardForm()
        }
        else -> {
            // "control" -> Default safe fallback if flag rule isn't ready
            showLegacyCreditCardForm()
        }
    }
}
```

---

## 4. The Instant "Kill Switch" Pattern

If a newly launched feature causes crashes, high battery drain, or severe backend overload:
1. Engineer flips the flag to `off` in the Split.io console.
2. Connected mobile clients receive an SSE push notification within seconds and immediately revert to the legacy code path.
3. **No emergency hotfix build or App Store submission required!**

---

## 5. Offline Caching & Cold-Start Latency

To avoid blank screens on app startup:
- Use **Cached Treatments:** The SDK evaluates against the cached rules stored in disk from the previous session.
- **Ready Listener:** If fresh flags are required for first launch, use `client.on(SplitEvent.SDK_READY)` with a timeout fallback (e.g., 500ms max).

---

## 6. Split.io vs LaunchDarkly Comparison

| Feature | Split.io | LaunchDarkly |
| :--- | :--- | :--- |
| **Primary Strength** | Feature flags tightly tied to **data & error metrics** | World-class enterprise targeting rules and scaling |
| **Real-Time Streaming** | Server-Sent Events (SSE) | Server-Sent Events (SSE) |
| **Statistical Analysis** | Built-in metric attribution | Integration with experimentation platforms |
| **Local Evaluation** | Supported on mobile & backend | Supported on mobile & backend |
