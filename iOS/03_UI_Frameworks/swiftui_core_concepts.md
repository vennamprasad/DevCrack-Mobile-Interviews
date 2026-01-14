# 🎨 SwiftUI Core Concepts
> **Targeted for iOS Developers**
> **Note:** Modifiers, Environment, and Layout.

![SwiftUI](https://img.shields.io/badge/Framework-SwiftUI-3399CC?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Modifiers & Order](#1-modifiers--order)
- [2. Environment](#2-environment)
- [3. Preference Keys](#3-preference-keys)

---

### Q1. Why does Modifier order matter?

**Answer:**
Modifiers wrap the view in a new View type.
```swift
Text("Hello")
    .padding()      // 1. Adds padding around text
    .background(.red) // 2. Adds red background around (text + padding)
```
vs
```swift
Text("Hello")
    .background(.red) // 1. Adds red background around text
    .padding()      // 2. Adds padding around (red background + text)
```
They produce efficient visual differences.

### Q2. What is `@Environment`?

**Answer:**
A way to read system-provided values or injected dependencies.
- System: `.colorScheme` (Dark mode), `.locale`, `.presentationMode` (Dismiss).
- Injected: Custom classes injected via `.environmentObject()`.

### Q3. `ViewBuilder`?

**Answer:**
A result builder that creates a constructed view from closures. It allows you to list multiple generic child views (e.g., in `VStack { ... }`) and combine them into a single `TupleView`.

### Q4. Layout System in one sentence?

**Answer:**
"Parent proposes a size, Child chooses its own size, Parent places the Child."
(Unlike UIKit where Parent often dictates the exact frame of the child).
