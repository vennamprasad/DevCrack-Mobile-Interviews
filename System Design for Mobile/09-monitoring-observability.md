# 📊 Monitoring & Observability
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Track health, performance, and user behavior.

![Monitoring](https://img.shields.io/badge/DevOps-Monitoring-orange?style=for-the-badge&logo=prometheus&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Three Pillars (Metrics, Logs, Traces)](#three-pillars-of-observability)
- [2. Metrics Collection](#1-metrics-collection)
- [3. Crash Reporting](#2-crash-reporting)
- [4. KPI Targets](#monitoring-dashboard-metrics)

---

### Q10. How do you monitor and observe system performance?

**Answer:**

Monitoring and observability help detect issues, measure performance, and understand user experience.

**Three Pillars of Observability:**

```
1. Metrics  - What is happening? (Numbers, graphs)
2. Logs     - Why is it happening? (Events, errors)
3. Traces   - Where is it happening? (Request flow)
```

**1. Metrics Collection:**

```kotlin
// Track app performance metrics
class PerformanceMetrics @Inject constructor(
    private val analytics: FirebaseAnalytics
) {
    // API call metrics
    fun trackApiCall(
        endpoint: String,
        method: String,
        statusCode: Int,
        duration: Long
    ) {
        analytics.logEvent("api_call") {
            param("endpoint", endpoint)
            param("method", method)
            param("status_code", statusCode.toLong())
            param("duration_ms", duration)
            param("success", (statusCode in 200..299).toString())
        }

        // Track slow API calls
        if (duration > 5000) {
            analytics.logEvent("slow_api_call") {
                param("endpoint", endpoint)
                param("duration_ms", duration)
            }
        }
    }

    // Memory usage
    fun trackMemoryUsage() {
        val runtime = Runtime.getRuntime()
        val usedMemory = runtime.totalMemory() - runtime.freeMemory()
        val maxMemory = runtime.maxMemory()
        val usagePercent = (usedMemory.toFloat() / maxMemory * 100).toInt()

        analytics.logEvent("memory_usage") {
            param("used_mb", usedMemory / 1024 / 1024)
            param("usage_percent", usagePercent.toLong())
        }
    }
}
```

**2. Crash Reporting:**

```kotlin
class CrashReportingInitializer @Inject constructor(
    private val crashlytics: FirebaseCrashlytics
) {
    fun initialize(userId: String?) {
        crashlytics.setCrashlyticsCollectionEnabled(true)
        userId?.let { crashlytics.setUserId(it) }

        crashlytics.setCustomKey("app_version", BuildConfig.VERSION_NAME)
        crashlytics.setCustomKey("device_model", Build.MODEL)
        crashlytics.setCustomKey("os_version", Build.VERSION.SDK_INT)
    }
}
```

**Monitoring Dashboard Metrics:**

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| **App Crash Rate** | < 0.1% | > 1% |
| **API Success Rate** | > 99% | < 95% |
| **Screen Load Time** | < 2s | > 5s |
| **Memory Usage** | < 70% | > 85% |

---
