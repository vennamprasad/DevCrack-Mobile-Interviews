# 🧪 JUnit Testing Framework
> **Targeted for Android Developers**
> **Note:** Unit testing standards, assertions, and annotations.

![JUnit](https://img.shields.io/badge/Testing-JUnit_4/5-red?style=for-the-badge&logo=junit5&logoColor=white)

---

## 📖 Table of Contents
- [1. Basics](#basics)
- [2. Annotations (JUnit 4 vs 5)](#annotations)
- [3. Assertions](#assertions)
- [4. Parameterized Tests](#parameterized-tests)

---

### Q1. What is JUnit?

**Answer:**
JUnit is the standard unit testing framework for Java/Kotlin.
- **JUnit 4**: Legacy, still widely used in Android.
- **JUnit 5 (Jupiter)**: Modern, modular, better kotlin support.

### Q2. JUnit 4 vs JUnit 5?

**Answer:**
| Feature | JUnit 4 | JUnit 5 |
| :--- | :--- | :--- |
| **Test Method** | `@Test` | `@Test` (from different package) |
| **Lifecycle** | `@Before`, `@After` | `@BeforeEach`, `@AfterEach` |
| **Static Lifecycle** | `@BeforeClass`, `@AfterClass` | `@BeforeAll`, `@AfterAll` |
| **Assertions** | `org.junit.Assert` | `org.junit.jupiter.api.Assertions` |
| **Ignore** | `@Ignore` | `@Disabled` |
| **Tagging** | `@Category` | `@Tag` |

### Q3. How do you test for Exceptions?

**Answer:**

**JUnit 4:**
```java
@Test(expected = IllegalArgumentException.class)
public void testException() {
    throw new IllegalArgumentException();
}
```

**JUnit 5 (Recommended):**
```kotlin
@Test
fun testException() {
    assertThrows<IllegalArgumentException> {
        calculator.divide(10, 0)
    }
}
```

### Q4. Parameterized Tests Example?

**Answer:**
Allows running the same test with different inputs.
```kotlin
@ParameterizedTest
@ValueSource(ints = [1, 3, 5, -3, 15])
fun isOdd_ShouldReturnTrueForOddNumbers(number: Int) {
    assertTrue(Numbers.isOdd(number))
}
```

### Q5. What is the Arrange-Act-Assert (AAA) pattern?

**Answer:**
A common pattern for structuring tests:
1.  **Arrange**: Set up the object to be tested (create instance, mocks).
2.  **Act**: Call the method under test.
3.  **Assert**: Verify the result matches expectations.

```kotlin
@Test
fun testAddition() {
    // Arrange
    val calculator = Calculator()
    
    // Act
    val result = calculator.add(2, 2)
    
    // Assert
    assertEquals(4, result)
}
```