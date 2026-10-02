# ⚡ Statsig: Modern Feature Gates, Dynamic Config & Automated Pulse Metrics

> **The modern all-in-one experimentation standard: Unifying feature gating, dynamic configuration, product analytics, and automated health checks without pipeline fragmentation.**

---

## 📌 Executive Summary

Historically, tech organizations were forced to stitch together three separate vendor SDKs:
1. **LaunchDarkly / Split.io** for feature flags.
2. **Optimizely / Eppo** for A/B test statistical analysis.
3. **Amplitude / Mixpanel** for user product analytics.

**Statsig** consolidates all three into a single lightweight client SDK. By marrying feature gates with automatic telemetry ingestion, Statsig generates **Pulse Metrics**—automated real-time dashboards that prove not just whether a feature was turned on, but whether it increased crash rates, battery consumption, latency, or revenue.

---

## 🏗️ Core Pillars of the Statsig Architecture

```
                                  [ Statsig Cloud / Warehouse-Native ]
                                                   │
                       ┌───────────────────────────┼───────────────────────────┐
                       ▼                           ▼                           ▼
              [ 1. Feature Gates ]        [ 2. Dynamic Config ]       [ 3. Experiments ]
             (Boolean Rollouts &        (Remote JSON / Layout       (Multivariate Statistical
               Kill Switches)              Style Tokens)                  A/B Testing)
                       │                           │                           │
                       └───────────────────────────┬───────────────────────────┘
                                                   │
                                      (Unified Mobile Client SDK)
                                                   ▼
                                         [ In-Memory Cache ]
                                                   │
                                     (Automatic Health Telemetry)
                                                   ▼
                                      [ Real-Time Pulse Engine ]
                             (Detects Crashes, Latency, & Conversions)
```

---

## 💻 Production Implementation (Android & iOS)

### 1. Android (Kotlin) Implementation

```kotlin
// build.gradle.kts
dependencies {
    implementation("com.statsig:android-sdk:1.35.0")
}
```

```kotlin
class ExperimentationManager(private val application: Application) {

    private val user = StatsigUser("user_abc123").apply {
        email = "developer@example.com"
        country = "US"
        appVersion = BuildConfig.VERSION_NAME
        custom = mapOf(
            "loyalty_tier" to "platinum",
            "device_memory_gb" to "8"
        )
    }

    suspend fun initialize() {
        Statsig.client.initializeAsync(
            application,
            "client-sdk-key-here",
            user,
            StatsigOptions(
                // Cache evaluations locally to prevent white screens on cold boot
                loadCacheFromDisk = true,
                initTimeoutMs = 2500 // Cap initial blocking to 2.5 seconds
            )
        )
    }

    // 1. Feature Gate (Boolean Evaluation)
    fun isAiSearchEnabled(): Boolean {
        return Statsig.checkGate("enable_ai_semantic_search")
    }

    // 2. Dynamic Config (Runtime parameters without app store update)
    fun getCheckoutConfig(): CheckoutStyleConfig {
        val config: DynamicConfig = Statsig.getConfig("checkout_layout_config")
        return CheckoutStyleConfig(
            showApplePayFirst = config.getBoolean("show_apple_pay_first", false),
            primaryColorHex = config.getString("button_color", "#0066FF"),
            maxItemLimit = config.getInt("max_items", 10)
        )
    }

    // 3. Running an A/B/n Experiment & Logging Exposure
    fun getRecommendationEngineVariant(): String {
        val experiment = Statsig.getExperiment("search_recommendation_algorithm_v2")
        // Statsig automatically logs the exposure event when you call getExperiment
        return experiment.getString("algorithm_model", "collaborative_filtering")
    }

    // 4. Logging custom conversion events for automated Pulse analysis
    fun logPurchaseCompleted(orderId: String, amountUsd: Double) {
        Statsig.logEvent("purchase_completed", value = amountUsd, metadata = mapOf("order_id" to orderId))
    }
}
```

### 2. iOS (Swift) Implementation

```swift
import Statsig

class FeatureFlagService {
    static let shared = FeatureFlagService()

    func initialize(userId: String) {
        let user = StatsigUser(userID: userId)
        user.custom = ["app_version": Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? ""]

        Statsig.initialize(sdkKey: "client-sdk-key-here", user: user) { error in
            if let error = error {
                print("Statsig failed to sync latest values: \(error). Using local cache.")
            }
        }
    }

    func isNewCheckoutEnabled() -> Bool {
        return Statsig.checkGate("new_checkout_flow")
    }
}
```

---

## 📊 The "Pulse" Advantage: Automated Health Guardrails

In standard feature flag systems, an engineer turns on a flag for 5% of users. If that feature causes memory leaks or background thread starvation, the engineer might not notice until users complain or crash stats spike hours later.

### Statsig Pulse Engine
Every time a feature gate or experiment is evaluated, Statsig correlates that evaluation with downstream device telemetry:

```
[ Gate: new_feed_algorithm ]
┌───────────────────────────────┬─────────────────┬──────────────────────┐
│ Metric                        │ Lift / Impact   │ Statistical Status   │
├───────────────────────────────┼─────────────────┼──────────────────────┤
│ 30-Day Retention              │ + 4.2%          │ 🟢 Statistically Sig │
│ Time Spent in App             │ + 11.5%         │ 🟢 Statistically Sig │
│ App Startup Latency (TTID)    │ - 12ms          │ ⚪ Neutral           │
│ App Crash Rate                │ + 0.8%          │ 🔴 CRITICAL GUARDRAIL│
└───────────────────────────────┴─────────────────┴──────────────────────┘
⚠️ Automatic Circuit Breaker: Gate paused automatically due to crash threshold breach!
```

---

## 🎯 Global Holdouts & Layered Experimentation

When 15 mobile product teams run experiments simultaneously on the same checkout screen, two experiments often collide:
- **Team A** tests a new Green Button vs. Blue Button.
- **Team B** tests a 1-Step Checkout vs. 3-Step Checkout.

If a user gets both variants simultaneously, the statistical results become contaminated.

### How Statsig Solves It:
1. **Layers (Mutual Exclusion)**: Multiple experiments are grouped into a "Layer". A user is allocated to only *one* experiment within that Layer at a time.
2. **Global Holdout Groups**: 5% of all users are held out from *all* feature releases for 6 months. This allows leadership to measure the true cumulative impact of all product changes against a control baseline.

---

## ⚖️ Vendor Comparison: Split vs. LaunchDarkly vs. Eppo vs. Statsig

| Feature | LaunchDarkly | Split.io | Eppo | Statsig |
| :--- | :--- | :--- | :--- | :--- |
| **Primary DNA** | Feature Flagging & Safe Delivery | Feature Delivery & Attribution | Warehouse-Native Statistical Rigor | Unified Flags + Product Analytics + A/B |
| **Real-Time Edge** | SSE Streaming (<200ms) | SSE Streaming + Polling fallback | Client evaluation / Polling | HTTP / Edge SSE Streaming |
| **Pulse Health Guards**| Requires Datadog integration | Built-in basic monitoring | Requires Snowflake/BigQuery sync | **Built-in automated telemetry correlation** |
| **Warehouse-Native** | No (Cloud Managed) | No (Cloud Managed) | **Yes (Direct SQL on Snowflake/BigQuery)** | **Both (Cloud or Warehouse-Native)** |
| **Best Used By** | Enterprise DevOps & Platform teams | Large financial & enterprise orgs | Data Science teams obsessed with statistics (CUPED) | Fast-moving mobile startups & modern tech unicorns |

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How do you evaluate feature flags for anonymous/unauthenticated users during app install, and merge their state once they log in?"
* **Answer**:
  1. Generate an ephemeral UUID upon the very first app launch and persist it in EncryptedSharedPreferences (Android) or Keychain (iOS).
  2. Initialize the experimentation SDK with `StatsigUser(userID = localUuid)`.
  3. When the user successfully signs in or signs up, call `updateUser(StatsigUser(userID = authenticatedAccountId))`.
  4. Ensure the experimentation backend supports **identity stitching** so the anonymous conversion events (e.g., install -> add to cart) are merged with the authenticated user profile.
