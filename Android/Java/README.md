# ☕ Java for Android Engineers

> **Comprehensive review of Core and Advanced Java concepts required for Android platform internals, legacy codebases, and JVM technical interviews.**

![Java](https://img.shields.io/badge/Language-Java-ED8B00?style=for-the-badge&logo=java)
![JVM](https://img.shields.io/badge/Runtime-ART_%2F_JVM-blue?style=for-the-badge)
![Legacy](https://img.shields.io/badge/Scope-Core_&_Advanced-green?style=for-the-badge)

---

## 📖 Module Contents

| Guide | Description | Key Topics |
| :--- | :--- | :--- |
| **[Core Java Guide](./Core/core-java.md)** | Fundamentals of Java in Android development. | OOP (Inheritance, Polymorphism, Encapsulation, Abstraction), Pass-by-value, `equals()` and `hashCode()`, String pool, Exception hierarchy, Collections framework (`ArrayList`, `HashMap`, `ConcurrentHashMap`). |
| **[Java Cheat Sheet](./Core/cheetsheet.md)** | Quick-reference formula sheet. | Syntax patterns, access modifiers, memory areas (Stack vs Heap), garbage collection basics. |
| **[Advanced Java](./Advanced/advanced.md)** | Concurrency, memory model, and JVM internals. | Multithreading, `synchronized`, `volatile`, Java Memory Model (JMM), ThreadPoolExecutor, Generics & Type Erasure, Reflection, ClassLoaders. |

---

## 🧠 Java vs Kotlin Mental Model Bridge

| Java Concept | Kotlin Equivalent | Architectural Difference |
| :--- | :--- | :--- |
| `final class` | `class` (default closed) | Classes are final by default in Kotlin, requiring `open` to inherit |
| `static` methods/fields | `companion object` / top-level | Kotlin avoids static members in favor of objects and package-level functions |
| Checked Exceptions (`throws IOException`) | Unchecked only | Kotlin eliminates checked exceptions to reduce ceremony |
| `interface` with default methods | `interface` with implementation | Kotlin interfaces support concrete functions directly |
| Anonymous Inner Classes | Lambdas / Higher-order functions | Kotlin provides clean closure syntax with inline function optimization |
