## **Testing**

### 32. How to test Compose UI?

**Answer:**
Use `createComposeRule()` and Compose testing APIs.

```kotlin
class LoginScreenTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun testLogin() {
        composeTestRule.setContent {
            LoginScreen()
        }

        // Find and interact with nodes
        composeTestRule
            .onNodeWithText("Email")
            .performTextInput("test@example.com")

        composeTestRule
            .onNodeWithText("Password")
            .performTextInput("password123")

        composeTestRule
            .onNodeWithText("Login")
            .performClick()

        // Assert
        composeTestRule
            .onNodeWithText("Welcome!")
            .assertIsDisplayed()
    }
}
```

---

### 33. How to test ViewModel with Compose?

**Answer:**

```kotlin
@Test
fun testViewModelIntegration() {
    val viewModel = HomeViewModel()

    composeTestRule.setContent {
        HomeScreen(viewModel = viewModel)
    }

    // Trigger action
    composeTestRule
        .onNodeWithText("Load Data")
        .performClick()

    // Wait for async operation
    composeTestRule.waitUntil(timeoutMillis = 5000) {
        viewModel.uiState.value.isLoading == false
    }

    // Assert
    composeTestRule
        .onNodeWithText("Data loaded")
        .assertExists()
}
```

---

### 34. What are Semantics in Compose testing?

**Answer:**
Semantics provide metadata about UI elements for testing and accessibility.

```kotlin
@Composable
fun TestableButton() {
    Button(
        onClick = { },
        modifier = Modifier.semantics {
            contentDescription = "Submit button"
            testTag = "submit_btn"
        }
    ) {
        Text("Submit")
    }
}

// In test
composeTestRule
    .onNodeWithTag("submit_btn")
    .performClick()
```
