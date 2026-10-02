# 💥 Firebase Crashlytics & Performance Monitoring Mastery

> **The industry's most ubiquitous mobile reliability foundation: Native crash symbolication, NDK stack unwinding, custom keys, real-time performance traces, and BigQuery streaming analytics.**

---

## 📌 Executive Summary

**Firebase Crashlytics** and **Firebase Performance Monitoring** form the default observability standard for over 80% of Android and iOS mobile applications worldwide. 

Beyond simple unhandled exception tracking, an enterprise-grade Firebase deployment requires:
1. **Automated CI/CD symbolication** (R8/ProGuard `mapping.txt` and native NDK C/C++ debug symbols).
2. **Context-rich non-fatal logging** (`recordException`, custom key-value pairs, user identifiers).
3. **Automated performance metric collection** (Time to Initial Display, frozen frames, slow rendering).
4. **Streaming to Google BigQuery** for deep custom SQL retention and cohort crash analysis.

---

## 🏗️ Architectural Overview: Ingestion & Symbolication Pipeline

```
  [ Mobile Client: Android / iOS ]
                 │
                 ├── 1. JVM / Swift Uncaught Exception Handler
                 ├── 2. Native Signal Handler (SIGSEGV, SIGABRT, SIGBUS)
                 └── 3. Local Crash Cache (Disk Persistence)
                                 │
                         (Next App Launch)
                                 ▼
                     [ Firebase Ingestion API ]
                                 │
                 ┌───────────────┴────────────────┐
                 │                                │
                 ▼                                ▼
        [ Obfuscated Stack ]            [ Native Memory Offsets ]
         (e.g., com.app.a.b(Source:1))    (e.g., libcore.so + 0x3a4b)
                 │                                │
                 ▼                                ▼
        [ R8 / ProGuard Mapping ]        [ Native Symbols (dSYM / .so) ]
                 │                                │
                 └────────────────┬───────────────┘
                                  ▼
               [ Deobfuscated, Human-Readable Trace ]
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
        [ Firebase Console ]             [ BigQuery Real-Time Stream ]
        (Velocity Alerts & Trends)       (Custom SQL Analytics)
```

---

## 💻 Advanced Production Setup

### 1. Gradle Configuration for JVM & NDK Symbolication (Android)

```kotlin
// root build.gradle.kts
plugins {
    id("com.google.gms.google-services") version "4.4.1" apply false
    id("com.google.firebase.crashlytics") version "2.9.9" apply false
    id("com.google.firebase.firebase-perf") version "1.4.2" apply false
}

// app/build.gradle.kts
plugins {
    id("com.android.application")
    id("com.google.gms.google-services")
    id("com.google.firebase.crashlytics")
    id("com.google.firebase.firebase-perf")
}

android {
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            
            // Enable NDK crash reporting if your app uses C++ libraries (.so)
            configure<com.google.firebase.crashlytics.buildtools.gradle.CrashlyticsExtension> {
                mappingFileUploadEnabled = true
                nativeSymbolUploadEnabled = true
                unstrippedNativeLibsDir = "build/intermediates/merged_native_libs/release/out/lib"
            }
        }
    }
}

dependencies {
    implementation(platform("com.google.firebase:firebase-bom:32.8.0"))
    implementation("com.google.firebase:firebase-crashlytics-ktx")
    implementation("com.google.firebase:firebase-crashlytics-ndk") // For native C/C++
    implementation("com.google.firebase:firebase-perf-ktx")
}
```

---

## 🛠️ Production Logging Best Practices

### Setting Context Without Leaking PII (Kotlin)

```kotlin
class AppTelemetryManager(private val crashlytics: FirebaseCrashlytics) {

    fun initUserSession(userId: String, subscriptionTier: String, appVariant: String) {
        // Set user ID (Never use PII like email address or raw phone number)
        crashlytics.setUserId(userId)
        
        // Structured Key-Value tags for filtering in Firebase Console
        crashlytics.setCustomKeys {
            key("subscription_tier", subscriptionTier)
            key("app_variant", appVariant)
            key("device_locale", Locale.getDefault().toLanguageTag())
            key("build_commit", BuildConfig.GIT_SHA)
        }
    }

    fun recordNonFatalError(exception: Throwable, context: Map<String, String>) {
        // Add transient breadcrumb logs
        crashlytics.log("Non-fatal exception in checkout flow. Context: $context")
        
        // Custom keys specific to this error
        context.forEach { (k, v) ->
            crashlytics.setCustomKey("err_ctx_$k", v)
        }
        
        // Send to Firebase
        crashlytics.recordException(exception)
    }
}
```

---

## ⏱️ Firebase Performance Monitoring in Production

### 1. Tracking Screen Rendering & Frame Drops
Firebase Performance automatically tracks slow and frozen frames across Activities/Fragments:
- **Slow Frame**: Render time > **16ms** (drops below 60fps).
- **Frozen Frame**: Render time > **700ms** (user perceives a hard UI stutter).

### 2. Custom Code Traces & HTTP Metrics

```kotlin
class ImagePipeline {

    // Trace code execution time declaratively
    @AddTrace(name = "image_decode_and_cache", enabled = true)
    fun processHighResImage(bitmap: Bitmap, cacheKey: String) {
        // Processing logic...
    }

    // Manual Trace with custom attributes and counters
    fun fetchDynamicConfiguration() {
        val trace = FirebasePerformance.getInstance().newTrace("remote_config_sync")
        trace.start()
        
        try {
            // Add custom attribute to slice performance by carrier or server region
            trace.putAttribute("cdn_provider", "cloudflare")
            
            // Increment metric counter
            trace.incrementMetric("config_retry_count", 1)
            
            // ... Network operation ...
        } finally {
            trace.stop()
        }
    }
}
```

---

## 🔍 Exporting to BigQuery for SQL Forensics

Exporting Crashlytics to BigQuery unlocks enterprise cohort analysis that the Firebase Web UI cannot compute.

### Example: Identifying High-Impact Crashes by User Lifetime Value (LTV)

```sql
SELECT
  issue_id,
  issue_title,
  COUNT(DISTINCT user.id) AS affected_users,
  COUNT(event_timestamp) AS total_crashes,
  app_info.version_name AS app_version,
  device.model AS device_model
FROM
  `your-project.firebase_crashlytics.com_your_app_ANDROID_REALTIME`
WHERE
  DATE(TIMESTAMP_MICROS(event_timestamp)) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND (
    SELECT value 
    FROM UNNEST(custom_keys) 
    WHERE key = 'subscription_tier'
  ) = 'enterprise_vip'
GROUP BY
  1, 2, 5, 6
ORDER BY
  affected_users DESC
LIMIT 10;
```

---

## ⚖️ Observability Platform Decision Matrix

| Capability | Firebase Crashlytics & Perf | Sentry | Datadog RUM | Embrace.io |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Strength** | Free tier, Google Cloud integration, ubiquity | Developer ergonomics, breadcrumbs, ANR watchdog | Full-stack distributed tracing (Mobile to DB) | 100% session capture, mystery ANR timeline reconstruction |
| **Pricing Model** | **Free** (charges only for BigQuery storage/querying) | Event-based quota | Session-based pricing (per 1,000 sessions) | Device/Session-based enterprise license |
| **ANR Detection** | Android ExitInfo post-mortem | Custom Watchdog thread sampling | RUM Watchdog polling | **Continuous main-thread sampler** with pre-ANR call graph |
| **Best Used For** | Everyday mobile apps, startups, standard Google ecosystems | Mid-to-large engineering teams focused on developer velocity | Enterprise organizations with existing Datadog backend infrastructure | Large consumer mobile apps (fintech, rideshare, social) with high ANR stakes |

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How do you handle crash reporting when an unhandled exception occurs inside a native C++ library (`.so`) loaded via JNI?"
* **Answer**: Standard JVM `Thread.setDefaultUncaughtExceptionHandler` cannot catch POSIX signals (`SIGSEGV`, `SIGABRT`, `SIGBUS`, `SIGFPE`).
* **Implementation**:
  1. Add `firebase-crashlytics-ndk` to the dependencies.
  2. The NDK library registers native signal handlers via `sigaction`.
  3. When a segmentation fault occurs, the handler catches the signal, walks the native call stack, writes an unstripped memory minidump to disk, and re-raises the signal to allow OS process termination.
  4. In CI/CD, upload the unstripped `.so` symbol files to Firebase via `firebaseCrashlytics.nativeSymbolUploadEnabled = true` so the memory offsets can be mapped back to C++ source lines.

### Q2: "What are the common causes of missing or obfuscated stack traces in Crashlytics reports, and how do you resolve them in CI/CD?"
* **Answer**:
  1. **Missing ProGuard/R8 mapping file**: The CI build generated a release APK/AAB with code shrinking, but the Gradle task `uploadCrashlyticsMappingFile{Variant}` was skipped or failed.
  2. **Solution**: Ensure CI explicitly executes `./gradlew uploadCrashlyticsMappingFileRelease` or uses the automatic plugin trigger during assemble/bundle steps. Store mappings in an internal artifact repository (e.g., S3/GCS) with the build hash for reproducible debugging.
