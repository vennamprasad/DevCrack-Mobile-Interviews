# 🔄 View Lifecycle (SwiftUI)
> **Targeted for iOS Developers**
> **Note:** Appear, Disappear, and Identity.

![Lifecycle](https://img.shields.io/badge/SwiftUI-Lifecycle-blue?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Events](#1-events)
- [2. View Identity](#2-view-identity)
- [3. Redraw Triggers](#3-redraw-triggers)

---

### Q1. `onAppear` vs `task`?

**Answer:**
- **`onAppear`**: Synchronous. Runs when view enters hierarchy. Good for animations or tracking.
- **`task`**: Asynchronous. Part of Swift Concurrency. Starts immediately on appear, automatically cancels on disappear. **Best for data fetching**.

### Q2. `onChange(of:)`?

**Answer:**
Fires whenever the specified equatable value changes.
```swift
.onChange(of: selection) { newValue in
    print("User selected: \(newValue)")
}
```

### Q3. What is Structural Identity vs Explicit Identity?

**Answer:**
SwiftUI needs to know if two views are the same (to animate changes) or different (to transition).
- **Explicit (`.id(...)`)**: You manually tell SwiftUI "This is unique". Good for forcing a full view recreation.
- **Structural**: SwiftUI infers identity from the view hierarchy (e.g., `if-else` branches).

### Q4. Why is my View redrawing too often?

**Answer:**
- Passing a new **object reference** (even if data hasn't changed) to a child view not using `EquatableView`.
- Accessing a `@Published` property that updates frequently, even if that specific property isn't used in the `body`.
- **Fix**: Break views into smaller components using `let` properties (SwiftUI diffs value types very fast).
