# 👆 UI Testing
> **Targeted for iOS Developers**
> **Note:** XCUITest, Robots, and Accessibility.

![Testing](https://img.shields.io/badge/Testing-UI-blue?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Queries](#1-queries)
- [2. Handling Flakiness](#2-handling-flakiness)
- [3. Robot Pattern](#3-robot-pattern)

---

### Q1. How to find an element?

**Answer:**
Queries use the Accessibility Tree.
`app.buttons["Login"]`
`app.staticTexts["Welcome Message"]`
**Tip**: Set `.accessibilityIdentifier` in your View code to make finding elements robust (unaffected by localization).

### Q2. Wait for Existence?

**Answer:**
UI tests are flaky because things take time to appear (animations, network).
```swift
let button = app.buttons["Submit"]
XCTAssertTrue(button.waitForExistence(timeout: 5))
```

### Q3. What is the Robot Pattern?

**Answer:**
Abstracting test steps into helper classes ("Robots") to make tests readable.
```swift
// Test
LoginRobot()
   .enterUsername("john")
   .enterPassword("password")
   .tapLogin()
   .verifyHomeAppears()
```
This decouples the Test logic from the Query logic.

### Q4. Speeding up UI Tests?

**Answer:**
- Disable animations (`UIView.setAnimationsEnabled(false)` via Launch Argument).
- Mock the network (Run a local webserver or stub requests) so you aren't waiting for real API calls.
