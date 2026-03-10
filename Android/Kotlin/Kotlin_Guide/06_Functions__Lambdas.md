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
