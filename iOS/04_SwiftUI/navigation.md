# 🧭 Navigation in SwiftUI
> **Targeted for iOS Developers**
> **Note:** NavigationStack, Sheets, and Deep Linking.

![Navigation](https://img.shields.io/badge/SwiftUI-Navigation-green?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. NavigationStack (iOS 16+)](#1-navigationstack)
- [2. NavigationView (Legacy)](#2-navigationview)
- [3. Programmatic Navigation](#3-programmatic-navigation)

---

### Q1. `NavigationStack` vs `NavigationView`?

**Answer:**
- **`NavigationView`**: Deprecated. Had issues with programmatic navigation and split-view behavior.
- **`NavigationStack`**: Modern (iOS 16). Supports **path-based** navigation. You pass a Binding to a path (Array of data), and the stack renders the corresponding views.

### Q2. How to navigate programmatically?

**Answer:**
Using `NavigationStack(path: $path)`.
- Push: `path.append(MyDataType.detail(id: 1))`
- Pop: `path.removeLast()`
- Pop to Root: `path.removeAll()`

### Q3. `.sheet` vs `.fullScreenCover`?

**Answer:**
- **Sheet**: Modally presents a view (card style). Can be dismissed by dragging down. Context is preserved.
- **FullScreenCover**: Covers the entire screen. Cannot be dragged to dismiss (requires close button). Used for immersive flows (Login, Onboarding).

### Q4. Passing data back from a Detail view?

**Answer:**
1.  Pass a **`@Binding`** to the detail view.
2.  Use a shared **`@EnvironmentObject`**.
3.  Use a callback closure.
