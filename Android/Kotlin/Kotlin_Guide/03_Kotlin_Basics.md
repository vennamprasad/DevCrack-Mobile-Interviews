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
