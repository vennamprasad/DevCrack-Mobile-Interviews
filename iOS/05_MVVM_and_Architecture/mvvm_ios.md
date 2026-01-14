# 🏗️ MVVM in iOS
> **Targeted for iOS Developers**
> **Note:** ViewModel, Bindings, and Testing.

![MVVM](https://img.shields.io/badge/Architecture-MVVM-blueviolet?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. The Pattern](#1-the-pattern)
- [2. View vs ViewModel](#2-view-vs-viewmodel)
- [3. Bindings](#3-bindings)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

### Q1. Core Responsibilities?

**Answer:**
- **Model**: Data definitions (Structs, Core Data Entities).
- **View**: UI components (`UIView`, `UIViewController`, SwiftUI `View`).
    - *Responsibility*: Display data, capture user input.
    - *Restriction*: **Never** import business logic.
- **ViewModel**: The "Brain" for the View.
    - *Responsibility*: Fetch data, transform data for display, handle button taps.
    - *Restriction*: **Never** import `UIKit` or `SwiftUI` (keep it framework agnostic).

### Q2. How to bind View to ViewModel?

**Answer:**
1.  **Closures**: Simple. The VM calls a closure `onDataUpdated?()`.
2.  **Delegates**: Traditional. `delegate?.didUpdateData()`.
3.  **Observables**: Reactive.
    - **Combine**: `@Published` properties.
    - **SwiftUI**: `ObservableObject` protocol.
    - **RxSwift**: `BehaviorRelay`.

### Q3. "Massive View Controller" Solution?

**Answer:**
MVVM solves "Massive VC" by moving:
- Network calls,
- Data formatting (Date -> String),
- Validation logic,
Out of the VC and into the VM. The VC becomes a dumb wrapper that just binds data to UI elements.

---

### 5. Real-World Scenarios

### Q4. Scenario: The ViewModel is becoming "Massive" too.

**Answer:**
If VM has 2000 lines, you just shifted the problem.
**Fix**: Break it down.
- **Child ViewModels**: `HeaderViewModel`, `ListViewModel`.
- **Services**: Extract logic into `AuthService`, `AnalyticsService`.
- **Interactors/UseCases**: Extract business rules (`LoginUseCase`).

### Q5. Scenario: Navigation logic? Where does it go?

**Answer:**
**NOT** in the ViewModel (ViewModel shouldn't know about `UINavigationController`).
**NOT** in the View (tight coupling).
**Answer**: Use a **Coordinator**.
ViewModel exposes an event: `onLoginSuccess?()`.
View calls `coordinator.showHome()`.

### Q6. Scenario: MVVM with SwiftUI inputs?

**Answer:**
SwiftUI Views bind directly to VM properties (`TextField(text: $vm.username)`).
Ensure your VM implements `ObservableObject`.
Do not manually sync state back and forth; let the Binding handle it.

### Q7. Scenario: Dealing with complex animations?

**Answer:**
Animation logic belongs in the **View**.
VM state: `isLoading = true`.
View: `onChange(of: isLoading) { withAnimation { ... } }`.
Do not try to drive animation curves/duration from the VM.

### Q8. Scenario: Unit Testing the ViewModel?

**Answer:**
Because VM has no UIKit imports:
1.  Instantiate VM.
2.  Mock the NetworkService.
3.  Call `vm.fetchData()`.
4.  Assert `vm.items.count == 5`.
Easier than testing VC.

### Q9. Scenario: How to inject dependencies into VM?

**Answer:**
Constructor Injection.
```swift
class UserViewModel {
    let service: UserService
    init(service: UserService) { self.service = service }
}
```
Allows passing `MockUserService` during tests.

### Q10. Scenario: Handling "One-off" events (e.g., Show Alert, Toast)?

**Answer:**
State is persistent (e.g., `isLoading`). Events are transient.
If you use a Boolean `isErrorShown`, you must remember to set it back to `false` after showing the alert.
Alternatively, use a `PassthroughSubject` (Combine) for events that don't stick around.

### Q11. Scenario: Where to Format Data?

**Answer:**
**ViewModel**.
- Date -> String "2 hours ago".
- Price -> String "$19.99".
The View should receive ready-to-display Strings. It shouldn't be running `DateFormatter`.

### Q12. Scenario: CollectionView/Table View Protocols?

**Answer:**
The **View** (VC) implements `DataSource/Delegate`.
It asks the VM: `vm.numberOfItems` and `vm.item(at: indexPath)`.
Do NOT make the VM the delegate (imports UIKit).

### Q13. Scenario: Reference Cycles in MVVM?

**Answer:**
Closure binding is the danger zone.
`vm.onUpdate = { [weak self] in self?.tableView.reloadData() }`
If you forget `[weak self]`, View holds VM, VM holds View (via closure) -> Cycle.

### Q14. Scenario: What is "Inputs/Outputs" protocol pattern?

**Answer:**
Formalizing the VM interface.
```swift
protocol VMInputs { func tapLogin() }
protocol VMOutputs { var user: AnyPublisher<User, Never> { get } }
```
Ensures strict separation and clear API documentation.

### Q15. Scenario: Error Handling?

**Answer:**
VM catches error from Service.
VM maps Error to a user-friendly String.
VM updates `errorMessage` property.
View binds to `errorMessage` -> Shows Alert.
