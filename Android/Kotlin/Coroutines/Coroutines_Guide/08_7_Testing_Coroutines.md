## **7. Testing Coroutines**

### **Problem**: Testing async code is tricky

**Using TestDispatcher**:
```kotlin
@ExperimentalCoroutinesApi
class MyViewModelTest {
    private val testDispatcher = UnconfinedTestDispatcher()

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `test user data loading`() = runTest {
        val viewModel = MyViewModel(fakeRepository)

        viewModel.loadUser()

        // Assert immediately - no need to wait
        assertEquals(UserState.Success, viewModel.uiState.value)
    }
}
```

**Testing with delays**:
```kotlin
@Test
fun `test retry logic with delays`() = runTest {
    var attempts = 0
    val repository = ApiRepository()

    val result = repository.retryWithExponentialBackoff(times = 3) {
        attempts++
        if (attempts < 3) throw IOException("Fail")
        "Success"
    }

    assertEquals("Success", result)
    assertEquals(3, attempts)
    // runTest auto-advances virtual time, so test is instant
}
```
