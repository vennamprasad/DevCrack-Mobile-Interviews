# 🐘 Gradle Build System & CI/CD Mastery

> **The definitive guide to Android build systems, Gradle internals, Kotlin DSL (`.kts`), Version Catalogs, build speed optimization, and R8/ProGuard shrinking.**

![Gradle](https://img.shields.io/badge/Build_Tool-Gradle-02303A?style=for-the-badge&logo=gradle)
![KotlinDSL](https://img.shields.io/badge/Config-Kotlin_DSL-7F52FF?style=for-the-badge&logo=kotlin)
![Optimization](https://img.shields.io/badge/Performance-Build_Speed-green?style=for-the-badge)

---

## 📖 Module Contents

| Guide | Description | Target Level |
| :--- | :--- | :--- |
| **[01. Gradle Fundamentals & Q&A](./01_gradle_basics.md)** | Core concepts, tasks, dependency configurations (`implementation`, `api`, `compileOnly`), build variants, product flavors, and common interview questions. | Mid / Senior |
| **[02. Gradle Mastery (Staff / Lead)](./02_gradle_mastery.md)** | Deep-dive for senior/staff engineers: Groovy to KTS migration, Version Catalogs (`libs.versions.toml`), configuration cache, build scan profiling, R8 shrinking, and custom standalone Gradle plugins. | Senior / Staff |

---

## ⚡ Key Build Optimization Best Practices

1. **Enable Configuration Cache:** Reuse task graph calculation across builds (`org.gradle.configuration-cache=true`).
2. **Modularization for Parallel Execution:** Fine-grained module graphs allow Gradle to compile independent modules simultaneously on multi-core CPUs.
3. **Use `implementation` over `api`:** Restricts transitive dependency exposure, preventing downstream modules from recompiling when internal implementation details change.
4. **Avoid Non-Cacheable Custom Tasks:** Always define `@Input`, `@OutputDirectory`, `@PathSensitive`, and annotate tasks with `@CacheableTask`.
5. **Adopt Version Catalogs (`libs.versions.toml`):** Centralize dependency versions, bundles, and plugins with type-safe accessors in Kotlin DSL scripts.
