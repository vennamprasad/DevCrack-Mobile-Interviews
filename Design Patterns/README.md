# 📐 Software Design Patterns for Mobile Engineers

> **Mastery of Classic Gang of Four (GoF) Patterns and Mobile-Specific Architectural Paradigms.**

![Patterns](https://img.shields.io/badge/Pattern-GoF_&_Mobile-blue?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Design-Clean_Code-green?style=for-the-badge)
![Kotlin](https://img.shields.io/badge/Code-Kotlin_&_Swift-purple?style=for-the-badge)

---

## 📖 Complete Design Patterns Guide

Explore our comprehensive 9-part guide located in **[Design Patterns Guide](./Design_Patterns_Guide/README.md)**:

| Section | Topic & Scope |
| :--- | :--- |
| **[00. Intro](./Design_Patterns_Guide/00_Intro.md)** | Why design patterns matter in mobile and how to avoid anti-patterns. |
| **[01. Table of Contents](./Design_Patterns_Guide/01_Table_of_Contents.md)** | Full roadmap and catalog of covered patterns. |
| **[02. Creational Patterns](./Design_Patterns_Guide/02_Creational_Patterns.md)** | Singleton, Builder, Factory Method, Abstract Factory, Dependency Injection. |
| **[03. Structural Patterns](./Design_Patterns_Guide/03_Structural_Patterns.md)** | Adapter (RecyclerView/UI), Decorator, Facade (SDK wrappers), Composite. |
| **[04. Behavioral Patterns](./Design_Patterns_Guide/04_Behavioral_Patterns.md)** | Observer (Flow/LiveData/Combine), Strategy, Command, State, Chain of Responsibility. |
| **[05. Architectural Patterns](./Design_Patterns_Guide/05_Architectural_Patterns.md)** | MVC, MVP, MVVM, MVI, Clean Architecture, VIPER. |
| **[06. Mobile-Specific Patterns](./Design_Patterns_Guide/06_Android-Specific_Patterns.md)** | ViewHolder, Repository, UDF (Unidirectional Data Flow), Coordinator, Side Effect Handlers. |
| **[07. Best Practices](./Design_Patterns_Guide/07_Best_Practices.md)** | Pragmatic pattern selection, avoiding over-engineering, YAGNI, SOLID principles. |
| **[08. Summary](./Design_Patterns_Guide/08_Summary.md)** | Quick-reference cheat sheet and high-frequency interview questions. |

---

## 💡 Quick Reference: Mobile Pattern Mapping

| Need | Recommended Pattern | Mobile Real-World Example |
| :--- | :--- | :--- |
| Create complex UI configuration | **Builder** | `NotificationCompat.Builder`, `AlertDialog.Builder`, `URLRequest.Builder` |
| Isolate data fetching from storage | **Repository** | `UserRepository` coordinating Room DB + Retrofit API |
| Broadcast state changes | **Observer** | Kotlin `StateFlow`, RxJava `Observable`, Combine `AnyPublisher` |
| Decouple screen navigation | **Coordinator / Navigator** | Jetpack Navigation Compose, SwiftUI `NavigationStack` Coordinator |
| Intercept network requests | **Chain of Responsibility** | OkHttp Interceptors (`addInterceptor`) |
