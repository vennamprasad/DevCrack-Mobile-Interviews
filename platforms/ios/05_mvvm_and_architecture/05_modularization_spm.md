# 📦 Modularization
> **Targeted for Senior iOS Developers**
> **Note:** SPM, Frameworks, and Build Times.

![Modularization](https://img.shields.io/badge/Architecture-Modules-brown?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Monolith vs Modular via SPM](#1-monolith-vs-modular)
- [2. Benefits](#2-benefits)
- [3. Challenges](#3-challenges)

---

### Q1. What is Modularization?

**Answer:**
Breaking a large app (Monolith) into smaller, independent frameworks or packages (Modules).
- **Core**: Networking, Utilities, Extensions.
- **UI**: Design System.
- **Features**: Home, Profile, Login (depend on Core & UI).
- **App**: Thin glue layer connecting Features.

### Q2. Why Modularize?

**Answer:**
1.  **Build Times**: Changing code in "Home" doesn't require recompiling "Profile". Swift Package Manager (SPM) caches built modules.
2.  **Code Ownership**: Team A owns "Home", Team B owns "Profile". Clear boundaries.
3.  **Reusability**: "Core" module can be shared between the iOS App and an App Clip or Watch App.

### Q3. Static vs Dynamic Frameworks?

**Answer:**
- **Static (`.a`)**: Code is copied into the executable at compile time. Faster launch, larger app binary size.
- **Dynamic (`.dylib`/`.framework`)**: Code is loaded at runtime. Slower launch, shared memory, smaller initial app download (sometimes).
**Recommendation**: Use Static Library (Mergeable Libraries) for internal modules for best performance.

### Q4. Common Pitfalls?

**Answer:**
- **Circular Dependencies**: Module A imports B, B imports A. (Compiler Error).
- **Complexity**: Setting up the graph requires overhead.
