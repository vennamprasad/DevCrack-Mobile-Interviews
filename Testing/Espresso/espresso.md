# ☕ Espresso UI Testing
> **Targeted for Android Developers**
> **Note:** White-box UI testing within a single app.

![Espresso](https://img.shields.io/badge/Testing-Espresso-gray?style=for-the-badge&logo=android&logoColor=white)

---

## 📖 Table of Contents
- [1. Core Components](#core-components)
- [2. The Formula](#formula)
- [3. Idling Resources](#idling-resources)
- [4. Best Practices](#best-practices)

---

### Q1. What is Espresso?
**Answer:**
Espresso is a testing framework for Android to write reliable UI tests. It automatically **synchronizes** your test actions with the UI of your application, meaning it waits for UI events (like drawing) to finish before performing the next action.

### Q2. The Espresso Formula?
**Answer:**
Espresso tests follow a simple formula:
**`onView(ViewMatcher).perform(ViewAction).check(ViewAssertion)`**

1.  **onView()**: Find the view (Finder).
    - `withId(R.id.btn_login)`
    - `withText("Submit")`
2.  **perform()**: Do something (Action).
    - `click()`
    - `typeText("Hello")`
    - `scrollTo()`
3.  **check()**: Validation (Assertion).
    - `matches(isDisplayed())`
    - `matches(withText("Success"))`

**Example:**
```kotlin
@Test
fun testLoginFlow() {
    // 1. Type email
    onView(withId(R.id.email)).perform(typeText("user@example.com"))
    
    // 2. Click login
    onView(withId(R.id.btn_login)).perform(click())
    
    // 3. Verify success message
    onView(withText("Welcome")).check(matches(isDisplayed()))
}
```

### Q3. What are Idling Resources?
**Answer:**
Espresso knows when the UI thread is busy, but it **does not know** about background threads (e.g., API calls).
**Idling Resources** allow you to teach Espresso to wait for your background operations to complete before proceeding.
- If you don't use them for network calls, tests will fail ("No views in hierarchy") because Espresso checks before the data loads.
- **Alternatives**: Use `CountingIdlingResource` or replace Dispatchers in tests.

### Q4. How to handle RecyclerViews?
**Answer:**
Standard `onView` doesn't work well because items are recycled (not all are on screen).
Use **`espresso-contrib`** library:
```kotlin
// Scroll to position 10 and verify text
onView(withId(R.id.recycler_view))
    .perform(RecyclerViewActions.scrollToPosition<ViewHolder>(10))
    
onView(withText("Item 10")).check(matches(isDisplayed()))
```

### Q5. Espresso Rule?
**Answer:**
You need an `ActivityScenarioRule` to launch the activity before tests.
```kotlin
@get:Rule
val activityRule = ActivityScenarioRule(MainActivity::class.java)
```
