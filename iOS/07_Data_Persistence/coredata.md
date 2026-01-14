# 🗄️ Core Data
> **Targeted for iOS Developers**
> **Note:** Object Graph vs Database.

![Core Data](https://img.shields.io/badge/Storage-Core_Data-blue?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. The Stack](#1-the-stack)
- [2. Concurrency](#2-concurrency)
- [3. Fetching](#3-fetching)

---

### Q1. Is Core Data a Database?

**Answer:**
**No**, it's an **Object Graph Manager**.
It *can* use SQLite as a backing store, but its primary job is managing the lifecycle of objects (Entities) and their relationships.
Unlike SQL, you work with Swift objects, not rows/tables.

### Q2. The Core Data Stack?

**Answer:**
1.  **Managed Object Model**: The Schema (Entities).
2.  **Persistent Store Coordinator**: Handles the file on disk (SQLite).
3.  **Managed Object Context (MOC)**: The "Scratchpad". You load objects here, modify them, and call `save()` to push changes to disk.

### Q3. Thread Safety?

**Answer:**
`NSManagedObjectContext` is **not Thread Safe**.
- **Main Context**: Use on Main Thread (UI).
- **Background Context**: Use `perform { ... }` block to execute work on the correct internal queue. passing Managed Objects between threads results in a crash (use `ObjectID` instead).

### Q4. `NSFetchedResultsController`?

**Answer:**
A helper class efficiently managing the results of a Core Data fetch request and displaying data to the user. It integrates with TableView/CollectionView to handle batch updates (insert/delete rows) automatically when data changes.
