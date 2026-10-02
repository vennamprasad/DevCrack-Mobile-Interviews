# ⚙️ OperationQueue
> **Targeted for iOS Developers**
> **Note:** Dependencies and Cancellation.

![Operations](https://img.shields.io/badge/Concurrency-Operations-grey?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Operation vs GCD](#1-operation-vs-gcd)
- [2. Dependencies](#2-dependencies)
- [3. Cancellation](#3-cancellation)

---

### Q1. Difference from GCD?

**Answer:**
`OperationQueue` is built on top of GCD.
- **GCD**: Fire and forget. Lightweight closures. Hard to cancel.
- **Operation**: Object-oriented (`Operation` class). Can fail, retry, have dependencies, and be cancelled.

### Q2. How to handle Dependencies?

**Answer:**
You can ensure Task B starts only after Task A finishes.
```swift
let op1 = BlockOperation { ... }
let op2 = BlockOperation { ... }
op2.addDependency(op1) // op2 waits for op1
queue.addOperations([op1, op2], waitUntilFinished: false)
```

### Q3. What is `maxConcurrentOperationCount`?

**Answer:**
Limits the number of tasks running at once.
- Set to `1` to turn an OperationQueue into a **Serial Queue**.
- Set to `N` to control load (e.g., limit image downloads to 4 at a time).

### Q4. Implementation state?

**Answer:**
Subclassing `Operation` requires managing state variables: `isReady`, `isExecuting`, `isFinished`, `isCancelled`. Usually tedious, hence `BlockOperation` is preferred for simple tasks.
