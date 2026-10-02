# 🔬 Perfetto System Tracing & Performance Profiling Mastery

> **The definitive Senior & Staff Android Engineer guide to system tracing, frame jank diagnostics, kernel scheduling, and SQL-powered performance analysis with Perfetto.**

![Perfetto](https://img.shields.io/badge/Profiler-Perfetto-FF5722?style=for-the-badge&logo=google&logoColor=white)
![Android](https://img.shields.io/badge/Platform-Android_10_--_15+-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Tracing](https://img.shields.io/badge/Engine-ftrace_%26_atrace-blue?style=for-the-badge)
![Level](https://img.shields.io/badge/Target-Senior_%2F_Staff_%2F_Architect-purple?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Why Perfetto? The Heisenberg Effect in Profiling](#1-why-perfetto-the-heisenberg-effect-in-profiling)
- [2. System Architecture & Internals](#2-system-architecture--internals)
- [3. Key Android Tracks to Inspect](#3-key-android-tracks-to-inspect)
- [4. Instrumenting Code: Java, Kotlin, Native NDK, and Compose](#4-instrumenting-code)
- [5. How to Capture Traces (CLI, Web UI, On-Device, Macrobenchmark)](#5-how-to-capture-traces)
- [6. The Superpower: Querying Traces with SQL](#6-the-superpower-querying-traces-with-sql)
- [7. Real-World Case Studies & Diagnostics](#7-real-world-case-studies)
- [8. High-Frequency Staff Interview Questions & Answers](#8-high-frequency-staff-interview-questions)

---

## 1. Why Perfetto? The Heisenberg Effect in Profiling

Traditional CPU profilers (like Java Sampling or Method Tracing in Android Studio) suffer from the **Heisenberg Effect**: *the act of observing the system alters its performance*.
- **Method Tracing:** Injects instrumentation hooks into every method entrance and exit, introducing up to **5x–10x slowdown**. A 2ms function suddenly takes 15ms, creating fake jank and distorting thread race conditions.
- **Sampling Profilers:** Pause threads periodically to inspect the call stack, missing micro-jank events that occur between samples.

### Enter Perfetto
Introduced in Android 9 and standard in Android 10+, **Perfetto** operates at the Linux kernel level via `ftrace` and userspace `atrace`.
- **Zero-Copy Architecture:** Data buffers are written to shared memory pages mapped between kernel and userspace daemons.
- **Microsecond Precision:** Records exact hardware VSYNC timings, context switches, and CPU clock frequencies.
- **Ultra-Low Overhead (< 1% CPU):** Safe to run in production benchmarking and complex user flows without degrading frame rate.

---

## 2. System Architecture & Internals

```
┌─────────────────────────────────────────────────────────────┐
│                       Your Android App                      │
│   androidx.tracing (userspace atrace tag: /sys/.../trace_marker) │
└──────────────────────────────┬──────────────────────────────┘
                               │ POSIX write()
┌──────────────────────────────▼──────────────────────────────┐
│                    Linux Kernel (ftrace)                     │
│   - CPU Scheduler (sched_switch, sched_wakeup)              │
│   - CPU Frequency (cpu_frequency, cpu_idle)                 │
│   - Hardware Clocks & IRQs                                  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Ring Buffer (Zero-Copy)
┌──────────────────────────────▼──────────────────────────────┐
│                  Perfetto Daemons (Native C++)               │
│   - traced_probes (Collects kernel ftrace + sysfs metrics)  │
│   - traced (Central daemon managing shared memory pages)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ Compact Protocol Buffer (.pftrace)
┌──────────────────────────────▼──────────────────────────────┐
│            Analysis: ui.perfetto.dev / trace_processor      │
│            SQLite Query Engine + WebGL Timeline Renderer    │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Key Android Tracks to Inspect

When opening a `.perfetto-trace` in [ui.perfetto.dev](https://ui.perfetto.dev), prioritize these tracks:

### A. UI Thread (`main` / `tid == pid`)
- **`Choreographer#doFrame`:** Triggered by VSYNC. Must complete its pipeline within **16.6ms (60 FPS)** or **8.3ms (120 FPS)**.
  - Phase 1: `input` (Touch event processing).
  - Phase 2: `animation` (ValueAnimator evaluation).
  - Phase 3: `traversal` (`measure`, `layout`, `draw` passes).

### B. `RenderThread`
- Compiles Canvas draw operations into GPU display lists and handles Vulkan/OpenGL ES commands:
  - `syncFrameState`: Synchronizes UI thread view tree properties with render thread data.
  - `DrawFrame`: Submits GPU draw packets to the driver queue.
  - *Symptom:* If the UI thread completes in 3ms, but `RenderThread` takes 22ms, your bottleneck is complex draw shaders, excessive overdraw, or large bitmaps—not CPU business logic.

### C. SurfaceFlinger & Hardware Composer (HWC)
- The system compositor. Confirms whether the rendered buffer was actually presented to the physical screen hardware or dropped (`BufferQueue` exhaustion).

### D. CPU Scheduling & Core Allocation
- Shows exactly which CPU core ran your thread.
- **Big.LITTLE Architecture:** Reveals if the OS scheduler throttled your UI thread onto a low-power, weak "LITTLE" efficiency core due to high battery temperature or CPU load.

---

## 4. Instrumenting Code

### A. Kotlin / AndroidX Tracing (Recommended)
Include dependency:
```kotlin
// build.gradle.kts
implementation("androidx.tracing:tracing-ktx:1.2.0")
```

Wrap critical code blocks:
```kotlin
import androidx.tracing.trace

fun processOrderFeed(orders: List<Order>) {
    trace("OrderFeed:Process") {
        val filtered = trace("OrderFeed:Filter") {
            orders.filter { it.isValid }
        }
        updateUI(filtered)
    }
}
```

### B. Asynchronous Tracing
When work spans across multiple coroutines or background threads:
```kotlin
import androidx.tracing.Trace

val cookie = orderId.hashCode()

fun startNetworkRequest(orderId: String) {
    Trace.beginAsyncSection("FetchOrderData", cookie)
    apiService.getOrder(orderId) { result ->
        Trace.endAsyncSection("FetchOrderData", cookie)
    }
}
```

### C. Jetpack Compose Recomposition Tracing
Enable automatic tracking of Composable recomposition timelines in Perfetto:
```kotlin
// build.gradle.kts
implementation("androidx.compose.runtime:runtime-tracing:1.7.0")
```
When recorded with Macrobenchmark, Composable functions appear directly on the timeline with recomposition counts and skip statistics!

### D. Native C++ NDK Code
```cpp
#include <android/trace.h>

void processImageFrame() {
    ATrace_beginSection("NDK_ProcessImageFrame");
    // CPU-heavy image filter
    ATrace_endSection();
}
```

---

## 5. How to Capture Traces

### Method 1: Web Browser UI (Easiest)
1. Open Chrome and navigate to **[ui.perfetto.dev](https://ui.perfetto.dev)**.
2. Connect your Android device via USB (`adb devices` must see it).
3. Click **Record new trace** -> Target: **Android device**.
4. Select presets: **Rendering & UI**, **CPU frequency**, **Memory**.
5. Click **Start Recording**, reproduce the bug on your phone, then click **Stop**.

### Method 2: Command Line (Production / Automation)
Run Google's standalone Python trace recorder:
```bash
# Record 10 seconds of rendering, scheduling, and view updates
curl -O https://raw.githubusercontent.com/google/perfetto/master/tools/record_android_trace

python3 record_android_trace -o trace_output.pftrace -t 10s -b 64mb \
    sched freq am wm gfx view binder_driver
```

### Method 3: Macrobenchmark + Baseline Profiles
```kotlin
@RunWith(AndroidJUnit4::class)
class StartupBenchmark {
    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun startupCold() = benchmarkRule.measureRepeated(
        packageName = "com.example.app",
        metrics = listOf(StartupTimingMetric(), FrameTimingMetric()),
        compilationMode = CompilationMode.Partial(),
        iterations = 5,
        setupBlock = { pressHome() }
    ) {
        startActivityAndWait()
    }
}
```

---

## 6. The Superpower: Querying Traces with SQL

Perfetto contains an embedded SQLite database engine called `trace_processor`. You can query billions of nanosecond metrics with declarative SQL in the Web UI:

### Query 1: Find the 10 Longest Frames on the UI Thread
```sql
SELECT
  ts / 1e6 AS start_ms,
  dur / 1e6 AS duration_ms,
  name
FROM slice
WHERE name LIKE '%Choreographer#doFrame%'
ORDER BY dur DESC
LIMIT 10;
```

### Query 2: Identify Synchronous Binder Calls Blocking Main Thread
Synchronous IPC to system servers (`PackageManager`, `LocationManager`, `WindowManager`) blocks the UI thread:
```sql
SELECT
  s.name,
  s.dur / 1e6 AS duration_ms,
  t.name AS thread_name
FROM slice s
JOIN thread_track tt ON s.track_id = tt.id
JOIN thread t ON tt.utid = t.utid
WHERE s.name LIKE 'binder transaction'
  AND t.name = 'com.example.app'
  AND s.dur > 5000000 -- More than 5ms
ORDER BY s.dur DESC;
```

### Query 3: Measure Exact App Startup Time (`reportFullyDrawn`)
```sql
SELECT
  name,
  dur / 1e6 AS duration_ms
FROM slice
WHERE name LIKE 'ActivityManager:reportFullyDrawn%'
LIMIT 1;
```

---

## 7. Real-World Case Studies

### Case 1: The "Mysterious" RecyclerView Jitter
- **Symptom:** Fast fling scrolling drops 8–10 frames consecutively.
- **Perfetto Investigation:**
  - UI Thread showed repeated `RV CreateView` taking **14ms** each inside `doFrame`.
  - Zooming in revealed an XML inflation parse of a deeply nested `LinearLayout` with weights.
- **Fix:** Switched item layout to a flat `ConstraintLayout`, enabled item prefetching, and shared `RecycledViewPool` across nested tabs. Dropped `doFrame` from 28ms to 3.2ms.

### Case 2: Accidental Disk I/O on Main Thread via SharedPreferences
- **Symptom:** Startup jank during splash screen.
- **Perfetto Investigation:**
  - UI Thread was in `UNINTERRUPTIBLE_SLEEP` (marked as `D` state in Linux scheduler).
  - Slice stack showed `SharedPreferencesImpl.getString()` waiting on `mLock` while another thread was writing a 2MB JSON string to disk.
- **Fix:** Migrated to asynchronous **Jetpack DataStore** running on `Dispatchers.IO`.

---

## 8. High-Frequency Staff Interview Questions

### Q1: What is the difference between Systrace and Perfetto?
> **Answer:** Systrace is a legacy Python tool that read from `/sys/kernel/debug/tracing` and output large HTML files. Perfetto is a modern C++ platform using shared-memory ring buffers, Protocol Buffers (`.pftrace`), and an integrated SQLite analysis engine (`trace_processor`). Perfetto has vastly lower overhead (< 1% CPU vs 5-15%), records longer sessions, and supports native heap memory profiling (`heapprofd`).

### Q2: Why might a frame drop even if `Choreographer#doFrame` took only 4ms?
> **Answer:** Frame rendering is a two-stage pipeline. The UI thread prepares display lists during `doFrame` (Stage 1), but the **`RenderThread`** must submit those commands to the GPU driver via OpenGL/Vulkan (Stage 2). If the RenderThread blocks on shader compilation, GPU buffer swapping (`eglSwapBuffers`), or texture uploads, the frame will miss the VSYNC deadline and drop, regardless of how fast the UI thread was.

### Q3: How do you detect thread lock contention in Perfetto?
> **Answer:** In the CPU slice track, inspect the thread state. If a thread is in state `S` (Sleeping) or `D` (Disk/I/O Sleep) during an active frame, click the slice to see the **Wakeup from** event. Perfetto highlights the exact thread that was holding the lock and which line awoke your blocked thread.

### Q4: How does Perfetto integrate with Jetpack Compose?
> **Answer:** With `androidx.compose.runtime:runtime-tracing`, the Compose compiler injects tracing markers around `@Composable` functions. When profiled in Perfetto, developers can see individual Composable evaluations on the timeline, identifying unwanted recomposition cascades, missed memoization (`remember`), and unstable parameter re-evaluations.
