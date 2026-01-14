# 💥 Crash Logs
> **Targeted for iOS Developers**
> **Note:** Symbolication, Signals, and Exception Types.

![Crash](https://img.shields.io/badge/Debug-Crash_Logs-red?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Symbolication](#1-symbolication)
- [2. Common Exceptions](#2-common-exceptions)
- [3. Signals (SIGSEGV, SIGABRT)](#3-signals)

---

### Q1. What is Symbolication?

**Answer:**
The process of waiting memory addresses (e.g., `0x0001234`) into human-readable function names (`MyClass.myFunction`).
Requires the **dSYM** (Debug Symbol) file generated during the build.

### Q2. What is SIGABRT?

**Answer:**
**Signal Abort**.
Usually an "Uncaught Exception" caused by logic errors, not memory errors.
- **Common Cause**: Force unpacking nil (`!`), Interface Builder connection missing (`IBOutlet` is disconnected).

### Q3. What is SIGSEGV?

**Answer:**
**Signal Segmentation Violation**.
Invalid memory access.
- **Cause**: Dereferencing a null pointer (unsafe Swift), accessing deallocated memory (Use-after-free), or stack overflow.

### Q4. "Watchdog" Timeout (0x8badf00d)?

**Answer:**
The crash code literally reads "Ate Bad Food".
Occurs when the app takes too long to launch, terminate, or respond to system events.
- **Fix**: Move heavy work off the main thread during `didFinishLaunchingWithOptions`.
