# ✨ Animations in SwiftUI
> **Targeted for iOS Developers**
> **Note:** Explicit vs Implicit, Transitions, and MatchedGeometryEffect.

![Animation](https://img.shields.io/badge/SwiftUI-Animations-purple?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Implicit vs Explicit](#1-implicit-vs-explicit)
- [2. Transitions](#2-transitions)
- [3. Matched Geometry](#3-matched-geometry)

---

### Q1. Implicit (`.animation`) vs Explicit (`withAnimation`)?

**Answer:**
- **Implicit**: Attached to a view. Animates *any* change that affects that view.
  ```swift
  .opacity(isVisible ? 1 : 0)
  .animation(.spring(), value: isVisible)
  ```
- **Explicit**: Wrap the state change. Specific.
  ```swift
  withAnimation(.spring()) {
      isVisible.toggle()
  }
  ```
  *Recommendation*: Use **Explicit** for better control.

### Q2. What is a Transition?

**Answer:**
Controls how a View **enters or leaves** the hierarchy (not just frame changes).
- `.transition(.slide)`
- `.transition(.scale)`
- Only works if the View is conditionally removed (`if showView { View() }`).

### Q3. `matchedGeometryEffect`?

**Answer:**
The "Hero Animation" of SwiftUI.
It interpolates the size and position of a view in one part of the hierarchy to match another view elsewhere, creating a smooth "morphing" effect (e.g., Grid Item -> Detail View).
Requires a shared `@Namespace`.

### Q4. Custom Timing Curves?

**Answer:**
- **Linear**: Constant speed.
- **EaseIn/Out**: Slow start/end.
- **Spring**: Physics-based (bouncy). Most natural for UI.
