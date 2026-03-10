## **8. Testing Flows**

### **Problem**: How to test asynchronous flows

**Using Turbine Library**:
```kotlin
@Test
fun `test search flow emits correct results`() = runTest {
    val viewModel = SearchViewModel(fakeRepository)

    viewModel.searchResults.test {
        // Initial state
        assertEquals(emptyList(), awaitItem())

        // Trigger search
        viewModel.onSearchQueryChanged("kotlin")

        // Skip intermediate emissions if any
        // Then assert final result
        assertEquals(listOf("Kotlin Coroutines", "Kotlin Flows"), awaitItem())

        cancelAndIgnoreRemainingEvents()
    }
}
```

**Without Turbine**:
```kotlin
@Test
fun `test flow emissions`() = runTest {
    val flow = flow {
        emit(1)
        delay(100)
        emit(2)
        delay(100)
        emit(3)
    }

    val results = mutableListOf<Int>()
    flow.toList(results)

    assertEquals(listOf(1, 2, 3), results)
}

@Test
fun `test StateFlow updates`() = runTest {
    val viewModel = MyViewModel(fakeRepository)

    val job = launch {
        viewModel.uiState.collect {
            // Assertions here
        }
    }

    viewModel.loadData()

    advanceUntilIdle()  // Advance virtual time

    assertEquals(UiState.Success, viewModel.uiState.value)

    job.cancel()
}
```
