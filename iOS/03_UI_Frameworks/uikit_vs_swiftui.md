# ⚔️ UIKit vs SwiftUI
> **Targeted for iOS Developers**
> **Note:** Imperative vs Declarative, Interop.

![UI](https://img.shields.io/badge/iOS-UI_Frameworks-blueviolet?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Fundamental Differences](#1-fundamental-differences)
- [2. Pros & Cons](#2-pros--cons)
- [3. Interoperability](#3-interoperability)

---

### Q1. Imperative (UIKit) vs Declarative (SwiftUI)?

**Answer:**
- **Imperative (UIKit)**: You tell the system *how* to build the UI step-by-step.
  - "Create a button. Set its frame. Set its title. Add it to subview."
  - **State**: You manage state updates manually (e.g., updating a label text when data changes).
- **Declarative (SwiftUI)**: You describe *what* the UI should look like for a given state.
  - "The UI is a generic list of users."
  - **State**: The framework automatically rebuilds the UI when state changes.

### Q2. Architecture Differences?

**Answer:**
- **UIKit**: Heavily reliant on **MVC** (UIViewController is central).
- **SwiftUI**: Designed for **MVVM**. The View observes a ViewModel (ObservableObject), and bindings update the UI automatically.

### Q3. How to use UIKit inside SwiftUI?

**Answer:**
Use `UIViewRepresentable` (for Views) or `UIViewControllerRepresentable` (for VCs).
1.  Conform to the protocol.
2.  Implement `makeUIView` (create the UIKit view).
3.  Implement `updateUIView` (update UIKit view from SwiftUI state).

### Q4. How to use SwiftUI inside UIKit?

**Answer:**
Use `UIHostingController`.
It wraps a SwiftUI View and presents it like a normal UIViewController.
```swift
let swiftUIView = MyView()
let hostingController = UIHostingController(rootView: swiftUIView)
present(hostingController, animated: true)
```
