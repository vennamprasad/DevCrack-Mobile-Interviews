# 🌊 Async/Await Deep Dive
> **Targeted for Senior iOS Developers**
> **Note:** Actors, Sendable, and TaskGroups.

![Async](https://img.shields.io/badge/Concurrency-Deep_Dive-orange?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Actors](#1-actors)
- [2. Sendable Protocol](#2-sendable)
- [3. TaskGroup](#3-taskgroup)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

### Q1. What is an Actor?

**Answer:**
A reference type (like class) that protects its mutable state. 
- Only one task can access the actor's state at a time (Serial access).
- Prevents Data Races.
- Calls to an actor must be `await`ed.

### Q2. `@MainActor`?

**Answer:**
A global actor singleton that represents the Main Thread.
Annotating a class, function, or property with `@MainActor` ensures it *always* runs on the main thread.
```swift
@MainActor
class ViewModel: ObservableObject {
    func updateUI() { ... } // Safe
}
```

### Q3. Explain `Sendable`.

**Answer:**
A marker protocol indicating that a type is safe to pass between concurrent boundaries (Threads/Actors).
- **Value types** (structs/enums) are automatically Sendable.
- **Classes** are Sendable only if they are final and have immutable properties (or internal locking).
- Closures marked `@Sendable` cannot capture mutable local variables.

### Q4. `ThrowingTaskGroup`?

**Answer:**
Allows dynamic creation of tasks (e.g., looping through an array of URLs and fetching them all in parallel).
```swift
await withThrowingTaskGroup(of: Data.self) { group in
    for url in urls {
        group.addTask { try await fetch(url) }
    }
    for try await result in group { ... }
}
```

---

### 5. Real-World Scenarios

### Q5. Scenario: "Actor Reentrancy" caused a bug. What is it?

**Answer:**
Actors prevent simultaneous access, but they assume functions can be paused (`await`).
1.  Func A starts. Modifies state to "Loading".
2.  Func A awaits API. (Paused). **Actor lock is released**.
3.  Func B starts. Modifies state to "Empty".
4.  Func A resumes. Modifies state to "Loaded".
**Bug**: State was corrupted/changed while Func A was sleeping.
**Fix**: Check state validity *after* every `await`.

### Q6. Scenario: `Task.sleep` usage?

**Answer:**
`try await Task.sleep(nanoseconds: 1 * 1_000_000_000)`.
Unlike `Thread.sleep` (which blocks system thread), this suspends the task efficiently, allowing the thread to do other work.

### Q7. Scenario: Converting legacy callback-based API to Async/Await?

**Answer:**
Use **CheckedContinuation**.
```swift
func fetchUser() async throws -> User {
    return try await withCheckedThrowingContinuation { continuation in
        legacyFetch { result, error in
            if let e = error { continuation.resume(throwing: e) }
            else { continuation.resume(returning: result!) }
        }
    }
}
```
**Rule**: You must call resume *exactly once*.

### Q8. Scenario: `async let` vs `TaskGroup`?

**Answer:**
- **`async let`**: Fixed number of tasks (e.g., "Get Profile" AND "Get Friends").
- **`TaskGroup`**: Dynamic loop (e.g., "Get Details for these 50 IDs").

### Q9. Scenario: How to unit test async code?

**Answer:**
XCTest supports async.
```swift
func testDownload() async throws {
    let data = try await service.download()
    XCTAssertNotNil(data)
}
```

### Q10. Scenario: Compiler Error "Type cannot be passed to a concurrent closure because it is not Sendable".

**Answer:**
You are passing a mutable Class across threads.
- Fix 1: Make it a `struct`.
- Fix 2: Make it an `actor`.
- Fix 3: Mark it `@unchecked Sendable` (if you promise you are handling locking manually).

### Q11. Scenario: Cancellation of a long running loop?

**Answer:**
Your async function loops 1 million times processing records. User cancels.
- The loop continues unless you check `Task.isCancelled`.
- **Fix**: Add `try Task.checkCancellation()` inside the loop occasionally.

### Q12. Scenario: `Task.init` vs `Task.detached` priority?

**Answer:**
- `Task.init`: Inherits priority (e.g., UserInitiated).
- `Task.detached`: Default priority (unless specified).
If debugging a slow UI update, check if you accidentally used `detached` which might run on a lower priority thread.

### Q13. Scenario: Global Actor/Singleton?

**Answer:**
You can define your own Global Actor if you want a specific subsystem (e.g., database) to always run on one shared serial executor.
```swift
@globalActor actor DatabaseActor {
    static let shared = DatabaseActor()
}
@DatabaseActor func save() { ... }
```

### Q14. Scenario: Swift 6 Strict Concurrency?

**Answer:**
Swift 6 enables "Complete Strict Concurrency Checking".
It produces warnings/errors for every possible race condition (passing non-Sendable types).
A strict audit of your codebase is required (lots of `@Sendable` annotations needed).

### Q15. Scenario: `AsyncSequence`?

**Answer:**
Like a list, but items arrive over time.
- Reading from a socket.
- Processing a large file line-by-line.
Usage: `for try await line in file.lines { ... }`.
