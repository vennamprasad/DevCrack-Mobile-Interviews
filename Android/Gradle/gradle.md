# 🐘 Gradle Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Mastering Gradle is key for build speed optimization and CI/CD pipelines.

![Gradle](https://img.shields.io/badge/Build_Tool-Gradle-02303A?style=for-the-badge&logo=gradle&logoColor=white)
![Groovy](https://img.shields.io/badge/Language-Groovy-4298B8?style=for-the-badge&logo=apachegroovy&logoColor=white)
![Kotlin](https://img.shields.io/badge/DSL-Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)

---

## 📖 Table of Contents
- [1. Basics & Benefits](#-1-what-is-gradle)
- [2. Dependencies & Plugins](#-4-how-do-you-define-dependencies-in-gradle)
- [3. Build Types & Flavors](#-14-how-do-you-define-build-variants-in-android-using-gradle)
- [4. Performance Optimization](#-22-what-is-build-caching-in-gradle)
- [5. Custom Tasks & Logic](#-6-how-do-you-create-a-custom-gradle-task)
- [6. Advanced Concepts](#-advanced-questions)

---

## ✅ Overview

**Gradle** is the official build tool for Android. It is a powerful, flexible build automation tool that uses a Domain Specific Language (DSL) (Groovy or Kotlin) to describe builds.

**Key Features:**
*   **Incremental Builds:** Recompiles only what changed.
*   **Build Cache:** Reuses outputs from previous builds.
*   **Parallel Execution:** Runs independent tasks simultaneously.

---

## 🧩 Interview Questions (Q&A)

### 1. What is the Gradle Wrapper (`gradlew`)?
It is a script that invokes a declared version of Gradle, downloading it beforehand if necessary. It ensures **consistency**: every developer (and CI server) builds with the exact same Gradle version.

### 2. `implementation` vs `api`?
*   **`implementation`**: Dependency is internal. Changing it does *not* force recompilation of consumers. **Faster builds.**
*   **`api`**: Dependency is transitive. It is exposed to consumers. Changing it forces recompilation of all modules depending on this module.

### 3. Build Types vs Product Flavors?
*   **Build Types**: Technical variations (Debug, Release, Staging). Different signing keys, ProGuard rules, debug flags.
*   **Product Flavors**: Functional/Brand variations (Free, Paid, WhiteLabel). Different app IDs, resources, logic.
*   **Build Variant** = Flavor + Build Type (e.g., `FreeDebug`).

### 4. What is `settings.gradle`?
The file executed during the **Initialization Phase**. It defines which modules (subprojects) are included in the build (`include ':app', ':data'`).

### 5. Gradle Build Phases lifecycle?
1.  **Initialization**: Determines which projects participate in the build.
2.  **Configuration**: Executes build scripts (`build.gradle`), creates the task graph. **(Heavy logic here slows down sync!)**
3.  **Execution**: Executes the selected tasks.

### 6. Optimizing Build Speed?
1.  **Enable Daemon**: Keeps Gradle JVM running.
2.  **Parallel Execution**: `org.gradle.parallel=true`.
3.  **Configuration on Demand**: Configure only relevant modules.
4.  **Avoid Dynamic Versions**: (`1.0.+` forces network checks).
5.  **Offline Mode**: For faster iteration when no new deps needed.

### 7. What is `buildSrc`?
A special directory in the project root containing build logic (plugins, constants, dependency versions). It is compiled and added to the classpath of all build scripts. It allows better IDE support (autocomplete) for Kotlin DSL compared to `ext` blocks.

### 8. Custom Task Example

```groovy
task copyDocs(type: Copy) {
    from 'src/main/doc'
    into 'build/target/doc'
    doLast {
        println "Docs copied!"
    }
}
```

### 9. Dependency Resolution Strategy
How to handle version conflicts (e.g., Lib A needs Gson 2.8, Lib B needs Gson 2.9).
```groovy
configurations.all {
    resolutionStrategy {
        force 'com.google.code.gson:gson:2.9.0'
        // or failOnVersionConflict()
    }
}
```

### 10. ProGuard / R8
R8 is the new code shrinker (replacing ProGuard). It performs:
1.  **Shrinking**: Removes unused code/resources.
2.  **Obfuscation**: Renames classes/fields to short names (security).
3.  **Optimization**: Inlines functions, removes unused interfaces.

---