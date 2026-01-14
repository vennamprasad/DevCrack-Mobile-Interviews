# 🦜 Mockito & Mocking Frameworks
> **Targeted for Android Developers**
> **Note:** Isolating dependencies and verifying behavior.

![Mockito](https://img.shields.io/badge/Testing-Mockito-green?style=for-the-badge&logo=android&logoColor=white)

---

## 📖 Table of Contents
- [1. Core Concepts](#core-concepts)
- [2. Mocking vs Spying](#mocking-vs-spying)
- [3. Common Annotations](#common-annotations)
- [4. Alternatives (MockK)](#alternatives)

---

### Q1. What is Mockito and why is it used?

**Answer:**
Mockito is a popular open-source Java framework used for unit testing by creating **mock objects**. It allows developers to simulate the behavior of complex, real objects and verify interactions, making it easier to write and maintain tests without relying on external dependencies (like Network or Database).

### Q2. How do you create a mock object?

**Answer:**
**1. Using `Mockito.mock()`:**
```java
List mockedList = Mockito.mock(List.class);
```

**2. Using `@Mock` annotation:**
```java
@Mock
List<String> mockedList;

@Before
public void init() {
    MockitoAnnotations.openMocks(this);
}
```

### Q3. `when()` vs `verify()`?

**Answer:**
- **Stubbing (`when`)**: Defines **what** the mock should do when a method is called.
  ```java
  // When get(0) is called, return "first"
  when(mockedList.get(0)).thenReturn("first");
  ```
- **Verifying (`verify`)**: Checks **if** a method was called with specific arguments.
  ```java
  // Verify that add("one") was called exactly once
  verify(mockedList).add("one");
  ```

### Q4. Mocking vs Spying?

**Answer:**
| Feature | Mock | Spy |
| :--- | :--- | :--- |
| **Object** | Completely fake object. | Wrapper around a **real** object. |
| **Behavior** | All methods return defaults (null/0) unless stubbed. | Real methods are called unless stubbed. |
| **Use Case** | strict isolation. | Testing legacy code or partial mocking. |

**Example Spy:**
```java
List list = new ArrayList();
List spyList = spy(list);

// Real method called
spyList.add("one"); 
verify(spyList).add("one");

// Stubbing a spy
doReturn(100).when(spyList).size();
```

### Q5. What is the difference between `@Mock` and `@InjectMocks`?

**Answer:**
- **`@Mock`**: Creates a mock object (e.g., `UserRepository`).
- **`@InjectMocks`**: Creates an instance of the class under test (e.g., `UserViewModel`) and automatically injects the available `@Mock`s into it.

```java
@Mock
UserRepository repository;

@InjectMocks
UserViewModel viewModel; // Repository is injected here
```

### Q6. Mockito with Kotlin (MockK)?

**Answer:**
While Mockito works with Kotlin, **MockK** is often preferred because:
1.  Mockito has trouble mocking `final` classes/functions (default in Kotlin).
2.  MockK has first-class support for Coroutines (`coEvery`, `coVerify`).
3.  MockK syntax is more idiomatic to Kotlin.

**MockK Example:**
```kotlin
val mockUser = mockk<User>()
every { mockUser.name } returns "John"
verify { mockUser.name }
```
