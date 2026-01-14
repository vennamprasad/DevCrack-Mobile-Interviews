# 🏛️ MVP Architecture Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**

![MVP](https://img.shields.io/badge/Architecture-MVP-blue?style=for-the-badge)
![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)

---

## ✅ What is MVP?

**MVP (Model-View-Presenter)** is a design pattern used to separate the presentation layer from the business logic. It’s commonly used in Android development, especially with XML-based UI (pre-Jetpack Compose).

It improves testability and code organization by decoupling UI from business logic.

---

## 🔄 Flow Overview
User interacts with View
↓
View forwards input to Presenter
↓
Presenter processes logic, updates Model
↓
Model returns data to Presenter
↓
Presenter updates the View


---

## 🧩 Components of MVP

| Component     | Responsibility                                                                  |
|---------------|---------------------------------------------------------------------------------|
| **Model**     | Handles business logic, data operations, API calls, and database interactions.  |
| **View**      | Interface representing the UI (Activity/Fragment or custom View).               |
| **Presenter** | Acts as a middleman. Fetches data from the Model and updates the View.          |

---

## 📱 Example (Login Flow)

1. **User** enters email/password → `View` sends data to `Presenter`
2. **Presenter** validates input, requests login from `Model`
3. **Model** returns success or failure
4. **Presenter** tells `View` to show result (e.g., success message or error)

---

## ✅ Benefits

- **Improved testability**: Business logic is in Presenter, which can be unit tested easily.
- **Separation of concerns**: Clear boundaries between UI and logic.
- **Reusable View and Presenter contracts**: Easier to swap UI components.

---

## ⚠️ Drawbacks

- Can lead to **boilerplate code**, especially with large View interfaces.
- The **Presenter** can become large if not well-structured (known as "God class").
- Manual **View-to-Presenter** binding can be tedious.

---

## 🔄 Comparison with MVC & MVVM & MVI

| Pattern | Data Flow            | State Type   | Testability | Common Use Case          |
|--------|----------------------|--------------|-------------|---------------------------|
| MVC    | Bidirectional         | Mutable      | Medium      | Legacy systems/web        |
| MVP    | View → Presenter → Model | Mutable | Good        | Android (pre-Compose)     |
| MVVM   | View ↔ ViewModel (LiveData) | Mutable | Very Good   | Modern Android XML        |
| MVI    | Intent → Model → ViewState → View | Immutable | Excellent | Jetpack Compose/Redux    |

---

## 🛠️ Sample Interface Contracts

```kotlin
// View
interface LoginView {
    fun showLoading()
    fun hideLoading()
    fun showError(message: String)
    fun navigateToHome()
}

// Presenter
interface LoginPresenter {
    fun onLoginClicked(email: String, password: String)
}

