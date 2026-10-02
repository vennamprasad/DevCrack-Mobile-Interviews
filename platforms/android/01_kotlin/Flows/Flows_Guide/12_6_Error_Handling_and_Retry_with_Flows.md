## **6. Error Handling and Retry with Flows**

### **Problem**: Network calls fail, need retry logic

```kotlin
class NetworkRepository {
    fun fetchDataWithRetry(): Flow<Result<Data>> = flow {
        emit(Result.Loading)

        val data = api.fetchData()
        emit(Result.Success(data))
    }
    .retry(3) { cause ->
        // Only retry on IO exceptions, with delay
        (cause is IOException).also { shouldRetry ->
            if (shouldRetry) delay(1000)
        }
    }
    .catch { exception ->
        emit(Result.Error(exception.message ?: "Unknown error"))
    }

    // Advanced retry with exponential backoff
    fun fetchDataWithExponentialBackoff(): Flow<Data> = flow {
        api.fetchData()
    }.retryWhen { cause, attempt ->
        if (cause is IOException && attempt < 3) {
            delay(1000 * 2.0.pow(attempt.toInt()).toLong())
            true
        } else {
            false
        }
    }
}

// Usage
viewModelScope.launch {
    repository.fetchDataWithRetry().collect { result ->
        when (result) {
            is Result.Loading -> showLoading()
            is Result.Success -> showData(result.data)
            is Result.Error -> showError(result.message)
        }
    }
}
```

**Custom Retry Operator**:
```kotlin
fun <T> Flow<T>.retryWithBackoff(
    maxRetries: Int = 3,
    initialDelay: Long = 1000L,
    maxDelay: Long = 10000L,
    factor: Double = 2.0
): Flow<T> = retryWhen { cause, attempt ->
    if (cause is IOException && attempt < maxRetries) {
        val delay = (initialDelay * factor.pow(attempt.toInt()))
            .toLong()
            .coerceAtMost(maxDelay)
        delay(delay)
        true
    } else {
        false
    }
}

// Usage
fun getUser(): Flow<User> = flow {
    emit(api.fetchUser())
}.retryWithBackoff()
```
