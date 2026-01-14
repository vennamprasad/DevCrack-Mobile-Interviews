# 🖼️ UIKit Core Concepts
> **Targeted for iOS Developers**
> **Note:** View Hierarchy, Auto Layout, and View Controllers.

![UIKit](https://img.shields.io/badge/Framework-UIKit-CC4400?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. View Hierarchy](#1-view-hierarchy)
- [2. Auto Layout](#2-auto-layout)
- [3. Core Components](#3-core-components)

---

### Q1. `UIView` vs `CALayer`?

**Answer:**
- **UIView**: Handles Layout and Touch Handling.
- **CALayer**: Handles Content Rendering (Drawing) and Animation. Underneath every UIView is a CALayer.
- **Why distinction?**: Separation of concerns. On macOS, Views are click-heavy, on iOS touch-heavy, but drawing logic is shared via Core Animation (CALayer).

### Q2. Explain `safeAreaLayoutGuide`.

**Answer:**
A rectangular area that ensures content is not covered by:
- The dynamic island / notch.
- The home indicator.
- Navigation or Tab bars.
constraints should be pinned to the `safeAreaLayoutGuide`, not the superview edges.

### Q3. Intrinsic Content Size?

**Answer:**
The size a view "wants" to be based on its content.
- `UILabel`: Size of the text.
- `UIButton`: Size of the title + padding.
- `UIView`: No intrinsic size (defaults to 0,0).
Auto Layout uses this to calculate layout without explicit width/height constraints.

### Q4. `setNeedsLayout` vs `layoutIfNeeded`?

**Answer:**
- **`setNeedsLayout`**: Flags the view for a layout update. It will happen during the next update cycle (async).
- **`layoutIfNeeded`**: Forces a layout update **immediately** if one is pending. (Used inside animation blocks to animate constraint changes).
