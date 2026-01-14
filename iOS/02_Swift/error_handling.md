# ⚠️ Error Handling
> **Targeted for iOS Developers**
> **Note:** Do-Try-Catch, Result Type, and Custom Errors.

![Error Handling](https://img.shields.io/badge/Swift-Errors-red?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Throwing Errors](#1-throwing-errors)
- [2. Do-Try-Catch](#2-do-try-catch)
- [3. Result Type](#3-result-type)
- [4. Never & FatalError](#4-never--fatalerror)

---

### Q1. How do you define a custom error?

**Answer:**
Adopt the `Error` protocol (usually with an Enum).
```swift
enum NetworkError: Error {
    case invalidURL
    case timeout
}
```

### Q2. `try` vs `try?` vs `try!`?

**Answer:**
- **`try`**: Used in a `do-catch` block. You handle the error.
- **`try?`**: Converts the result to an **Optional**. (Returns `nil` if error occurs). No catch block needed.
- **`try!`**: Crashes runtime if an error occurs. Use only when 100% sure it won't fail (e.g., loading a bundled file).

### Q3. What is the `Result` type?

**Answer:**
An enum with two cases: `.success(Value)` and `.failure(Error)`.
Useful for async completion handlers.
```swift
func fetch(completion: (Result<Data, Error>) -> Void) {
    if success { completion(.success(data)) }
    else { completion(.failure(error)) }
}
```

### Q4. `fatalError()` vs `assert()`?

**Answer:**
- **`assert()`**: Checks a condition. Crashes ONLY in **Debug** builds. Removed in Release.
- **`fatalError()`**: Crashes in **both** Debug and Release. Use when the app creates an invalid state it cannot recover from.
