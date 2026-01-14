# 🐘 Gradle Mastery for Android Engineers

> **Target Audience:** Staff Engineers & DevOps focus.
> **Scope:** Build Speed, Dependency Management, R8, and Custom Plugins.

![Gradle](https://img.shields.io/badge/Make-Gradle-blue?style=for-the-badge&logo=gradle)

---

## 📖 Table of Contents
- [Level 1: The Basics (Groovy vs KTS)](#level-1-the-basics)
- [Level 2: Build Speed Optimization](#level-2-build-speed-optimization)
- [Level 3: Dependencies & Version Catalogs](#level-3-dependencies--version-catalogs)
- [Level 4: R8, ProGuard & Obfuscation](#level-4-r8-proguard--obfuscation)
- [Level 5: Custom Plugins & CI/CD](#level-5-custom-plugins--cicd)

---

## Level 1: The Basics

### Q1. KTS (Kotlin DSL) vs Groovy?
**Answer:**
*   **Groovy**: Dynamic, legacy default. Harder autocomplete.
*   **KTS**: Statically typed. Excellent IDE support (jump to definition). Compile-time checks. **Preferred for new projects**.

### Q2. What are `buildTypes` vs `productFlavors`?
**Answer:**
*   **Build Types**: Optimization levels (Debug vs Release). Same codebase, different compilation flags.
*   **Product Flavors**: Functional variations (Free vs Paid, Dev vs Prod API). Can have different source sets (`src/paid/java`).
*   **Build Variant**: Combination (e.g., `paidRelease`).

### Q3. What is the `settings.gradle.kts` file for?
**Answer:**
It defines **which modules** are included in the project build.
`include(":app", ":domain", ":data")`.
Also used for `dependencyResolutionManagement` (Repositories).

### Q4. Difference between `implementation` vs `api`?
**Answer:**
*   **implementation**: Dependency is hidden from consumers. (Faster build).
    *   App -> Module A -> Module B. App cannot see Module B classes.
*   **api**: Dependency is transitively exposed. (Slower build).
    *   App -> Module A -> Module B. App CAN see Module B classes.

---

## Level 2: Build Speed Optimization

### Q5. How to enable Parallel Builds?
**Answer:**
In `gradle.properties`:
```properties
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.daemon=true
```
Decoupled projects build faster physically.

### Q6. What is the Configuration Cache?
**Answer:**
Gradle records the graph of tasks and their inputs.
If inputs haven't changed, Gradle **skips the configuration phase** entirely and jumps strictly to execution.
Enable with: `org.gradle.configuration-cache=true`.

### Q7. How to debug a slow build?
**Answer:**
Run: `./gradlew assembleDebug --scan`.
Generates a **Build Scan** URL.
Inspect:
1.  **Task Execution**: Which task took longest?
2.  ** Critical Path**: Which chain of dependencies blocked others?
3.  **Cache Misses**: Why was a task re-run?

### Q8. What is `kapt` vs `ksp`?
**Answer:**
*   **kapt**: Kotlin Annotation Processing Tool. Generates Java stubs. Slow.
*   **KSP**: Kotlin Symbol Processing. Direct parsing of Kotlin AST. **2x faster**. Use KSP for Room, Glide, Moshi.

---

## Level 3: Dependencies & Version Catalogs

### Q9. What is a Version Catalog (`libs.versions.toml`)?
**Answer:**
Centralized place to manage dependencies.
**Structure**:
```toml
[versions]
retrofit = "2.9.0"

[libraries]
retrofit = { module = "com.squareup.retrofit2:retrofit", version.ref = "retrofit" }

[bundles]
networking = ["retrofit", "okhttp"]
```
**Usage**: `implementation(libs.retrofit)`

### Q10. How to handle Dependency Conflicts (Duplicate Classes)?
**Answer:**
*   **Force**: `implementation("com.example:lib:1.0") { force = true }`
*   **Exclude**:
    ```kotlin
    implementation("com.example:lib:1.0") {
        exclude(group = "org.json", module = "json")
    }
    ```
*   **Strict**: Use BOM (Bill of Materials) to enforce versions.

---

## Level 4: R8, ProGuard & Obfuscation

### Q11. Difference between ProGuard and R8?
**Answer:**
*   **ProGuard**: Java tool. Shrinks, Obfuscates, Optimizes bytecode.
*   **R8**: Google's replacement. Does everything ProGuard does + acts as the D8 compiler (Java -> Dex).
*   **Advantage**: R8 is faster because it combines Desugaring, Shrinking, and Dexing in one step.

### Q12. Why do we need `proguard-rules.pro`?
**Answer:**
To tell R8 **what NOT to obfuscate**.
If you use Reflection (e.g., GSON, Retrofit), R8 will rename fields (`name` -> `a`), causing matching to fail.
**Fix**: `-keep class com.example.models.** { *; }`

### Q13. What is "Resource Shrinking"?
**Answer:**
Removes unused resources (images, layouts) from the APK.
`isShrinkResources = true`.
**Note**: Only works if `isMinifyEnabled = true` (Code shrinking) is also on.

---

## Level 5: Custom Plugins & CI/CD

### Q14. How to write a Custom Gradle Plugin?
**Answer:**
Create a `buildSrc` directory or a standalone module.
Class implements `Plugin<Project>`.
```kotlin
class MyPlugin : Plugin<Project> {
    override fun apply(project: Project) {
        project.task("hello") {
            doLast { println("Hello Gradle") }
        }
    }
}
```

### Q15. CI/CD Pipeline optimization?
**Answer:**
1.  **Cache Dependencies**: Cache `~/.gradle/caches`.
2.  **Shallow Clone**: `git clone --depth 1`.
3.  **Static Analysis Parallelization**: Run Lint, Detekt, and Tests in parallel jobs.

### Q16. Real-Scenario: "Manifest Merger Failed".
**Debug:**
Usually two libraries declaring different values for the same attribute (e.g., `android:allowBackup`).
**Fix:**
Add `tools:replace="android:allowBackup"` in your App's Manifest.
