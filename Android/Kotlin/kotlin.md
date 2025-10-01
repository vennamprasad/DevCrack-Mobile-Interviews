# What is Kotlin?

Kotlin is a modern, statically typed programming language developed by JetBrains. It runs on the Java Virtual Machine (JVM) and can also be compiled to JavaScript or native code. Kotlin is fully interoperable with Java, meaning you can use Kotlin and Java code together in the same project.

## Key Features of Kotlin

- **Concise Syntax:** Reduces boilerplate code compared to Java.
- **Null Safety:** Built-in null safety helps prevent null pointer exceptions.
- **Extension Functions:** Allows you to extend existing classes with new functionality.
- **Coroutines:** Simplifies asynchronous programming and concurrency.
- **Smart Casts:** Automatically casts types when possible.
- **Data Classes:** Simplifies the creation of classes for holding data.
- **Interoperability:** 100% interoperable with Java libraries and frameworks.

## How is Kotlin Better Than Java?

### 1. **Conciseness**
Kotlin code is more concise and expressive. For example, data classes, type inference, and default arguments reduce the amount of code you need to write.

**Java:**
```java
public class User {
    private String name;
    private int age;
    // getters, setters, constructor, toString, equals, hashCode
}
```
**Kotlin:**
```kotlin
data class User(val name: String, val age: Int)
```

### 2. **Null Safety**
Kotlin's type system distinguishes between nullable and non-nullable types, reducing the risk of null pointer exceptions.

**Java:**
```java
String name = null; // Possible NullPointerException
```
**Kotlin:**
```kotlin
var name: String? = null // Compiler enforces null checks
```

### 3. **Coroutines for Asynchronous Programming**
Kotlin provides coroutines for easy and efficient asynchronous programming, making code easier to read and maintain.

### 4. **Extension Functions**
You can add new functions to existing classes without modifying their source code.

**Kotlin:**
```kotlin
fun String.isEmail(): Boolean { /* ... */ }
```

### 5. **Smart Casts**
Kotlin automatically casts types when it is safe to do so, reducing the need for explicit casting.

### 6. **Interoperability**
Kotlin can use all existing Java libraries and frameworks, making migration easy.

### 7. **Modern Language Features**
Kotlin supports features like lambda expressions, higher-order functions, destructuring declarations, and more, which make it more expressive and powerful.

## Interview Questions and Answers

### Q1. What is the difference between suspend functions and regular functions in Kotlin?
**Answer:** Suspend functions can suspend execution without blocking a thread and must be called from a coroutine or another suspend function. They are marked with the suspend modifier.
```kotlin
suspend fun fetch(): String { /* network call */ }
```

### Q2. How does structured concurrency work in Kotlin coroutines?
**Answer:** Structured concurrency ties child coroutines to a parent scope (CoroutineScope), ensuring proper lifecycle, propagation of cancellations and exceptions, and predictable resource cleanup using scope builders like coroutineScope and supervisorScope.

### Q3. What is the difference between launch and async?
**Answer:** launch starts a coroutine for side-effects and returns a Job; async returns a Deferred<T> for a result that you await.

### Q4. When should you use withContext?
**Answer:** Use withContext to switch coroutine dispatcher for a block (e.g., IO work) without creating a new top-level coroutine; it preserves structured concurrency.
```kotlin
withContext(Dispatchers.IO) { readFile() }
```

### Q5. How does cancellation work in coroutines?
**Answer:** Cancellation is cooperative; suspending functions check for cancellation and throw CancellationException. Use isActive or ensureActive for custom checks.

### Q6. What is a SupervisorJob and when to use it?
**Answer:** SupervisorJob prevents failure of one child from cancelling siblings; use in top-level supervisors where one child failure shouldn't cancel others.

### Q7. Difference between coroutineScope and supervisorScope?
**Answer:** coroutineScope cancels all children if one fails; supervisorScope isolates failures so sibling coroutines can continue.

### Q8. What is Dispatchers.IO vs Dispatchers.Default?
**Answer:** Dispatchers.IO is optimized for blocking I/O with a large thread pool; Dispatchers.Default is optimized for CPU-bound tasks using a shared pool.

### Q9. Explain coroutineDispatcher and CoroutineName context elements.
**Answer:** CoroutineContext holds elements like dispatcher for threading and CoroutineName for debug-friendly names. Combine via + operator.

### Q10. What is a Flow in Kotlin?
**Answer:** Flow is a cold asynchronous stream that emits multiple values sequentially; supports backpressure, operators, and suspending collection.

### Q11. Cold vs Hot streams: what's the difference?
**Answer:** Cold streams (Flow) start producing when collected; hot streams (SharedFlow, StateFlow, Channel) produce independent of collectors.

### Q12. When to use StateFlow vs SharedFlow?
**Answer:** Use StateFlow for observable state with a single latest value and replay=1; SharedFlow for event streams requiring configurable replay/buffer.

### Q13. How to convert a suspend function to a Flow?
**Answer:** Use flow { emit(suspendCall()) } or flow { while (...) emit(...) } to produce multiple emissions.

### Q14. What is buffer() in Flow and when is it useful?
**Answer:** buffer decouples producers and consumers by providing a buffer, improving throughput when producer is faster than consumer.

### Q15. Explain flatMapConcat vs flatMapMerge vs flatMapLatest.
**Answer:** flatMapConcat concatenates inner flows sequentially; flatMapMerge merges them concurrently; flatMapLatest cancels previous inner flow when a new one arrives.

### Q16. How does Flow handle exceptions?
**Answer:** Use catch { } to handle exceptions upstream; onCompletion can handle completion and errors; exceptions propagate as usual if not caught.

### Q17. What are Kotlin Channels and when to use them?
**Answer:** Channels are rendezvous/buffered queues for communicating between coroutines, useful for producer-consumer and pipeline patterns.

### Q18. How to cancel a coroutine that is blocked on a suspendCancellableCoroutine or blocking call?
**Answer:** Use suspendCancellableCoroutine and register an onCancellation handler; for blocking calls use withContext(Dispatchers.IO) and check isActive or use cancellable APIs.

### Q19. What is actor pattern in coroutines?
**Answer:** Actor is a coroutine that receives messages via Channel and processes them sequentially to safely manage mutable state without locks.

### Q20. Explain Structured Exception Handling in coroutines.
**Answer:** Exceptions in parent coroutine usually cancel children; SupervisorJob and supervisorScope allow isolating exceptions; CoroutineExceptionHandler catches uncaught exceptions on parent-level jobs.

### Q21. What is reified type parameter and when to use it?
**Answer:** reified allows access to the concrete type at runtime for inline functions, enabling type checks/casts and reflection without passing KClass.

### Q22. How do inline functions affect performance and code size?
**Answer:** Inline eliminates call overhead and enables reified generics and non-local returns, but increases bytecode size when used heavily.

### Q23. Explain noinline and crossinline modifiers.
**Answer:** noinline prevents inlining of lambda parameters; crossinline forbids non-local returns from a lambda to be inlined in caller.

### Q24. What are inline classes (value classes) and their benefits?
**Answer:** Value classes wrap a single value and can be inlined at runtime to avoid heap allocation, improving performance while maintaining type safety.
```kotlin
@JvmInline value class UserId(val id: Long)
```

### Q25. How does Kotlin handle nullability and platform types?
**Answer:** Kotlin types are nullable (?) or non-null; platform types from Java have unknown nullability and require caution as compiler won’t enforce.

### Q26. What is the difference between lateinit and lazy?
**Answer:** lateinit is for var non-null properties initialized later (no thread-safety by default); lazy is for val initialized on first access, with configurable thread-safety.

---

### Q27. How to write a custom property delegate?
**Answer:** Implement getValue and setValue (for var). Use operator functions and store delegated state.
```kotlin
class ExampleDelegate {
    operator fun getValue(thisRef: Any?, prop: KProperty<*>) = "value"
}
var p by ExampleDelegate()
```

### Q28. Explain covariance and contravariance in Kotlin generics.
**Answer:** Use out for covariance (producers, read-only) and in for contravariance (consumers, write-only). They affect subtyping relationships.

---

### Q29. What are star-projections?
**Answer:** Star-projection (*) is used when generic type argument is unknown; e.g., List<*> allows any List regardless of element type.

### Q30. How do sealed classes differ from enums?
**Answer:** Sealed classes allow hierarchical and payload-bearing types with exhaustive when expressions; enums are fixed constant values without payloads (unless add properties).

### Q31. What is expect/actual in Kotlin Multiplatform?
**Answer:** expect declares platform-specific APIs in common code; actual provides platform implementations in platform modules.

### Q32. How to create a DSL in Kotlin?
**Answer:** Use higher-order functions, extension functions, lambdas with receiver, and operators to create readable builders and DSLs.
```kotlin
fun html(block: HTML.() -> Unit) = HTML().apply(block)
```

### Q33. Explain suspendCoroutine vs suspendCancellableCoroutine.
**Answer:** suspendCoroutine doesn't support cancellation callbacks; suspendCancellableCoroutine integrates with coroutine cancellation and lets you register onCancellation.

### Q34. What is Continuation and how is it used?
**Answer:** Continuation represents the rest of computation for a suspend function; you can obtain it in low-level APIs to resume operations, but it's advanced internals.

### Q35. How to manage shared mutable state across coroutines safely?
**Answer:** Prefer confinement (single coroutine/actor/StateFlow), use Mutex.withLock for critical sections, or atomic primitives (atomicfu) for lock-free updates.

### Q36. What is Mutex vs synchronized?
**Answer:** Mutex is a suspending mutual exclusion primitive usable in coroutines, allowing suspension while waiting; synchronized blocks block threads and should be avoided in coroutines.

### Q37. How to test coroutines deterministically?
**Answer:** Use TestCoroutineScheduler/TestDispatcher or runTest from kotlinx-coroutines-test to control virtual time and scheduling.

### Q38. Explain coroutineScope vs runBlocking.
**Answer:** runBlocking blocks the calling thread (used in main/tests) to run a coroutine; coroutineScope is suspending and does not block a thread.

### Q39. What is tailrec and when is it applicable?
**Answer:** tailrec marks tail-recursive functions for optimization into loops; only works when the recursive call is in tail position and function is non-suspending.

### Q40. How does Kotlin's smart cast work with mutable properties?
**Answer:** Smart casts apply when the compiler can prove immutability (val or local variable) or after null checks; mutable properties may not be smart-cast unless private and no concurrent mutation.

### Q41. How to interoperate with Java when exceptions are involved?
**Answer:** Kotlin doesn't require checked exceptions; annotate Java methods or handle exceptions normally. Use @Throws to generate proper Java signatures when calling Kotlin from Java.

### Q42. Explain KClass vs Class in reflection.
**Answer:** KClass is Kotlin's reflection type (kotlin.reflect.KClass); use .java to get the Java Class. Use kotlin-reflect for advanced features.

### Q43. What is Ktor and how do coroutines fit in?
**Answer:** Ktor is an asynchronous Kotlin server/client framework built on coroutines, enabling non-blocking I/O and structured concurrency for request handling.

### Q44. How to implement operator overloading effectively?
**Answer:** Define functions with operator modifier (plus, get, invoke, etc.) to provide natural syntax for domain types.
```kotlin
operator fun Point.plus(o: Point) = Point(x+o.x, y+o.y)
```

### Q45. How to create a thread-safe singleton in Kotlin?
**Answer:** Use object declaration (initialized lazily and thread-safe) or lazy { } with synchronized mode.
```kotlin
object Manager { /* single instance */ }
```

### Q46. What is KAPT vs KSP?
**Answer:** KAPT (annotation processing) generates Java stubs and is slower; KSP is a Kotlin-native symbol processing API offering better performance and direct Kotlin support.

### Q47. How to design immutable data structures idiomatically?
**Answer:** Use data classes, val properties, copy() for transformations, and persistent collections (or wrappers) to avoid mutation.

### Q48. How does kotlinx.serialization compare to other libs?
**Answer:** kotlinx.serialization is Kotlin-first, supports multiplatform and compiler plugin-generated serializers, offering concise annotations and tight integration.

### Q49. Describe difference between apply, run, let, also, and with.
**Answer:** apply returns the receiver after configuring it; run returns lambda result with receiver; let passes receiver as it (argument) and returns result; also returns receiver after acting with it; with is similar to run but not an extension.

### Q50. How to handle long-running blocking operations in Kotlin?
**Answer:** Offload them to Dispatchers.IO using withContext or to a separate thread pool; avoid blocking main/Default dispatchers.

### Q51. What are platform types and how to avoid pitfalls?
**Answer:** Platform types come from Java and have no nullability info; treat them cautiously, add explicit nullability or checks, and prefer null-safe wrappers or annotations.

### Q52. How to use sealed interfaces and advantages over sealed classes?
**Answer:** Sealed interfaces allow implementing types across files and can be implemented by classes, interfaces or enums; they provide the same exhaustive when benefits as sealed classes with more flexibility.

### Q53. How to create coroutine-based backpressure strategies?
**Answer:** Use buffer with specified capacity and onBufferOverflow strategies, conflation (conflate), or combine with channels and suspending producers to manage backpressure.

### Q54. How to implement a cancellable callback API bridging to coroutines?
**Answer:** Wrap callbacks with suspendCancellableCoroutine, register cancellation handler to cancel underlying callback subscription or close resources.

### Q55. Best practices for exception handling in coroutine-based libraries?
**Answer:** Use structured concurrency to propagate exceptions, provide meaningful CoroutineExceptionHandler for top-level logging, and use Result/ sealed types when representing recoverable errors.
