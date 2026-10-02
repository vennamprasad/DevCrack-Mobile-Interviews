## **2. Error Handling Patterns**

### **Problem**: One failed coroutine shouldn't crash the entire app

**Basic Try-Catch**:
```kotlin
viewModelScope.launch {
    try {
        val data = repository.fetchData()
        _uiState.value = UiState.Success(data)
    } catch (e: IOException) {
        _uiState.value = UiState.Error("Network error")
    } catch (e: Exception) {
        _uiState.value = UiState.Error("Unknown error")
    }
}
```

**CoroutineExceptionHandler** (Global handler):
```kotlin
class MyViewModel : ViewModel() {
    private val exceptionHandler = CoroutineExceptionHandler { _, exception ->
        _errorState.value = exception.message
        logErrorToAnalytics(exception)
    }

    fun loadData() {
        viewModelScope.launch(exceptionHandler) {
            val data = repository.fetchData() // Any unhandled exception goes to handler
            _uiState.value = data
        }
    }
}
```

**supervisorScope** (One failure doesn't cancel siblings):
```kotlin
suspend fun loadDashboard(): Dashboard {
    return supervisorScope {
        val news = async {
            try { fetchNews() }
            catch (e: Exception) { emptyList() }  // Fail gracefully
        }
        val weather = async {
            try { fetchWeather() }
            catch (e: Exception) { null }
        }
        val stocks = async {
            try { fetchStocks() }
            catch (e: Exception) { emptyList() }
        }

        Dashboard(
            news = news.await(),
            weather = weather.await(),
            stocks = stocks.await()
        )
    }
}
```

**Why It Matters**: In `coroutineScope`, if one child fails, all siblings are canceled. With `supervisorScope`, siblings continue even if one fails.
