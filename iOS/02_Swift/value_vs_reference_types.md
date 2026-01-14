# 📦 Value vs Reference Types
> **Targeted for iOS Developers**
> **Note:** Structs, Enums vs Classes.

![Types](https://img.shields.io/badge/Swift-Types-blue?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. The Differences](#1-the-differences)
- [2. When to use which?](#2-when-to-use-which)
- [3. Mutability](#3-mutability)

---

### Q1. Main difference between Struct and Class?

**Answer:**
| Feature | Struct / Enum | Class |
| :--- | :--- | :--- |
| **Type** | Value Type | Reference Type |
| **Assignment** | Copied (Unique instance) | Shared (Pointer copy) |
| **Memory** | Stack (Mostly) | Heap |
| **Inheritance** | No | Yes |
| **Deinit** | No | Yes |

### Q2. What happens when you pass a Struct to a function?

**Answer:**
It is **copied**. The function receives a separate instance. Modifying it inside the function does not affect the original unless passed as `inout`.
**Copy-on-Write (COW)**: Swift optimizes collections (Arrays, Dictionaries) to only copy the actual data *when modified*, not just when passed, saving performance.

### Q3. Why are Value Types preferred in Swift?

**Answer:**
1.  **Safety**: No shared state. You know your data won't be changed by another part of the app unexpectedly.
2.  **Thread Safety**: Since each thread gets a copy, race conditions are harder to create.
3.  **Performance**: Stack allocation is faster than Heap allocation.

### Q4. When should you use a Class?

**Answer:**
1.  **Identity matters**: You need to track a specific instance (e.g., a File Handler, Network Manager).
2.  **Shared State**: You want changes to reflect everywhere.
3.  **Objective-C Interop**: Bridging requiring `NSObject`.
