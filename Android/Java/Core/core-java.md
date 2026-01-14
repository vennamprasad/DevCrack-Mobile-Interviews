# ☕ Core Java Interview Guide
> **Targeted for Junior - Senior Android Developer Roles**
> **Note:** A solid foundation in Core Java is non-negotiable for Android development, even in a Kotlin-first world.

![Java](https://img.shields.io/badge/Language-Java-ED8B00?style=for-the-badge&logo=java&logoColor=white)
![Core](https://img.shields.io/badge/Level-Core-green?style=for-the-badge)
![OOP](https://img.shields.io/badge/Topic-OOP-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. OOP Concepts](#-1-oop-concepts)
- [2. String Handling](#-2-string-handling)
- [3. Collections Framework](#-3-collections-framework)
- [4. Exceptions](#-4-exceptions)
- [5. Multithreading Basics](#-5-multithreading-basics)

---

## ✅ Overview

**Core Java** is the backbone of Android. It includes the basic syntax, Object-Oriented Principles (OOP), Exception Handling, and the Collections Framework.

---

## 🧩 Interview Questions (Q&A)

### 1. OOP Concepts

#### Four Pillars of OOP?
1.  **Encapsulation:** Wrapping data (fields) and code (methods) together (e.g., `private` fields with getters/setters).
2.  **Inheritance:** Mechanism where one class acquires the properties of another (`extends`).
3.  **Polymorphism:** One interface, many forms (Method Overloading & Overriding).
4.  **Abstraction:** Hiding internal details and showing only functionality (Abstract Classes & Interfaces).

#### Overloading vs Overriding?
*   **Overloading:** Same method name, different parameters (Compile-time Polymorphism).
*   **Overriding:** Same method signature in child class (Runtime Polymorphism).

#### Abstract Class vs Interface?
*   **Abstract Class:** Can have state (fields) and constructors. "Is-a" relationship.
*   **Interface:** Contract only. "Has-a" or "Can-do" capability. (Java 8 allowed `default` methods).

---

### 2. String Handling

#### Strings Immutable?
Yes. Once created, a `String` object cannot be changed. This makes them thread-safe and allows caching (String Pool).

#### String vs StringBuffer vs StringBuilder?
*   **String:** Immutable. Slow modifications.
*   **StringBuffer:** Mutable & Synchronized (Thread-safe). Slower.
*   **StringBuilder:** Mutable & Non-Synchronized (Not Thread-safe). Fastest.

---

### 3. Collections Framework

#### ArrayList vs LinkedList?
*   **ArrayList:** Backed by an array. Fast random access (`get(i)`). Slow insertions (array resizing).
*   **LinkedList:** Doubly-linked list. Fast insertions/deletions. Slow random access.

#### HashMap vs Hashtable?
*   **HashMap:** Non-synchronized. Allows 1 null key. Fast.
*   **Hashtable:** Synchronized. No nulls. Slow (Legacy).

#### Set vs List?
*   **List:** Ordered, allows duplicates.
*   **Set:** Unordered, UNIQUE elements only.

---

### 4. Exceptions

#### Checked vs Unchecked?
*   **Checked:** Verified at compile-time (e.g., `IOException`). Must be handled with `try-catch`.
*   **Unchecked:** Runtime exceptions (e.g., `NullPointerException`). Developer error.

#### `final` vs `finally` vs `finalize`?
*   **`final`:** Keyword to make constant.
*   **`finally`:** Block in try-catch always executed (cleanup).
*   **`finalize`:** Method called by GC before object destruction (Deprecated).

---

### 5. Multithreading Basics

#### Lifecycle of a Thread?
New -> Runnable -> Running -> Blocked/Waiting -> Terminated.

#### `wait()` vs `sleep()`?
*   **`wait()`:** Object class. Releases the lock.
*   **`sleep()`:** Thread class. Keeps the lock.

---