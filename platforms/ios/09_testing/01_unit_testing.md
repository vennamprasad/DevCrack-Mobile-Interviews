# 🧪 Modern iOS Unit Testing: Swift Testing Framework & XCTest

> **The next-generation testing standard for Apple platforms: Comparing Apple's new Swift Testing framework (`import Testing`, `@Test`, `#expect`) against legacy `XCTest`, parameterized tests, async testing, and actor isolation.**

---

## 📌 Executive Summary

With the release of Swift 6 and Xcode 16, Apple introduced **Swift Testing**—a completely reimagined, macro-powered testing framework designed from the ground up for modern Swift:
- **No more `XCTestCase` class inheritance**: Tests are simple global functions or structs.
- **Unified Expectations**: Replaces dozens of verbose assertions (`XCTAssertEqual`, `XCTAssertTrue`, `XCTAssertNil`) with two expressive macros: **`#expect`** and **`#require`**.
- **Native Parameterized Testing**: Test hundreds of edge cases with one function using `@Test(arguments:)`.
- **Parallel by Default**: Tests execute concurrently across all available CPU cores unless explicitly isolated.

---

## ⚖️ Swift Testing vs. Legacy XCTest

| Feature | Legacy XCTest (`import XCTest`) | Modern Swift Testing (`import Testing`) |
| :--- | :--- | :--- |
| **Structure** | Classes inheriting from `XCTestCase` | Plain structs or global functions (no inheritance) |
| **Test Declaration** | Functions prefixed with `test...()` | `@Test` macro attribute on any function name |
| **Assertions** | `XCTAssertEqual`, `XCTAssertTrue`, etc. | **`#expect(...)`** (continues) and **`#require(...)`** (stops on failure) |
| **Parameterized Tests**| Manual `for` loops (single failure fails entire loop) | **`@Test(arguments: [...])`** (each argument is an isolated test case!) |
| **Organization** | Method naming / Test Suites | `@Suite`, `.tags()`, and descriptive display names |
| **Concurrency** | Sequential by default | **Concurrent / parallel execution by default** |

---

## 💻 Writing Tests with the Swift Testing Framework

### 1. Basic Assertions with `#expect` and `#require`

```swift
import Testing
@testable import ShoppingApp

@Suite("Shopping Cart Calculation Suite")
struct CartCalculationTests {

    @Test("Validates total price calculation with discounts")
    func calculateTotal() {
        var cart = ShoppingCart()
        cart.addItem(Product(name: "Shoes", price: 100.0), quantity: 2)
        cart.applyDiscountCoupon("10PERCENT")

        // #expect evaluates the condition and continues if it fails
        #expect(cart.totalPrice == 180.0)
        #expect(cart.itemCount == 2)
    }

    @Test("Unwrapping optional values safely")
    func fetchUserProfile() throws {
        let user = UserManager.shared.findUser(id: "usr_99")
        
        // #require unwraps the optional; if nil, the test HALTS immediately!
        let unwrappedUser = try #require(user)
        
        #expect(unwrappedUser.email == "dev@example.com")
    }
}
```

---

### 2. Parameterized Testing: Testing 10 Inputs in 1 Test

In XCTest, testing multiple inputs required writing a `for` loop. If the 2nd input failed, XCTest aborted the test, preventing you from knowing if inputs 3–10 would pass.

In **Swift Testing**, each argument executes as an **independent test runner**:

```swift
@Suite("Email Validation Suite")
struct EmailValidatorTests {

    @Test(
        "Validates email format across valid and invalid addresses",
        arguments: [
            ("valid.user@example.com", true),
            ("ceo@company.org", true),
            ("plainaddress", false),
            ("@missingusername.com", false),
            ("user@.com.my", false)
        ]
    )
    func testEmailValidation(email: String, expectedResult: Bool) {
        let isValid = EmailValidator.isValid(email)
        #expect(isValid == expectedResult)
    }
}
```

---

### 3. Testing Swift Concurrency & Async Code

Swift Testing integrates natively with `async`/`await`:

```swift
@Suite("Payment Gateway Async Tests")
struct PaymentGatewayTests {

    @Test("Processes Stripe Payment Intent asynchronously")
    func processPayment() async throws {
        let gateway = MockPaymentGateway()
        
        let result = try await gateway.charge(amount: 50.0, token: "tok_visa")
        
        #expect(result.status == .success)
        #expect(result.transactionId != nil)
    }

    // Testing Actor-isolated code
    @Test("Thread-safe bank account balance operations")
    @MainActor
    func verifyMainActorViewModel() async {
        let viewModel = AccountViewModel()
        await viewModel.deposit(100.0)
        
        #expect(viewModel.balance == 100.0)
    }
}
```

---

### 4. Categorizing with Tags & Custom Traits

Group and filter tests in Xcode's Test Navigator using **Tags**:

```swift
extension Tag {
    @Tag static var criticalCheckout: Self
    @Tag static var networkDependent: Self
}

@Suite("Checkout Core Engine", .tags(.criticalCheckout))
struct CheckoutEngineTests {

    @Test(
        "Verifies fraud check on high-value orders",
        .tags(.criticalCheckout),
        .timeLimit(.minutes(1)) // Fails if test exceeds 60 seconds!
    )
    func fraudDetection() async throws {
        // ...
    }

    @Test(
        "Disabled until API v2 goes live",
        .disabled("Backend endpoint not yet deployed")
    )
    func apiV2EndpointTest() {
        // Skipped automatically in CI
    }
}
```

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "What is the difference between `#expect` and `#require` in Apple's Swift Testing framework?"
* **Answer**:
  - **`#expect(condition)`**: Non-fatal assertion. If the expression evaluates to `false`, the test is marked as failed, but execution **continues** to evaluate subsequent assertions. Useful for validating multiple independent UI properties on the same screen.
  - **`#require(try optionalValue)`**: Fatal assertion. If the expression is `false` or the optional is `nil`, the macro throws an error and **terminates the current test immediately**. Crucial when subsequent test steps depend on a non-null object to prevent crashes.

### Q2: "How do you test that an asynchronous `AsyncSequence` emits expected values over time in Swift?"
* **Answer**:
  - Iterate through the `AsyncSequence` using a `for await` loop, or collect a specific number of items using an async helper:
  ```swift
  @Test("Validates price ticker stream emissions")
  func testPriceStream() async throws {
      let tickerStream = PriceTicker.shared.subscribe(symbol: "AAPL")
      var receivedPrices: [Double] = []

      for await price in tickerStream.prefix(3) {
          receivedPrices.append(price)
      }

      #expect(receivedPrices.count == 3)
      #expect(receivedPrices.allSatisfy { $0 > 0.0 })
  }
  ```
