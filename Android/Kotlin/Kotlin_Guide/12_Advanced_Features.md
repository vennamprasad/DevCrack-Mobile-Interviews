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
