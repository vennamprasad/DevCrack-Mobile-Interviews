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
