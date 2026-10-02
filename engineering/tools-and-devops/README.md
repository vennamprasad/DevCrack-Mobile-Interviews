# 🛠️ Mobile Developer Tools, DevOps, Observability & Experimentation

> **The modern mobile platform engineering toolkit: CI/CD automation, network debugging, full-stack observability (Datadog/Sentry), and progressive experimentation (Split.io/Eppo).**

![Tools](https://img.shields.io/badge/Tools-DevOps_%26_Platform-blue?style=for-the-badge)
![Observability](https://img.shields.io/badge/Observability-Datadog_%26_Sentry-purple?style=for-the-badge)
![Flags](https://img.shields.io/badge/Flags-Split.io_%26_Eppo-green?style=for-the-badge)

---

## 📖 Module Catalog

| Category | Guide Hub | Key Topics & Tools |
| :--- | :--- | :--- |
| **Observability & Reliability** | **[Observability Hub](./observability/README.md)** | **[01. Datadog Mobile RUM & APM](./observability/01_datadog_mobile_rum.md)**: W3C distributed tracing, Mobile Vitals, Session Replay.<br>**[02. Sentry Crash & Performance](./observability/02_sentry_crash_and_performance.md)**: Watchdog ANR, breadcrumbs, release health.<br>**[03. Embrace.io Observability](./observability/03_embrace_mobile_observability.md)**: 100% session capture, mystery ANR timeline reconstruction, OOM forensics.<br>**[04. Firebase Crashlytics & Perf](./observability/04_firebase_crashlytics_and_perf.md)**: R8 & NDK symbolication, custom non-fatal error keys, BigQuery streaming. |
| **Feature Delivery & A/B Testing** | **[Experimentation & Flags Hub](./experimentation-and-flags/README.md)** | **[01. Split.io & Feature Flags](./experimentation-and-flags/01_split_io_and_feature_flags.md)**: Instant emergency kill switches, progressive canary rollouts.<br>**[02. Eppo & Statistical Testing](./experimentation-and-flags/02_eppo_and_ab_testing.md)**: Warehouse-native experimentation, CUPED variance reduction.<br>**[03. LaunchDarkly Enterprise](./experimentation-and-flags/03_launchdarkly_enterprise_flags.md)**: Server-Sent Events (SSE) edge streaming, offline caching, circuit breakers.<br>**[04. Statsig Feature Gates](./experimentation-and-flags/04_statsig_modern_feature_gates.md)**: Dynamic configs, pulse health metrics (crash/latency correlation), holdout groups. |
| **Build Systems & Monorepos** | **[Build Systems Hub](./build-systems/README.md)** | **[01. Bazel, Buck2, Develocity & Tuist](./build-systems/01_bazel_and_buck2_monorepos.md)**: Hermetic DAG compilation, Remote Build Caching (RBE), Tuist binary framework caching for iOS, Develocity Predictive Test Selection (PTS), and KSP optimization. |
| **UI Automation & Device Farms** | **[UI Automation Hub](./ui-automation/README.md)** | **[01. Maestro & Cloud Device Farms](./ui-automation/01_maestro_and_device_farms.md)**: Declarative YAML UI testing with Maestro, automated animation tolerance, Firebase Test Lab Robo testing, and 20-device parallel sharding. |
| **Memory & Heap Forensics** | **[Memory & Leaks Hub](./memory-and-leak-detection/README.md)** | **[01. LeakCanary & Memory Profiling](./memory-and-leak-detection/01_leakcanary_and_memory_profiling.md)**: Android GC root tracing, Shark engine `.hprof` analysis, iOS ARC strong retain cycles, and Xcode Memory Graph debugger. |
| **Headless Snapshot Testing** | **[Snapshot Testing Hub](./snapshot-testing/README.md)** | **[01. Paparazzi & Snapshot Testing](./snapshot-testing/01_paparazzi_and_roborazzi.md)**: Headless JVM LayoutLib rendering for Compose/Views, Point-Free SwiftUI testing, dynamic font scaling, and Git LFS golden image workflows. |
| **Binary Optimization & Size** | **[Binary & Performance Hub](./binary-and-performance/README.md)** | **[01. Emerge Tools & Size Optimization](./binary-and-performance/01_emerge_tools_size_and_startup.md)**: DEX / Mach-O size breakdown, real-device startup flamegraphs, Reaper dead-code elimination, and CI size budgets. |
| **Linking & Attribution (MMP)** | **[Linking & Attribution Hub](./linking-and-attribution/README.md)** | **[01. Branch.io & AppsFlyer](./linking-and-attribution/01_branch_and_appsflyer_attribution.md)**: Universal Links, Android App Links, Deferred Deep Linking, MMP last-touch attribution, and Apple SKAdNetwork. |
| **Release Orchestration** | **[Release Management Hub](./release-management/README.md)** | **[01. Runway Release Trains](./release-management/01_runway_mobile_release_trains.md)**: Automated release trains, Apple Phased Releases vs Google Play Staged Rollouts, and stability health gating. |
| **Network Inspection** | **[Network Inspection Hub](./network-inspection/README.md)** | **[01. Proxyman & Chucker](./network-inspection/01_proxyman_and_chucker.md)**: Native macOS proxy, zero-cert Atlantis SDK, on-device Chucker inspection.<br>**[Charles Proxy Hub](./charles/README.md)**: SSL rewrite rules, throttling, and API mocking. |
| **CI / CD Automation** | **[CI/CD & Fastlane Hub](./ci-cd/README.md)** | **[01. CI/CD Pipelines](./ci-cd/01_ci_cd_pipelines.md)**: Runner strategies, caching, secrets management.<br>**[02. Fastlane Deep Dive](./ci-cd/02_fastlane_automation.md)**: Deterministic code signing (`match`), TestFlight deploy (`pilot`), Play Store deploy (`supply`). |
| **Source Control & APIs** | **[Git Hub](./git/README.md)** & **[Postman Hub](./postman/README.md)** | **[01. Advanced Git Guide](./git/01_git_guide.md)**: Interactive rebase, `git bisect`, `git reflog`.<br>**[01. Postman Testing](./postman/01_postman_api_testing.md)**: Collections, environments, and mock servers. |

---

[⬅️ Back to Engineering Overview](../README.md)
