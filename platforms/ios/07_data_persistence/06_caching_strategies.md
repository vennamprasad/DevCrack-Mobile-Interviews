# 🚀 Caching Strategies
> **Targeted for Senior iOS Developers**
> **Note:** Memory vs Disk, NSCache.

![Cache](https://img.shields.io/badge/Performance-Caching-orange?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Memory Cache vs Disk Cache](#1-memory-vs-disk)
- [2. NSCache](#2-nscache)
- [3. URLCache](#3-urlcache)

---

### Q1. Core Concept: Two-Level Caching?

**Answer:**
1.  **Memory Cache (L1)**: Very fast (RAM). Volatile. Cleared on app kill or low memory.
2.  **Disk Cache (L2)**: Slower (File System). Persistent. Survives app restarts.
**Flow**: Check Memory -> Check Disk -> Fetch Network -> Write Disk -> Write Memory.

### Q2. What is `NSCache`?

**Answer:**
A mutable collection (like a Dictionary) but:
- **Thread-safe**: Can be accessed from multiple threads.
- **Auto-Eviction**: Automatically removes items when system memory is low.
- **Non-Copying**: Does not copy keys (unlike Dictionary).

### Q3. `URLCache`?

**Answer:**
The built-in caching for `URLSession`.
- Caches HTTP responses based on Headers (`Cache-Control`, `ETag`).
- Requires correct server configuration to work well.
- `URLCache.shared = URLCache(memoryCapacity: ..., diskCapacity: ...)`

### Q4. Custom Implementations?

**Answer:**
Libraries like **Kingfisher** or **SDWebImage** implement robust image caching.
- Downsampling images to save memory.
- Asymtotic expiration (delete files older than 7 days).
