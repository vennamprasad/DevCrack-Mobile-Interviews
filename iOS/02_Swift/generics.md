# 🧬 Generics
> **Targeted for Senior iOS Developers**
> **Note:** Generic Functions, Types, and Constraints.

![Generics](https://img.shields.io/badge/Swift-Generics-purple?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Generic Functions](#1-generic-functions)
- [2. Type Constraints](#2-type-constraints)
- [3. Opaque Types (`some`)](#3-opaque-types-some)
- [4. Existential Types (`any`)](#4-existential-types-any)

---

### Q1. Why use Generics?

**Answer:**
To write flexible, reusable code that works with any type, avoiding duplication.
**Array** and **Dictionary** are generics (`Array<Element>`).

### Q2. Example of a Generic Function?

**Answer:**
```swift
func swapTwoValues<T>(_ a: inout T, _ b: inout T) {
    let temporaryA = a
    a = b
    b = temporaryA
}
```

### Q3. What are Type Constraints?

**Answer:**
Restricting a generic type to inherit from a class or conform to a protocol.
```swift
// T must conform to Equatable
func findIndex<T: Equatable>(of value: T, in array: [T]) -> Int? { ... }
```

### Q4. `some View` vs `any View`?

**Answer:**
- **`some View` (Opaque Type)**: The concrete type is fixed at compile time, but hidden from the caller. High performance (Static Dispatch). Used in SwiftUI `body`.
- **`any View` (Existential Type)**: A box that can hold *any* type conforming to View. Type can change at runtime. Slower (Dynamic Dispatch).
