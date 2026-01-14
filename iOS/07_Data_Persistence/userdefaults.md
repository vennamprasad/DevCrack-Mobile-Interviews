# ⚙️ UserDefaults
> **Targeted for iOS Developers**
> **Note:** Lightweight storage for settings.

![UserDefaults](https://img.shields.io/badge/Storage-UserDefaults-lightgrey?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. When to use?](#1-when-to-use)
- [2. What to store?](#2-what-to-store)
- [3. Performance](#3-performance)

---

### Q1. What is UserDefaults?

**Answer:**
A simple key-value store for saving user preferences. It persists data across app launches.
- **Backend**: Uses a `.plist` file located in the app's Library/Preferences folder.

### Q2. Is it secure?

**Answer:**
**NO**.
The plist file is unencrypted. Anyone with access to the file system (Jailbreak) can read it.
**Never store**: Passwords, API Tokens, or PII.

### Q3. Performance Implications?

**Answer:**
**Loaded into memory** at launch.
- If you store a large image or huge JSON blob, it slows down app startup.
- **Limit**: Keep it for small flags (`Bool`, `Int`, `String`).

### Q4. `UserDefaults.standard.synchronize()`?

**Answer:**
Deprecated.
In the past, you called this to force a write to disk. Now, the OS handles synchronization automatically and efficiently.
