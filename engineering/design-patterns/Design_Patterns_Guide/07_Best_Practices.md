## **Best Practices**

### Q19. When should you use which pattern?

**Answer:**

**Creational Patterns:**
- **Singleton**: Database, Network client, Logger
- **Factory**: Creating Views, Fragments, ViewHolders
- **Builder**: Complex objects with many optional parameters
- **Dependency Injection**: Everything! (Recommended)

**Structural Patterns:**
- **Adapter**: RecyclerView, integrating third-party libraries
- **Decorator**: Adding features to Views, OkHttp Interceptors
- **Facade**: Simplifying complex subsystems
- **Proxy**: Lazy loading, access control, caching

**Behavioral Patterns:**
- **Observer**: LiveData, Flow, event handling
- **Strategy**: Algorithms that change at runtime
- **Command**: Undo/Redo, queuing operations
- **Chain of Responsibility**: Touch event handling, logging

**Architectural Patterns:**
- **MVVM**: Modern Android apps (recommended)
- **MVP**: Legacy apps, more control
- **MVI**: Complex state management, predictability

---

### Q20. Common Interview Questions

**Q: What's the difference between Singleton and Static class?**
```kotlin
// Static class (object in Kotlin)
object StaticUtils {
    fun doSomething() { }
}

// Singleton
class Singleton private constructor() {
    companion object {
        @Volatile
        private var instance: Singleton? = null

        fun getInstance(): Singleton {
            return instance ?: synchronized(this) {
                instance ?: Singleton().also { instance = it }
            }
        }
    }
}
```
- Singleton can implement interfaces, extend classes
- Static class cannot have state that requires initialization
- Singleton can be lazy-loaded
- Static is initialized when class loads

**Q: How do you make Singleton thread-safe in Android?**
```kotlin
// Thread-safe lazy initialization
class ThreadSafeSingleton private constructor() {
    companion object {
        val instance: ThreadSafeSingleton by lazy(LazyThreadSafetyMode.SYNCHRONIZED) {
            ThreadSafeSingleton()
        }
    }
}

// Using object (thread-safe by default)
object SafeSingleton {
    // Thread-safe
}

// Double-checked locking
class DoubleCheckedSingleton private constructor() {
    companion object {
        @Volatile
        private var instance: DoubleCheckedSingleton? = null

        fun getInstance(): DoubleCheckedSingleton {
            return instance ?: synchronized(this) {
                instance ?: DoubleCheckedSingleton().also { instance = it }
            }
        }
    }
}
```

**Q: How does RecyclerView use design patterns?**
- **Adapter Pattern**: RecyclerView.Adapter adapts data to views
- **ViewHolder Pattern**: Caches view references
- **Observer Pattern**: notify methods update views
- **Strategy Pattern**: LayoutManager defines layout strategy

**Q: Explain dependency injection in Android**
- Provides dependencies from outside
- Improves testability
- Reduces coupling
- Hilt/Dagger are recommended frameworks

**Q: What's the difference between MVP and MVVM?**
- MVP: View interface, manual updates, more boilerplate
- MVVM: Data binding, lifecycle-aware, less boilerplate
- MVVM is Google's recommended pattern
