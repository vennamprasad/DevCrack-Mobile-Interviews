## **Object-Oriented Programming**

### Q8. What are data classes and their benefits?

**Answer:**
Data classes are classes whose main purpose is to hold data. The compiler automatically generates:
- `equals()` and `hashCode()`
- `toString()`
- `copy()` function
- `componentN()` functions for destructuring

```kotlin
data class User(
    val name: String,
    val age: Int,
    val email: String = "" // Default parameter
)

val user1 = User("John", 25, "john@example.com")

// toString() - auto-generated
println(user1) // User(name=John, age=25, email=john@example.com)

// copy() - create modified copy
val user2 = user1.copy(age = 26)

// equals() and hashCode() - structural equality
val user3 = User("John", 25, "john@example.com")
println(user1 == user3) // true

// Destructuring
val (name, age, email) = user1
println("$name is $age years old")

// In collections
val users = setOf(user1, user3) // Only one element (equals)
```

**Requirements:**
- Primary constructor must have at least one parameter
- All parameters must be `val` or `var`
- Cannot be abstract, open, sealed, or inner

---

### Q9. What is the difference between open, abstract, and sealed classes?

**Answer:**

**Open Classes:**
```kotlin
// Default: classes are final
class Regular // Cannot be inherited

// Open: can be inherited
open class Base {
    open fun doSomething() {}
}

class Derived : Base() {
    override fun doSomething() {}
}
```

**Abstract Classes:**
```kotlin
abstract class Shape {
    abstract fun area(): Double

    // Can have concrete members
    fun describe() = "This is a shape"
}

class Circle(val radius: Double) : Shape() {
    override fun area() = Math.PI * radius * radius
}
```

**Sealed Classes:**
```kotlin
// Restricted class hierarchies
sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val message: String) : Result()
    object Loading : Result()
}

// Exhaustive when
fun handle(result: Result) = when (result) {
    is Result.Success -> println(result.data)
    is Result.Error -> println(result.message)
    Result.Loading -> println("Loading...")
    // No else needed - compiler knows all subclasses
}
```

| Type | Inheritance | Instantiation | Subclasses |
|------|-------------|---------------|------------|
| **open** | Can be inherited | Can be instantiated | Anywhere |
| **abstract** | Must be inherited | Cannot be instantiated | Anywhere |
| **sealed** | Restricted hierarchy | Cannot be instantiated | Same file/package |

---

### Q10. What are object declarations and companion objects?

**Answer:**

**Object Declaration (Singleton):**
```kotlin
object DatabaseManager {
    private var connection: Connection? = null

    fun connect() {
        connection = createConnection()
    }

    fun query(sql: String) {
        // Thread-safe singleton
    }
}

// Usage
DatabaseManager.connect()
DatabaseManager.query("SELECT * FROM users")
```

**Companion Object:**
```kotlin
class User(val name: String) {
    companion object {
        // Like static in Java
        const val MAX_AGE = 150

        fun create(name: String): User {
            return User(name)
        }
    }
}

// Usage
val maxAge = User.MAX_AGE
val user = User.create("John")

// Named companion
class MyClass {
    companion object Factory {
        fun create(): MyClass = MyClass()
    }
}

val instance = MyClass.create()
// or
val instance2 = MyClass.Factory.create()
```

**Object Expression (Anonymous class):**
```kotlin
val clickListener = object : OnClickListener {
    override fun onClick(view: View) {
        // Handle click
    }
}

// With properties
val counter = object {
    var count = 0
    fun increment() { count++ }
}
```

---

### Q11. What are interfaces in Kotlin?

**Answer:**
Interfaces can contain abstract methods and concrete implementations.

```kotlin
interface Clickable {
    // Abstract method
    fun click()

    // Default implementation
    fun showMessage() {
        println("Clicked!")
    }
}

interface Focusable {
    fun focus()
    fun showMessage() {
        println("Focused!")
    }
}

// Implement multiple interfaces
class Button : Clickable, Focusable {
    override fun click() {
        println("Button clicked")
    }

    override fun focus() {
        println("Button focused")
    }

    // Must override if conflict
    override fun showMessage() {
        super<Clickable>.showMessage() // Call specific implementation
        super<Focusable>.showMessage()
    }
}

// Interface with properties
interface User {
    val name: String // Abstract property
    val email: String
        get() = "$name@example.com" // Custom getter

    fun displayInfo() {
        println("User: $name, Email: $email")
    }
}

class Person(override val name: String) : User
```

---

### Q12. What is the difference between `interface` and `abstract class`?

**Answer:**

| Feature | Interface | Abstract Class |
|---------|-----------|----------------|
| **Multiple inheritance** | Yes | No (single inheritance) |
| **Constructors** | No | Yes |
| **State (properties)** | No backing fields | Yes, can have state |
| **Access modifiers** | Public only | Any modifier |
| **Implementation** | Can have default | Can have any |

```kotlin
// Interface - no state
interface Flyable {
    fun fly()
}

// Abstract class - can have state
abstract class Animal(val name: String) {
    abstract fun makeSound()

    fun sleep() {
        println("$name is sleeping")
    }
}

// Can implement multiple interfaces
class Bird(name: String) : Animal(name), Flyable {
    override fun makeSound() {
        println("Chirp!")
    }

    override fun fly() {
        println("$name is flying")
    }
}
```
