# 🚀 SwiftUI Performance Optimization
> **Targeted for Senior iOS Developers**
> **Note:** View Redraws, Equatable, and Profiling.

![Performance](https://img.shields.io/badge/SwiftUI-Performance-red?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Identifying Issues](#1-identifying-issues)
- [2. Optimization Techniques](#2-optimization-techniques)
- [3. EquatableView](#3-equatableview)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

### Q1. How to debug redraws?

**Answer:**
1.  **Instruments**: "SwiftUI View Body" instrument.
2.  **Debug Print**: `let _ = Self._printChanges()` inside the `body`. It prints *why* the view is redrawing (e.g., "@self changed", "Prop 'user' changed").
3.  **Random Background**: Give views a random background color on init/body to visually see flashes of redraws.

### Q2. Why use `EquatableView`?

**Answer:**
By default, SwiftUI checks if a View's parameters changed. If they are complex structs, diffing takes time.
Conform your View to `Equatable`.
```swift
struct MyView: View, Equatable {
    let id: Int
    // ...
    static func == (lhs: MyView, rhs: MyView) -> Bool {
        return lhs.id == rhs.id
    }
}
```
SwiftUI will skip calling `body` if `==` returns true.

### Q3. Minimize Modifier Cost?

**Answer:**
Expensive modifiers (Shadows, Corner Radius, Blurs) cause off-screen rendering.
- Use `.drawingGroup()`: Flattens the view hierarchy into a single GPU-rendered image (Metal). Useful for complex graphics, bad for text quality.

### Q4. Heavy Computations?

**Answer:**
Never calculate heavy data inside `var body: some View`.
`body` can be called 60-120 times a second. Move logic to the **ViewModel** or compute once in `onAppear`/`task`.

---

### 5. Real-World Scenarios

### Q5. Scenario: A List with 1000 items is laggy when scrolling using `List`.

**Answer:**
1.  **Row Complexity**: Is the row computing something heavy?
2.  **Identifiers**: Are you using `id: \.uuid` where a new UUID is generated every time? That forces a redraw. Use stable IDs.
3.  **Images**: Are you loading images on the main thread? Use `AsyncImage`.

### Q6. Scenario: `LazyVGrid` is stuttering when new items appear.

**Answer:**
"Lazy" means items are created just before they appear. If the creation (init) of your ItemView is heavy, sending it to the main thread causes a stutter (dropped frame).
**Fix**: Simplify the `init()` of the child view. Do not trigger network calls or format dates in `init()`.

### Q7. Scenario: High CPU usage even when the app is idle.

**Answer:**
Check for **infinite animation loops**.
Example: `ProgressView()` spinning forever even if hidden (via opacity).
**Fix**: Use `if isVisible { ProgressView() }` to remove it from the hierarchy when not needed.

### Q8. Scenario: Typing in a TextField causes the whole screen to reload.

**Answer:**
The TextField updates a `@State` string. If that state is passed to the *root* view, everything redrawing is technically correct behavior.
**Fix**: Isolate the TextField into a subview that holds its own `@State`. Or verify if other views strictly depend on that text.

### Q9. Scenario: Memory Graph shows thousands of Environment objects.

**Answer:**
Leak.
Passing `.environmentObject` to a View that doesn't need it doesn't cause a leak, BUT capturing it in a closure (e.g., inside a modifier) might.

### Q10. Scenario: When to use `GeometryReader`?

**Answer:**
Sparingly.
`GeometryReader` breaks the layout flow (it expands to fill all space).
It also triggers redraws whenever the parent size changes.
**Alt**: Use `PreferenceKeys` to coordinate size changes without the heavy hammer of GeometryReader.

### Q11. Scenario: App is slow on older devices (iPhone X) but fine on iPhone 15 Pro.

**Answer:**
Likely **Off-Screen Rendering**.
Usage of `.shadow`, `.cornerRadius`, `.mask`.
**Fix**:
- Use `.clipShape(RoundedRectangle...)` instead of mask where possible.
- Use `shadowPath` in UIKit, or `.drawingGroup()` in SwiftUI for static content.

### Q12. Scenario: `AnyView` impact?

**Answer:**
Using `AnyView` (Type erasure) destroys the view's identity.
SwiftUI cannot diff "Old View" vs "New View" efficiently, so it destroys/recreates the underlying object (Structural Identity lost).
**Avoid**: `func makeView() -> AnyView`. Use `@ViewBuilder` instead.

### Q13. Scenario: `ForEach` with indices?

**Answer:**
`ForEach(0..<items.count, id: \.self)` is dangerous.
If you delete item 0, item 1 becomes item 0. SwiftUI tries to animate the change but gets confused because the ID (index) matches the old one but the data changed.
**Always** use stable IDs (e.g., UUID or DB Primary Key).

### Q14. Scenario: Background threads & UI?

**Answer:**
If you accidentally update a `@Published` property from a background thread, SwiftUI complains (purple warning) and behavior is undefined.
**Fix**: `await MainActor.run { val = newVal }`.

### Q15. Scenario: Image resizing is creating a memory spike.

**Answer:**
Loading a 4K image into a 50x50 icon View.
SwiftUI `Image(uiImage: ...)` loads the full bitmap.
**Fix**: Downsample the image using `ImageIO` *before* creating the UIImage/SwiftUI View.
