## **Null Safety**

### Q13. How does Kotlin handle null safety?

**Answer:**
Kotlin's type system distinguishes between nullable and non-nullable types.

```kotlin
// Non-nullable (default)
var name: String = "John"
// name = null // ❌ Compilation error

// Nullable
var nullableName: String? = "John"
nullableName = null // ✅ OK

// Safe call operator ?.
val length = nullableName?.length // null if nullableName is null

// Elvis operator ?:
val length2 = nullableName?.length ?: 0 // 0 if null

// Not-null assertion !!
val length3 = nullableName!!.length // Throws NPE if null (use carefully!)

// Safe cast as?
val number: Int? = value as? Int // null if cast fails

// Let function
nullableName?.let {
    println("Name is $it")
} // Only executes if not null
```

---

### Q14. What is the difference between `lateinit` and lazy?

**Answer:**

**lateinit:**
```kotlin
class MyActivity : Activity() {
    // For var, non-null properties initialized later
    lateinit var adapter: RecyclerView.Adapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        adapter = MyAdapter() // Initialize later
    }

    fun checkInitialized() {
        if (::adapter.isInitialized) {
            // Use adapter
        }
    }
}
```

**lazy:**
```kotlin
class DataManager {
    // For val, initialized on first access
    val database: Database by lazy {
        println("Initializing database")
        Database.create() // Computed once, then cached
    }

    // Thread-safety modes
    val lazyValue by lazy(LazyThreadSafetyMode.SYNCHRONIZED) {
        // Thread-safe (default)
        expensiveComputation()
    }

    val fastLazy by lazy(LazyThreadSafetyMode.NONE) {
        // Not thread-safe, faster
        simpleComputation()
    }
}
```

| Feature | lateinit | lazy |
|---------|----------|------|
| **Property type** | var | val |
| **Nullability** | Non-null | Any |
| **Types** | Only classes/objects | Any type |
| **Initialization** | Explicit assignment | Computed on first access |
| **Thread safety** | No (by default) | Yes (by default) |
| **Check initialized** | `::property.isInitialized` | Not needed |

---

### Q15. What are safe calls, elvis operator, and not-null assertions?

**Answer:**

**Safe Call Operator `?.`:**
```kotlin
val name: String? = null
val length = name?.length // null (no NPE)

// Chain safe calls
val country = user?.address?.city?.country
```

**Elvis Operator `?:`:**
```kotlin
// Provide default value if null
val length = name?.length ?: 0

// Return early
fun process(input: String?): Int {
    val value = input ?: return -1
    return value.length
}

// Throw exception
val email = user?.email ?: throw IllegalStateException("Email required")
```

**Not-Null Assertion `!!`:**
```kotlin
// Throws NPE if null - use with caution!
val length = name!!.length

// When to use !!:
// 1. You're 100% sure it's not null
// 2. Better crash than silent failure
// 3. During migration from Java

// Better alternatives:
val length = name?.length ?: 0 // Elvis
val length = requireNotNull(name).length // With message
val length = checkNotNull(name).length // Similar to requireNotNull
```

**Let Function:**
```kotlin
// Execute block only if not null
name?.let {
    println("Name: $it")
    println("Length: ${it.length}")
}

// With multiple nullable values
val result = value1?.let { v1 ->
    value2?.let { v2 ->
        v1 + v2
    }
}
```

---

### Q16. What are platform types and how to handle them?

**Answer:**
Platform types are types from Java that have unknown nullability.

```kotlin
// Java code
public class JavaClass {
    public String getName() {
        return "John"; // Could return null!
    }
}

// Kotlin code
val javaObj = JavaClass()
val name = javaObj.name // Platform type: String!

// ❌ Dangerous - might crash
val length = name.length

// ✅ Safe handling
val safeName: String? = javaObj.name // Treat as nullable
val length = safeName?.length ?: 0

// Or use safe calls
val length2 = javaObj.name?.length ?: 0

// Use nullability annotations in Java
@Nullable
public String getName() {
    return null;
}

@NotNull
public String getName() {
    return "John";
}
```
