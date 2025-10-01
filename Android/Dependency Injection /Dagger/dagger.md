# Dagger Dependency Injection Interview Questions (Basic & Advanced)

---

## Basic Questions

### 1. What is Dependency Injection?
**Answer:**  
Dependency Injection (DI) is a design pattern that allows an object to receive its dependencies from an external source rather than creating them itself.

---

### 2. What is Dagger?
**Answer:**  
Dagger is a compile-time dependency injection framework for Java and Android, developed by Google.

---

### 3. What are the main components of Dagger?
**Answer:**  
- `@Module`
- `@Provides`
- `@Component`
- `@Inject`

---

### 4. How do you define a Dagger module?
**Answer:**  
A module is a class annotated with `@Module` that provides dependencies using `@Provides` methods.

```java
@Module
class NetworkModule {
    @Provides
    fun provideApiService(): ApiService = ApiServiceImpl()
}
```

---

### 5. What is a Dagger component?
**Answer:**  
A component is an interface annotated with `@Component` that connects modules and injection targets.

```java
@Component(modules = [NetworkModule::class])
interface AppComponent {
    fun inject(activity: MainActivity)
}
```

---

### 6. How do you inject dependencies using Dagger?
**Answer:**  
Use the `@Inject` annotation on fields or constructors.

```java
class MainActivity : AppCompatActivity() {
    @Inject lateinit var apiService: ApiService
}
```

---

### 7. What is constructor injection in Dagger?
**Answer:**  
Dependencies are provided via the class constructor annotated with `@Inject`.

```java
class UserRepository @Inject constructor(private val apiService: ApiService)
```

---

### 8. What is field injection?
**Answer:**  
Dependencies are injected directly into fields annotated with `@Inject`.

---

### 9. What is method injection?
**Answer:**  
Dependencies are injected via methods annotated with `@Inject`.

---

### 10. How do you scope dependencies in Dagger?
**Answer:**  
Use custom scope annotations (e.g., `@Singleton`) to control the lifecycle of dependencies.

```java
@Singleton
@Component(modules = [NetworkModule::class])
interface AppComponent
```

---

## Advanced Questions

### 11. What is subcomponent in Dagger?
**Answer:**  
A subcomponent inherits and extends the object graph of a parent component, useful for nested scopes.

---

### 12. How do you use qualifiers in Dagger?
**Answer:**  
Qualifiers (`@Named`, custom annotations) distinguish between different objects of the same type.

```java
@Provides
@Named("prod")
fun provideProdApiService(): ApiService = ProdApiService()
```

---

### 13. What is the difference between `@Singleton` and custom scopes?
**Answer:**  
`@Singleton` provides a single instance for the entire component, while custom scopes can define lifecycles for specific use cases (e.g., per activity).

---

### 14. How does Dagger differ from other DI frameworks like Guice or Spring?
**Answer:**  
Dagger generates code at compile-time, resulting in better performance and no reflection overhead.

---

### 15. How do you inject dependencies into Android components (Activity, Fragment)?
**Answer:**  
Call the component's `inject()` method in the lifecycle method (e.g., `onCreate`).

---

### 16. What is `@Binds` annotation?
**Answer:**  
`@Binds` is used to bind an implementation to an interface, replacing `@Provides` for abstract methods.

```java
@Module
abstract class RepositoryModule {
    @Binds
    abstract fun bindUserRepository(repo: UserRepositoryImpl): UserRepository
}
```

---

### 17. What is multibinding in Dagger?
**Answer:**  
Multibinding allows you to inject collections (e.g., `Set`, `Map`) of objects using `@IntoSet` or `@IntoMap`.

---

### 18. How do you handle circular dependencies in Dagger?
**Answer:**  
Refactor code to avoid circular dependencies or use `@Inject` on constructors carefully.

---

### 19. What is assisted injection?
**Answer:**  
Assisted injection allows you to inject dependencies that require runtime parameters using `@AssistedInject`.

---

### 20. How do you test Dagger components?
**Answer:**  
Use test-specific modules and components to provide mock dependencies.

---

### 21. What is the role of `@Component.Factory` and `@Component.Builder`?
**Answer:**  
They allow passing parameters to components at creation time.

---

### 22. How does Dagger handle dependency graph validation?
**Answer:**  
Dagger validates the dependency graph at compile-time, reporting errors for missing or conflicting dependencies.

---

### 23. How do you use Dagger with ViewModels in Android?
**Answer:**  
Inject dependencies into ViewModels using constructor injection and provide them via Dagger modules.

---

### 24. What is the difference between `@Provides` and `@Inject`?
**Answer:**  
`@Provides` is used in modules to provide dependencies, while `@Inject` is used on constructors or fields to request dependencies.

---

### 25. How do you migrate from Dagger 2 to Hilt?
**Answer:**  
Replace Dagger components and modules with Hilt annotations (`@HiltAndroidApp`, `@AndroidEntryPoint`, etc.) and refactor code accordingly.

---
