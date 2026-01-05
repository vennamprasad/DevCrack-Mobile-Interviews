# 🦄 Kotlin Multiplatform (KMP/KMM) Interview Questions
*(Targeted for Senior Android Developer / Team Lead Roles)*

## ✅ Section 1 — Core Concepts & Architecture

### 1. Philosophy & Basics

**Q: Contrast KMP (KMM) vs Flutter vs React Native.**
*   **Flutter/RN:** "Write Once, Run Anywhere". Shared Logic + **Shared UI**. You render your own canvas (Flutter) or map to native widgets (RN).
*   **KMP:** "Shared Logic, **Native UI**". You share the business logic (Networking, Database, ViewModels) but write 100% native UI (Jetpack Compose for Android, SwiftUI/UIKit for iOS).
*   *Advantage:* Zero compromise on UI/UX. No "uncanny valley". Deep platform integration is seamless.
*   *Disadvantage:* You still have to write the UI twice.

**Q: KMM vs KMP?**
*   **KMM (Kotlin Multiplatform Mobile):** A subset of KMP focused specifically on iOS and Android sharing. (Google deprecated the "KMM" term in favor of just "Kotlin Multiplatform" but it is still widely used in job descriptions).
*   **KMP (Kotlin Multiplatform):** The broad technology that targets JVM, JS, Native (iOS/Mac/Windows/Linux), and Wasm.

**Q: Explain the `expect` / `actual` mechanism.**
The core building block of platform-specific code.
*   **Common Source:** You define a signature `expect fun getPlatformName(): String`.
*   **Android Source:** You provide the specific implementation: `actual fun getPlatformName() = "Android"`.
*   **iOS Source:** You provide the specific implementation: `actual fun getPlatformName() = UIDevice.currentDevice.systemName()`.
*   *Note:* In strict hexagonal architecture, prefer defining an `interface` in common code and implementing it in native modules via Dependency Injection (Koin) to avoid checking `expect` classes everywhere.

### 2. Compilation & Binaries

**Q: How does KMP run on iOS?**
*   **Kotlin/Native Compiler (LLVM):** Compiles Kotlin code into native machine code (ARM64/X64).
*   **Output:** Generates an **Apple Framework** (`.framework`) containing the binary and an Objective-C Header file (`.h`).
*   **Integration:** Xcode links this framework just like any other 3rd party ObjC/Swift library. Swift calls the ObjC headers (Interop).

**Q: What is `cinterop`?**
A tool that allows Kotlin/Native to interact with C/Objective-C libraries. It generates Kotlin bindings for C headers, allowing you to call C APIs directly from Kotlin code.

---

## ✅ Section 2 — Memory & Concurrency (Critical)

### 3. Memory Management

**Q: Explain the "Old" vs "New" Memory Manager.**
*   **Old (Strict):** Objects were "Frozen" (immutable) if shared between threads. Sending a mutable object to another thread caused `InvalidMutabilityException`. This was the biggest pain point of KMM.
*   **New (Default since Kotlin 1.7.20):** Uses a Tracing Garbage Collector in Kotlin/Native.
    *   Allows mutable objects to be shared across threads (like in JVM).
    *   Removes the need for `freeze()`.
    *   Matches typical developer expectations from Java/Kotlin.

### 4. Concurrency

**Q: How do Coroutines work on iOS?**
*   Since the New Memory Manager, usage is seamless.
*   **Main Dispatcher:** Maps to `dispatch_get_main_queue()` (GCD) on iOS.
*   **IO/Default Dispatcher:** Maps to background GCD queues.
*   **Collecting Flows in Swift:** Use libraries like **SKIE** (Syndi KMP Interop Extensions) or write a wrapper class (`CommonFlow`) to expose a callback or Swift-friendly async/await function, as pure Kotlin `suspend` functions compile to ObjC completion handlers (blocks) which can be clunky.

---

## ✅ Section 3 — Ecosystem & Project Structure

### 5. Libraries

**Q: What is the "Holy Trinity" of KMP libraries?**
To share as much as possible, you need Multiplatform libraries:
1.  **Networking:** Ktor (uses OkHttp on Android, NSURLSession on iOS).
2.  **Database:** SQLDelight (Generates type-safe Kotlin APIs from SQL).
3.  **Serialization:** `kotlinx.serialization` (JSON parsing).
*   *Dependency Injection:* **Koin** (Service Locator) is the standard. Hilt/Dagger works only on Android. **Kodein** is another option.

### 6. Project Setup

**Q: Explain the SourceSets.**
*   `commonMain`: Pure Kotlin. No `java.*` or `android.*` imports allowed. All business logic lives here.
*   `androidMain`: Access to Android SDK (`Context`, `Activity`).
*   `iosMain`: Access to iOS SDK (`UIKit`, `Foundation` via Kotlin/Native bindings).

---

## ✅ Section 4 — Real-World Scenario

### 7. Challenges

**Q: How do you handle Swift-only APIs (like SwiftUI or Combine)?**
Kotlin/Native generates Objective-C headers, not Swift.
*   **Generics:** ObjC generics are lightweight, so complex Kotlin types maps to `id` (Any) or lose strict typing in Swift.
*   **Sealed Classes:** Mapped to ObjC classes, requiring ugly casting in Swift switches.
*   **Solution:** Use **SKIE** (plugin) to generate real Swift enums and async/await bindings, strictly improving the Swift developer experience.

**Q: How do you Debug iOS crashes in Kotlin code?**
*   Use `dSYM` files generated by the Kotlin compiler to symbolicate stack traces in Crashlytics.
*   Use the **Kotlin Multiplatform Mobile** plugin in Android Studio to run/debug the iOS app directly with break points in Kotlin code.

**Q: Best practice for ViewModels?**
*   **Old Way:** Wrapper class in Swift calling Kotlin logic.
*   **New Way (Recommended):** Share the ViewModel in `commonMain` (using libraries like **Voyager** or **Decompose** or strict MVVM). The iOS View (`struct View`) observes the Shared ViewModel's `StateFlow`.
