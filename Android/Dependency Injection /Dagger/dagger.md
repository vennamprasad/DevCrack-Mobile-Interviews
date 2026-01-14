# 🗡️ Dagger Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Dagger 2 is the industry standard for DI in Android, though Hilt (built on top of Dagger) is now recommended for new projects.

![Dagger](https://img.shields.io/badge/Google-Dagger_2-orange?style=for-the-badge&logo=google&logoColor=white)
![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)
![DI](https://img.shields.io/badge/Pattern-Dependency_Injection-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Core Concepts](#-1-what-is-dependency-injection)
- [2. Components & Modules](#-3-what-are-the-main-components-of-dagger)
- [3. Scopes & Qualifiers](#-10-how-do-you-scope-dependencies-in-dagger)
- [4. Advanced Dagger](#-advanced-questions)
- [5. Common Annotations](#-3-what-are-the-main-components-of-dagger)

---

## ✅ Overview

**Dagger** is a fully static, compile-time dependency injection framework for both Java and Android. It uses annotation processing to generate code that bootstraps dependency injection.

**Key Benefits:**
*   **Compile-time safety:** No runtime reflection errors.
*   **Performance:** Code is generated at build time, avoiding reflection overhead.
*   **Scalability:** Works well in large codebases.

---

## 🧩 Interview Questions (Q&A)

### 1. What is Dependency Injection (DI)?
DI is a design pattern where a class allows an external entity to "inject" its dependencies rather than creating them itself. This promotes loose coupling and easier testing.

### 2. Dagger Components Breakdown
*   **`@Module`**: Classes that define methods (annotated with `@Provides`) to provide dependencies (e.g., Retrofit instance).
*   **`@Component`**: Interfaces that bridge Modules and Injection Targets (Activities/Fragments). They tell Dagger which dependencies to provide to whom.
*   **`@Provides`**: Methods inside Modules that create and return dependencies.
*   **`@Inject`**:
    *   **Constructor Injection:** Requesting Dagger to create the class instance.
    *   **Field Injection:** Requesting Dagger to populate a field (used in Android classes like Activity).

### 3. How do you define a Module?

```kotlin
@Module
object NetworkModule {
    @Provides
    @Singleton
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}
```

### 4. What is the difference between `@Provides` vs `@Binds`?
*   **`@Provides`**: Used when you need to run code to create an instance (e.g., using a Builder, external library classes).
*   **`@Binds`**: Used to bind an implementation to an interface. It is more efficient as Dagger doesn't generate a separate factory class (it just casts the type). **Must be in an abstract class/interface.**

```kotlin
@Module
abstract class RepositoryModule {
    @Binds
    abstract fun bindRepo(repoImpl: UserRepositoryImpl): UserRepository
}
```

### 5. What are Subcomponents?
A **Subcomponent** is a child component that inherits bindings from its parent but has a distinct lifecycle (scope). For example, a `UserComponent` might only live while a user is logged in, whereas the `AppComponent` lives forever.

### 6. Explain Scopes (`@Singleton`, Custom Scopes)
Scopes ensure a single instance of a dependency exists within a specific component's lifecycle.
*   **`@Singleton`**: Default scope typically used for `AppComponent`.
*   **`@ActivityScope`**: Custom scope for dependencies that should live as long as the Activity.

```kotlin
@Scope
@Retention(AnnotationRetention.RUNTIME)
annotation class ActivityScope
```

### 7. What involves Constructor Injection vs Field Injection?
*   **Constructor Injection:** Preferred. Dagger knows how to create the object.
    ```kotlin
    class ViewModel @Inject constructor(private val repo: Repo)
    ```
*   **Field Injection:** Required for Android Framework classes (Activity, Fragment, Service) because the OS instantiates them, not Dagger.
    ```kotlin
    class MainActivity : AppCompatActivity() {
        @Inject lateinit var viewModel: MainViewModel
    }
    ```

### 8. How to handle Multiple Implementations (`@Named`)?
Use **Qualifiers**.
```kotlin
@Provides
@Named("Auth")
fun provideAuthRetrofit(): Retrofit = ...

@Provides
@Named("Public")
fun providePublicRetrofit(): Retrofit = ...

// Usage
@Inject constructor(@Named("Auth") private val retrofit: Retrofit)
```

### 9. What is Multibinding?
Allows binding multiple objects into a collection (Set or Map) that can be injected. Useful for plugin architectures or ViewModel factories (mapping ViewModel Class to Provider).
*   `@IntoSet`, `@IntoMap`, `@StringKey`.

### 10. Circular Dependencies
Occurs when A needs B, and B needs A.
*   **Solution 1:** Refactor design (usually indicates bad architecture).
*   **Solution 2:** Use `Lazy<T>` or `Provider<T>` to break the instantiation cycle.

---
