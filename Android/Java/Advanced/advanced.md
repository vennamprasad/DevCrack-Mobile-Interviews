# ☕ Advanced Java Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Deep understanding of Memory Model, Concurrency, and Internals is required for Senior roles.

![Java](https://img.shields.io/badge/Language-Java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![Advanced](https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge)
![Concurrency](https://img.shields.io/badge/Topic-Concurrency-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Memory & Internals](#-1-memory--internals)
- [2. Concurrency & Threads](#-2-concurrency--threads)
- [3. Advanced Concepts (Reflection, Serialization)](#-3-advanced-concepts)
- [4. Collections & Streams](#-4-collections--streams)
- [5. Design Patterns](#-5-design-patterns)

---

## ✅ Overview

**Advanced Java** covers the intricacies of the JVM, threading models, and efficient data processing. For Android, understanding these ensures you write jank-free, leak-free, and performant applications.

---

## 🧩 Interview Questions (Q&A)

### 1. Memory & Internals

#### `==` vs `.equals()`?
*   `==`: Compares **references** (memory address). Fast.
*   `.equals()`: Compares **content** (logically equivalent). Can be overridden.

#### Java Memory Model (JMM)?
Defines how threads interact through memory. Key concepts:
*   **Atomicity:** Operations are indivisible.
*   **Visibility:** Changes typically happen in CPU cache. `volatile` flushes changes to main memory.
*   **Ordering:** JVM reorders instructions for performance. `happens-before` relationship prevents this.

#### `final` Keyword?
*   **Variable:** Constant value.
*   **Method:** Cannot be overridden.
*   **Class:** Cannot be inherited (e.g., `String` class).

#### `static` Keyword?
Belongs to the **Class**, not instances. Loaded once by ClassLoader.
*   **Static Block:** Runs once when class is loaded.
*   **Static Method:** Utility functions (cannot access instance `this`).

---

### 2. Concurrency & Threads

#### `volatile` vs `synchronized`?
*   **`volatile`**: Ensures **Visibility**. Reads/writes go directly to Main Memory. Does NOT guarantee atomicity (e.g., `i++` is not safe).
*   **`synchronized`**: Ensures **Atomicity** & **Visibility**. Only one thread enters the block. Slower due to lock overhead.

#### Deadlock?
Two threads wait forever for each other to release a lock.
*   **Prevention:** Acquire locks in a consistent order. Use `tryLock()` with timeout.

#### `ExecutorService` vs `Thread`?
*   **Thread:** Expensive to create/destroy (1MB stack). OS managed.
*   **ExecutorService:** Thread Pool. Reuses threads. Efficient for handling many tasks.

#### `CompletableFuture`?
Introducted in Java 8. Represents a Future that can be explicitly completed. Supports chaining (`thenApply`, `thenCompose`) and combining (`allOf`) async tasks without "Callback Hell".

---

### 3. Advanced Concepts

#### Reflection?
Ability to inspect class metadata (methods, fields) at runtime.
*   **Use Case:** DI Frameworks (Dagger/Hilt), Retrofit, Gson.
*   **Drawback:** Slower, breaks type safety, bypasses encapsulation (`private`).

#### Serialization?
Converting an object implementation to a byte stream (for File I/O or Network).
*   **`transient`**: Skips a field during serialization (e.g., `password`).
*   **`serialVersionUID`**: Version control for serialized classes.

#### `WeakReference` vs `SoftReference`?
*   **Strong:** `obj = new Object()` (Never collected).
*   **Soft:** Collected only if JVM runs out of memory (Good for Caching).
*   **Weak:** Collected on next GC cycle (Good for Listeners/Maps to prevent leaks).

---

### 4. Collections & Streams

#### `HashMap` vs `ConcurrentHashMap`?
*   **HashMap:** Not thread-safe. Fast.
*   **ConcurrentHashMap:** Thread-safe. Uses bucket-level locking (Segment locking in Java 7, CAS + synchronized in Java 8+). Much faster than `Hashtable`.

#### `ArrayList` vs `LinkedList`?
*   **ArrayList:** Dynamic Array. Fast Read (`O(1)`). Slow Insert/Delete (`O(n)` - shifting). Cache-friendly.
*   **LinkedList:** Doubly Linked List. Slow Read (`O(n)`). Fast Insert/Delete (`O(1)`). High memory overhead (Next/Prev pointers).

#### Stream API?
Functional-style operations on streams of elements.
*   **Intermediate:** `filter`, `map`, `sorted` (Lazy).
*   **Terminal:** `collect`, `forEach`, `reduce` (Eager).
```java
List<String> result = names.stream()
    .filter(s -> s.startsWith("A"))
    .collect(Collectors.toList());
```

---

### 5. Design Patterns

#### Singleton Pattern
Ensures only one instance exists.
**Best Practice:** Double-Checked Locking.
```java
class Singleton {
    private static volatile Singleton instance;
    private Singleton() {} // Private Constructor
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) instance = new Singleton();
            }
        }
        return instance;
    }
}
```
---
