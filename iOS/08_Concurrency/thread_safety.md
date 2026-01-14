# 🛡️ Thread Safety
> **Targeted for Senior iOS Developers**
> **Note:** Locks, Semaphores, and Atomics.

![Safety](https://img.shields.io/badge/Concurrency-Safety-red?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Race Condition](#1-race-condition)
- [2. Semaphores](#2-semaphores)
- [3. NSLock vs Actor](#3-nslock-vs-actor)

---

### Q1. What is a Race Condition?

**Answer:**
When multiple threads access shared data simultaneously, and at least one is writing. The final state depends on timing (chaos).
**Example**: Two threads increment `count` (val 5) at the same time. Both read 5, both write 6. Count should be 7, but is 6.

### Q2. `DispatchSemaphore`?

**Answer:**
A primitive to control access to a resource by multiple threads.
- `wait()`: Decrements count (blocks if < 0).
- `signal()`: Increments count.
- **Usage**: Limit concurrent downloads, or make an async task synchronous (wait for callback).

### Q3. `NSLock`?

**Answer:**
A simple Mutex (Mutual Exclusion) lock.
`lock.lock()` -> Do critical work -> `lock.unlock()`.
**Warning**: If you lock twice on the same thread without unlocking (Recursive Lock), you deadlock. Use `NSRecursiveLock` if needed.

### Q4. Why prefer Actors over Locks?

**Answer:**
- **Deadlock Free**: Actors generally prevent deadlocks (though reentrancy can cause logic bugs).
- **Compiler Checked**: The compiler forces you to use `await`, ensuring you don't forget to lock.
- **Performance**: Optimized for Swift's concurrency pool.
