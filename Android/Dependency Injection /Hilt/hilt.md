# 🗡️ Hilt Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Hilt is Google's recommended DI solution for Android, built on top of Dagger.

![Hilt](https://img.shields.io/badge/Jetpack-Hilt-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Dagger](https://img.shields.io/badge/Powered_By-Dagger-orange?style=for-the-badge)
![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)

---

## 📖 Table of Contents
- [1. Basics & Setup](#-basics)
- [2. Annotations](#-3-what-is-the-purpose-of-inject-annotation)
- [3. Components & Scopes](#-9-what-are-hilt-components)
- [4. ViewModels & WorkManager](#-12-how-do-you-inject-viewmodels-with-hilt)
- [5. Testing](#-20-how-do-you-test-hilt-based-classes)
- [6. Migration](#-19-how-does-hilt-differ-from-manual-dagger-setup)

---

## ✅ Overview

**Hilt** provides a standard way to incorporate Dagger dependency injection into an Android application. It defines a standard set of components for Android classes and simplified setup modules.

**Hilt vs Dagger:**
*   **Standardization:** Hilt has predefined standard components (`SingletonComponent`, `ActivityComponent`). Dagger requires manual component definition.
*   **Boilerplate:** Hilt generates the components and wiring code, significantly reducing code.
*   **AndroidX Support:** Built-in support for `ViewModel`, `WorkManager`, and `Compose`.

---

## 🧩 Interview Questions (Q&A)

### 1. How do you set up Hilt?
1.  Annotate the `Application` class with `@HiltAndroidApp`.
2.  Annotate Android Entry Points (Activities, Fragments) with `@AndroidEntryPoint`.

```kotlin
@HiltAndroidApp
class MyApp : Application()

@AndroidEntryPoint
class MainActivity : AppCompatActivity()
```

### 2. Main Hilt Annotations
*   **`@HiltAndroidApp`**: Triggers Hilt's code generation for the app.
*   **`@AndroidEntryPoint`**: Marks an Activity/Fragment/Service to receive dependencies.
*   **`@InstallIn`**: Specifies which component a module belongs to (e.g., `SingletonComponent`).
*   **`@HiltViewModel`**: Integrates ViewModel injection.

### 3. What Components are available in Hilt?
*   `SingletonComponent` (App wide)
*   `ActivityRetainedComponent` (Survives config changes, for ViewModels)
*   `ActivityComponent`
*   `FragmentComponent`
*   `ViewComponent`
*   `ServiceComponent`

### 4. How do you provide dependencies?
Using Modules.

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    
    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit { ... }
}
```

### 5. `@Provides` vs `@Binds` in Hilt?
*   **`@Provides`**: For external classes (Retrofit, Room) or where you need custom initialization code.
*   **`@Binds`**: For binding interfaces to implementations. Hilt optimizes this (no factory generation).

### 6. Inspecting Scopes
*   `@Singleton`: Available everywhere, same instance.
*   `@ActivityScoped`: One instance per Activity lifecycle.
*   `@ViewModelScoped`: One instance per ViewModel.

### 7. How to inject instances not supported by Hilt? (EntryPoint)
Sometimes you need dependencies in a class not supported by Hilt (e.g., a ContentProvider or a plain Java/Kotlin class hooked into a 3rd party library). Use **`@EntryPoint`**.

```kotlin
@EntryPoint
@InstallIn(SingletonComponent::class)
interface AnalyticsEntryPoint {
    fun analyticsService(): AnalyticsService
}

// Usage
val entryPoint = EntryPointAccessors.fromApplication(context, AnalyticsEntryPoint::class.java)
val service = entryPoint.analyticsService()
```

### 8. Testing with Hilt
*   Use `@HiltAndroidTest`.
*   Use `@UninstallModules` to replace production modules with test modules (mocks).

```kotlin
@HiltAndroidTest
@UninstallModules(NetworkModule::class)
class MainTest {
    @get:Rule var hiltRule = HiltAndroidRule(this)
    
    @Inject lateinit var repo: Repository // MOCKED via TestModule
}
```

### 9. Constructor Injection in ViewModel
Simplified with `@HiltViewModel`.

```kotlin
@HiltViewModel
class MainViewModel @Inject constructor(
    private val repository: Repository
) : ViewModel()
```

---
