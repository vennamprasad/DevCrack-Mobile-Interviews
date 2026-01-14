# ☕ Core Java Cheat Sheet for Android Developers

> **Quick Reference**: Essential syntax, concepts, and APIs for coding interviews.

---

## 🏗️ 1. Basics & Syntax

### Primitives
| Type | Bytes | Range | Default |
| :--- | :---: | :--- | :---: |
| `byte` | 1 | -128 to 127 | 0 |
| `short` | 2 | -32,768 to 32,767 | 0 |
| `int` | 4 | -2^31 to 2^31-1 | 0 |
| `long` | 8 | -2^63 to 2^63-1 | 0L |
| `float` | 4 | ~7 decimal digits | 0.0f |
| `double`| 8 | ~15 decimal digits | 0.0d |
| `char` | 2 | Unicode 0 to 65,535 | '\u0000' |
| `boolean`| 1* | true / false | false |
*(Size depends on JVM implementation)*

### Wrapper Classes (Auto-boxing/Unboxing)
*   `Integer`, `Double`, `Boolean` etc. are Objects.
*   **Comparison**: Always use `.equals()` for wrappers. `==` compares references (addresses), though caching for small Integers (-128 to 127) exists.

### String Immutability
*   `String` is **immutable**. Modifications create new objects.
*   **StringBuilder**: Mutable, not thread-safe (Fast).
*   **StringBuffer**: Mutable, thread-safe (Slow).
*   **String Pool**: Literals (`"Hello"`) are cached. `new String("Hello")` forces new heap object.

---

## 🧬 2. Object Oriented Programming (OOP)

### Access Modifiers
| Modifier | Class | Package | Subclass | World |
| :--- | :---: | :---: | :---: | :---: |
| `public` | ✅ | ✅ | ✅ | ✅ |
| `protected`| ✅ | ✅ | ✅ | ❌ |
| `default` | ✅ | ✅ | ❌ | ❌ |
| `private` | ✅ | ❌ | ❌ | ❌ |

### Keywords
*   **`static`**: Belongs to class, not instance. `static` methods cannot access non-static members.
*   **`final`**:
    *   *Variable*: Constant (cannot reassign reference).
    *   *Method*: Cannot be overridden.
    *   *Class*: Cannot be subclassed (e.g., `String`).
*   **`abstract`**: Class cannot be instantiated. Can have abstract (no body) and concrete methods.
*   **`interface`**: Contract. All vars are `public static final`. Methods `public abstract` (pre-Java 8). Java 8+ allows `default` and `static` methods.

### Polymorphism
*   **Overloading** (Compile-time): Same method name, different parameters.
*   **Overriding** (Runtime): Same signature in subclass. Use `@Override`.

---

## 📦 3. Collections Framework (Big O)

| Interface | Implementation | Get | Add | Contains | Remove | Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **List** | `ArrayList` | O(1) | O(1)* | O(n) | O(n) | Resizing is O(n). Fast read. |
| | `LinkedList` | O(n) | O(1) | O(n) | O(1) | Doubly linked. Fast insert/del at ends. |
| **Set** | `HashSet` | - | O(1) | O(1) | O(1) | Unordered. No duplicates. Uses HashMap internally. |
| | `TreeSet` | - | O(log n) | O(log n) | O(log n) | Sorted (Red-Black Tree). |
| | `LinkedHashSet` | - | O(1) | O(1) | O(1) | Insertion order preserved. |
| **Map** | `HashMap` | O(1) | O(1) | O(1) | O(1) | Unordered K-V pairs. Allows 1 null key. |
| | `TreeMap` | O(log n) | O(log n) | O(log n) | O(log n) | Sorted by Key. |
| | `LinkedHashMap` | O(1) | O(1) | O(1) | O(1) | Order preserved (Insert or Access). |

### Comparison
*   **Comparable**: `compareTo(obj)` (Natural ordering, implemented by class).
*   **Comparator**: `compare(obj1, obj2)` (Custom ordering, passed to Collection).

---

## ⚡ 4. Concurrency

### Threads
*   **`extends Thread`**: Limit inheritance.
*   **`implements Runnable`**: Better, separates task from runner.
*   **`implements Callable<T>`**: Like Runnable but returns result/throws Exception.

### Synchronization
*   **`synchronized` method**: Locks the instance (`this`).
*   **`synchronized` block**: Locks specific object. Better performance scope.
*   **`static synchronized`**: Locks the `Class` object (Global lock for class).

### Volatile
*   Guarantees variable visibility across threads (reads directly from main memory, skips CPU cache).
*   Does **NOT** guarantee atomicity (e.g., `count++` is not safe).

### ExecutorService
*   `FixedThreadPool(n)`: Reuses n threads.
*   `CachedThreadPool()`: Creates new threads as needed, kills idle ones.
*   `SingleThreadExecutor()`: Sequential execution.

---

## 🌊 5. Java 8+ Features

### Functional Interfaces
An interface with exactly one abstract method.
*   `Predicate<T>`: `T -> boolean` (e.g., filter).
*   `Consumer<T>`: `T -> void` (e.g., forEach).
*   `Function<T, R>`: `T -> R` (e.g., map).
*   `Supplier<T>`: `() -> T` (e.g., factories).

### Streams API
Sequence of elements supporting sequential/parallel operations.
```java
List<String> names = users.stream()           // Source
    .filter(u -> u.age > 18)                  // Intermediate (Lazy)
    .map(User::getName)                       // Intermediate (Lazy)
    .sorted()                                 // Intermediate (Lazy)
    .collect(Collectors.toList());            // Terminal (Eager)
```
*   **Intermediate**: `filter`, `map`, `flatMap`, `distinct`, `sorted`, `peek`, `limit`.
*   **Terminal**: `collect`, `forEach`, `reduce`, `count`, `anyMatch`, `findFirst`.

### Optional
Avoids `NullPointerException`.
```java
Optional<String> optionalName = Optional.ofNullable(name);
String safeName = optionalName.orElse("Unknown");
optionalName.ifPresent(n -> print(n));
```

---

## 🧱 6. Memory Model

### Stack vs Heap
*   **Stack**: Stores method calls, local primitives, and *references* to objects. Thread-safe (each thread has own stack).
*   **Heap**: Stores all Objects (and static members). Shared memory. subject to Garbage Collection.

### Garbage Collection Roots
Objects reachable from:
1.  Local variables in Active Stack Frames.
2.  Static variables.
3.  Active Threads.
4.  JNI References.

---

## 🧩 7. Generics

### Types
*   `E`: Element (Collection)
*   `K`, `V`: Key, Value
*   `T`: Type

### Wildcards
*   **`List<?>`**: Unbounded. Read-only (mostly).
*   **`List<? extends Number>`**: Upper Bounded. Can hold Number, Integer, Double. **Producer** (Get data). Cannot add (except null).
*   **`List<? super Integer>`**: Lower Bounded. Can hold Integer, Number, Object. **Consumer** (Add data).
> **PECS**: Producer Extends, Consumer Super.

---

## 🛠️ 8. Common Code Snippets

### Singleton (Double-Checked Locking)
```java
public class Singleton {
    private static volatile Singleton instance;
    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

### Try-with-Resources (AutoCloseable)
```java
// Automatically closes stream (even if exception occurs)
try (BufferedReader br = new BufferedReader(new FileReader(path))) {
    return br.readLine();
}
```
