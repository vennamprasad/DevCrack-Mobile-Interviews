# ⚡ Kotlin Coroutines & Structured Concurrency

> **Mastering lightweight asynchronous programming: Scopes, dispatchers, cancellation, error handling, thread safety, testing, and production concurrency patterns.**

---

## 📚 Curriculum Catalog

| Chapter | Topic & Focus |
| :--- | :--- |
| **[01. Coroutine Scopes & Context](./01_coroutine_scopes_and_context.md)** | `CoroutineScope`, `CoroutineContext`, `Job`, `Dispatchers`, and Android lifecycle scopes (`viewModelScope`, `lifecycleScope`). |
| **[02. Sequential vs Parallel Execution](./02_sequential_vs_parallel_execution.md)** | `launch` vs `async`, `awaitAll()`, parallel decomposition, and avoiding sequential bottlenecks. |
| **[03. Error Handling & Supervision](./03_error_handling_and_supervision.md)** | `CoroutineExceptionHandler`, `SupervisorJob`, `supervisorScope`, and isolating child failures. |
| **[04. Thread Safety & Mutex](./04_thread_safety_and_mutex.md)** | Race conditions, `Mutex`, atomic primitives (`AtomicInteger`), and thread confinement (`newSingleThreadContext`). |
| **[05. Exponential Backoff & Retries](./05_exponential_backoff_and_retries.md)** | Network retry logic with full jitter, backoff algorithms, and timeout handling with `withTimeout`. |
| **[06. Coordinating Network & Database](./06_coordinating_network_and_database.md)** | Offline-first data flow, background sync orchestration, and cache invalidation. |
| **[07. Proper Cancellation Handling](./07_proper_cancellation_handling.md)** | Cooperative cancellation, `isActive`, `ensureActive()`, `yield()`, and `NonCancellable` cleanup blocks. |
| **[08. Unit Testing Coroutines](./08_testing_coroutines.md)** | `StandardTestDispatcher`, `UnconfinedTestDispatcher`, `runTest`, virtual time advancement, and swapping `Dispatchers.Main`. |
| **[09. Performance Optimizations](./09_performance_optimizations.md)** | Avoiding thread pool starvation, choosing between `Default` and `IO` dispatchers, and coroutine memory footprints. |
| **[10. Interview Scenarios & Common Bugs](./10_interview_scenarios_and_bugs.md)** | Real-world concurrency interview questions, common production anti-patterns, and debugging memory leaks. |

---

[⬅️ Back to Kotlin Master Hub](../README.md)
