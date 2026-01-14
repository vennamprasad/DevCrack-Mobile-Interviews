# 🔌 Protocols & Extensions
> **Targeted for iOS Developers**
> **Note:** POP (Protocol Oriented Programming), Defaults, and Extensions.

![Protocols](https://img.shields.io/badge/Swift-Protocols-green?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Protocols](#1-protocols)
- [2. Protocol Oriented Programming](#2-pop)
- [3. Extensions](#3-extensions)
- [4. Associated Types](#4-associated-types)

---

### Q1. What is a Protocol?

**Answer:**
A blueprint of methods, properties, and other requirements. Classes, Structs, and Enums can adopt them.
```swift
protocol Drivable {
    var speed: Int { get }
    func drive()
}
```

### Q2. What is Protocol Oriented Programming (POP)?

**Answer:**
Swift prefers composition over inheritance.
Instead of deep class hierarchies (`class Bird -> class FlyingBird -> class Eagle`), you use protocols (`protocol Flyable`).
- **Extensions**: Provide default implementations in protocol extensions throughout your app.
```swift
extension Flyable {
    func fly() { print("Flying high") }
}
```

### Q3. Explain `associatedtype`.

**Answer:**
Used creating generic protocols. It's a placeholder name for a type used in the protocol, defined by the adopting type.
```swift
protocol Container {
    associatedtype Item
    mutating func append(_ item: Item)
}
// Struct IntStack: Container { typealias Item = Int ... }
```

### Q4. Extensions vs Subclassing?

**Answer:**
- **Extension**: Adds functionality to an *existing* class/struct/enum without modifying the original source code. Cannot add stored properties.
- **Subclassing**: Can modify behavior (override) and add stored properties. Limited to Classes.
