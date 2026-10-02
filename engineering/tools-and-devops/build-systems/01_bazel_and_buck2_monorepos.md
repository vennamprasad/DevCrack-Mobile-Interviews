# 🏗️ Enterprise Mobile Build Systems: Bazel, Buck2, Develocity & Tuist

> **Scaling compilation in large mobile monorepos: Hermetic builds, directed acyclic graphs (DAG), remote build caching, and deterministic project generation.**

---

## 📌 Executive Summary

When a mobile engineering team expands past 50–100 engineers and the codebase exceeds hundreds of modules, **standard Gradle and Xcode build systems hit scalability bottlenecks**:
- Clean builds take **15 to 45 minutes** in CI and on developer laptops.
- Incremental compilation breaks frequently due to non-hermetic tasks, forcing engineers to `./gradlew clean` or delete `DerivedData`.
- iOS teams suffer from perpetual git merge conflicts inside Xcode's `.pbxproj` file.

To solve this, tier-1 tech companies (Google, Meta, Uber, Pinterest, Lyft, Dropbox, Stripe) migrated their mobile codebases to **Bazel**, **Buck2**, or enhanced Gradle with **Develocity (Gradle Enterprise)** and **Tuist**.

---

## 🏗️ The Problem with Standard Mobile Builds

```
Traditional Gradle / Xcode Builds (Imperative & Stateful):
[ Source Files ] ──> [ Gradle Plugin Execution (Arbitrary I/O, Network, System Time) ]
❌ Problem: Build is NOT hermetic! Two identical checkouts can produce different binary hashes.
❌ Problem: Cache invalidation is brittle. One small change re-triggers recompilation of 50 unrelated modules.

Hermetic Build Systems: Bazel / Buck2 (Pure Functional Graph):
Input Hash = Hash(Source Files + Compiler Toolchain + Build Flags)
                              │
                              ▼
[ Action Graph (DAG) ] ──> [ Cache Key Lookup in Remote Cache (S3 / Redis) ]
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
      [ Cache HIT ]                     [ Cache MISS ]
 (Download pre-built .aar / .a     (Compile in sandboxed container,
  in 200ms without compiling!)      upload binary to Remote Cache)
```

---

## ⚡ Bazel & Buck2: Key Principles

### 1. Hermeticity
A build is **hermetic** if it is completely isolated from the host machine:
- It cannot read environment variables, system clocks, or make arbitrary network calls.
- Every compiler (JDK, Android SDK, Clang, Swift toolchain) is checked in or hermetically downloaded as a pinned artifact.
- **Result:** If the inputs match, the binary output is guaranteed to be **byte-for-byte identical**, whether compiled on an M3 MacBook Pro in London or an Ubuntu runner in AWS.

### 2. Distributed Remote Caching & Remote Execution
- **Remote Cache**: When the CI server builds the `main` branch, it pushes all compiled intermediate targets to an S3/GCS remote cache. When a developer pulls `main` locally, **their build time drops by 80–90%** because they download pre-compiled artifacts.
- **Remote Execution (RBE)**: Distributes parallel compilation actions across a farm of thousands of cloud workers, compiling a 2-million-line app in **under 2 minutes**.

---

## 🍎 Tuist: Scaling iOS Modularization

For iOS teams that want compilation acceleration without the extreme overhead of migrating away from Xcode, **Tuist** has become the industry standard.

```
                  [ Project.swift Manifests ]
                              │
                              ▼
                      [ Tuist CLI Engine ]
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
  [ Generates .xcodeproj ]         [ Binary Caching (Cache Warm) ]
 (Zero git merge conflicts;       (Swaps internal source frameworks
  .pbxproj is git-ignored)         for pre-compiled .xcframeworks!)
```

### Tuist `Project.swift` Example:
```swift
import ProjectDescription

let project = Project(
    name: "FeatureCheckout",
    targets: [
        .target(
            name: "FeatureCheckout",
            destinations: .iOS,
            product: .framework,
            bundleId: "com.company.FeatureCheckout",
            sources: ["Sources/**"],
            dependencies: [
                .project(target: "CoreNetwork", path: "../CoreNetwork"),
                .project(target: "DesignSystem", path: "../DesignSystem")
            ]
        )
    ]
)
```
- **Command:** `tuist generate` -> Creates fresh Xcode project in 3 seconds.
- **Command:** `tuist cache warm` -> Compiles all upstream dependencies into binaries so Xcode only compiles the specific file the developer is editing.

---

## 🐘 Develocity (Gradle Enterprise): Modern Android Acceleration

For teams committed to Gradle, **Develocity** adds enterprise caching and intelligence without changing the build system:

1. **Remote Build Cache**: Reuses task outputs across the entire engineering organization.
2. **Predictive Test Selection (PTS)**:
   - Uses machine learning trained on git diff history and code coverage graphs.
   - On a typical PR, instead of running all 10,000 unit tests, PTS identifies and runs **only the ~300 tests impacted by the diff**, slashing CI test suite times from 35 minutes to 4 minutes.
3. **Build Scans**: Deep telemetry detailing task duration, garbage collection pauses, dependency resolution bottlenecks, and cache miss reasons.

---

## ⚖️ Build System Decision Matrix

| Dimension | Standard Gradle / Xcode | Develocity (Gradle Enterprise) | Tuist (iOS) | Bazel / Buck2 |
| :--- | :--- | :--- | :--- | :--- |
| **Migration Cost** | Zero (Default) | Low (Gradle plugin configuration) | Medium (Write `Project.swift`) | **Extremely High** (Months of dedicated infra team effort) |
| **Monorepo Scale** | Poor (>50 devs) | Good (Up to 200 devs) | Excellent for iOS | **Unlimited (Used by Google/Meta at 10,000+ devs)** |
| **Remote Cache** | Local only | Enterprise cloud cache | Binary framework cache | **Full distributed RBE & Cache** |
| **Hermeticity** | No | Partial | No | **Strict 100% Hermetic** |
| **IDE Integration** | Seamless (Android Studio / Xcode) | Seamless | Native Xcode | Requires specialized IDE plugins (Tulsi / Bazel plugin) |

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How would you diagnose and fix a 30-minute mobile CI build bottleneck in a growing startup?"
* **Answer**:
  1. **Phase 1: Instrumentation & Build Profiling**: Run a Gradle Build Scan or Xcode build timing summary (`-showBuildTimingSummary`) to identify the top 5 longest-running tasks (usually annotation processing/KAPT, code shrinking/R8, or bloated test suites).
  2. **Phase 2: Quick Wins**:
     - Migrate legacy KAPT (Kotlin Annotation Processing Tool) to **KSP (Kotlin Symbol Processing)**, which speeds up Room/Moshi/Dagger compilation by 2x–4x.
     - Enable Gradle Configuration Cache (`org.gradle.configuration-cache=true`).
     - Separate unit tests from instrumented emulator tests.
  3. **Phase 3: Caching & Modularization**:
     - Split large monolith modules into decoupled feature modules with clear API/implementation boundaries.
     - Implement Remote Build Caching so PR builds only compile modified modules.

### Q2: "What is the difference between an API dependency and an Implementation dependency in Gradle, and how does it affect incremental compilation?"
* **Answer**:
  - `implementation`: Internal to the module. If Module B changes internal code, Module A **does not need to recompile**.
  - `api`: Leaks transitively into the consumer's compile classpath. If Module B changes an `api` dependency, **Module A and all downstream consumers must be completely recompiled**.
  - **Rule**: Always default to `implementation` to maximize build cache hits and minimize DAG re-evaluation.
