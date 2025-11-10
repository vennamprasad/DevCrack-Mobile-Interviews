# Kotlin Interview Questions & Answers

A comprehensive guide covering basic to advanced Kotlin concepts for Android developers preparing for technical interviews.

---

## **Table of Contents**
1. [Kotlin Basics](#kotlin-basics)
2. [Object-Oriented Programming](#object-oriented-programming)
3. [Null Safety](#null-safety)
4. [Functions & Lambdas](#functions--lambdas)
5. [Collections](#collections)
6. [Coroutines](#coroutines)
7. [Flow & Channels](#flow--channels)
8. [Generics](#generics)
9. [Delegation](#delegation)
10. [Advanced Features](#advanced-features)
11. [Best Practices](#best-practices)

---

## **What is Kotlin?**

Kotlin is a modern, statically typed programming language developed by JetBrains. It runs on the Java Virtual Machine (JVM) and can also be compiled to JavaScript or native code. Kotlin is fully interoperable with Java, meaning you can use Kotlin and Java code together in the same project.

### **Key Features of Kotlin**

- **Concise Syntax:** Reduces boilerplate code compared to Java
- **Null Safety:** Built-in null safety helps prevent null pointer exceptions
- **Extension Functions:** Allows you to extend existing classes with new functionality
- **Coroutines:** Simplifies asynchronous programming and concurrency
- **Smart Casts:** Automatically casts types when possible
- **Data Classes:** Simplifies the creation of classes for holding data
- **Interoperability:** 100% interoperable with Java libraries and frameworks

### **How is Kotlin Better Than Java?**

#### **1. Conciseness**
Kotlin code is more concise and expressive. Data classes, type inference, and default arguments reduce boilerplate.

**Java:**
```java
public class User {
    private String name;
    private int age;

    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }

    @Override
    public boolean equals(Object o) { /* ... */ }
    @Override
    public int hashCode() { /* ... */ }
    @Override
    public String toString() { /* ... */ }
}
```

**Kotlin:**
```kotlin
data class User(val name: String, val age: Int)
```

#### **2. Null Safety**
Kotlin's type system distinguishes between nullable and non-nullable types.

**Java:**
```java
String name = null; // Possible NullPointerException
int length = name.length(); // Crashes
```

**Kotlin:**
```kotlin
var name: String? = null // Nullable
val length = name?.length ?: 0 // Safe call with elvis operator
```

#### **3. Coroutines for Asynchronous Programming**
Kotlin provides coroutines for easy and efficient asynchronous programming.

#### **4. Extension Functions**
Add functionality to existing classes without inheritance.

**Kotlin:**
```kotlin
fun String.isEmail(): Boolean {
    return this.contains("@") && this.contains(".")
}

"test@example.com".isEmail() // true
```

---

## **Kotlin Basics**

### Q1. What are the basic data types in Kotlin?

**Answer:**
Kotlin has the following basic types:

**Numbers:**
- `Byte` (8-bit)
- `Short` (16-bit)
- `Int` (32-bit)
- `Long` (64-bit)
- `Float` (32-bit)
- `Double` (64-bit)

**Other:**
- `Boolean` (true/false)
- `Char` (16-bit Unicode character)
- `String` (immutable text)

```kotlin
val intNumber: Int = 42
val longNumber: Long = 42L
val floatNumber: Float = 3.14f
val doubleNumber: Double = 3.14
val char: Char = 'A'
val text: String = "Hello"
val isTrue: Boolean = true
```

**Important:** In Kotlin, everything is an object - there are no primitive types like in Java.

---

### Q2. What is the difference between `val` and `var`?

**Answer:**

| Feature | val | var |
|---------|-----|-----|
| **Mutability** | Immutable (read-only) | Mutable |
| **Reassignment** | Cannot be reassigned | Can be reassigned |
| **Java equivalent** | final variable | regular variable |
| **Best practice** | Prefer val | Use only when needed |

```kotlin
val name = "John" // Immutable
// name = "Jane" // ❌ Compilation error

var age = 25 // Mutable
age = 26 // ✅ OK

// Note: val reference is immutable, but object can be mutable
val list = mutableListOf(1, 2, 3)
list.add(4) // ✅ OK - list reference is same, content changed
// list = mutableListOf(5, 6) // ❌ Error - can't reassign
```

---

### Q3. What is type inference in Kotlin?

**Answer:**
Type inference allows the compiler to automatically determine the type of a variable based on its value.

```kotlin
// Explicit type
val name: String = "John"
val age: Int = 25

// Type inference (preferred)
val name = "John" // Inferred as String
val age = 25 // Inferred as Int

// When type inference is needed
val numbers = listOf(1, 2, 3) // List<Int>
val mixed = listOf(1, "two", 3.0) // List<Any>
```

**When to specify types explicitly:**
- Public API functions
- When the inferred type is not obvious
- When you need a specific type (e.g., `Long` instead of `Int`)

```kotlin
val number = 42 // Int
val longNumber: Long = 42 // Explicitly Long
```

---

### Q4. What are String templates in Kotlin?

**Answer:**
String templates allow embedding expressions inside strings using `$` or `${}`.

```kotlin
val name = "John"
val age = 25

// Simple variable
println("My name is $name") // "My name is John"

// Expression
println("Next year I'll be ${age + 1}") // "Next year I'll be 26"

// Complex expression
val user = User("Jane", 30)
println("User: ${user.name}, Age: ${user.age}")

// Escape $
println("Price: \$100") // "Price: $100"

// Multi-line strings
val json = """
    {
        "name": "$name",
        "age": $age
    }
""".trimIndent()
```

---

### Q5. What is the difference between `==` and `===`?

**Answer:**

| Operator | Purpose | Java equivalent |
|----------|---------|-----------------|
| `==` | Structural equality (content) | `.equals()` |
| `===` | Referential equality (same object) | `==` |

```kotlin
val a = "Hello"
val b = "Hello"
val c = a

// Structural equality
println(a == b) // true - same content
println(a == c) // true - same content

// Referential equality
println(a === b) // may be true (string pool)
println(a === c) // true - same reference

// With objects
data class Person(val name: String)
val p1 = Person("John")
val p2 = Person("John")
val p3 = p1

println(p1 == p2) // true - same content (data class equals)
println(p1 === p2) // false - different objects
println(p1 === p3) // true - same reference
```

---

### Q6. What are ranges in Kotlin?

**Answer:**
Ranges represent a sequence of values with a start and end.

```kotlin
// Closed range (includes both ends)
val numbers = 1..10 // 1 to 10 inclusive
val chars = 'a'..'z'

// Half-open range (excludes end)
val numbers2 = 1 until 10 // 1 to 9

// Downward range
val countdown = 10 downTo 1 // 10, 9, 8, ..., 1

// Step
val evens = 0..10 step 2 // 0, 2, 4, 6, 8, 10

// Check membership
if (5 in 1..10) {
    println("5 is in range")
}

// Iterate
for (i in 1..5) {
    println(i)
}

// With characters
for (c in 'a'..'e') {
    println(c) // a, b, c, d, e
}

// Reversed
for (i in 5 downTo 1) {
    println(i) // 5, 4, 3, 2, 1
}
```

---

### Q7. What are when expressions?

**Answer:**
`when` is Kotlin's replacement for switch statements, but much more powerful.

```kotlin
// Basic when
val number = 2
when (number) {
    1 -> println("One")
    2 -> println("Two")
    3 -> println("Three")
    else -> println("Other")
}

// Return value
val result = when (number) {
    1 -> "One"
    2 -> "Two"
    else -> "Other"
}

// Multiple conditions
when (number) {
    1, 2, 3 -> println("Small")
    in 4..10 -> println("Medium")
    else -> println("Large")
}

// Type checking
fun describe(obj: Any) = when (obj) {
    is String -> "String of length ${obj.length}"
    is Int -> "Integer"
    is List<*> -> "List with ${obj.size} items"
    else -> "Unknown"
}

// Without argument (replaces if-else)
val age = 25
when {
    age < 18 -> println("Minor")
    age < 65 -> println("Adult")
    else -> println("Senior")
}

// Smart cast in when
sealed class Result
data class Success(val data: String) : Result()
data class Error(val error: String) : Result()

fun handle(result: Result) = when (result) {
    is Success -> println("Data: ${result.data}") // Smart cast
    is Error -> println("Error: ${result.error}") // Smart cast
}
```

---

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

---

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

---

## **Functions & Lambdas**

### Q17. What are extension functions?

**Answer:**
Extension functions allow adding new functions to existing classes without modifying them.

```kotlin
// Extension function
fun String.isEmail(): Boolean {
    return contains("@") && contains(".")
}

// Usage
"test@example.com".isEmail() // true
"invalid".isEmail() // false

// Extension with generic
fun <T> List<T>.secondOrNull(): T? {
    return if (size >= 2) this[1] else null
}

listOf(1, 2, 3).secondOrNull() // 2

// Extension on nullable type
fun String?.orEmpty(): String {
    return this ?: ""
}

val name: String? = null
println(name.orEmpty()) // ""

// Extensions cannot access private members
class MyClass {
    private val secret = "hidden"
}

fun MyClass.getSecret() {
    // Cannot access 'secret' - compilation error
}

// Extensions are resolved statically
open class Parent
class Child : Parent()

fun Parent.foo() = "Parent"
fun Child.foo() = "Child"

val obj: Parent = Child()
println(obj.foo()) // "Parent" - based on declared type
```

---

### Q18. What are higher-order functions?

**Answer:**
Functions that take functions as parameters or return functions.

```kotlin
// Function that takes function as parameter
fun calculate(x: Int, y: Int, operation: (Int, Int) -> Int): Int {
    return operation(x, y)
}

// Usage
val sum = calculate(5, 3) { a, b -> a + b } // 8
val product = calculate(5, 3) { a, b -> a * b } // 15

// Function that returns function
fun makeMultiplier(factor: Int): (Int) -> Int {
    return { number -> number * factor }
}

val double = makeMultiplier(2)
println(double(5)) // 10

// Built-in higher-order functions
val numbers = listOf(1, 2, 3, 4, 5)

numbers.filter { it % 2 == 0 } // [2, 4]
numbers.map { it * 2 } // [2, 4, 6, 8, 10]
numbers.forEach { println(it) }
numbers.reduce { acc, i -> acc + i } // 15
```

---

### Q19. What are lambda expressions?

**Answer:**
Lambda expressions are anonymous functions that can be passed as values.

```kotlin
// Basic syntax
val sum = { a: Int, b: Int -> a + b }
println(sum(3, 5)) // 8

// With type inference
val numbers = listOf(1, 2, 3)
numbers.filter { it > 1 } // 'it' is implicit parameter

// Multiple parameters
val operation = { x: Int, y: Int, z: Int ->
    println("Computing...")
    x + y + z // Last expression is returned
}

// No parameters
val greet = { println("Hello!") }
greet()

// Trailing lambda (if last parameter)
fun repeat(times: Int, action: () -> Unit) {
    for (i in 1..times) action()
}

repeat(3) {
    println("Hello")
}

// Multiple lambdas - named arguments
fun process(
    onStart: () -> Unit,
    onComplete: () -> Unit
) {
    onStart()
    // Work...
    onComplete()
}

process(
    onStart = { println("Starting") },
    onComplete = { println("Done") }
)

// Lambda with receiver
fun buildString(action: StringBuilder.() -> Unit): String {
    val sb = StringBuilder()
    sb.action()
    return sb.toString()
}

val str = buildString {
    append("Hello")
    append(" ")
    append("World")
}
```

---

### Q20. What are inline functions?

**Answer:**
Inline functions copy the function body to the call site, eliminating function call overhead.

```kotlin
// Regular function (has call overhead)
fun regularFunction(block: () -> Unit) {
    block()
}

// Inline function (no call overhead)
inline fun inlineFunction(block: () -> Unit) {
    block()
}

// Benefits:
// 1. Performance - no function call overhead
// 2. Can use reified type parameters
// 3. Allow non-local returns

// Reified type parameters
inline fun <reified T> isType(value: Any): Boolean {
    return value is T // Can check type at runtime
}

println(isType<String>("Hello")) // true
println(isType<Int>("Hello")) // false

// Non-local returns
fun processItems(items: List<Int>) {
    items.forEach {
        if (it == 0) return // Returns from processItems (inline)
    }
}

// noinline - prevent inlining specific lambda
inline fun foo(
    inlined: () -> Unit,
    noinline notInlined: () -> Unit
) {
    inlined()
    notInlined()
}

// crossinline - forbid non-local returns
inline fun bar(crossinline block: () -> Unit) {
    val runnable = Runnable {
        block() // Cannot use non-local return
    }
}
```

**When to use inline:**
- Functions with lambda parameters (especially suspend functions)
- Small, frequently called functions
- When you need reified type parameters

**When NOT to use inline:**
- Large functions (increases code size)
- Functions stored in properties or returned
- Functions with many call sites

---

### Q21. What is the difference between `apply`, `run`, `let`, `also`, and `with`?

**Answer:**

| Function | Receiver | Return | Use case |
|----------|----------|--------|----------|
| `apply` | `this` | Context object | Configuration |
| `run` | `this` | Lambda result | Computation |
| `let` | `it` | Lambda result | Null-safe calls |
| `also` | `it` | Context object | Side effects |
| `with` | `this` | Lambda result | Group calls |

**apply** - Configure object:
```kotlin
val user = User().apply {
    name = "John"
    age = 25
    email = "john@example.com"
}
```

**run** - Compute value:
```kotlin
val result = user.run {
    "$name is $age years old"
}
```

**let** - Null-safe operations:
```kotlin
user?.let {
    println("User: ${it.name}")
    sendEmail(it.email)
}
```

**also** - Additional operations:
```kotlin
val numbers = mutableListOf(1, 2, 3)
    .also { println("Before: $it") }
    .also { it.add(4) }
    .also { println("After: $it") }
```

**with** - Group function calls:
```kotlin
with(user) {
    println(name)
    println(age)
    println(email)
}
```

**Complete Example:**
```kotlin
data class Person(var name: String = "", var age: Int = 0)

// apply - returns Person
val person1 = Person().apply {
    name = "Alice"
    age = 25
}

// run - returns String
val desc = person1.run {
    "$name is $age years old"
}

// let - returns Int?
val nameLength = person1.let {
    it.name.length
}

// also - returns Person
val person2 = Person().also {
    it.name = "Bob"
    println("Created person: ${it.name}")
}

// with - returns Unit
with(person1) {
    println(name)
    println(age)
}
```

---

## **Collections**

### Q22. What are the different collection types in Kotlin?

**Answer:**

**Immutable Collections (Read-only):**
```kotlin
// List - ordered, allows duplicates
val list = listOf(1, 2, 3, 2)
val emptyList = emptyList<Int>()

// Set - unordered, unique elements
val set = setOf(1, 2, 3, 2) // [1, 2, 3]
val emptySet = emptySet<Int>()

// Map - key-value pairs
val map = mapOf(
    "name" to "John",
    "age" to "25"
)
val emptyMap = emptyMap<String, String>()
```

**Mutable Collections:**
```kotlin
// Mutable List
val mutableList = mutableListOf(1, 2, 3)
mutableList.add(4)
mutableList.remove(2)

// Mutable Set
val mutableSet = mutableSetOf(1, 2, 3)
mutableSet.add(4)

// Mutable Map
val mutableMap = mutableMapOf("a" to 1)
mutableMap["b"] = 2
mutableMap.remove("a")
```

**Specific Implementations:**
```kotlin
// ArrayList
val arrayList = arrayListOf(1, 2, 3)

// LinkedList
val linkedList = LinkedList<Int>()

// HashSet
val hashSet = hashSetOf(1, 2, 3)

// LinkedHashSet (maintains insertion order)
val linkedHashSet = linkedSetOf(1, 2, 3)

// HashMap
val hashMap = hashMapOf("a" to 1)

// LinkedHashMap (maintains insertion order)
val linkedHashMap = linkedMapOf("a" to 1)
```

---

### Q23. What are collection operations in Kotlin?

**Answer:**

**Transformation:**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// map - transform elements
numbers.map { it * 2 } // [2, 4, 6, 8, 10]

// mapIndexed - with index
numbers.mapIndexed { index, value ->
    "$index: $value"
}

// flatMap - flatten nested collections
listOf(listOf(1, 2), listOf(3, 4))
    .flatMap { it } // [1, 2, 3, 4]

// flatten
listOf(listOf(1, 2), listOf(3, 4))
    .flatten() // [1, 2, 3, 4]
```

**Filtering:**
```kotlin
numbers.filter { it % 2 == 0 } // [2, 4]
numbers.filterNot { it % 2 == 0 } // [1, 3, 5]
numbers.filterIndexed { index, value -> index % 2 == 0 }

// Partition - split into two lists
val (evens, odds) = numbers.partition { it % 2 == 0 }
```

**Aggregation:**
```kotlin
numbers.sum() // 15
numbers.average() // 3.0
numbers.max() // 5
numbers.min() // 1
numbers.count() // 5
numbers.count { it % 2 == 0 } // 2

// reduce - accumulate from first element
numbers.reduce { acc, i -> acc + i } // 15

// fold - accumulate with initial value
numbers.fold(10) { acc, i -> acc + i } // 25
```

**Grouping:**
```kotlin
val words = listOf("a", "abc", "ab", "def", "abcd")

// groupBy - create map of groups
words.groupBy { it.length }
// {1=[a], 3=[abc, def], 2=[ab], 4=[abcd]}

// associateBy - create map by key
words.associateBy { it.length }
// {1=a, 3=def, 2=ab, 4=abcd}

// associate - create map with transform
words.associate { it to it.length }
// {a=1, abc=3, ab=2, def=3, abcd=4}
```

**Ordering:**
```kotlin
numbers.sorted() // [1, 2, 3, 4, 5]
numbers.sortedDescending() // [5, 4, 3, 2, 1]
words.sortedBy { it.length }
words.sortedByDescending { it.length }
```

---

### Q24. What are sequences and when to use them?

**Answer:**
Sequences are lazily evaluated collections, processing elements one by one instead of creating intermediate collections.

```kotlin
// List (eager) - creates intermediate collections
val result1 = listOf(1, 2, 3, 4, 5)
    .map { it * 2 } // Creates new list [2, 4, 6, 8, 10]
    .filter { it > 5 } // Creates new list [6, 8, 10]
    .sum() // 24

// Sequence (lazy) - no intermediate collections
val result2 = listOf(1, 2, 3, 4, 5)
    .asSequence()
    .map { it * 2 }
    .filter { it > 5 }
    .sum() // 24

// Order of operations differs
val numbers = listOf(1, 2, 3, 4, 5)

// List: map all, then filter all
numbers
    .map {
        println("map $it")
        it * 2
    }
    .filter {
        println("filter $it")
        it > 5
    }
// Output: map 1, map 2, ..., map 5, filter 2, filter 4, ..., filter 10

// Sequence: process each element completely
numbers
    .asSequence()
    .map {
        println("map $it")
        it * 2
    }
    .filter {
        println("filter $it")
        it > 5
    }
    .toList()
// Output: map 1, filter 2, map 2, filter 4, ...

// Generate infinite sequences
val infiniteNumbers = generateSequence(1) { it + 1 }
val first10 = infiniteNumbers.take(10).toList()

// When to use sequences:
// 1. Large collections
// 2. Multiple operations
// 3. Want lazy evaluation
// 4. Don't need all results immediately
```

---

## **Coroutines**

### Q25. What are coroutines in Kotlin?

**Answer:**
Coroutines are lightweight threads that allow writing asynchronous code sequentially.

```kotlin
// Basic coroutine
import kotlinx.coroutines.*

fun main() = runBlocking {
    launch {
        delay(1000L)
        println("World!")
    }
    println("Hello")
}
// Output: Hello, World! (after 1 second)

// Structured concurrency
suspend fun doWork() = coroutineScope {
    launch {
        delay(1000L)
        println("Task 1")
    }
    launch {
        delay(500L)
        println("Task 2")
    }
}

// Async/await for results
suspend fun fetchUser(): User {
    return coroutineScope {
        val name = async { fetchUserName() }
        val age = async { fetchUserAge() }
        User(name.await(), age.await())
    }
}
```

**Key Concepts:**
- **Suspend functions:** Can be paused and resumed
- **Coroutine Scope:** Defines lifecycle
- **Dispatchers:** Control which thread executes coroutine
- **Jobs:** Handle for coroutine lifecycle

---

### Q26. What is the difference between `suspend` functions and regular functions?

**Answer:**

```kotlin
// Regular function - blocks thread
fun fetchData(): String {
    Thread.sleep(1000) // Blocks current thread
    return "Data"
}

// Suspend function - suspends coroutine
suspend fun fetchDataSuspend(): String {
    delay(1000) // Suspends coroutine, doesn't block thread
    return "Data"
}

// Suspend functions can call other suspend functions
suspend fun processData() {
    val data = fetchDataSuspend() // Can call suspend function
    // Process data
}

// Can only be called from coroutine or another suspend function
fun normalFunction() {
    // fetchDataSuspend() // ❌ Error - can't call suspend function

    runBlocking {
        fetchDataSuspend() // ✅ OK - inside coroutine
    }
}

// Suspend functions don't block threads
suspend fun example() {
    println("Start: ${Thread.currentThread().name}")
    delay(1000) // Suspends, other coroutines can run
    println("End: ${Thread.currentThread().name}") // May be different thread
}
```

**Key Differences:**
- Suspend functions can be paused and resumed
- Don't block threads
- Can only be called from coroutines
- Marked with `suspend` keyword
- Compiled into state machine by Kotlin compiler

---

### Q27. What is structured concurrency in Kotlin coroutines?

**Answer:**
Structured concurrency ties child coroutines to a parent scope, ensuring proper lifecycle management.

```kotlin
// Structured concurrency ensures:
// 1. Parent waits for all children
// 2. Cancellation propagates
// 3. Exceptions propagate

suspend fun fetchUserData() = coroutineScope {
    // All launched coroutines are children
    val profile = async { fetchProfile() }
    val posts = async { fetchPosts() }
    val friends = async { fetchFriends() }

    // coroutineScope waits for all children
    UserData(
        profile.await(),
        posts.await(),
        friends.await()
    )
} // Won't return until all children complete

// Cancellation propagation
suspend fun example() = coroutineScope {
    val job1 = launch {
        repeat(100) {
            println("Job 1: $it")
            delay(100)
        }
    }

    val job2 = launch {
        repeat(100) {
            println("Job 2: $it")
            delay(100)
        }
    }

    delay(500)
    cancel() // Cancels both job1 and job2
}

// Exception propagation
suspend fun failing() = coroutineScope {
    launch {
        delay(100)
        throw Exception("Failed!") // Cancels parent and siblings
    }

    launch {
        delay(200)
        println("This won't print")
    }
}
```

---

### Q28. What is the difference between `launch` and `async`?

**Answer:**

**launch:**
```kotlin
// Fire and forget
// Returns Job
// For side effects

val job: Job = scope.launch {
    println("Doing work")
    delay(1000)
    println("Done")
}

job.cancel() // Can cancel
job.join() // Can wait for completion
```

**async:**
```kotlin
// Returns result
// Returns Deferred<T>
// For computations

val deferred: Deferred<String> = scope.async {
    delay(1000)
    "Result"
}

val result = deferred.await() // Get result
```

**Comparison:**
```kotlin
suspend fun example() = coroutineScope {
    // launch - no return value
    launch {
        val data = fetchData()
        updateUI(data)
    }

    // async - returns value
    val result1 = async { computeValue1() }
    val result2 = async { computeValue2() }
    val sum = result1.await() + result2.await()

    // Parallel execution
    val results = listOf(
        async { task1() },
        async { task2() },
        async { task3() }
    ).awaitAll()
}
```

| Feature | launch | async |
|---------|--------|-------|
| **Return type** | Job | Deferred<T> |
| **Purpose** | Side effects | Computation |
| **Get result** | N/A | await() |
| **Exception handling** | Crashes parent | Exception stored, thrown on await() |

---

### Q29. What is `withContext` and when to use it?

**Answer:**
`withContext` switches the dispatcher for a block of code while preserving structured concurrency.

```kotlin
suspend fun fetchData(): String = withContext(Dispatchers.IO) {
    // Runs on IO dispatcher
    val response = api.fetch()
    response.data
} // Automatically switches back

// Use cases:
suspend fun loadUser(userId: String) {
    // Default dispatcher
    showLoading()

    // Switch to IO for network/database
    val user = withContext(Dispatchers.IO) {
        database.getUser(userId)
    }

    // Back to original dispatcher
    updateUI(user)
}

// vs launch/async
fun badExample() {
    scope.launch {
        // Create new coroutine (extra overhead)
        val result = async(Dispatchers.IO) {
            fetchData()
        }.await()
    }
}

fun goodExample() {
    scope.launch {
        // Just switch dispatcher (lighter)
        val result = withContext(Dispatchers.IO) {
            fetchData()
        }
    }
}

// Multiple withContext calls
suspend fun complexOperation() {
    // CPU-intensive work
    val processed = withContext(Dispatchers.Default) {
        processData()
    }

    // Save to database
    withContext(Dispatchers.IO) {
        database.save(processed)
    }

    // Update UI
    withContext(Dispatchers.Main) {
        updateUI(processed)
    }
}
```

---

### Q30. How does cancellation work in coroutines?

**Answer:**
Cancellation is cooperative - coroutines must check for cancellation.

```kotlin
// Cancel a coroutine
val job = scope.launch {
    repeat(1000) {
        println("Working $it")
        delay(100)
    }
}

delay(500)
job.cancel() // Request cancellation
job.join() // Wait for cancellation

// Or combine
job.cancelAndJoin()

// Checking cancellation
suspend fun doWork() {
    repeat(1000) { i ->
        // delay() checks cancellation automatically
        delay(100)

        // For non-suspending loops, check manually
        if (!isActive) {
            throw CancellationException()
        }
        // or
        ensureActive()

        println("Work $i")
    }
}

// Non-cancellable work
suspend fun important() {
    withContext(NonCancellable) {
        // This block ignores cancellation
        saveToDatabase()
        cleanupResources()
    }
}

// Finally block for cleanup
val job = launch {
    try {
        repeat(1000) {
            delay(100)
        }
    } finally {
        withContext(NonCancellable) {
            cleanup() // Always executes
        }
    }
}

// Timeout
withTimeout(5000) {
    // Cancelled if takes more than 5 seconds
    longRunningOperation()
}

// Timeout or null (doesn't throw)
val result = withTimeoutOrNull(5000) {
    longRunningOperation()
} // null if timeout
```

---

### Q31. What is a SupervisorJob and when to use it?

**Answer:**
SupervisorJob prevents failure of one child from cancelling siblings.

```kotlin
// Regular Job - one failure cancels all
val scope = CoroutineScope(Job())
scope.launch {
    try {
        throw Exception("Failed!")
    } catch (e: Exception) {
        // Even with try-catch, siblings are cancelled
    }
}
scope.launch {
    // This gets cancelled when sibling fails
    delay(1000)
    println("Won't print")
}

// SupervisorJob - failures are isolated
val supervisorScope = CoroutineScope(SupervisorJob())
supervisorScope.launch {
    throw Exception("Failed!")
}
supervisorScope.launch {
    // This continues running
    delay(1000)
    println("Will print")
}

// SupervisorScope function
suspend fun example() = supervisorScope {
    launch {
        throw Exception("Failed!")
    }

    launch {
        delay(1000)
        println("Still running")
    }
}

// Use case: Independent tasks
class ViewModel : ViewModel() {
    private val viewModelScope = CoroutineScope(
        SupervisorJob() + Dispatchers.Main
    )

    fun fetchData() {
        // Each fetch is independent
        viewModelScope.launch {
            fetchUsers() // If this fails...
        }

        viewModelScope.launch {
            fetchPosts() // ...this continues
        }
    }
}

// Exception handling with SupervisorJob
val scope = CoroutineScope(SupervisorJob())
scope.launch {
    try {
        riskyOperation()
    } catch (e: Exception) {
        handleError(e)
    }
}
```

---

### Q32. What are Dispatchers in Kotlin coroutines?

**Answer:**
Dispatchers determine which thread(s) a coroutine uses.

```kotlin
// Dispatchers.Main - UI thread (Android)
launch(Dispatchers.Main) {
    updateUI()
}

// Dispatchers.IO - I/O operations (network, files, database)
launch(Dispatchers.IO) {
    val data = database.query()
    val response = api.fetch()
}

// Dispatchers.Default - CPU-intensive work
launch(Dispatchers.Default) {
    val result = complexCalculation()
    processLargeData()
}

// Dispatchers.Unconfined - Don't recommend (advanced)
launch(Dispatchers.Unconfined) {
    // Runs in caller thread until first suspension
}

// Custom dispatcher
val customDispatcher = Executors.newFixedThreadPool(4)
    .asCoroutineDispatcher()

launch(customDispatcher) {
    // Work on custom thread pool
}

customDispatcher.close() // Remember to close

// Real-world example
suspend fun loadUser(id: String): User {
    return withContext(Dispatchers.IO) {
        // Network call on IO dispatcher
        val response = api.getUser(id)

        // Parse on Default dispatcher
        withContext(Dispatchers.Default) {
            parseUser(response)
        }
    }
}
```

| Dispatcher | Thread Pool | Use Case |
|------------|-------------|----------|
| **Main** | UI thread | UI updates |
| **IO** | 64 threads | Network, file, database |
| **Default** | CPU cores | Heavy computation |
| **Unconfined** | Varies | Special cases only |

---

## **Flow & Channels**

### Q33. What is Flow in Kotlin?

**Answer:**
Flow is a cold asynchronous stream that emits values sequentially.

```kotlin
// Create Flow
fun numbersFlow(): Flow<Int> = flow {
    for (i in 1..5) {
        delay(100)
        emit(i) // Emit values
    }
}

// Collect Flow
suspend fun example() {
    numbersFlow().collect { value ->
        println(value) // 1, 2, 3, 4, 5
    }
}

// Flow builders
val flow1 = flowOf(1, 2, 3) // From values
val flow2 = listOf(1, 2, 3).asFlow() // From collection
val flow3 = flow { emit(1) } // Custom

// Flow is cold - doesn't run until collected
val numbers = flow {
    println("Flow started")
    emit(1)
}
// "Flow started" not printed yet

numbers.collect { println(it) }
// Now "Flow started" prints, then 1
```

---

### Q34. What is the difference between cold and hot streams?

**Answer:**

**Cold Streams (Flow):**
```kotlin
// Each collector gets own execution
val coldFlow = flow {
    println("Flow started")
    emit(1)
    emit(2)
}

// First collector
coldFlow.collect { println("Collector 1: $it") }
// Output:
// Flow started
// Collector 1: 1
// Collector 1: 2

// Second collector (starts from beginning)
coldFlow.collect { println("Collector 2: $it") }
// Output:
// Flow started (again!)
// Collector 2: 1
// Collector 2: 2
```

**Hot Streams (SharedFlow, StateFlow, Channel):**
```kotlin
// SharedFlow - hot stream
val hotFlow = MutableSharedFlow<Int>()

// Emit values
scope.launch {
    hotFlow.emit(1)
    hotFlow.emit(2)
}

// Collectors share same stream
scope.launch {
    hotFlow.collect { println("Collector 1: $it") }
}

scope.launch {
    hotFlow.collect { println("Collector 2: $it") }
}
// Both collectors receive same values
```

| Feature | Cold (Flow) | Hot (SharedFlow/StateFlow) |
|---------|-------------|----------------------------|
| **Execution** | Per collector | Shared |
| **Start** | On collect | Immediately |
| **Values** | All from start | Only new values |
| **Use case** | API calls, DB queries | Events, state |

---

### Q35. What is StateFlow vs SharedFlow?

**Answer:**

**StateFlow:**
```kotlin
// Always has a value
val _state = MutableStateFlow(0)
val state: StateFlow<Int> = _state.asStateFlow()

// Update
_state.value = 1
_state.update { it + 1 }

// Collect (always gets current value)
state.collect { value ->
    println(value) // Immediately prints current value, then updates
}

// Properties
state.value // Get current value synchronously
```

**SharedFlow:**
```kotlin
// May not have initial value
val _events = MutableSharedFlow<Event>(
    replay = 1, // Cache last N values
    extraBufferCapacity = 10, // Buffer for slow collectors
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)
val events: SharedFlow<Event> = _events.asSharedFlow()

// Emit
_events.emit(Event.Click)
_events.tryEmit(Event.Click) // Non-suspending

// Collect
events.collect { event ->
    handleEvent(event)
}
```

**Comparison:**
```kotlin
// StateFlow - for state
class ViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState.Loading)
    val uiState = _uiState.asStateFlow()

    fun loadData() {
        _uiState.value = UiState.Success(data)
    }
}

// SharedFlow - for events
class ViewModel : ViewModel() {
    private val _events = MutableSharedFlow<Event>()
    val events = _events.asSharedFlow()

    fun onClick() {
        viewModelScope.launch {
            _events.emit(Event.Navigate)
        }
    }
}
```

| Feature | StateFlow | SharedFlow |
|---------|-----------|------------|
| **Initial value** | Required | Optional |
| **Replay** | Always 1 | Configurable |
| **Current value** | Yes (.value) | No |
| **Use case** | UI state | One-time events |
| **Conflation** | Yes | Configurable |

---

### Q36. What are Flow operators?

**Answer:**

**Transformation:**
```kotlin
val numbers = flowOf(1, 2, 3, 4, 5)

// map
numbers.map { it * 2 }
    .collect { println(it) } // 2, 4, 6, 8, 10

// filter
numbers.filter { it % 2 == 0 }
    .collect { println(it) } // 2, 4

// transform - custom transformation
numbers.transform { value ->
    emit(value)
    emit(value * 2)
}.collect { println(it) } // 1, 2, 2, 4, 3, 6, ...
```

**Intermediate operators:**
```kotlin
// take - limit number of values
numbers.take(3).collect { println(it) } // 1, 2, 3

// drop - skip first N values
numbers.drop(2).collect { println(it) } // 3, 4, 5

// debounce - emit only after quiet period
searchQuery
    .debounce(300)
    .collect { query ->
        search(query)
    }

// distinctUntilChanged - skip consecutive duplicates
flow { emit(1); emit(1); emit(2); emit(2) }
    .distinctUntilChanged()
    .collect { println(it) } // 1, 2

// onEach - perform action on each value
numbers
    .onEach { println("Processing $it") }
    .collect()
```

**Terminal operators:**
```kotlin
// collect - consume values
numbers.collect { value -> }

// first - get first value
val first = numbers.first()

// toList - collect to list
val list = numbers.toList()

// reduce - accumulate
val sum = numbers.reduce { acc, value -> acc + value }

// fold - accumulate with initial
val sum2 = numbers.fold(0) { acc, value -> acc + value }
```

**Exception handling:**
```kotlin
flow {
    emit(1)
    throw Exception("Error")
}
    .catch { e ->
        println("Caught: ${e.message}")
        emit(0) // Can emit recovery value
    }
    .collect { println(it) }

// onCompletion
numbers
    .onCompletion { cause ->
        if (cause != null) {
            println("Flow completed with error: $cause")
        } else {
            println("Flow completed successfully")
        }
    }
    .collect()
```

---

### Q37. What are flatMap operators in Flow?

**Answer:**

**flatMapConcat** - Sequential:
```kotlin
// Process flows sequentially
flowOf(1, 2, 3)
    .flatMapConcat { value ->
        flow {
            emit("$value-a")
            delay(100)
            emit("$value-b")
        }
    }
    .collect { println(it) }
// Output: 1-a, 1-b, 2-a, 2-b, 3-a, 3-b
```

**flatMapMerge** - Concurrent:
```kotlin
// Process flows concurrently
flowOf(1, 2, 3)
    .flatMapMerge(concurrency = 2) { value ->
        flow {
            emit("$value-a")
            delay(100)
            emit("$value-b")
        }
    }
    .collect { println(it) }
// Output: 1-a, 2-a, 1-b, 2-b, 3-a, 3-b (interleaved)
```

**flatMapLatest** - Cancel previous:
```kotlin
// Cancel previous flow when new value arrives
searchQuery
    .flatMapLatest { query ->
        searchDatabase(query)
    }
    .collect { results ->
        updateUI(results)
    }
// If new query arrives, previous search is cancelled
```

**Real-world examples:**
```kotlin
// Sequential API calls
fun getUsers(): Flow<User> = flow {
    val userIds = getUserIds()
    userIds
        .asFlow()
        .flatMapConcat { id ->
            getUserDetails(id)
        }
        .collect { emit(it) }
}

// Parallel API calls
fun getUsersParallel(): Flow<User> =
    getUserIds()
        .asFlow()
        .flatMapMerge(concurrency = 5) { id ->
            getUserDetails(id)
        }

// Search with cancellation
val searchResults = searchQuery
    .debounce(300)
    .flatMapLatest { query ->
        searchApi(query)
    }
```

---

### Q38. What are Channels and when to use them?

**Answer:**
Channels are hot streams for communication between coroutines (like queues).

```kotlin
// Create channel
val channel = Channel<Int>()

// Producer
launch {
    for (i in 1..5) {
        channel.send(i)
        delay(100)
    }
    channel.close() // Signal completion
}

// Consumer
launch {
    for (value in channel) {
        println(value)
    }
}

// Channel types
val unlimited = Channel<Int>(Channel.UNLIMITED) // Unbounded
val buffered = Channel<Int>(10) // Buffer of 10
val rendezvous = Channel<Int>() // No buffer (default)
val conflated = Channel<Int>(Channel.CONFLATED) // Keeps only latest

// Produce/consume pattern
fun produceNumbers() = produce {
    repeat(5) { send(it) }
}

suspend fun consumeNumbers() {
    produceNumbers().consumeEach { value ->
        println(value)
    }
}

// Use cases:
// 1. Producer-consumer pattern
val workChannel = Channel<Work>()

// Multiple producers
repeat(5) { workerId ->
    launch {
        generateWork(workerId).forEach { work ->
            workChannel.send(work)
        }
    }
}

// Multiple consumers
repeat(3) { consumerId ->
    launch {
        for (work in workChannel) {
            processWork(consumerId, work)
        }
    }
}

// 2. Pipeline
fun CoroutineScope.produceSquares() = produce {
    repeat(5) { send(it * it) }
}

fun CoroutineScope.processSquares(
    input: ReceiveChannel<Int>
) = produce {
    for (value in input) {
        send(value * 2)
    }
}

val squares = produceSquares()
val processed = processSquares(squares)
processed.consumeEach { println(it) }
```

**Flow vs Channel:**

| Feature | Flow | Channel |
|---------|------|---------|
| **Type** | Cold | Hot |
| **Start** | On collect | Immediately |
| **Collectors** | Multiple (independent) | Multiple (shared) |
| **Use case** | Streams, transformations | Communication, queues |

---

## **Generics**

### Q39. What are generics in Kotlin?

**Answer:**
Generics allow writing type-safe code that works with any type.

```kotlin
// Generic class
class Box<T>(val value: T)

val intBox = Box(42) // Box<Int>
val stringBox = Box("Hello") // Box<String>

// Generic function
fun <T> printValue(value: T) {
    println(value)
}

printValue(42) // Type inferred
printValue("Hello")

// Generic with constraints
fun <T : Number> sum(a: T, b: T): Double {
    return a.toDouble() + b.toDouble()
}

// Multiple type parameters
class Pair<A, B>(val first: A, val second: B)
val pair = Pair(1, "one")

// Generic interface
interface Repository<T> {
    fun save(item: T)
    fun findById(id: Int): T?
}

class UserRepository : Repository<User> {
    override fun save(item: User) { }
    override fun findById(id: Int): User? = null
}
```

---

### Q40. What is variance (covariance and contravariance)?

**Answer:**

**Covariance (`out`)** - Producer:
```kotlin
// Producer - can only produce T, not consume
interface Producer<out T> {
    fun produce(): T
    // fun consume(item: T) // ❌ Error - can't consume
}

// Subtyping preserved
open class Animal
class Dog : Animal()

val dogProducer: Producer<Dog> = object : Producer<Dog> {
    override fun produce() = Dog()
}

// ✅ OK - covariant
val animalProducer: Producer<Animal> = dogProducer

// Real example: List<out T>
val dogs: List<Dog> = listOf()
val animals: List<Animal> = dogs // ✅ OK
```

**Contravariance (`in`)** - Consumer:
```kotlin
// Consumer - can only consume T, not produce
interface Consumer<in T> {
    fun consume(item: T)
    // fun produce(): T // ❌ Error - can't produce
}

// Subtyping reversed
val animalConsumer: Consumer<Animal> = object : Consumer<Animal> {
    override fun consume(item: Animal) { }
}

// ✅ OK - contravariant
val dogConsumer: Consumer<Dog> = animalConsumer

// Real example: Comparable<in T>
interface Comparable<in T> {
    fun compareTo(other: T): Int
}
```

**Invariance** - Neither:
```kotlin
// Can both produce and consume
interface Box<T> {
    fun set(item: T)
    fun get(): T
}

// Not covariant or contravariant
val dogBox: Box<Dog> = object : Box<Dog> {
    var item: Dog? = null
    override fun set(item: Dog) { this.item = item }
    override fun get() = item!!
}

// ❌ Error - invariant
// val animalBox: Box<Animal> = dogBox

// Real example: MutableList<T>
val dogsList: MutableList<Dog> = mutableListOf()
// val animalsList: MutableList<Animal> = dogsList // ❌ Error
```

**Summary:**
- `out T` - Covariant - Producer - Can only return T
- `in T` - Contravariant - Consumer - Can only accept T
- `T` - Invariant - Both - Can do both

---

### Q41. What are star-projections?

**Answer:**
Star-projection (`*`) represents an unknown type.

```kotlin
// With List<*>
val list: List<*> = listOf(1, 2, 3)
// Can read as Any?
val item: Any? = list.first()
// Cannot add (unknown type)
// list.add(1) // ❌ Error - MutableList needed

// Function accepting any List
fun printList(list: List<*>) {
    for (item in list) {
        println(item) // item is Any?
    }
}

printList(listOf(1, 2, 3))
printList(listOf("a", "b", "c"))

// With multiple type parameters
class Pair<A, B>

val pair: Pair<*, *> = Pair(1, "one")

// Real-world use case
fun getListSize(list: List<*>): Int {
    return list.size // OK - doesn't depend on type
}

// Star-projection vs Any
val listAny: List<Any> = listOf(1, "two", 3.0) // List of Any
val listStar: List<*> = listOf(1, 2, 3) // Unknown type

// Use when:
// 1. Don't care about type
// 2. Only need type-independent operations
// 3. Want to accept any parameterized type
```

---

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

---

## **Advanced Features**

### Q44. What are inline classes (value classes)?

**Answer:**
Value classes wrap a single value and can be inlined to avoid heap allocation.

```kotlin
@JvmInline
value class UserId(val id: Long)

@JvmInline
value class Password(val value: String)

// Type safety
fun getUser(userId: UserId): User { }
fun setPassword(password: Password) { }

// Cannot accidentally mix types
val userId = UserId(123)
val password = Password("secret")

// getUser(123) // ❌ Error - need UserId
getUser(userId) // ✅ OK

// Runtime performance - no wrapper object
// At runtime: getUser(123L) - no UserId object created

// Benefits:
// 1. Type safety
// 2. No runtime overhead
// 3. Named types

// Restrictions:
// - Must have single property
// - Must be val
// - Cannot have init block
// - Cannot extend other classes

// Use cases:
@JvmInline
value class Meters(val value: Double)

@JvmInline
value class Kilometers(val value: Double)

fun distance(meters: Meters): Kilometers {
    return Kilometers(meters.value / 1000)
}
```

---

### Q45. What is `reified` type parameter?

**Answer:**
`reified` allows access to generic type at runtime in inline functions.

```kotlin
// Without reified - type erased at runtime
fun <T> genericFunction(value: Any): Boolean {
    // return value is T // ❌ Error - cannot check type
    return false
}

// With reified - type available at runtime
inline fun <reified T> isType(value: Any): Boolean {
    return value is T // ✅ OK
}

println(isType<String>("Hello")) // true
println(isType<Int>("Hello")) // false

// Real-world examples:

// 1. Type-safe casting
inline fun <reified T> Any.safeCast(): T? {
    return this as? T
}

val number: Int? = "123".safeCast() // null

// 2. Starting Activity in Android
inline fun <reified T : Activity> Context.startActivity() {
    val intent = Intent(this, T::class.java)
    startActivity(intent)
}

// Usage
startActivity<MainActivity>()

// 3. JSON parsing
inline fun <reified T> String.fromJson(): T {
    return Gson().fromJson(this, T::class.java)
}

val user: User = jsonString.fromJson()

// 4. Type filtering
inline fun <reified T> List<*>.filterIsInstanceTyped(): List<T> {
    return filterIsInstance<T>()
}

val mixed: List<Any> = listOf(1, "two", 3, "four")
val strings: List<String> = mixed.filterIsInstanceTyped()
// ["two", "four"]
```

---

### Q46. What are sealed interfaces?

**Answer:**
Sealed interfaces restrict implementation to known subclasses (like sealed classes).

```kotlin
// Sealed class
sealed class Result {
    data class Success(val data: String) : Result()
    data class Error(val message: String) : Result()
}

// Sealed interface (Kotlin 1.5+)
sealed interface DataState

data class Loading(val progress: Int) : DataState
data class Success(val data: String) : DataState
data class Error(val error: Throwable) : DataState

// Can also implement in enums
enum class NetworkState : DataState {
    IDLE,
    CONNECTING
}

// Benefits over sealed class:
// 1. Can implement multiple sealed interfaces
sealed interface UiState
sealed interface LoadingState

data class LoadingData(val progress: Int) : UiState, LoadingState

// 2. More flexible hierarchy
sealed interface Shape {
    val area: Double
}

sealed interface ColoredShape : Shape {
    val color: String
}

data class Circle(
    override val area: Double,
    override val color: String
) : ColoredShape

// Exhaustive when
fun handle(state: DataState) = when (state) {
    is Loading -> println("Loading: ${state.progress}%")
    is Success -> println("Success: ${state.data}")
    is Error -> println("Error: ${state.error}")
    NetworkState.IDLE -> println("Idle")
    NetworkState.CONNECTING -> println("Connecting")
    // Compiler ensures all cases covered
}
```

---

### Q47. What are DSLs (Domain-Specific Languages) in Kotlin?

**Answer:**
DSLs use Kotlin features to create readable, domain-specific code.

```kotlin
// Lambda with receiver
fun buildString(action: StringBuilder.() -> Unit): String {
    val sb = StringBuilder()
    sb.action()
    return sb.toString()
}

val result = buildString {
    append("Hello")
    append(" ")
    append("World")
}

// HTML DSL example
class HTML {
    fun body(init: Body.() -> Unit) {
        Body().init()
    }
}

class Body {
    fun h1(text: String) {
        println("<h1>$text</h1>")
    }
}

fun html(init: HTML.() -> Unit): HTML {
    val html = HTML()
    html.init()
    return html
}

// Usage
html {
    body {
        h1("Title")
        h1("Subtitle")
    }
}

// Type-safe builders for configuration
class DatabaseConfig {
    var host: String = "localhost"
    var port: Int = 5432
    var username: String = ""
    var password: String = ""
}

fun database(init: DatabaseConfig.() -> Unit): DatabaseConfig {
    return DatabaseConfig().apply(init)
}

val config = database {
    host = "db.example.com"
    port = 3306
    username = "admin"
    password = "secret"
}

// Extension functions for DSL
@DslMarker
annotation class MyDslMarker

@MyDslMarker
class Router {
    private val routes = mutableMapOf<String, () -> Unit>()

    fun get(path: String, handler: () -> Unit) {
        routes[path] = handler
    }
}

fun router(init: Router.() -> Unit): Router {
    return Router().apply(init)
}

val myRouter = router {
    get("/users") { println("Get users") }
    get("/posts") { println("Get posts") }
}
```

---

### Q48. What is `tailrec` and tail recursion?

**Answer:**
`tailrec` optimizes tail-recursive functions into loops.

```kotlin
// Regular recursion (stack overflow risk)
fun factorial(n: Int): Long {
    return if (n == 1) 1
    else n * factorial(n - 1) // Not tail recursive
}

// Tail recursion (last operation is recursive call)
tailrec fun factorialTail(n: Int, acc: Long = 1): Long {
    return if (n == 1) acc
    else factorialTail(n - 1, n * acc) // Tail recursive
}

// Compiled to loop:
fun factorialOptimized(n: Int, acc: Long = 1): Long {
    var n2 = n
    var acc2 = acc
    while (true) {
        if (n2 == 1) return acc2
        else {
            acc2 = n2 * acc2
            n2 = n2 - 1
        }
    }
}

// More examples
tailrec fun sum(n: Int, acc: Int = 0): Int {
    return if (n == 0) acc
    else sum(n - 1, acc + n)
}

tailrec fun findElement(
    list: List<Int>,
    target: Int,
    index: Int = 0
): Int? {
    return when {
        index >= list.size -> null
        list[index] == target -> index
        else -> findElement(list, target, index + 1)
    }
}

// Requirements for tailrec:
// 1. Last operation must be recursive call
// 2. Cannot have try-catch around recursive call
// 3. Cannot be open/override
// 4. Only for functions, not lambdas
```

---

## **Best Practices**

### Q49. What are Kotlin coding conventions?

**Answer:**

**Naming:**
```kotlin
// Classes/Interfaces - PascalCase
class MyClass
interface MyInterface

// Functions/Properties - camelCase
fun myFunction()
val myProperty = 0

// Constants - UPPER_SNAKE_CASE
const val MAX_COUNT = 100

// Type parameters - Single letter or PascalCase
class Box<T>
class Box<out TOutput>
```

**Formatting:**
```kotlin
// Prefer expression body for single expression
fun double(x: Int) = x * 2

// Use trailing comma
val list = listOf(
    1,
    2,
    3, // Trailing comma
)

// Named arguments for clarity
createUser(
    name = "John",
    age = 25,
    email = "john@example.com"
)
```

**Immutability:**
```kotlin
// Prefer val over var
val name = "John" // ✅
var age = 25 // Use only when needed

// Prefer immutable collections
val list = listOf(1, 2, 3) // ✅
val mutableList = mutableListOf(1, 2, 3) // Use only when needed
```

**Null safety:**
```kotlin
// Prefer safe calls over !!
val length = name?.length ?: 0 // ✅
val length = name!!.length // ❌ Avoid

// Use require/check for validation
fun setAge(age: Int) {
    require(age >= 0) { "Age must be positive" }
    this.age = age
}
```

---

### Q50. What are common Kotlin idioms?

**Answer:**

**Creating DTOs:**
```kotlin
data class Customer(val name: String, val email: String)
```

**Default values:**
```kotlin
fun foo(a: Int = 0, b: String = "") { }
```

**Filtering a list:**
```kotlin
val positives = list.filter { it > 0 }
```

**Checking element presence:**
```kotlin
if (email in emails) { }
```

**String interpolation:**
```kotlin
println("Name: $name")
```

**Instance checks:**
```kotlin
when (x) {
    is Foo -> x.bar()
    is Bar -> x.foo()
}
```

**Read-only list/map:**
```kotlin
val list = listOf(1, 2, 3)
val map = mapOf("a" to 1, "b" to 2)
```

**Lazy property:**
```kotlin
val lazy: String by lazy { computeString() }
```

**Extension functions:**
```kotlin
fun String.spaceToCamelCase() { /*...*/ }
"Convert this".spaceToCamelCase()
```

**Singleton:**
```kotlin
object Resource {
    val name = "Name"
}
```

**If-not-null shorthand:**
```kotlin
value?.let {
    // execute if not null
}
```

**If-not-null-else shorthand:**
```kotlin
val result = value?.let {
    // if not null
} ?: run {
    // if null
}
```

**Execute if null:**
```kotlin
value ?: run {
    // execute if null
}
```

**Return on when:**
```kotlin
fun transform(color: String): Int = when (color) {
    "Red" -> 0
    "Green" -> 1
    else -> throw IllegalArgumentException()
}
```

**Try-catch expression:**
```kotlin
val result = try {
    count()
} catch (e: ArithmeticException) {
    throw IllegalStateException(e)
}
```

**If expression:**
```kotlin
val result = if (param == 1) {
    "one"
} else {
    "other"
}
```

**Builder-style usage:**
```kotlin
fun arrayOfMinusOnes(size: Int): IntArray {
    return IntArray(size).apply { fill(-1) }
}
```

**Single-expression functions:**
```kotlin
fun theAnswer() = 42
```

**Call multiple methods on an object (with):**
```kotlin
class Turtle {
    fun penDown()
    fun penUp()
    fun turn(degrees: Double)
    fun forward(pixels: Double)
}

val turtle = Turtle()
with(turtle) {
    penDown()
    for (i in 1..4) {
        forward(100.0)
        turn(90.0)
    }
    penUp()
}
```

---

## **Summary**

### **Key Concepts to Master:**

**Basics:**
- Data types, variables (val/var)
- Null safety (?., ?:, !!)
- String templates
- When expressions
- Ranges

**OOP:**
- Classes (data, sealed, open, abstract)
- Interfaces
- Objects (singleton, companion, anonymous)
- Inheritance and delegation

**Functions:**
- Extension functions
- Higher-order functions
- Lambdas
- Inline functions
- Scope functions (apply, let, run, also, with)

**Collections:**
- List, Set, Map (immutable/mutable)
- Collection operations (map, filter, reduce)
- Sequences for lazy evaluation

**Coroutines:**
- Suspend functions
- Structured concurrency
- launch vs async
- Dispatchers
- Cancellation
- Exception handling

**Flow:**
- Cold vs hot streams
- StateFlow vs SharedFlow
- Flow operators
- Channels

**Advanced:**
- Generics and variance
- Delegation
- Inline/value classes
- Reified types
- DSLs
- Tail recursion

**Best Practices:**
- Immutability
- Null safety
- Code conventions
- Kotlin idioms

---

### **Interview Tips:**
1. Explain with code examples
2. Mention practical use cases
3. Compare with Java when relevant
4. Discuss performance implications
5. Show understanding of "why" not just "how"
6. Be ready to write code
7. Know coroutines well (critical for Android)

---

**Resources:**
- Kotlin Official Documentation
- Kotlin Koans (practice)
- Kotlin Coroutines Guide
- Android Developers Kotlin Guide
- Kotlin Flow Documentation
