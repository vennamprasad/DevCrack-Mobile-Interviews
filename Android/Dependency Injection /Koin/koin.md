# ⚡ Koin Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Koin is a "Service Locator" DSL for Kotlin, though often referred to as DI. It is very popular in **KMP** (Kotlin Multiplatform).

![Koin](https://img.shields.io/badge/Koin-Framework-orange?style=for-the-badge&logo=kotlin&logoColor=white)
![KMP](https://img.shields.io/badge/Kotlin-Multiplatform-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)
![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)

---

## 📖 Table of Contents
- [1. Koin Basics & DSL](#-1-what-is-koin)
- [2. Definitions (Single vs Factory)](#-3-what-is-the-difference-between-single-and-factory-in-koin)
- [3. Android Integration](#-4-how-do-you-start-koin-in-an-android-application)
- [4. Advanced Scopes](#-11-how-do-you-scope-dependencies-in-koin)
- [5. Testing & Verification](#-10-how-do-you-test-code-using-koin)
- [6. Koin vs Hilt](#-koin-vs-hilt)

---

## ✅ Overview

**Koin** is a lightweight, pragmatic, and Kotlin-first dependency injection framework. It uses a DSL (Domain Specific Language) rather than annotations/code-generation (like Dagger).

**Key Features:**
*   **No Code Generation:** Faster build times (uses reflection/inline functions).
*   **Kotlin DSL:** Clean and concise configuration.
*   **Multiplatform:** Native support for KMP (Android, iOS, Desktop).

---

## 🧩 Interview Questions (Q&A)

### 1. What are the key Koin DSL keywords?
*   **`module { }`**: Creates a Koin module (container for definitions).
*   **`single { }`**: Creates a Singleton (created once, same instance returned).
*   **`factory { }`**: Creates a new instance every time it is injected.
*   **`viewModel { }`**: Special definition for Android ViewModels (handles lifecycle).
*   **`get()`**: Resolves a dependency inside a definition.

### 2. How do you set up Koin in Android?
In the `Application` class:

```kotlin
startKoin {
    androidContext(this@MyApp)
    androidLogger()
    modules(appModule, networkModule)
}
```

### 3. How do you inject in an Activity/Fragment?
Using Kotlin delegates:

```kotlin
class MainActivity : AppCompatActivity() {
    // Lazy injection
    private val viewModel: MainViewModel by viewModel()
    private val repository: Repository by inject()
}
```

### 4. What is the difference between `single` vs `factory`?
*   **`single`**: The instance is cached. Subsequent calls return the same object. (Like `@Singleton`).
*   **`factory`**: No cache. A new object is created for every injection request.

### 5. How to pass runtime parameters?
Use `parametersOf`.

```kotlin
// Module
factory { (id: String) -> UserPresenter(id) }

// Usage
val presenter: UserPresenter by inject { parametersOf("user_123") }
```

### 6. Scopes in Koin
Scopes allow dependencies to live for a specific duration (e.g., typically tied to an Activity or a custom flow).

```kotlin
val myScope = module {
    scope<MyActivity> {
        scoped { SessionManager() } // Lives as long as MyActivity scope exists
    }
}
```

### 7. How does Koin handle Lazy Injection?
By default, Koin injections via `by inject()` are **lazy**. The dependency is not resolved (created) until the property is first accessed.

### 8. Koin vs Hilt (Pros/Cons)
*   **Koin:**
    *   ➕ No code gen (Fast build).
    *   ➕ Easy KMP support.
    *   ➕ Simple DSL.
    *   ➖ Runtime crashes if dependency missing (though `verify()` checks help).
    *   ➖ Slightly slower runtime performance (reflection) compared to Dagger.
*   **Hilt:**
    *   ➕ Compile-time safety (Build fails if dependency missing).
    *   ➕ Standard for Android.
    *   ➖ Slow build times (KAPT/KSP).
    *   ➖ Steep learning curve (Components/Modules annotations).

### 9. Testing with Koin
Koin provides `koin-test` library.

```kotlin
class MyTest : KoinTest {
    @Test
    fun testRepo() {
        startKoin { modules(testModule) }
        
        val repo: Repository by inject()
        assertNotNull(repo)
        
        stopKoin()
    }
}
```

---