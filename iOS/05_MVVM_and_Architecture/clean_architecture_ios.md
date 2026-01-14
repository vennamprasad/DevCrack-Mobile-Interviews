# 🧼 Clean Architecture in iOS
> **Targeted for Senior iOS Developers**
> **Note:** VIPER, Use Cases, and Separation of Concerns.

![Clean](https://img.shields.io/badge/Architecture-Clean-green?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. VIPER](#1-viper)
- [2. Domain Layer](#2-domain-layer)
- [3. Data Layer](#3-data-layer)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

### Q1. Components of VIPER?

**Answer:**
- **View**: Displays content. Sends user interactions to Presenter.
- **Interactor**: Business logic. Fetches data (Network/DB).
- **Presenter**: Formats data for View. Handles UI logic.
- **Entity**: Simple data models.
- **Router (Wireframe)**: Handles navigation between screens.

### Q2. Architecture Layers (Uncle Bob's Clean)?

**Answer:**
1.  **Presentation Layer**: UI (MVVM/VIPER).
2.  **Domain Layer**: Pure Swift. Contains **Entities** and **Use Cases** (Interactors). Defines *Repository Interfaces*.
3.  **Data Layer**: Implementing Repository Interfaces. Database, Networking, API models.

### Q3. Why separate Domain and Data?

**Answer:**
To make the specific database or API implementation **irrelevant** to the business rules.
- You can switch from Realm to Core Data without changing a single line of business logic in the Domain layer.
- You can swap a Real Network Repositories with a Mock Memory Repository for testing effortlessly.

### Q4. What is a Use Case?

**Answer:**
A class encapsulating a specific business action.
- `LoginUserUseCase`
- `GetRecentPostsUseCase`
It usually has a single `execute()` function. It makes the code readable and reusable across different ViewModels.

---

### 5. Real-World Scenarios

### Q5. Scenario: Where to handle "Analytics"?

**Answer:**
- **UI Events** (Button tap): Presenter/ViewModel.
- **Business Events** (User purchased): Interactor/UseCase.
- Ideally, inject an `AnalyticsService` into these components so you don't couple them to a specific 3rd party SDK.

### Q6. Scenario: "Clean Architecture" feels like boilerplate. 5 files for a "Hello World" screen?

**Answer:**
Yes, that's the trade-off.
**Fix**:
- Use it complexity warrants it (not for a Login screen).
- Use **Code Snippets** or **Xcode Templates** to generate the files.
- Stick to MVVM for simple screens, VIPER for complex ones.

### Q7. Scenario: Where do you format strings? (Date -> "5 mins ago")?

**Answer:**
**Presenter** (in VIPER) or **ViewModel**.
The Interactor/UseCase should return raw Data (`Date` object).
The View should receive ready-to-render strings.

### Q8. Scenario: Interactor returns Data directly?

**Answer:**
Ideally, Interactor returns **Domain Entities**.
The Data Repository maps **DTOs** (Decodable structs from API) to Domain Entities before returning them.
This insulates the app from API changes (e.g., if API renames `id` to `user_id`, you only change the mapping in Data layer).

### Q9. Scenario: Router dependency cycle?

**Answer:**
Presenter needs Router. Router creates the View (which needs Presenter).
**Fix**: Use weak references where appropriate (e.g., Router usually doesn't need to hold the View strongly after pushing it, or View holds Presenter strongly, Presenter holds Router).

### Q10. Scenario: How to share data between modules in Clean Arch?

**Answer:**
Via the **Domain Layer**.
If "Shopping Cart" and "Checkout" are separate modules, they both depend on a shared "CartDomain" module that defines the `Cart` entity and `CartRepository` interface.

### Q11. Scenario: Unit Testing the Interactor?

**Answer:**
Mock the Repository.
`let interactor = GetUser(repo: MockRepo())`.
Assert that `interactor.execute()` returns the expected user from the mock.
This tests purely business logic (e.g., "User is premium if points > 100").

### Q12. Scenario: Implementing "Pull to Refresh" in Clean Arch?

**Answer:**
1.  View detects pull -> Notify Presenter `viewDidPullToRefresh()`.
2.  Presenter calls Interactor `fetchData(force: true)`.
3.  Interactor tells Repository to ignore cache.

### Q13. Scenario: Dealing with Core Data threading in Clean Arch?

**Answer:**
The Data Layer (Repository) handles the threading.
It performs the fetch on background context, converts `NSManagedObject` to a plain swift struct (Entity), and returns the struct to the Domain Layer on the Main Thread (or allows Domain to be async).
Never pass `NSManagedObject` up to the Presenter.

### Q14. Scenario: Massive Interactor?

**Answer:**
If one Interactor does everything (`UserInteractor`), break it up.
`UpdateProfileInteractor`, `ChangePasswordInteractor`, `DeleteAccountInteractor`.
Single Responsibility Principle.

### Q15. Scenario: Combining multiple APIS?

**Answer:**
**Interactor**.
It calls `repo.getA()` and `repo.getB()`, combines them using `zip` or `async let`, applies logic, and returns the result.
The Presenter just waits for the final result.
