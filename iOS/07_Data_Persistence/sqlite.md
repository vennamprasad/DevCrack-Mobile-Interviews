# 🪨 SQLite & GRDB
> **Targeted for iOS Developers**
> **Note:** Raw SQL and Lightweight Wrappers.

![SQLite](https://img.shields.io/badge/Storage-SQLite-blue?style=for-the-badge&logo=sqlite&logoColor=white)

---

## 📖 Table of Contents
- [1. Why use SQLite directly?](#1-why-use-sqlite-directly)
- [2. Wrappers (GRDB, SQLite.swift)](#2-wrappers)

---

### Q1. Why choose SQLite over Core Data?

**Answer:**
- **Performance**: For massive bulk inserts, raw SQL is faster.
- **Portability**: Code/Schemas can be shared with Android/Backend.
- **Simplicity**: If you just need a simple table lookup without object graph overhead.
- **Control**: Full control over specific queries and indexes.

### Q2. Popular Libraries?

**Answer:**
- **GRDB.swift**: A "toolkit for SQLite databases". Highly recommended. Type-safe, supports WAL mode, concurrency.
- **SQLite.swift**: Type-safe wrapper.
- **FMDB**: Objective-C wrapper (Legacy).

### Q3. WAL Mode?

**Answer:**
**Write-Ahead Logging**.
Allows simultaneous Readers and Writers.
- Without WAL: A write locks the database (readers block).
- With WAL: Writers write to a separate log file, integrated later. Readers read from the DB file.
Essential for performant apps.
