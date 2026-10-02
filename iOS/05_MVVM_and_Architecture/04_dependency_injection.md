# 💉 Dependency Injection
> **Targeted for iOS Developers**
> **Note:** Initializer Injection, Swinject, and Service Locator.

![DI](https://img.shields.io/badge/Pattern-DI-yellow?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Types of DI](#1-types-of-di)
- [2. Why use protocols?](#2-why-use-protocols)
- [3. Container Libraries](#3-container-libraries)

---

### Q1. Why Dependency Injection?

**Answer:**
To decouple classes.
Instead of `Class A` creating `Class B` internally (Tight Coupling), `Class A` asks for `Class B` to be passed to it.
This allows replacing `Class B` with `MockClassB` during testing.

### Q2. Types of Injection?

**Answer:**
1.  **Constructor/Initializer Injection** (Best): Pass dependencies in `init()`. Ensures object is fully formed.
    ```swift
    init(api: APIService) { self.api = api }
    ```
2.  **Property Injection**: Set public properties after init.
3.  **Method Injection**: Pass dependency in the function call.

### Q3. What is a DI Container?

**Answer:**
A central place to register and resolve dependencies.
- **Swinject**: Popular 3rd party library.
- **Service Locator**: A singleton registry (Simpler, but can hide dependencies).
- **Factory Pattern**: Simple static functions returning configured objects.

### Q4. Property Wrappers for DI?

**Answer:**
Tools like `Resolver` or custom wrappers (`@Injected`) allow syntax like:
```swift
@Injected var network: NetworkService
```
Pros: Clean syntax.
Cons: Hides dependencies (implicit), hard to debug layout issues if resolution fails.
