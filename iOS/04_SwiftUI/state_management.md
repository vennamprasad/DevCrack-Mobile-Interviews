# 🧠 State Management in SwiftUI
> **Targeted for iOS Developers**
> **Note:** Property Wrappers and Flow of Data.

![State](https://img.shields.io/badge/SwiftUI-State-orange?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Data Flow Primitives](#1-data-flow-primitives)
- [2. Best Practices](#2-best-practices)
- [3. Observation framework (iOS 17)](#3-observation-framework-ios-17)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

### Q1. Diff between `@StateObject` and `@ObservedObject`?

**Content:**
- **`@StateObject`**: Safely creates and owns the object. **Use when YOU create the object** (e.g., inside the View that owns the ViewModel). It survives view redraws.
- **`@ObservedObject`**: Watches an object passed to it. **Use for dependencies** passed in. If you use this to create an object, it might get destroyed/recreated on every view redraw, losing state.

### Q2. `@Binding` usage?

**Answer:**
Creates a two-way connection between a property that stores data, and a view that displays and changes it.
**Example**: A Toggle Switch. The switch doesn't own the boolean, it just toggles the boolean owned by the parent view.

### Q3. `ObservableObject` vs `@Observable` (iOS 17)?

**Answer:**
- **`ObservableObject`** (Pre-iOS 17): Requires `class` conformance, properties need `@Published`. View needs `@ObservedObject`.
- **`@Observable`** (iOS 17+ Macro): Just mark the class with `@Observable`. No need for `@Published`. SwiftUI automatically tracks specific property access. Cleaner and more performant.

### Q4. `@AppStorage` & `@SceneStorage`?

**Answer:**
- **`@AppStorage`**: Wrapper around `UserDefaults`. Automatically invalidates view when the key changes.
- **`@SceneStorage`**: Persists data for the specific scene (window) instance. (Good for restoring tab selection or text draft upon restoration).

---

### 5. Real-World Scenarios

### Q5. Scenario: Your logic inside `init()` of a ViewModel is running multiple times unnecessarily.

**Answer:**
This happens if you initialize an `@ObservedObject` inside a View's init.
`View` structs are recreated frequently.
**Fix**: Use `@StateObject`. It is designed to instantiate the object *once* and keep it alive across view updates.

### Q6. Scenario: You want to pass a Binding to a subview, but you also need to run a side-effect (e.g., Analytics) when it changes.

**Answer:**
Construct a custom `Binding`.
```swift
let customBinding = Binding(
    get: { self.isOn },
    set: { newValue in
        self.isOn = newValue
        Analytics.track("Toggle changed to \(newValue)")
    }
)
Toggle("Enable", isOn: customBinding)
```

### Q7. Scenario: "Modifying state during view update, this will cause undefined behavior". Why?

**Answer:**
You are changing a `@State` or `@Published` property inside the `var body: some View` computation itself (or a constructor called by it).
**Fix**: Move the logic to `.onAppear`, `.task`, or a Button action. The `body` must be a pure function of the state, not a modifier of it.

### Q8. Scenario: Deeply nested child view needs access to User Settings. Passing bindings down 5 layers is ugly.

**Answer:**
Use **`@EnvironmentObject`**.
- Inject at the top: `.environmentObject(userSettings)`
- Read at the bottom: `@EnvironmentObject var settings: UserSettings`
**Crash Risk**: If you forget to inject it at the top, the app crashes at runtime when the child tries to access it.

### Q9. Scenario: How to force a View to reset its state completely?

**Answer:**
Change its **`id`**.
SwiftUI uses `id` to track identity. If `id` changes, SwiftUI destroys the old view (and its `@State`) and creates a fresh one.
```swift
MyFormView().id(resetID)
```

### Q10. Scenario: `@Published` property creates a loop?

**Answer:**
If View A updates Object B, and Object B updates View A immediately, you can get an infinite loop.
**Fix**: Use `objectWillChange.send()` manually if needed, or ensure data flow is unidirectional.

### Q11. Scenario: You need to observe `UserDefaults` changes from a ViewModel (not a View).

**Answer:**
`@AppStorage` only works in Views.
In a VM, use **KVO** (Key-Value Observing) or Combine:
```swift
UserDefaults.standard.publisher(for: \.myKey)
    .sink { ... }
```

### Q12. Scenario: Performance issue with `@EnvironmentObject`?

**Answer:**
If you inject a massive object (e.g., `AppStore` containing everything), *any* change to *any* property causes *every* view observing it to re-evaluate `body`.
**Fix**: Slice your environment objects into smaller, focused chunks (`UserStore`, `ThemeStore`, `NavigationStore`).

### Q13. Scenario: `@State` in a recursive view (e.g., comments outline)?

**Answer:**
`@State` relies on the View's position in the hierarchy. In recursive views, ensure each node has a stable identity (using `ForEach` with `id: \.self` or `Identifiable`). Without it, SwiftUI creates/destroys state unpredictably during expansion/collapse.

### Q14. Scenario: Using Actors with SwiftUI State?

**Answer:**
Difficult naturally. SwiftUI expects synchronous state access for rendering.
**Pattern**: The Actor does the work (background), then `await`s on `@MainActor` to update the ViewModel's `@Published` property.

### Q15. Scenario: How to initialize `@State` with a value passed from parent?

**Answer:**
**Don't**.
If you do `_text = State(initialValue: parentValue)`, it only works **once** (on init). If parentValue changes later, the `@State` ignores it (because `@State` is managed by SwiftUI storage).
**Fix**: If the value comes from outside, use `@Binding` or `let` (if read-only). Use `@State` only for internal, private data.
