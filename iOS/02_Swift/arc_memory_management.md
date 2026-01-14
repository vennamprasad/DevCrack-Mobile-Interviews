# 🧠 ARC & Memory Management
> **Targeted for Senior iOS Developers**
> **Note:** Retain Cycles, Weak, Unowned.

![Memory](https://img.shields.io/badge/Swift-Memory-red?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. ARC Basics](#1-arc-basics)
- [2. Retain Cycles](#2-retain-cycles)
- [3. Weak vs Unowned](#3-weak-vs-unowned)
- [4. Closure Captures](#4-closure-captures)
- [5. Real-World Scenarios](#5-real-world-scenarios)

---

### Q1. How does ARC work?

**Answer:**
**Automatic Reference Counting**.
- Every time you create a strong reference to a class instance, ARC increases its reference count (+1).
- When the reference is removed (variable set to nil or goes out of scope), count decreases (-1).
- When count == 0, memory is deallocated (`deinit` called).

### Q2. What is a Retain Cycle?

**Answer:**
When two objects hold **strong** references to each other.
- Object A holds B.
- Object B holds A.
- Neither can ever reach count 0.
- Result: **Memory Leak**.

### Q3. `weak` vs `unowned`?

**Answer:**
Both break retain cycles by **not** increasing reference count.
- **`weak`**:
    - Must be `Optional` (`var`).
    - Becomes `nil` when the object is deallocated.
    - Safe.
- **`unowned`**:
    - Non-Optional (`let` or `var`).
    - Assumes the object **will never be nil** when accessed.
    - **Crash** if accessed after deallocation.
    - Use only when lifecycle is strictly tied (e.g., Card -> internal CreditCardChip).

### Q4. Retain Cycles in Closures?

**Answer:**
Closures are reference types. If a class instance holds a closure, and the closure uses `self` (capturing it strongly), you create a cycle.
**Fix**: Catch lists.
```swift
lazy var myClosure: () -> Void = { [weak self] in
    self?.doSomething()
}
```

---

### 5. Real-World Scenarios

### Q5. Scenario: You dismissed a ViewController, but `deinit` is never called. Memory usage keeps growing. Why?

**Answer:**
Most likely a **Retain Cycle**.
Common culprits:
1.  **Delegates**: Did you declare `weak var delegate: MyDelegate?`? If you missed `weak`, it's strong by default.
2.  **Timers**: A standard `Timer.scheduledTimer` retains its target (`self`). Use `[weak self]` in the block-based timer API instead.
3.  **Closures**: Did you capture `self` inside a network callback or animation block?

### Q6. Scenario: You are parsing 10,000 high-res images in a loop. Memory spikes to 2GB and crashes.

**Answer:**
ARC cleans up memory *at the end of the scope*. In a loop, the scope doesn't end until the loop finishes 10,000 times.
**Fix**: Use **`autoreleasepool`**.
```swift
for image in images {
    autoreleasepool {
        process(image) // Temporary objects created here are freed immediately after this block
    }
}
```

### Q7. Scenario: App crashes with `_swift_abortRetainUnowned`.

**Answer:**
You accessed an **`unowned`** reference after the object it pointed to was deallocated.
**Debugging**:
- Check who owns the object.
- If the object (e.g., Parent) can die before the child (e.g., Task), use `weak` instead of `unowned`.

### Q8. Scenario: You see "Purple Exclamation Marks" in Xcode while debugging.

**Answer:**
That is the **Runtime Sanitizer** (e.g., Main Thread Checker or Address Sanitizer).
If it's a memory issue, it might be the **Memory Graph Debugger** flagging a leak.
- Click the icon.
- Look at the graph.
- If you see two nodes pointing at each other with no external arrows, that's your cycle.

### Q9. Scenario: When to use `[unowned self]` over `[weak self]` in a closure?

**Answer:**
Use `unowned` **ONLY** if you are 100% sure the closure will *never* execute after `self` is deallocated.
**Safe bet**: Always use `weak`. The overhead of checking for nil is negligible compared to the risk of a crash.
**Example where `unowned` is okay**: In a `UIView` setup code where the closure is keeping a subview updated, and the closure is destroyed when the view is.

### Q10. Scenario: Handling `self` in `DispatchQueue.main.asyncAfter`?

**Answer:**
If you fire a delayed task for 10 seconds later, and the user leaves the screen instantly:
- **Strong self**: The VC stays alive for 10s (invisible), code runs, then VC dies. (Safe but wasteful).
- **Weak self**: The VC dies instantly. Code runs 10s later, finds self is nil, and stops. (Preferred).

### Q11. Scenario: C-Interoperability & Unsafe Pointers?

**Answer:**
When working with C APIs (e.g., Core Audio, OpenGL), you manage memory manually (`malloc`/`free`).
Swift provides `UnsafeMutablePointer<T>`.
- **Rule**: If you `allocate()`, you MUST `deallocate()`. ARC does not touch these.

### Q12. Scenario: `lazy` var causing memory issues?

**Answer:**
`lazy` vars are not thread-safe by default.
If two threads access a `lazy` var simultaneously for the first time, it might be initialized **twice**. Depending on what the init does (e.g., opening a file connection), this could be a leak or logic bug.

### Q13. Scenario: Object kept alive by a Singleton callback?

**Answer:**
You subscribe to a Singleton: `NotificationCenter.default.addObserver(...)`.
If you don't remove the observer (in older iOS versions), the center holds a reference to you.
(Modern iOS cleans up observers automatically, but custom Singletons might not).
**Fix**: Ensure your custom `Broadcaster` singleton holds weak references to its subscribers (`NSMapTable` or a wrapper struct).

### Q14. Scenario: Why defines `@escaping` closure?

**Answer:**
An `@escaping` closure is passed as an argument but called *after* the function returns (e.g., Asynchronous API).
Because it escapes the function scope, it MUST capture its state (and `self`) strongly to exist later.
**Implication**: You almost always need `[weak self]` in escaping closures.

### Q15. Scenario: Does `static` variable ever get deallocated?

**Answer:**
No. Static properties (Singletons) live for the entire lifecycle of the App.
If you store a large array in a `static var` and never clear it, that memory is "leaked" (in the sense that it's permanently occupied) until the app is killed.
