# 🔄 MVI Architecture Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**

![MVI](https://img.shields.io/badge/Architecture-MVI-blue?style=for-the-badge)
![Jetpack Compose](https://img.shields.io/badge/Jetpack%20Compose-4285F4?style=for-the-badge&logo=android&logoColor=white)

---

## ✅ What is MVI?

**MVI (Model-View-Intent)** is an architectural pattern primarily used in modern Android development (especially with **Jetpack Compose**, **Kotlin**, and **unidirectional data flow** paradigms). It's inspired by **The Elm Architecture** and **Redux**.

MVI focuses on **single-direction data flow** and **immutable state** management.

---

## 🔄 Flow Overview

Intent (User Action)
↓
ViewModel processes Intent
↓
Model (Business Logic & State)
↓
Emits new ViewState
↓
View renders the ViewState

## 🧩 Components of MVI

| Component     | Responsibility                                                            |
|---------------|---------------------------------------------------------------------------|
| **Intent**    | User actions (e.g., button click, text input).                            |
| **Model**     | Processes intents into new **states** via business logic and data layer.  |
| **ViewState** | Immutable state representing the entire UI.                               |
| **View**      | Observes state and renders the UI.                                        |

---

## 🧠 Core Principles

- **Unidirectional Data Flow**: Data flows in a single direction, making state management predictable.
- **Immutable State**: The entire UI state is stored in one object. When changes occur, a new copy is created.
- **Pure Functions**: Transformations from intent to state are done via pure functions (no side effects).

---

## 📱 Example (Login Screen)

1. **User types in email** → `Intent.EmailChanged("user@example.com")`
2. **User clicks login** → `Intent.SubmitLogin`
3. **ViewModel** handles the intent and produces new **ViewState**
4. **View** observes `ViewState` and updates UI accordingly

---

## ✅ Benefits of MVI

- Easier **testing** due to pure functions and clear state.
- Predictable and **reliable UI behavior**.
- Great for **real-time UI updates** (chat apps, forms, etc.).
- Scales well in **complex UIs** with multiple states.

---

## ⚠️ Considerations

- More **boilerplate** compared to simpler patterns.
- Can be **overkill for very small UIs**.
- Requires careful **state design** and memory management.

---

## 🔄 Comparison with MVC & MVVM

| Pattern | Data Flow           | State            | Testability | Used In           |
|--------|---------------------|------------------|-------------|-------------------|
| MVC    | Bidirectional        | Mutable          | Medium      | Web/legacy Android|
| MVVM   | Bidirectional (LiveData/Binding) | Mutable  | Good        | Modern Android    |
| MVI    | Unidirectional       | Immutable        | Excellent   | Compose, Redux    |

