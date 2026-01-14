# 🚀 Android Performance Mastery: 50+ Interview Questions

> **Target Audience:** Senior/Staff Android Engineers.
> **Scope:** Memory, Battery, Networks, Startup, and Rendering.

![Performance](https://img.shields.io/badge/Android-Performance-orange?style=for-the-badge&logo=android)

---

## 📖 Table of Contents
- [Level 1: Memory Management (1-10)](#level-1-memory-management)
- [Level 2: UI Rendering (11-20)](#level-2-ui-rendering)
- [Level 3: App Startup (21-30)](#level-3-app-startup)
- [Level 4: Network & Battery (31-40)](#level-4-network--battery)
- [Level 5: Tools & Profiling (41-50)](#level-5-tools--profiling)
- [Level 6: Real-World Scenarios (51+)](#level-6-real-world-scenarios)

---

## Level 1: Memory Management

### Q1. What is the difference between Dalvik and ART memory models?
**Answer:**
*   **Dalvik**: Used JIT (Just-In-Time). Garbage Collection (GC) was "stop-the-world" and caused visible stutters.
*   **ART (Android Runtime)**: Uses AOT (Ahead-Of-Time) compilation. improved GC (Concurrent Mark Sweep) which minimizes pauses. Allocations are faster (Thread-Local Allocation Buffer).

### Q2. Explain "Memory Churn".
**Answer:**
Rapidly allocating and deallocating objects in a short loop (e.g., inside `onDraw()`).
*   **Effect**: Triggers frequent GC events.
*   **Result**: CPU spikes, dropped frames (Jank).

### Q3. How does `LeakCanary` work internally?
**Answer:**
1.  Hooks into `Activity.onDestroy()`.
2.  Waits 5 seconds, then forces a GC.
3.  Checks if the Activity implementation is still held in memory (using `WeakReference`).
4.  If yes, it dumps the Java Heap (hprof), analyzes it with "Shark", and finds the GC Root holding the reference.

### Q4. WeakReference vs SoftReference vs PhantomReference?
**Answer:**
1.  **Strong**: Normal assignment (`val x = Obj()`). Never collected.
2.  **Soft**: Collected only if JVM is running low on memory. (Good for caching).
3.  **Weak**: Collected eagerly on the next GC event. (Good for avoiding leaks in Listeners/Handlers).
4.  **Phantom**: Enqueued when object is finalized. Used for scheduling cleanup actions.

### Q5. What is a "Bitmap Pool"?
**Answer:**
Reusing Bitmap memory to avoid allocation cost.
*   **Why**: Bitmaps are large. Allocating them forces OS to find contiguous memory blocks.
*   **How**: Use `BitmapFactory.Options.inBitmap` to recycle an existing bitmap's memory for a new image of the same size.

---

## Level 2: UI Rendering

### Q6. How does Android render a frame? (The Pipeline)
**Answer:**
1.  **Measure**: View determines its size.
2.  **Layout**: View determines its position.
3.  **Draw**: View generates display lists.
4.  **Sync**: CPU sends data to GPU.
5.  **Rasterize**: GPU turns primitives into pixels.
6.  **Composite**: SurfaceFlinger combines layers.

### Q7. What is "Overdraw"? How to debug it?
**Answer:**
Painting the same pixel multiple times in a single frame (e.g., Background color + Card color + Image + Text).
*   **Debug**: "Debug GPU Overdraw" in Developer Options.
    *   **Blue**: 1x
    *   **Green**: 2x
    *   **Pink**: 3x
    *   **Red**: 4x+ (Bad)

### Q8. Why is `ConstraintLayout` better for performance than nested `LinearLayouts`?
**Answer:**
`ConstraintLayout` flattens the view hierarchy.
Nested layouts cause "Exponential Measurement" (Parent triggers measure called on Child, Child triggers measure on Parent). Flat hierarchy = Single pass.

### Q9. What is `Choreographer`?
**Answer:**
The coordinator of the UI loop. It listens to VSYNC signals (hardware refresh). When VSYNC triggers, Choreographer tells the main thread to run `doFrame()` (Input -> Animation -> Traversal).

### Q10. Why should you never block the Main Thread?
**Answer:**
Android targets 60 FPS (16.6ms per frame). If Main Thread works for >16ms, the frame is dropped ("Jank"). The user sees a stutter.

---

## Level 3: App Startup

### Q11. Cold Start vs Warm Start vs Hot Start?
**Answer:**
*   **Cold**: App process is dead. OS creates process -> Initialize objects -> Layout -> Draw. (Slowest).
*   **Warm**: Process exists, but Activity needs recreation (e.g., Back navigation).
*   **Hot**: Activity is in memory, just brought to foreground (Fastest).

### Q12. How to optimize Cold Start time?
**Answer:**
1.  **Lazy Load**: Don't initialize everything in `Application.onCreate()`. Use Dagger `Lazy<>` or Startup Library.
2.  **ViewStub**: Inflate UI hierarchies only when needed.
3.  **Baseline Profiles**: Pre-compile critical paths (AOT) to avoid JIT cost on first run.

### Q13. What is "Baseline Profile"?
**Answer:**
A dictionary of classes/methods stored in `assets/dexopt/baseline.prof`. Google Play installs this immediately. The OS compiles these methods to machine code *during installation*, speeding up the first launch by 30-40%.

### Q14. How to detect Slow Startup?
**Answer:**
*   **Logcat**: Look for `Displayed` tag: `ActivityManager: Displayed com.example/.MainActivity: +850ms`.
*   **Android Vitals**: Google Play Console dashboard.

---

## Level 4: Network & Battery

### Q15. How does `JobScheduler` / `WorkManager` save battery?
**Answer:**
They "batch" requests. Instead of waking up the radio 10 times for 10 apps, the OS wakes it up once and lets all apps sync data together. This reduces "Radio Active State" drain.

### Q16. What is "Doze Mode"?
**Answer:**
If the device is stationary and screen-off for a while:
*   Network access is restricted.
*   Syncs/Jobs are deferred.
*   Wakelocks are ignored.
*   Maintenance windows occur periodically to allow batch processing.

### Q17. GZIP vs Brotli?
**Answer:**
Compression algorithms for network responses.
*   **GZIP**: Standard.
*   **Brotli**: Google's algorithm. 15-20% better compression than GZIP. Supported by OkHttp.

### Q18. Protocol Buffers vs JSON?
**Answer:**
*   **JSON**: Human readable, text-based. Large payload size. Parsing is CPU intensive.
*   **Protobuf**: Binary, compact. Smaller size. Faster serialization/deserialization. Use for high-performance configs.

---

## Level 5: Tools & Profiling

### Q19. `Systrace` vs `Perfetto`?
**Answer:**
*   **Systrace**: Older tool. Python script wrapping `atrace`.
*   **Perfetto**: New standard (Android 10+). Web-based UI (`ui.perfetto.dev`). Can trace kernel scheduling, CPU frequency, and userspace annotations.

### Q20. What is "StrictMode"?
**Answer:**
A developer tool that detects accidental Header/Disk operations on the Main Thread.
```kotlin
StrictMode.setThreadPolicy(StrictMode.ThreadPolicy.Builder()
    .detectDiskReads()
    .detectDiskWrites()
    .detectNetwork()
    .penaltyLog()
    .build())
```

### Q21. Use cases for "Profile GPU Rendering" bars?
**Answer:**
Visual bars on screen showing how much time each frame took. Horizontal line = 16ms target.
Spike in "Measure/Layout" (Green) = Complexity in Views.
Spike in "Process" (Red) = Main thread busy logic.

---

## Level 6: Real-World Scenarios

### Q51. User reports App freezes when scrolling a huge list of images.
**Debug:**
Likely doing Bitmap decoding on Main Thread or frequent GC.
**Fix:**
1.  Check `onBindViewHolder`. Is it loading images synchronously?
2.  Use Glide/Coil.
3.  Check if `setItemViewCacheSize` helps.
4.  Run Profiler -> "Memory" -> Check for allocation spikes.

### Q52. Battery Historian shows "Wake Lock" held for 4 hours.
**Debug:**
App kept CPU awake preventing deep sleep.
**Fix:**
Search code for `PowerManager.WakeLock`. Ensure `release()` is called in `finally` block. Replace with `WorkManager` where possible.

### Q53. App takes 5 seconds to show the first screen, but only on low-end devices.
**Debug:**
Heavy initialization in `Application.onCreate`. High CPU contention.
**Fix:**
Use `androidx.startup`. Offload non-critical SDK inits (Analytics, Crashlytics) to a background thread or initialize lazily.

### Q54. "ANR" (Application Not Responding) happens randomly.
**Debug:**
Main thread blocked for 5+ seconds.
**Fix:**
Pull `traces.txt` from the device. Look for "main" thread state.
*   **Waiting**: Deadlock?
*   **Native**: Stuck in heavy calculation?
*   **Binder**: Waiting for IPC (Inter-Process Communication) from another app?
