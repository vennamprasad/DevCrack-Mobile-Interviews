# Hilt Interview Questions (Basic & Advanced)

## Basic Questions

### 1. What is Hilt?
**Answer:**  
Hilt is a dependency injection library for Android that reduces the boilerplate of manual DI in your project.

---

### 2. Why use Hilt over Dagger in Android?
**Answer:**  
Hilt simplifies Dagger setup by providing standard components, automatic integration with Android classes, and better tooling support.

---

### 3. How do you enable Hilt in an Android project?
**Answer:**  
Add Hilt dependencies in `build.gradle` and annotate your Application class with `@HiltAndroidApp`.

```kotlin
@HiltAndroidApp
class MyApp : Application()
```

---

### 4. What is the purpose of `@Inject` annotation?
**Answer:**  
`@Inject` tells Hilt how to provide instances of a class.

---

### 5. What is a Hilt module?
**Answer:**  
A Hilt module is a class annotated with `@Module` and `@InstallIn` that provides dependencies using `@Provides` or `@Binds`.

---

### 6. How do you inject dependencies into an Activity?
**Answer:**  
Annotate the Activity with `@AndroidEntryPoint` and use `@Inject` for fields.

```kotlin
@AndroidEntryPoint
class MainActivity : AppCompatActivity() {
    @Inject lateinit var repository: MyRepository
}
```

---

### 7. What is `@AndroidEntryPoint`?
**Answer:**  
It marks Android classes (Activity, Fragment, etc.) as injection targets for Hilt.

---

### 8. What is the difference between `@Provides` and `@Binds`?
**Answer:**  
`@Provides` returns an instance, while `@Binds` binds an implementation to an interface.

---

### 9. What are Hilt components?
**Answer:**  
Hilt components are containers that manage the lifecycle and scope of dependencies (e.g., SingletonComponent, ActivityComponent).

---

### 10. How do you scope dependencies in Hilt?
**Answer:**  
Use scope annotations like `@Singleton`, `@ActivityScoped`, etc.

---

### 11. What is `@Singleton` in Hilt?
**Answer:**  
It scopes a dependency to the lifetime of the application.

---

### 12. How do you inject ViewModels with Hilt?
**Answer:**  
Annotate ViewModel with `@HiltViewModel` and use `@Inject` in its constructor.

```kotlin
@HiltViewModel
class MyViewModel @Inject constructor(
    private val repository: MyRepository
) : ViewModel()
```

---

### 13. Can you inject dependencies into a Service or BroadcastReceiver?
**Answer:**  
Yes, annotate them with `@AndroidEntryPoint`.

---

### 14. What is the purpose of `@InstallIn`?
**Answer:**  
It specifies which Hilt component the module is installed in.

---

### 15. How do you provide different implementations for the same interface?
**Answer:**  
Use qualifiers like `@Named` or custom qualifiers.

```kotlin
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class RemoteDataSource

@Module
@InstallIn(SingletonComponent::class)
object DataSourceModule {
    @RemoteDataSource
    @Provides
    fun provideRemoteDataSource(): DataSource = RemoteDataSourceImpl()
}
```

---

## Advanced Questions

### 16. How does Hilt handle dependency graph validation?
**Answer:**  
Hilt validates the dependency graph at compile time, ensuring all dependencies are provided.

---

### 17. What are entry points in Hilt?
**Answer:**  
Entry points are interfaces annotated with `@EntryPoint` to access dependencies outside Hilt-managed classes.

---

### 18. How do you inject dependencies into classes not supported by `@AndroidEntryPoint`?
**Answer:**  
Use Hilt entry points.

---

### 19. How does Hilt differ from manual Dagger setup?
**Answer:**  
Hilt automates component creation, lifecycle management, and integration with Android classes.

---

### 20. How do you test Hilt-based classes?
**Answer:**  
Use `@HiltAndroidTest` and `@UninstallModules` for replacing modules in tests.

---

### 21. What is `@UninstallModules` used for?
**Answer:**  
It removes modules from the dependency graph during testing.

---

### 22. How do you inject dependencies into custom classes (not Android components)?
**Answer:**  
Use constructor injection and pass dependencies from Hilt-injected classes.

---

### 23. How does Hilt handle multi-binding?
**Answer:**  
Use Dagger's `@IntoSet` or `@IntoMap` annotations in Hilt modules.

---

### 24. How do you handle circular dependencies in Hilt?
**Answer:**  
Refactor code to avoid circular dependencies or use `Provider<T>`.

---

### 25. How do you provide runtime values with Hilt?
**Answer:**  
Use `@Provides` methods that accept parameters or use assisted injection.

---

### 26. What is assisted injection in Hilt?
**Answer:**  
Assisted injection allows passing runtime parameters to constructors along with injected dependencies.

---

### 27. How do you inject dependencies into a Fragment?
**Answer:**  
Annotate the Fragment with `@AndroidEntryPoint` and use `@Inject`.

---

### 28. Can you use Hilt with Kotlin Multiplatform?
**Answer:**  
Hilt is designed for Android; for multiplatform, use Koin or manual DI.

---

### 29. How do you share dependencies between modules in a multi-module project?
**Answer:**  
Install modules in `SingletonComponent` or appropriate shared component.

---

### 30. What are custom scopes in Hilt?
**Answer:**  
Custom scopes are user-defined annotations for scoping dependencies, but Hilt recommends using built-in scopes.

---

## References

- [Hilt Official Documentation](https://developer.android.com/training/dependency-injection/hilt-android)
- [Dagger Documentation](https://dagger.dev/)
