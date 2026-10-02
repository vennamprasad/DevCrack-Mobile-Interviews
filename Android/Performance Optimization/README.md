# ⚡ Android Performance Engineering & Optimization

> **Comprehensive guide to diagnosing and fixing memory leaks, dropped frames (jank), slow app startup, battery drain, and network bloat.**

![Performance](https://img.shields.io/badge/Performance-Optimization-green?style=for-the-badge&logo=speedtest)
![Memory](https://img.shields.io/badge/Memory-Leak_Detection-red?style=for-the-badge)
![Profiling](https://img.shields.io/badge/Profiling-Perfetto_%26_Studio-blue?style=for-the-badge)

---

## 📖 Module Contents

| Guide | Description | Key Focus Areas |
| :--- | :--- | :--- |
| **[01. Android Performance Q&A](./performance.md)** | Core interview questions on performance essentials. | Key focus areas, memory leak detection, View hierarchy optimization, background battery drain, and network batching. |
| **[02. Performance Mastery (50+ Questions)](./performance_mastery.md)** | Deep-dive staff-level performance question bank. | **Memory:** GC churn, bitmap pools, native leaks, heap dumps.<br>**UI & Rendering:** Choreographer, VSYNC, GPU overdraw, Compose recomposition skipping.<br>**Startup:** Cold/Warm/Hot start, Baseline Profiles, App Startup library.<br>**Network & Battery:** Radio state machine, Doze mode, WorkManager constraints.<br>**Tools:** Perfetto, Systrace, Android Studio Memory/CPU Profiler. |

---

## 🎯 The Performance Core Checklist

1. **App Startup Optimization:**
   - Implement **Baseline Profiles** (`androidx.profileinstaller`) to trigger Ahead-of-Time (AOT) DEX compilation on app installation.
   - Defer non-critical SDK initializations using `App Startup` library or background coroutines.
2. **UI Rendering & 60/120 FPS:**
   - Keep Main thread work under **16.6ms** (60Hz) or **8.3ms** (120Hz).
   - In Compose, ensure stable types (`@Immutable`, `@Stable`), avoid unstable lambdas, and derive state with `derivedStateOf`.
3. **Memory & Leak Prevention:**
   - Never hold long-lived static references to `Activity` or `Context` (use `ApplicationContext` where appropriate).
   - Unregister listeners and cancel coroutine scopes in `onDestroy()` / `onCleared()`.
4. **Battery & Background Limits:**
   - Never poll servers with timers; use **Firebase Cloud Messaging (FCM)** push notifications with data payloads.
   - Batch background uploads with `WorkManager` with `NetworkType.UNMETERED` and `requiresCharging=true` constraints.
