# 🦅 Swift Basics
> **Targeted for Beginners & Juniors**
> **Note:** Syntax, Optionals, and Control Flow.

![Swift](https://img.shields.io/badge/Language-Swift-orange?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Variables & Constants](#1-variables--constants)
- [2. Optionals](#2-optionals)
- [3. Control Flow](#3-control-flow)
- [4. Functions](#4-functions)
- [5. Real-World Scenarios](#5-real-world-scenarios)

---

### Q1. `let` vs `var`?

**Answer:**
- **`let`**: Defines a **constant**. Value cannot be changed once set. (Preferred for safety).
- **`var`**: Defines a **variable**. Value can be mutated.

### Q2. What are Optionals?

**Answer:**
A type that handles the **absence of a value**. Use `?` to declare.
```swift
var name: String? = nil // Valid
var age: Int = 25       // Cannot be nil
```
**Unwrapping:**
1.  `if let`: Safe unwrap.
2.  `guard let`: Early exit if nil.
3.  `??`: Default value (Nil Coalescing).
4.  `!`: Force Unwrap (Crash if nil).

### Q3. Explain `guard` vs `if`.

**Answer:**
- **`if`**: Standard conditional. Logic is nested inside braces.
- **`guard`**: Focuses on the "unhappy path". Logic is linear. Must `return` or `throw` if condition fails.
```swift
guard let user = user else { return }
// 'user' is now available here, outside the block
```

### Q4. What is a Tuple?

**Answer:**
A compound type that groups multiple values.
```swift
let httpError = (404, "Not Found")
let (code, message) = httpError
```
Useful for returning multiple values from a function without creating a struct.

---

### 5. Real-World Scenarios

### Q5. Scenario: Your app is slow when searching for a User ID in an array of 10,000 users. How do you fix it?

**Answer:**
**Switch from Array to Set.**
- **Array**: `contains()` is **O(n)** (Linear). It checks every item one by one.
- **Set**: `contains()` is **O(1)** (Constant). It hashes the value and jumps directly to a memory bucket.
- **Trade-off**: Sets are unordered. If order matters, use `NSOrderedSet` (O(1) lookup, O(n) insert).

### Q6. Scenario: You need to ensure a lock is released or a file is closed, regardless of how the function exits (return or error).

**Answer:**
Use **`defer`**.
The code inside `defer { ... }` runs just before the current scope exits.
```swift
func processFile() {
    let file = openFile()
    defer { closeFile(file) } // executing last
    
    if file.isEmpty { return }
    // ... processing
} 
// closeFile called here automatically
```

### Q7. Scenario: A heavy object (e.g., Image Processing Manager) is slowing down the launch, but it's not always used.

**Answer:**
Use **`lazy`**.
The property will not be initialized until it is accessed for the first time.
```swift
lazy var imageManager = ImageProcessor()
```
**Constraint**: Must be a `var` (because the underlying value changes from nil to initialized) and inside a struct/class.

### Q8. Scenario: You have a closure used in multiple places with a complex signature `(Int, String, Error?) -> Void`. It's messy.

**Answer:**
Use **`typealias`** to improve readability.
```swift
typealias CompletionHandler = (Int, String, Error?) -> Void

func fetchData(completion: CompletionHandler) { ... }
```

### Q9. Scenario: How do you loop through numbers with a specific step (e.g., every 5th number)?

**Answer:**
Use **`stride`**.
```swift
// 0, 5, 10, 15... (Excluding 20)
for i in stride(from: 0, to: 20, by: 5) {
    print(i)
}
```

### Q10. Scenario: You need to extract Associated Values from an Enum in a `switch` statement.

**Answer:**
Pattern matching with `let`.
```swift
enum Result {
    case success(data: String)
    case failure(error: Error)
}

switch result {
case .success(let data):
    print("Got data: \(data)")
case .failure(let error):
    print("Failed: \(error)")
}
```

### Q11. Scenario: You want to execute multiple cases in a switch statement without copying code (e.g., Case A and Case B do the same thing).

**Answer:**
1.  **Multiple patterns**: `case .a, .b: doSomething()`
2.  **`fallthrough`**: explicitly continues to the next case (Swift switch doesn't fall through by default).
    ```swift
    case .legacy:
        print("Legacy warning")
        fallthrough
    case .standard:
        process()
    ```

### Q12. Scenario: Which performs better for string concatenation: `+` operator or String Interpolation?

**Answer:**
**String Interpolation** (`"\(a) \(b)"`) is generally preferred for readability and is optimized by the compiler.
For massive implementation (loops), use `StringBuilder` pattern (appending to a generic string buffer) to avoid creating temporary string objects for every `+` operation.

### Q13. Scenario: What is `Void` in Swift?

**Answer:**
`Void` is actually a typealias for an empty tuple `()`.
Functions that "don't return anything" actually return `()` hiddenly.

### Q14. Scenario: Checking API Version availability?

**Answer:**
Use `#available`.
```swift
if #available(iOS 15, *) {
    // Use new API
} else {
    // Fallback
}
```

### Q15. Scenario: You want to debug a function but `print()` is cluttering the console in Release builds.

**Answer:**
Wrap print statements in a preprocessor macro or global function that checks for `#if DEBUG`.
```swift
func dprint(_ items: Any...) {
    #if DEBUG
    print(items)
    #endif
}
```
Or use the new `Logger` (OSLog) which is more performant and can be filtered in Console.app.
