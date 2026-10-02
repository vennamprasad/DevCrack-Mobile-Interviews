# 🚦 GCD (Grand Central Dispatch)
> **Targeted for iOS Developers**
> **Note:** Dispatch Queues, Groups, and Barriers.

![GCD](https://img.shields.io/badge/Concurrency-GCD-lightgrey?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Queues](#1-queues)
- [2. DispatchGroup](#2-dispatchgroup)
- [3. Barriers](#3-barriers)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

### Q1. Main vs Global Queue?

**Answer:**
- **Main**: Serial. UI updates. High priority.
- **Global**: Concurrent. Background work. QoS classes:
    - `.userInteractive` (Animations)
    - `.userInitiated` (Immediate results, e.g., Open File)
    - `.utility` (Long running, e.g., Download)
    - `.background` (Pre-fetching)

### Q2. `sync` vs `async`?

**Answer:**
- **`sync`**: Blocks the current thread until the task finishes.
- **`async`**: Returns immediately, task runs eventually.
**Deadlock Danger**: Calling `main.sync` from the Main Thread causes a deadlock because the queue waits for the block, and the block waits for the queue.

### Q3. What is a DispatchGroup?

**Answer:**
Allows tracking a group of tasks.
```swift
let group = DispatchGroup()
group.enter(); api1 { group.leave() }
group.enter(); api2 { group.leave() }

group.notify(queue: .main) {
    print("All APIs finished")
}
```

### Q4. Readers-Writers Problem (Barrier)?

**Answer:**
Use a **Concurrent Queue** with a **Barrier Flag**.
- **Reads**: Run concurrently (`queue.async`).
- **Writes**: Run exclusively (`queue.async(flags: .barrier)`). The barrier ensures no other reads/writes happen while writing.

---

### 5. Real-World Scenarios

### Q5. Scenario: User reports the UI freezes for 0.5s when scrolling.

**Answer:**
You are likely running heavy code on the **Main Thread**.
- JSON Decoding?
- Image Filtering?
- DateFormatter creation?
**Fix**: Dispatch to background.
```swift
DispatchQueue.global(qos: .userInitiated).async {
    let result = heavyWork()
    DispatchQueue.main.async { updateUI(result) }
}
```

### Q6. Scenario: You need to download 3 images, wait for ALL to finish, then update UI.

**Answer:**
Use **DispatchGroup**.
(See Q3).
**Gotcha**: Ensure you call `leave()` even if the download fails (error case), otherwise `notify` is never called.

### Q7. Scenario: A thread-safe Array crashes randomly.

**Answer:**
You might be returning a reference to an object *inside* the lock, but modifying it outside?
Or you are using a concurrent queue but forgot the barrier for writes.
**Concurrent Read / Exclusive Write** is the standard pattern.

### Q8. Scenario: `DispatchQueue.main.sync` usage?

**Answer:**
Rarely good.
Only valid use case: You are on a background thread, and you need to fetch a value from the Main Thread *synchronously* to proceed. (And implementation must ensure you aren't already on main).

### Q9. Scenario: Priority Inversion?

**Answer:**
High-priority queue (User Interactive) is waiting for a Low-priority queue (Background) to release a lock. System might upgrade the priority of the low queue temporarily to solve this, but it hurts performance.

### Q10. Scenario: How to delay execution?

**Answer:**
`DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) { ... }`.
**Warning**: If you need to cancel this, GCD is clunky (need `DispatchWorkItem`). `Timer` or `async/await` (Task.sleep) is often better for cancellable delays.

### Q11. Scenario: Semaphore limiting network calls?

**Answer:**
You have 1000 URLs. You want to download max 4 at a time.
```swift
let semaphore = DispatchSemaphore(value: 4)
for url in urls {
    globalQueue.async {
        semaphore.wait() // -1
        download(url)
        semaphore.signal() // +1
    }
}
```

### Q12. Scenario: Avoiding "Explosion" of threads?

**Answer:**
If you dispatch 1000 tasks to a concurrent queue `queue.async`, GCD might spawn 64+ threads, consuming thread stack memory.
**Fix**: Use `concurrentPerform` (legacy `apply`) which tunes itself to the number of Cores, or use DispatchSemaphore to throttle.

### Q13. Scenario: What is QoS "Unspecified"?

**Answer:**
The system infers priority from the current thread. If you call it from Main, it might be high. If from background, low. Explicitly setting QoS is safer.

### Q14. Scenario: Detecting if on Main Thread?

**Answer:**
`Thread.isMainThread`.
Useful for assertions in UI code.
`assert(Thread.isMainThread)`

### Q15. Scenario: Correct way to update UI from Background?

**Answer:**
Bad: `label.text = "Done"` (Crash).
Good: `DispatchQueue.main.async { label.text = "Done" }`.
Better (Modern): Use actors or `@MainActor` to let the compiler enforce this.
