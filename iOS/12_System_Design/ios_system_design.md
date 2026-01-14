# 🏗️ iOS System Design
> **Targeted for iOS Developers**
> **Note:** High-level architecture, components, and trade-offs.

![Design](https://img.shields.io/badge/System-Design-blueviolet?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. The Framework](#1-the-framework)
- [2. Requirements](#2-requirements)
- [3. Components](#3-components)

---

### Q1. How to approach a Mobile System Design interview?

**Answer:**
**RAD C**:
1.  **Requirements**: Functional (Chat, Feed) & Non-functional (Offline support, Security, Real-time).
2.  **Architecture**: Networking, Data storage, Caching.
3.  **Data Model**: Entities (User, Message).
4.  **Component Design**: deep dive into difficult parts (Image loading, Sync engine).

### Q2. Client-Side Database choice?

**Answer:**
- **Core Data/SwiftData**: Complex relationships, Object graph management. Good for Offline-first.
- **SQLite/GRDB**: Performance, Simple relational data.
- **Realm**: Fast, easy API, cross-platform.
- **UserDefaults**: Only for settings.

### Q3. API Protocol choice?

**Answer:**
- **REST**: Standard, cacheable, easy to debug.
- **GraphQL**: Flexible, reduces over-fetching (good for mobile battery/data).
- **WebSockets**: Real-time (Chat, Location).

### Q4. Image Loading Library vs Custom?

**Answer:**
**Use Library (Kingfisher/SDWebImage)**.
Building a robust image loader is hard:
- In-memory cache (LRU).
- Disk cache.
- Background decoding (to avoid UI stutter).
- Duplicate request coalescing.
- Downsampling (save RAM).
