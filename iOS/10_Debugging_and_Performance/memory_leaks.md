# 💧 Memory Leaks
> **Targeted for iOS Developers**
> **Note:** Retain Cycles, Debug Memory Graph.

![Memory](https://img.shields.io/badge/Debug-Memory-blue?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Identifying Leaks](#1-identifying-leaks)
- [2. Debug Memory Graph](#2-debug-memory-graph)
- [3. Zombie Objects](#3-zombie-objects)

---

### Q1. Common causes of Leaks?

**Answer:**
1.  **Closures**: Capturing `self` strongly in a callback stored by `self`.
2.  **Delegates**: Declaring a delegate property as `strong` instead of `weak`.
3.  **Timers**: A Timer scheduled on RunLoop retains its target (`self`). Use `weak` inside the timer block.

### Q2. Debug Memory Graph?

**Answer:**
A feature in Xcode (Visual Debugger).
- Click the "Memory Graph" icon while running.
- It pauses the app and shows instances of all objects in memory.
- **Leak Check**: Look for the purple "!" icon.
- **Inspector**: Shows who is holding a reference to the leaked object.

### Q3. How to fix a Closure Leak?

**Answer:**
Use a **Capture List**.
```swift
// Bad
button.onTap = { self.updateUI() }

// Good
button.onTap = { [weak self] in
    self?.updateUI()
}
```

### Q4. What are Zombie Objects?

**Answer:**
(Mostly Objective-C/Unsafe Swift).
When a deallocated object is accessed.
enable **Zombie Objects** in Scheme > Diagnostics. The runtime keeps deallocated objects alive as "Zombies" to catch invalid access and print a helpful error instead of random crashing.
