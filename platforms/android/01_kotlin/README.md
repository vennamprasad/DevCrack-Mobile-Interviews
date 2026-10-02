# 💜 Kotlin Mastery for Android & Mobile Engineers

> **The definitive curriculum for Kotlin: Language Internals, Advanced Coroutines, Reactive Asynchronous Flows, and Interview Coding Patterns.**

![Kotlin](https://img.shields.io/badge/Language-Kotlin-7F52FF?style=for-the-badge&logo=kotlin)
![Coroutines](https://img.shields.io/badge/Concurrency-Coroutines-blue?style=for-the-badge)
![Flows](https://img.shields.io/badge/Reactive-Flows_&_Channels-green?style=for-the-badge)

---

## 📖 Module Catalog

| Submodule | Description | Link |
| :--- | :--- | :--- |
| **Comprehensive Kotlin Guide** | 15-chapter deep-dive into language fundamentals, OOP, null safety, lambdas, generics, delegation, and modern best practices. | **[Kotlin_Guide](./Kotlin_Guide/README.md)** |
| **Coroutines Deep Dive** | 13-part master guide covering structured concurrency, scopes (`viewModelScope`, `lifecycleScope`), dispatchers, cancellation, error handling, and testing. | **[Coroutines Guide](./Coroutines/Coroutines_Guide/README.md)** |
| **Flows & Channels** | 19-part reactive streaming guide covering Cold vs Hot flows, `StateFlow` vs `SharedFlow`, debounce search, pagination, offline-first sync, and testing. | **[Flows Guide](./Flows/Flows_Guide/README.md)** |
| **Kotlin Interview Cheat Sheet** | Quick-reference syntax guide for collections, inline functions, reified types, and sealed classes. | **[cheatsheet.md](./01_cheatsheet.md)** |
| **Hands-On Coding Challenges** | Practical interview coding questions and algorithm implementations written in idiomatic Kotlin. | **[02_coding_challenges.md](./02_coding_challenges.md)** |

---

## ⚡ High-Yield Kotlin Interview Topics

1. **Inline Functions & `reified` Type Parameters:** How inline functions prevent lambda allocation overhead, and how `reified` bypasses JVM type erasure.
2. **Structured Concurrency:** Why coroutines launched in child scopes cancel when parent scopes fail, and how `SupervisorJob` isolates child failures.
3. **StateFlow vs SharedFlow vs Channel:**
   - `StateFlow`: Hot, holds single latest state, replay=1, conflated (drops duplicate emissions), lifecycle-safe with `repeatOnLifecycle`.
   - `SharedFlow`: Hot, broadcast event bus, customizable replay buffer, emits one-off events to multiple subscribers.
   - `Channel`: Hot, queue-based, 1-to-1 consumer pattern (each item received exactly once).
4. **Value Classes (`@JvmInline value class`):** Zero-overhead type-safety wrapping primitive types at compile time without heap allocations.
