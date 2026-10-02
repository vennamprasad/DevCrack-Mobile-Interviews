# 💜 Kotlin Mastery for Android & Mobile Engineers

> **The definitive curriculum for Kotlin: Language Internals, Advanced Coroutines, Reactive Asynchronous Flows, and Interview Coding Patterns.**

![Kotlin](https://img.shields.io/badge/Language-Kotlin-7F52FF?style=for-the-badge&logo=kotlin)
![Coroutines](https://img.shields.io/badge/Concurrency-Coroutines-blue?style=for-the-badge)
![Flows](https://img.shields.io/badge/Reactive-Flows_&_Channels-green?style=for-the-badge)

---

## 📖 Module Catalog

| Submodule | Description | Link |
| :--- | :--- | :--- |
| **01. Language Fundamentals** | 10-chapter deep-dive into language fundamentals, OOP, null safety, lambdas, collections, generics, delegation, and modern best practices. | **[01. Language Fundamentals](./01_language_fundamentals/README.md)** |
| **02. Coroutines Concurrency** | 10-part master guide covering structured concurrency, scopes (`viewModelScope`, `lifecycleScope`), dispatchers, cancellation, error handling, mutex, and testing. | **[02. Coroutines](./02_coroutines/README.md)** |
| **03. Flows & Channels** | 11-part reactive streaming guide covering Cold vs Hot flows, `StateFlow` vs `SharedFlow`, debounce search, pagination, offline-first sync, and testing with Turbine. | **[03. Flows & Channels](./03_flows_and_channels/README.md)** |
| **04. Kotlin Cheat Sheet** | Quick-reference syntax guide for collections, scope functions, inline functions, reified types, and sealed classes. | **[04_cheatsheet.md](./04_cheatsheet.md)** |
| **05. Coding Challenges** | Practical interview coding questions and algorithm implementations written in idiomatic Kotlin. | **[05_coding_challenges.md](./05_coding_challenges.md)** |

---

## ⚡ High-Yield Kotlin Interview Topics

1. **Inline Functions & `reified` Type Parameters:** How inline functions prevent lambda allocation overhead, and how `reified` bypasses JVM type erasure.
2. **Structured Concurrency:** Why coroutines launched in child scopes cancel when parent scopes fail, and how `SupervisorJob` isolates child failures.
3. **StateFlow vs SharedFlow vs Channel:**
   - `StateFlow`: Hot, holds single latest state, replay=1, conflated (drops duplicate emissions), lifecycle-safe with `repeatOnLifecycle`.
   - `SharedFlow`: Hot, broadcast event bus, customizable replay buffer, emits one-off events to multiple subscribers.
   - `Channel`: Hot, queue-based, 1-to-1 consumer pattern (each item received exactly once).
4. **Value Classes (`@JvmInline value class`):** Zero-overhead type-safety wrapping primitive types at compile time without heap allocations.
