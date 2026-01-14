# 🎻 Instruments Tool
> **Targeted for iOS Developers**
> **Note:** Time Profiler, Allocations, and Leaks.

![Instruments](https://img.shields.io/badge/Debug-Instruments-orange?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Time Profiler](#1-time-profiler)
- [2. Allocations](#2-allocations)
- [3. Leaks](#3-leaks)

---

### Q1. What is the Time Profiler?

**Answer:**
A tool to analyze CPU usage.
- It snapshots the call stack every millisecond.
- **Use case**: Finding "Heaviest Stack Trace" (methods taking the most time).
- **Tip**: Always profile in **Release Mode** (Optimizations On) to get real-world data.

### Q2. Allocations Instrument?

**Answer:**
Tracks memory usage over time.
- **Persistent Bytes**: Memory currently used.
- **Transient Buildup**: Memory allocated and freed rapidly (Churn).
- **Use case**: Finding "Memory Abandonment" (e.g., Cache growing indefinitely).

### Q3. How to detect Hangs?

**Answer:**
Instruments > **Hang Tracer**.
- Detects periods where the main thread is blocked for >250ms.
- Shows you exactly which function was blocking the UI.

### Q4. Signposts?

**Answer:**
`OSSignposter`.
A way to mark start/end events in your code that show up visually in Instruments.
```swift
let signposter = OSSignposter()
let state = signposter.beginInterval("Parsing JSON")
// ... work ...
signposter.endInterval("Parsing JSON", state)
```
