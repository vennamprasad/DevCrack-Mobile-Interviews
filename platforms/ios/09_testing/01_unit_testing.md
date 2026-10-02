# 🧪 Unit Testing
> **Targeted for iOS Developers**
> **Note:** XCTest, Assertions, and Expectations.

![Testing](https://img.shields.io/badge/Testing-Unit-green?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Arrange-Act-Assert](#1-arrange-act-assert)
- [2. XCTest Lifecycle](#2-lifecycle)
- [3. Testing Async Code](#3-async)

---

### Q1. Core Principle (AAA)?

**Answer:**
- **Arrange**: Set up the object & inputs.
- **Act**: Call the method.
- **Assert**: Check if the output matches expectations.
```swift
func testAdd() {
    let calc = Calculator() // Arrange
    let result = calc.add(2, 2) // Act
    XCTAssertEqual(result, 4) // Assert
}
```

### Q2. `setUp` vs `tearDown`?

**Answer:**
- **setUp**: Called *before* each `test...` method. Reset state here.
- **tearDown**: Called *after* each test. Clean up (delete files, etc).

### Q3. `XCTestExpectation`?

**Answer:**
Used for async code.
1.  Create `expectation`.
2.  Pass completion block.
3.  Calls `fulfill()` in block.
4.  `wait(for: [expectation], timeout: 1.0)`.

### Q4. Where to put test files?

**Answer:**
In the **Test Target**.
They do not ship with the App.
You must `@testable import MyApp` to access internal classes.
