# 🎭 Mocking & Stubbing
> **Targeted for iOS Developers**
> **Note:** Protoccols, Fakes, and Spies.

![Testing](https://img.shields.io/badge/Testing-Mocks-orange?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. Mock vs Stub vs Spy](#1-definitions)
- [2. Protocol Mocking](#2-protocol-mocking)
- [3. Libraries](#3-libraries)

---

### Q1. Terminology definitions?

**Answer:**
- **Dummy**: Passes arguments, never used.
- **Stub**: Returns canned answers (`return true`). No logic.
- **Mock**: Expects calls. Fails if calls don't happen.
- **Spy**: Records calls (`wasCalled = true`) for assertion later.

### Q2. How to Mock in Swift?

**Answer:**
Since Swift is static, we rely on Protocols.
```swift
protocol Network { func get() }

class MockNetwork: Network {
    var wasGetCalled = false
    func get() { wasGetCalled = true }
}

let mock = MockNetwork()
vm.network = mock
vm.load()
XCTAssertTrue(mock.wasGetCalled)
```

### Q3. Mocking URLSession?

**Answer:**
Instead of making real network calls, subclass `URLProtocol`.
Register it with `URLSessionConfiguration`.
It intercepts every request and returns the fake Data/Response you configured.

### Q4. Libraries?

**Answer:**
- **Cuckoo**: Generates mocks (Heavy).
- **Mockingbird**: Generating mocks.
- **Hand-rolled**: Swift developers often prefer writing simple hand-rolled mocks (Structs/Classes) as they are easier to maintain than tool-generated code.
