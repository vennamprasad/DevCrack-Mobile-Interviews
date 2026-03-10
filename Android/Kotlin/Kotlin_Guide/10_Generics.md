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
