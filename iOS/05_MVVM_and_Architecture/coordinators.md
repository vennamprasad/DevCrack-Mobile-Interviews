# 🗺️ Coordinator Pattern
> **Targeted for Senior iOS Developers**
> **Note:** Navigation Logic, Flow Controllers.

![Coordinator](https://img.shields.io/badge/Pattern-Coordinator-orange?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. The Problem](#1-the-problem)
- [2. The Solution](#2-the-solution)
- [3. Implementation](#3-implementation)

---

### Q1. What problem does it solve?

**Answer:**
In standard iOS (MVC), View Controllers push other View Controllers:
`self.navigationController?.pushViewController(DetailVC(), animated: true)`
This creates **tight coupling**. Parent VC must know about Child VC and how to configure it. It makes reuse hard and testing navigation impossible.

### Q2. How does a Coordinator work?

**Answer:**
A Coordinator is a plain object responsible for navigation flow.
1.  **AppCoordinator**: Holds the `UIWindow`. Starts the first VC.
2.  **ChildCoordinators**: Handle specific flows (e.g., AuthCoordinator, FeedCoordinator).
**Flow:**
- VC A tells Coordinator: "User tapped Login".
- Coordinator instantiates VC B, configures it, and pushes it.

### Q3. Protocol-based Communication?

**Answer:**
VCs should talk to Coordinators via **Delegates** or **Closures**.
- VC defines: `var didFinish: (() -> Void)?`
- Coordinator sets: `vc.didFinish = { [weak self] in self?.showNextScreen() }`
This keeps the VC completely unaware of the Coordinator or the next screen.

### Q4. SwiftUI "Coordinator"?

**Answer:**
In SwiftUI, "Coordinator" often refers to a `NSObject` class interacting with `UIViewRepresentable` delegates.
However, for navigation, the pattern is evolving into `NavigationStack` with `Path` binding managed by a Router/Flow object (StateObject).
