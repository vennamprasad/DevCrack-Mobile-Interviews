# 🖼️ Android Classic View System & UI Engineering

> **Comprehensive guide to the Android View system: View vs ViewGroup, Layouts, Custom Views, Measure/Layout/Draw passes, and Touch Event Dispatch.**

![AndroidUI](https://img.shields.io/badge/UI-View_System-3DDC84?style=for-the-badge&logo=android)
![Layouts](https://img.shields.io/badge/Layout-ConstraintLayout-blue?style=for-the-badge)
![Rendering](https://img.shields.io/badge/Rendering-Measure_Layout_Draw-orange?style=for-the-badge)

---

## 📖 Chapter Index

- **[Android UI Interview Questions & Answers](./01_views_and_layouts.md)**
  - **1. Core View Hierarchy:** `View` vs `ViewGroup`, View tree hierarchy, inflation process (`LayoutInflater`), and `findViewById` vs View Binding.
  - **2. Layout Management:** `ConstraintLayout` (chains, barriers, guidelines, ratios, flow), `LinearLayout` (weights and double measurement penalty), `RelativeLayout`, `FrameLayout`, and `CoordinatorLayout`.
  - **3. Screen Densities & Responsiveness:** Density-independent pixels (`dp`), scale-independent pixels (`sp`), resource qualifiers (`layout-sw600dp`, `drawable-xxhdpi`), and vector drawables (`VectorDrawableCompat`).
  - **4. The UI Rendering Pipeline:** The 3-phase drawing cycle:
    1. `onMeasure()`: Parents determine constraints (`MeasureSpec.EXACTLY`, `AT_MOST`, `UNSPECIFIED`) and children measure dimensions.
    2. `onLayout()`: Parents assign screen coordinates `(left, top, right, bottom)` to children.
    3. `onDraw()`: Canvas operations, Paint flags, hardware acceleration, and avoiding allocations inside `onDraw`.
  - **5. Touch Event Dispatch Architecture:** `dispatchTouchEvent()`, `onInterceptTouchEvent()`, `onTouchEvent()`, down-up motion event bubbling, and custom gesture detectors.

---

> [!NOTE]
> For modern declarative UI development with Jetpack Compose, see our dedicated 25-part **[Jetpack Compose Guide](../05_jetpack_compose/README.md)**.
