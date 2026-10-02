## **Delegation**

### Q42. What are delegated properties?

**Answer:**
Delegation allows property getters/setters to be handled by another object.

```kotlin
class Delegate {
    operator fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return "Delegated value for ${property.name}"
    }

    operator fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
        println("Setting ${property.name} = $value")
    }
}

class Example {
    var prop: String by Delegate()
}

val example = Example()
println(example.prop) // Delegated value for prop
example.prop = "new value" // Setting prop = new value
```

**Built-in delegates:**

**lazy:**
```kotlin
val heavyObject by lazy {
    println("Computing...")
    ExpensiveObject() // Computed once, then cached
}
```

**observable:**
```kotlin
var name: String by Delegates.observable("initial") { prop, old, new ->
    println("${prop.name}: $old -> $new")
}

name = "new value" // name: initial -> new value
```

**vetoable:**
```kotlin
var age: Int by Delegates.vetoable(0) { prop, old, new ->
    new >= 0 // Veto if negative
}

age = 25 // OK
age = -5 // Vetoed, stays 25
```

**notNull:**
```kotlin
var nonNull: String by Delegates.notNull()
// println(nonNull) // ❌ Throws exception
nonNull = "value"
println(nonNull) // OK
```

---

### Q43. What is class delegation?

**Answer:**
Delegation pattern where one class implements an interface by delegating to another object.

```kotlin
interface Base {
    fun print()
    fun message(): String
}

class BaseImpl : Base {
    override fun print() {
        println("BaseImpl")
    }

    override fun message() = "Hello from Base"
}

// Delegation with 'by'
class Derived(private val base: Base) : Base by base {
    // Override specific methods if needed
    override fun print() {
        println("Derived")
        base.print()
    }

    // message() automatically delegated to base
}

val base = BaseImpl()
val derived = Derived(base)

derived.print() // Derived, BaseImpl
println(derived.message()) // Hello from Base

// Real-world example
interface Repository {
    fun save(item: String)
    fun findAll(): List<String>
}

class DatabaseRepository : Repository {
    override fun save(item: String) {
        println("Saving to database: $item")
    }

    override fun findAll(): List<String> {
        return listOf("item1", "item2")
    }
}

class CachedRepository(
    private val repository: Repository
) : Repository by repository {
    private val cache = mutableListOf<String>()

    override fun findAll(): List<String> {
        if (cache.isEmpty()) {
            cache.addAll(repository.findAll())
        }
        return cache
    }
}
```
