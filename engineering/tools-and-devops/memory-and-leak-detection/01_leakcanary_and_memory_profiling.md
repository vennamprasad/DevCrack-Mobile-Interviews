# 🧠 Mobile Memory Leak Detection & Heap Forensics: LeakCanary & Instruments

> **Diagnosing and eliminating mobile memory leaks: In-app heap analysis with LeakCanary (Shark engine), ARC strong reference cycles, and Xcode Memory Graph profiling.**

---

## 📌 Executive Summary

Memory leaks in mobile applications are silent killers:
1. They degrade frame rates by forcing the Garbage Collector (GC) to run constantly (**GC thrashing**).
2. They retain entire Activities, ViewControllers, ViewModels, and Bitmaps in memory.
3. Eventually, the operating system (Android Low Memory Killer or iOS Jetsam) terminates the process with an uncatchable **Out-Of-Memory (OOM) SIGKILL**.

To ensure app stability, engineers use **LeakCanary** on Android to automatically catch leaks during development and **Xcode Instruments / Memory Graph Debugger** on iOS.

---

## 🔬 How Memory Leaks Occur: Android GC vs. iOS ARC

```
Android (Tracing Garbage Collection):
[ GC Root (e.g., Static Singleton / Main Thread) ]
                     │
                     ▼ (Strong Reference)
             [ Async Background Task ]
                     │
                     ▼ (Leaked Inner Class Reference)
         [ Leaked Activity (Destroyed) ] ──> Retains 80 MB Bitmap Heap!
❌ Result: Even after onDestroy(), GC cannot reclaim the Activity because a path to GC Root exists.

iOS (Automatic Reference Counting - ARC):
[ ViewController ] ──(Strong Reference)──> [ Closure / Delegate ]
       ▲                                            │
       └──────────────(Strong Reference)────────────┘
❌ Result: Retain Cycle! Reference count never reaches 0. Memory is permanently leaked.
```

---

## 🐤 LeakCanary Internals: How Square Solved Android Leaks

You do not need to write code to start LeakCanary; it automatically hooks into the Android Application lifecycle using an internal `ContentProvider`:

```kotlin
// build.gradle.kts (Debug Only!)
dependencies {
    // Zero lines of setup code needed!
    debugImplementation("com.squareup.leakcanary:leakcanary-android:2.14")
}
```

### The 4-Step LeakCanary Detection Pipeline:
1. **Object Watching**: When an `Activity.onDestroy()`, `Fragment.onDestroyView()`, or `ViewModel.onCleared()` fires, LeakCanary wraps the instance in a `KeyedWeakReference` tied to a `ReferenceQueue`.
2. **Garbage Collection Trigger**: LeakCanary waits 5 seconds, triggers an explicit GC (`Runtime.getRuntime().gc()`), and checks if the weak reference was cleared.
3. **Heap Dump (`.hprof`)**: If the object is still in memory after GC, it is marked as a **retained object**. Once 5 retained objects accumulate (or the app is backgrounded), LeakCanary dumps the memory heap into an `.hprof` file.
4. **Shark Engine Analysis**: The **Shark** analyzer parses the `.hprof` binary file directly on the phone, finds the leaking object, and finds the **shortest path to a GC Root**.

### Reading a LeakCanary Leak Trace

```
┬───
│ GC Root: Global JNI / Static field
│
├─ com.example.analytics.AnalyticsManager instance
│    ↓ AnalyticsManager.listener
├─ com.example.feature.CheckoutActivity$listener$1 instance
│    ↓ CheckoutActivity$listener$1.this$0 (anonymous inner class)
╰→ com.example.feature.CheckoutActivity instance
​     Leaking: YES (Activity.mDestroyed is true and Activity.mFinished is true)
​     Retaining 42.8 MB (Bitmap cache inside Activity)
```
**The Fix:** Unregister the listener in `onDestroy()` or pass an `Application` Context instead of the `Activity` Context to singletons!

---

## 🍎 iOS Memory Profiling: Xcode Memory Graph & Instruments

On iOS, memory leaks are almost exclusively caused by **retain cycles** where two objects hold strong references to each other.

```swift
// Leaky Pattern (Strong Reference in Closure)
class ProductViewModel {
    var onPriceUpdated: (() -> Void)?
    var price: Double = 100.0

    func bind() {
        // Leaks 'self' because closure captures 'self' strongly!
        self.onPriceUpdated = {
            print("Price changed: \(self.price)")
        }
    }
}

// Clean Pattern (Weak Capture List)
class ProductViewModelClean {
    var onPriceUpdated: (() -> Void)?
    var price: Double = 100.0

    func bind() {
        self.onPriceUpdated = { [weak self] in
            guard let self = self else { return }
            print("Price changed: \(self.price)")
        }
    }
}
```

### Profiling Tools in Xcode:
1. **Memory Graph Debugger**: Press the three-node graph icon in Xcode's debug bar. It visualizes the object reference graph and displays a purple exclamation mark next to detected retain cycles.
2. **Instruments -> Allocations**: Tracks "Dirty Memory" (memory that cannot be paged out by the OS). If dirty memory steadily climbs without dropping after popping a screen, you have an allocation leak.
3. **Instruments -> Leaks**: Periodically scans the heap to find allocated blocks of memory that have zero active pointers pointing to them.

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How does LeakCanary differentiate between a transient object that is waiting to be garbage collected and a genuine memory leak?"
* **Answer**:
  - LeakCanary uses `WeakReference` and `ReferenceQueue`.
  - When an Activity is destroyed, it is wrapped in a `KeyedWeakReference` associated with a `ReferenceQueue`.
  - Under normal circumstances, during the next GC cycle, the garbage collector clears the weak reference and enqueues it onto the queue.
  - LeakCanary polls the `ReferenceQueue` after a 5-second grace period. If the weak reference is **not** in the queue, LeakCanary triggers a forced GC. If the object remains uncollected after forced GC, it is definitively classified as a **retained leak**.

### Q2: "Why should LeakCanary NEVER be included in a release production build, and how do you enforce this in CI?"
* **Answer**:
  1. **Performance & UX Catastrophe**: Dumping a 500 MB heap (`Debug.dumpHprofData`) pauses the JVM completely for 2 to 6 seconds, freezing the UI and triggering user-perceived ANRs.
  2. **Storage Exhaustion**: Repeated `.hprof` files will quickly consume all user storage on low-end devices.
  3. **Security Risk**: A heap dump contains plaintext user credentials, session auth tokens, and decrypted credit card numbers residing in JVM memory.
  4. **Enforcement**: Include it strictly via `debugImplementation` in Gradle, and add an automated CI check asserting that `com.squareup.leakcanary` does not exist in the release dependency graph (`./gradlew app:dependencies --configuration releaseRuntimeClasspath`).
