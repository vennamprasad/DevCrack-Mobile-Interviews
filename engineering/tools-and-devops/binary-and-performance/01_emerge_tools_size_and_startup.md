# 🔬 Emerge Tools: Mobile Binary Analysis, App Size & Startup Profiling

> **The modern standard for binary health: Automated DEX / Mach-O size breakdown, real-device startup flamegraphs, Reaper dead-code elimination, and automated PR snapshot testing.**

---

## 📌 Executive Summary

For large consumer apps (like Airbnb, DoorDash, Uber, Stripe, and Square), **app download size** directly correlates with user conversion and install rates:
- Google Play research shows that **for every 6 MB increase in APK/AAB size, install conversion drops by 1%**.
- Apple App Store imposes strict cellular download limits (e.g., 200 MB warning limits).

**Emerge Tools** has emerged as the premier developer platform for continuous binary optimization, startup profiling, and visual regression testing directly inside the GitHub CI/CD pipeline.

---

## 🏗️ Core Platform Capabilities

```
                       [ Pull Request Created / CI Triggered ]
                                         │
                                         ▼
                      [ Emerge Tools CI Action / Fastlane ]
                                         │
     ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
     ▼                   ▼                               ▼                   ▼
[ 1. Size Analysis ] [ 2. Startup Profiling ]     [ 3. Reaper Engine ]  [ 4. Snapshot Tests ]
 • DEX / Mach-O diff  • Real-device lab testing    • Runtime dead code   • Pixel-diff checks
 • Asset compression  • Cold start flamegraphs       detection           • Dark mode & dynamic
 • Third-party SDK    • Main-thread jank alerts    • Unused classes        type audits
   bloat breakdown
     │                   │                               │                   │
     └───────────────────┼───────────────────────────────┴───────────────────┘
                         │
                         ▼
             [ GitHub PR Bot Comment ]
      (Block PR if size increases by >500 KB or 
       cold-start regresses by >50 ms)
```

---

## 📦 1. App Size Analysis: DEX, Mach-O & Resource Optimization

### What Emerge Analyzes in Android (AAB/APK):
1. **DEX File Overhead**: Method count, class hierarchy overhead, Kotlin metadata, lambda desugaring costs.
2. **Native Libraries (`.so`)**: C++ unstripped debug symbols, uncompressed native binaries.
3. **Asset & Resource Duplication**: Identifies uncompressed PNGs that should be WebP/VectorDrawables, duplicated strings, and unused localized translations.
4. **Third-Party SDK Blame**: Pinpoints exactly how many kilobytes a new dependency (e.g., Facebook SDK, Stripe SDK) adds to the final download and install size.

### What Emerge Analyzes in iOS (IPA/Mach-O):
1. **__TEXT and __DATA Segments**: Clean dissection of compiler code generation, Swift runtime metadata, and objective-C metadata overhead.
2. **Framework Overhead**: Dynamic vs. Static frameworks (`.dylib` vs. `.a`), dSYM overhead.

---

## ⚡ 2. Startup Analysis on Real Devices

Emulators and synthetic tests fail to measure real-world launch latency due to desktop host CPU power and missing hardware throttling.

### Emerge Lab Architecture:
- Emerge runs your build on **dedicated real Android and iOS hardware devices** in cloud device labs.
- It records CPU instructions, thread scheduling, and binder transactions.
- Produces an interactive **Flame Graph** showing exact method execution times during:
  - **Android**: `Application.attachBaseContext()` -> `Application.onCreate()` -> `Activity.onCreate()` -> **Time to Initial Display (TTID)**.
  - **iOS**: Dynamic linker execution (`dyld`), pre-main framework loading, `AppDelegate.didFinishLaunchingWithOptions` -> First CATransaction draw.

```
Example Emerge Startup Breakdown:
Total Cold Start: 480 ms
├── [dyld framework binding / init]: 120 ms
├── [Application.onCreate]: 210 ms
│   ├── [AnalyticsSDK.init()]: 95 ms  <-- IDENTIFIED BOTTLENECK! (Move to background worker)
│   ├── [Database.warmup()]: 60 ms
│   └── [Config.load()]: 55 ms
└── [First Activity Render / Layout]: 150 ms
```

---

## 💀 3. "Reaper": Dynamic Dead Code Elimination

Traditional tree-shaking (R8 on Android, Dead Code Stripping in Xcode) works via **static analysis**. However, static analysis cannot detect:
- Classes referenced via dynamic reflection.
- Legacy features or screens that are no longer navigated to by users.
- Stale feature flag variants where the code paths are dead but still compiled.

### How Reaper Works:
1. Reaper injects ultra-lightweight bytecode instrumentation into test builds.
2. As test suites and dogfood users navigate the app, Reaper logs which classes and methods are **actually touched**.
3. It cross-references runtime execution against the binary index and generates an automated **PR to delete dead code**.

---

## 🛠️ CI/CD Integration: GitHub Actions

```yaml
# .github/workflows/emerge_analysis.yml
name: Emerge Tools Binary Audit

on:
  pull_request:
    branches: [ main ]

jobs:
  build-and-analyze:
    runs-on: macos-14
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Build Release Bundle (AAB)
        run: ./gradlew :app:bundleRelease

      - name: Upload to Emerge Tools
        uses: EmergeTools/emerge-upload-action@v1
        with:
          api_token: ${{ secrets.EMERGE_API_TOKEN }}
          path: app/build/outputs/bundle/release/app-release.aab
          repo_name: ${{ github.repository }}
          sha: ${{ github.event.pull_request.head.sha }}
          base_sha: ${{ github.event.pull_request.base.sha }}
          pr_number: ${{ github.event.pull_request.number }}
```

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How do you systematically prevent 'App Bloat' across a 100+ engineer mobile organization?"
* **Answer**:
  1. **Enforce Size Budgets in CI/CD**: Integrate Emerge Tools into GitHub Actions with automated threshold checks. If a PR introduces >250 KB without an approved RFC, CI fails automatically.
  2. **Automate Dependency Audits**: Require all third-party SDK additions to undergo an Emerge binary diff evaluation before architecture approval.
  3. **Asset Optimization Pipeline**: Automatically convert PNG/JPEG assets to WebP (Android) or HEIC/PDF vector (iOS) during Gradle/Xcode build phases.
  4. **Dynamic Feature Modules (Play Feature Delivery)**: Move non-critical, heavy modules (e.g., AR camera, customer support chat, onboarding videos) to on-demand downloadable feature modules.

### Q2: "What is the difference between TTID (Time to Initial Display) and TTFD (Time to Full Display), and how do you optimize both?"
* **Answer**:
  - **TTID**: The time from app launch until the user sees the first frame of content (e.g., skeleton screen or cached placeholder). Target: **< 500 ms**.
  - **TTFD**: The time until the screen is fully interactive and populated with fresh server data.
  - **Optimization Strategy**:
    - Never perform synchronous disk I/O, database initialization, or network calls on the main thread during `Application.onCreate`.
    - Defer non-critical SDKs (e.g., ad tracking, social sharing, secondary analytics) using Android App Startup / Jetpack WorkManager or background Task queues.
    - Serve cached disk data immediately on the initial draw frame, then stream network deltas into the UI.
