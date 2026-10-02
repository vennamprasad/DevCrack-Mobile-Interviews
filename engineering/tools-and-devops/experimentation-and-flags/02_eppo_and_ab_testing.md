# 🧪 Eppo, Statsig & Mobile Experimentation (A/B Testing)

> **Next-generation warehouse-native A/B testing, statistical rigor, CUPED variance reduction, Sample Ratio Mismatch (SRM), and guardrail metric tracking.**

![Eppo](https://img.shields.io/badge/Platform-Eppo_Experimentation-00D47E?style=for-the-badge&logoColor=white)
![Statsig](https://img.shields.io/badge/Platform-Statsig-1976D2?style=for-the-badge&logoColor=white)
![Statistics](https://img.shields.io/badge/Math-CUPED_%26_Sequential_Testing-purple?style=for-the-badge)
![Level](https://img.shields.io/badge/Target-Senior_%2F_Staff_%2F_Lead-orange?style=for-the-badge)

---

## 📖 Table of Contents
- [1. The Evolution of Mobile Experimentation](#1-the-evolution-of-mobile-experimentation)
- [2. What is Eppo? Warehouse-Native Architecture](#2-what-is-eppo-warehouse-native-architecture)
- [3. Statistical Rigor: CUPED, P-Hacking & Sequential Testing](#3-statistical-rigor)
- [4. Sample Ratio Mismatch (SRM): The Silent Experiment Killer](#4-sample-ratio-mismatch-srm)
- [5. Android & iOS Client SDK Integration](#5-client-sdk-integration)
- [6. Eppo vs Statsig vs Split.io vs Optimizely](#6-platform-decision-matrix)
- [7. Staff Interview Questions & Answers](#7-staff-interview-questions)

---

## 1. The Evolution of Mobile Experimentation

Historically, mobile A/B testing was handled by tools like Firebase Remote Config or Optimizely. However, data teams faced severe pain points:
1. **Data Silos:** Experiment metrics lived in the vendor's black-box database, conflicting with business numbers in Snowflake or BigQuery.
2. **Peeking Problem (P-Hacking):** Teams stopped experiments early when they saw a temporary positive spike, shipping false-positive features that hurt revenue long term.
3. **Slow Iterations:** Experiments took 4–6 weeks to reach statistical significance.

---

## 2. What is Eppo? Warehouse-Native Architecture

**Eppo** is a modern experimentation platform founded by former Airbnb data scientists that runs **directly on top of your central data warehouse** (Snowflake, BigQuery, Databricks, Redshift):

```
┌────────────────────────────────────────────────────────┐
│                      Mobile App                        │
│   Evaluates variants locally & logs exposure events   │
└───────────────────────────┬────────────────────────────┘
                            │ Segment / Snowplow / Rudderstack
┌───────────────────────────▼────────────────────────────┐
│          Company Data Warehouse (Snowflake/BigQuery)   │
│   Single Source of Truth: Orders, Revenue, Retention   │
└───────────────────────────┬────────────────────────────┘
                            │ SQL Queries (No data export)
┌───────────────────────────▼────────────────────────────┐
│                     Eppo Platform                      │
│   Runs CUPED, Bayesian & Frequentist models in-place   │
└────────────────────────────────────────────────────────┘
```

---

## 3. Statistical Rigor: CUPED, P-Hacking & Sequential Testing

### A. CUPED (Controlled-experiment Using Pre-Experiment Data)
- **The Problem:** High variance in user behavior means experiments take weeks to prove that Variant B is truly better.
- **The Solution:** CUPED uses user behavior *before* the experiment began (e.g., historical user spend) as a covariate to remove background noise from the test metric.
- **Impact:** **Reduces variance by 30%–50%**, shortening experiment run times from 4 weeks to 2 weeks!

### B. Guardrail Metrics
A change might increase "Sign-ups" (primary metric) by 10%, but increase "App Crashes" by 25% or "Battery Drain" by 15%. Eppo automatically alerts and triggers safety shutdowns if **guardrail metrics** breach thresholds.

---

## 4. Sample Ratio Mismatch (SRM): The Silent Experiment Killer

**Sample Ratio Mismatch (SRM)** occurs when the actual proportion of users assigned to variants deviates from the expected configuration.

- **Example:** You configure a 50/50 split between Control and Treatment.
- **Result:** You receive 50,000 Control users and only 42,000 Treatment users.
- **Why It Happens:**
  - Variant B introduces a crash on Android 12 before the exposure event logs.
  - Variant B makes network payloads heavier, timing out on 3G connections.
- **Rule:** If Chi-Square test reveals `p < 0.001` for SRM, **the experiment is completely invalid** and must be discarded.

---

## 5. Client SDK Integration

### Android Kotlin Example
```kotlin
import cloud.eppo.android.EppoClient
import cloud.eppo.android.ConfigurationRequest

// 1. Initialize Eppo SDK in Application.onCreate
val eppoClient = EppoClient.init(
    apiKey = BuildConfig.EPPO_API_KEY,
    application = this,
    host = "https://fscdn.eppo.cloud"
)

// 2. Fetch assigned variant for the user (Evaluated locally)
val variant = eppoClient.getStringAssignment(
    subjectKey = currentUserId,
    flagKey = "onboarding_flow_experiment"
)

when (variant) {
    "personalized_carousel" -> showPersonalizedOnboarding()
    "video_intro" -> showVideoOnboarding()
    else -> showDefaultOnboarding() // Control
}
```

---

## 6. Platform Decision Matrix

| Platform | Core Strength | Architecture Type | Statistical Methods |
| :--- | :--- | :--- | :--- |
| **Eppo** | Enterprise experimentation rigor for high-scale tech companies | **Warehouse-Native** (Snowflake / BigQuery) | CUPED, Sequential testing, Bayesian & Frequentist |
| **Split.io** | Feature management, progressive rollouts & kill switches | Cloud-hosted with client-side caching | Automated metric attribution, canary monitoring |
| **Statsig** | All-in-one feature flags, autotuned A/B testing & product analytics | Cloud or Warehouse-native hybrid | CUPED, Holdout groups, automated impact analysis |
| **LaunchDarkly** | Complex enterprise rule targeting & massive flag scale | Cloud-hosted streaming | Integration with external analytics |

---

## 7. Staff Interview Questions

### Q1: Why is warehouse-native experimentation (like Eppo) superior to vendor-hosted analytics?
> **Staff Answer:** "Vendor-hosted tools require shipping duplicate event data into a third-party black box, which frequently disagrees with the company's verified financial metrics. Warehouse-native platforms like Eppo compute experiment statistics directly in Snowflake/BigQuery against the single source of truth (cleansed ledger entries, churn tables, and subscriptions). It also eliminates PII security risks because sensitive user data never leaves our cloud."

### Q2: What is CUPED and why does it matter to mobile teams?
> **Staff Answer:** "CUPED leverages pre-experiment historical data as a covariate to cancel out pre-existing user variance. On mobile, where user adoption can be slow, CUPED cuts required sample sizes by 30%–50%, enabling product teams to make definitive go/no-go rollout decisions in half the time without sacrificing statistical power."
