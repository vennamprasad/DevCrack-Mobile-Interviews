# ⚡ Async/Await Networking
> **Targeted for iOS Developers**
> **Note:** Structured Concurrency in API calls.

![Async](https://img.shields.io/badge/Swift-Async_Await-orange?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. The Old Way (Completion Handlers)](#1-the-old-way)
- [2. The New Way (Async/Await)](#2-the-new-way)
- [3. Parallel Requests](#3-parallel-requests)

---

### Q1. Why switch to Async/Await?

**Answer:**
- **Readability**: Code looks linear (top to bottom) instead of nested closures ("Pyramid of Doom").
- **Safety**: Compiler ensures you handle errors and return values on all paths.
- **Threading**: Automatically hops off the main thread for the wait, and hops back (if part of `@MainActor`).

### Q2. How to make parallel API calls?

**Answer:**
Use `async let` for concurrency.
```swift
async let users = fetchUsers()
async let posts = fetchPosts()

// This line waits for both to complete
let (u, p) = try await (users, posts)
```

### Q3. `Task` vs `Task.detached`?

**Answer:**
- **`Task { ... }`**: Inherits the priority and Actor context (e.g., MainActor) of the caller. Safe for UI updates.
- **`Task.detached { ... }`**: Does NOT inherit context. Runs on a generic background thread. Use for non-UI heavy work.

### Q4. Canceling a Request?

**Answer:**
Tasks supports cooperative cancellation.
Keep a reference to the `Task`. Call `task.cancel()`.
Inside the async function, check `try Task.checkCancellation()` to stop work early.
