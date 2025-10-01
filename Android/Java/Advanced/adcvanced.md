# Advanced Java Interview Questions and Answers

---

## 1. What is the difference between `==` and `.equals()` in Java?

- `==` compares object references.
- `.equals()` compares object values (can be overridden).

```java
String a = new String("test");
String b = new String("test");
System.out.println(a == b); // false
System.out.println(a.equals(b)); // true
```

---

## 2. Explain the concept of Java Reflection.

Reflection allows inspection and modification of classes, methods, and fields at runtime.

```java
Class<?> clazz = Class.forName("java.util.ArrayList");
Method[] methods = clazz.getDeclaredMethods();
```

---

## 3. What is the use of `transient` keyword?

It prevents serialization of a field.

```java
class User implements Serializable {
    transient String password;
}
```

---

## 4. What is the difference between `ArrayList` and `LinkedList`?

- `ArrayList`: Fast random access, slow insert/delete.
- `LinkedList`: Slow access, fast insert/delete.

---

## 5. What is the Java Memory Model?

Defines how threads interact through memory and what behaviors are allowed in concurrent execution.

---

## 6. What is the purpose of `volatile` keyword?

Ensures visibility of changes to variables across threads.

```java
volatile boolean flag = true;
```

---

## 7. What is the difference between `synchronized` method and block?

- Method: Locks entire method.
- Block: Locks specific code segment.

```java
synchronized void foo() {}
synchronized(this) { /* code */ }
```

---

## 8. What is a deadlock?

When two or more threads are blocked forever, each waiting for the other.

---

## 9. How do you prevent deadlocks?

- Lock ordering
- Using `tryLock`
- Minimizing synchronized blocks

---

## 10. What is the use of `final` keyword?

- Variable: Value can't change.
- Method: Can't override.
- Class: Can't inherit.

---

## 11. What is the difference between `HashMap` and `ConcurrentHashMap`?

- `HashMap` is not thread-safe.
- `ConcurrentHashMap` is thread-safe.

---

## 12. What is the Singleton pattern? How do you implement it?

Ensures only one instance of a class.

```java
class Singleton {
    private static Singleton instance;
    private Singleton() {}
    public static synchronized Singleton getInstance() {
        if (instance == null) instance = new Singleton();
        return instance;
    }
}
```

---

## 13. What is the difference between `throw` and `throws`?

- `throw`: Used to throw an exception.
- `throws`: Declares possible exceptions.

---

## 14. What is the use of `super` keyword?

Refers to superclass methods/constructors.

---

## 15. What is the difference between `abstract class` and `interface`?

- Abstract class: Can have method implementations.
- Interface: Only method signatures (Java 8+ allows default methods).

---

## 16. What is the Java Stream API?

Provides functional-style operations on collections.

```java
List<String> names = list.stream().filter(s -> s.startsWith("A")).collect(Collectors.toList());
```

---

## 17. What is the difference between `ExecutorService` and `Thread`?

- `Thread`: Direct thread management.
- `ExecutorService`: Manages thread pools.

---

## 18. What is the use of `Optional` class?

Represents a value that may be absent.

```java
Optional<String> name = Optional.ofNullable(null);
```

---

## 19. What is method overloading and overriding?

- Overloading: Same method name, different parameters.
- Overriding: Subclass redefines superclass method.

---

## 20. What is the difference between checked and unchecked exceptions?

- Checked: Checked at compile time.
- Unchecked: Checked at runtime.

---

## 21. What is the use of `static` keyword?

- Variable: Shared among all instances.
- Method: Belongs to class.

---

## 22. What is the difference between `String`, `StringBuilder`, and `StringBuffer`?

- `String`: Immutable.
- `StringBuilder`: Mutable, not thread-safe.
- `StringBuffer`: Mutable, thread-safe.

---

## 23. What is the use of `enum` in Java?

Defines a set of constants.

```java
enum Day { MONDAY, TUESDAY }
```

---

## 24. What is the difference between `wait()` and `sleep()`?

- `wait()`: Releases lock, used for inter-thread communication.
- `sleep()`: Pauses thread, doesn't release lock.

---

## 25. What is the use of `synchronized` keyword?

Ensures only one thread accesses a block/method at a time.

---

## 26. What is the difference between `public`, `private`, `protected`, and default access?

- `public`: Accessible everywhere.
- `private`: Accessible within class.
- `protected`: Accessible within package and subclasses.
- Default: Accessible within package.

---

## 27. What is the use of `this` keyword?

Refers to current object.

---

## 28. What is the difference between shallow copy and deep copy?

- Shallow: Copies references.
- Deep: Copies actual objects.

---

## 29. What is the use of `try-with-resources`?

Automatically closes resources.

```java
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    // use br
}
```

---

## 30. What is the difference between `Comparable` and `Comparator`?

- `Comparable`: Natural ordering, implemented in class.
- `Comparator`: Custom ordering, separate class.

---

## 31. What is the use of `default` methods in interfaces?

Allows method implementation in interfaces (Java 8+).

---

## 32. What is the difference between `List`, `Set`, and `Map`?

- `List`: Ordered, allows duplicates.
- `Set`: Unordered, no duplicates.
- `Map`: Key-value pairs.

---

## 33. What is the use of `@FunctionalInterface`?

Indicates interface with single abstract method.

---

## 34. What is the difference between `Class.forName()` and `ClassLoader.loadClass()`?

- `Class.forName()`: Loads and initializes class.
- `ClassLoader.loadClass()`: Loads class, doesn't initialize.

---

## 35. What is the use of `synchronized` collections?

Provides thread-safe collection operations.

---

## 36. What is the use of `Future` and `Callable`?

- `Callable`: Returns result, can throw exception.
- `Future`: Represents result of async computation.

---

## 37. What is the use of `ThreadLocal`?

Provides thread-local variables.

---

## 38. What is the difference between `JVM`, `JRE`, and `JDK`?

- `JVM`: Runs Java bytecode.
- `JRE`: JVM + libraries.
- `JDK`: JRE + development tools.

---

## 39. What is the use of `Serialization`?

Converts object to byte stream for storage/transfer.

---

## 40. What is the use of `Deserialization`?

Converts byte stream back to object.

---

## 41. What is the use of `lambda expressions`?

Enables functional programming.

```java
Runnable r = () -> System.out.println("Hello");
```

---

## 42. What is the use of `Predicate` interface?

Represents boolean-valued function.

```java
Predicate<String> isEmpty = String::isEmpty;
```

---

## 43. What is the use of `Stream.reduce()`?

Performs reduction on stream elements.

```java
int sum = list.stream().reduce(0, Integer::sum);
```

---

## 44. What is the use of `Collectors` class?

Provides reduction operations like grouping, partitioning.

---

## 45. What is the use of `CompletableFuture`?

Handles async programming with callbacks.

---

## 46. What is the use of `ForkJoinPool`?

Efficient parallel execution using work-stealing.

---

## 47. What is the use of `ReentrantLock`?

Provides advanced locking mechanisms.

---

## 48. What is the use of `CountDownLatch`?

Synchronizes threads by waiting for events.

---

## 49. What is the use of `CyclicBarrier`?

Synchronizes threads at a common barrier point.

---

## 50. What is the use of `Semaphore`?

Controls access to resources by multiple threads.

---

## 51. What is the use of `AtomicInteger`?

Provides atomic operations on integers.

---

## 52. What is the use of `Phaser`?

Flexible synchronization barrier for threads.

---

## 53. What is the use of `Timer` and `ScheduledExecutorService`?

Schedules tasks for future execution.

---

## 54. What is the use of `SoftReference`, `WeakReference`, and `PhantomReference`?

Different levels of object reachability for garbage collection.

---

## 55. What is the use of `ClassLoader`?

Loads classes dynamically at runtime.

---

## 56. What is the use of `Proxy` class?

Creates dynamic proxy instances for interfaces.

---

## 57. What is the use of `Annotation` in Java?

Provides metadata for code.

---

## 58. What is the use of `@Override`, `@Deprecated`, and `@SuppressWarnings`?

- `@Override`: Indicates method override.
- `@Deprecated`: Marks deprecated code.
- `@SuppressWarnings`: Suppresses compiler warnings.

---

## 59. What is the use of `Pattern` and `Matcher` classes?

Used for regex operations.

```java
Pattern p = Pattern.compile("\\d+");
Matcher m = p.matcher("123");
```

---

## 60. What is the use of `ResourceBundle`?

Handles internationalization (i18n).

---
