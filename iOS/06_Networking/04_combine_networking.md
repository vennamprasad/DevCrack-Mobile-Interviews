# 🧶 Combine Framework
> **Targeted for iOS Developers**
> **Note:** Reactive Networking, Publishers, and Subscribers.

![Combine](https://img.shields.io/badge/Framework-Combine-blue?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Components](#1-components)
- [2. Networking with Combine](#2-networking-with-combine)
- [3. Operators](#3-operators)

---

### Q1. Core Components?

**Answer:**
1.  **Publisher**: Emits values over time (`Just`, `Future`, `PassthroughSubject`).
2.  **Subscriber**: Receives values (`sink`, `assign`).
3.  **Operator**: Modifies the stream (`map`, `filter`, `debounce`, `combineLatest`).

### Q2. Why is Combine useful for Networking?

**Answer:**
It handles the entire pipeline declaratively:
Fetch -> Retry -> Decode -> Map Error -> Receive on Main Thread -> Assign to UI.
```swift
URLSession.shared.dataTaskPublisher(for: url)
    .retry(3)
    .map { $0.data }
    .decode(type: User.self, decoder: JSONDecoder())
    .receive(on: DispatchQueue.main)
    .sink(...)
```

### Q3. `PassthroughSubject` vs `CurrentValueSubject`?

**Answer:**
- **`PassthroughSubject`**: Broadcasts events to subscribers. Does NOT hold a value. (Like a doorbell).
- **`CurrentValueSubject`**: Holds a value. New subscribers get the most recent value immediately. (Like a light switch state).

### Q4. `AnyCancellable`?

**Answer:**
The token returned when you subscribe (`.sink`). You must store this token (e.g., in a `Set<AnyCancellable>`).
If you don't store it, the subscription is cancelled immediately and the request dies.
