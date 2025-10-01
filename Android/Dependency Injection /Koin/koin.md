# Koin Interview Questions (Basic & Advanced)

## Basic Questions

### 1. What is Koin?
**Answer:**  
Koin is a lightweight dependency injection framework for Kotlin developers, primarily used in Android and Kotlin applications.

---

### 2. How do you define a module in Koin?
**Answer:**  
A module is defined using the `module { }` DSL block.
```kotlin
val appModule = module {
    single { Repository() }
    factory { ViewModel(get()) }
}
```

---

### 3. What is the difference between `single` and `factory` in Koin?
**Answer:**  
- `single`: Provides a singleton instance.
- `factory`: Provides a new instance every time.

---

### 4. How do you start Koin in an Android application?
**Answer:**  
Initialize Koin in the `Application` class:
```kotlin
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        startKoin {
            androidContext(this@MyApp)
            modules(appModule)
        }
    }
}
```

---

### 5. How do you inject dependencies in an Android Activity using Koin?
**Answer:**  
Use `by inject()` or `by viewModel()`:
```kotlin
class MainActivity : AppCompatActivity() {
    val repo: Repository by inject()
    val viewModel: MainViewModel by viewModel()
}
```

---

### 6. What is `get()` in Koin?
**Answer:**  
`get()` retrieves an instance of a dependency from the Koin container.

---

### 7. How do you pass parameters to a dependency in Koin?
**Answer:**  
Use `parametersOf()`:
```kotlin
factory { (id: Int) -> UserRepository(id) }
val repo: UserRepository by inject { parametersOf(42) }
```

---

### 8. Can Koin be used outside Android?
**Answer:**  
Yes, Koin can be used in any Kotlin project, including JVM, JS, and Native.

---

### 9. How do you declare a ViewModel in Koin?
**Answer:**  
Use the `viewModel` DSL:
```kotlin
val appModule = module {
    viewModel { MainViewModel(get()) }
}
```

---

### 10. How do you test code using Koin?
**Answer:**  
Use `startKoin` with test modules and `declareMock` for mocking dependencies.

---

## Advanced Questions

### 11. How do you scope dependencies in Koin?
**Answer:**  
Use `scope` DSL for scoping:
```kotlin
val appModule = module {
    scope<MyActivity> {
        scoped { ScopedRepository() }
    }
}
```

---

### 12. What is the difference between `scoped` and `single`?
**Answer:**  
- `scoped`: Instance lives as long as the scope.
- `single`: Singleton for the whole Koin container.

---

### 13. How do you inject dependencies in a Fragment?
**Answer:**  
Same as Activity:
```kotlin
class MyFragment : Fragment() {
    val repo: Repository by inject()
}
```

---

### 14. How do you override a dependency in Koin?
**Answer:**  
Use `override = true`:
```kotlin
single(override = true) { MockRepository() }
```

---

### 15. How do you load multiple modules in Koin?
**Answer:**  
Pass a list to `modules()`:
```kotlin
startKoin {
    modules(listOf(appModule, networkModule, viewModelModule))
}
```

---

### 16. How do you handle dependency cycles in Koin?
**Answer:**  
Koin detects cycles and throws an exception. Refactor your dependencies to avoid cycles.

---

### 17. How do you inject dependencies in a custom class (not Activity/Fragment)?
**Answer:**  
Use `GlobalContext.get().get<Dependency>()` or inject via constructor.

---

### 18. How do you stop Koin?
**Answer:**  
Call `stopKoin()`.

---

### 19. How do you use Koin with coroutines?
**Answer:**  
Inject coroutine scopes or dispatchers as dependencies:
```kotlin
single { Dispatchers.IO }
```

---

### 20. How do you use Koin with Retrofit?
**Answer:**  
Declare Retrofit as a singleton:
```kotlin
single {
    Retrofit.Builder()
        .baseUrl("https://api.example.com")
        .build()
}
```

---

### 21. How do you use Koin with Room database?
**Answer:**  
Declare Room database and DAO as singletons:
```kotlin
single {
    Room.databaseBuilder(get(), AppDatabase::class.java, "db").build()
}
single { get<AppDatabase>().userDao() }
```

---

### 22. How do you inject dependencies in a Service?
**Answer:**  
Use `by inject()` in the Service class.

---

### 23. How do you declare a dependency with constructor parameters?
**Answer:**  
Use factory with parameters:
```kotlin
factory { (param: String) -> MyClass(param) }
```

---

### 24. How do you use Koin with multi-module projects?
**Answer:**  
Define modules in each submodule and load them in the main application.

---

### 25. How do you mock dependencies for unit testing?
**Answer:**  
Use `declareMock` or override modules with test implementations.

---

### 26. How do you check if a dependency is loaded in Koin?
**Answer:**  
Use `isLoaded()` on the module or check with `getOrNull()`.

---

### 27. How do you use Koin with Kotlin Multiplatform?
**Answer:**  
Use Koin's multiplatform support and share modules across platforms.

---

### 28. How do you inject a dependency lazily?
**Answer:**  
Use `by inject()` for lazy injection.

---

### 29. How do you handle dependency injection in background workers?
**Answer:**  
Inject dependencies in `Worker` using `by inject()`.

---

### 30. How do you debug Koin dependency graph?
**Answer:**  
Enable Koin logging:
```kotlin
startKoin {
    printLogger()
    modules(appModule)
}
```

---

*Feel free to expand or customize these questions for your interview needs!*