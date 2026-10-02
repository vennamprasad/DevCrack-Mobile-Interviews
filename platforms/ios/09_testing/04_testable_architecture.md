# 🏗️ Testable Architecture
> **Targeted for Senior iOS Developers**
> **Note:** Decoupling for Testability.

![Architecture](https://img.shields.io/badge/Testing-Architecture-purple?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Humble Object Pattern](#1-humble-object)
- [2. Singleton Problem](#2-singleton-problem)
- [3. Composition Root](#3-composition-root)

---

### Q1. Why is MVC hard to test?

**Answer:**
Logic is trapped inside `UIViewController`, which gets created by Storyboards or the System. You can't easily inject dependencies or capture the output (View changes).

### Q2. What is the Humble Object Pattern?

**Answer:**
Move all logic OUT of the hard-to-test class (ViewController) into a separate, easy-to-test class (ViewModel/Presenter).
The VC becomes "Humble" - it does nothing but forward events and update UI. We test the Logic class, and assume the Humble object works (or use UI Tests for it).

### Q3. Should you test Singletons?

**Answer:**
**Testing Singletons is hard** because state persists between tests. (Test A sets UserID, Test B expects nil but finds UserID).
**Fix**: Don't use `shared` instances directly. Inject them.
`init(api: API = API.shared)`. In tests, pass `MockAPI()`.

### Q4. Composition Root?

**Answer:**
The place where the graph of objects is assembled (usually `AppCoordinator` or `SceneDelegate`).
The goal is to have **Zero** `new Class()` calls inside your business logic classes. Everything is passed in.
