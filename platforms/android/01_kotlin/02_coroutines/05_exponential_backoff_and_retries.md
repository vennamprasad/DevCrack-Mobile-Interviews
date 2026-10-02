## **4. Network Retry Logic with Exponential Backoff**

### **Problem**: API calls fail intermittently - need smart retry

```kotlin
class ApiRepository {
    suspend fun <T> retryWithExponentialBackoff(
        times: Int = 3,
        initialDelay: Long = 1000L,
        maxDelay: Long = 10000L,
        factor: Double = 2.0,
        block: suspend () -> T
    ): T {
        var currentDelay = initialDelay

        repeat(times - 1) { attempt ->
            try {
                return block()
            } catch (e: IOException) {
                Log.e("Retry", "Attempt ${attempt + 1} failed: ${e.message}")
            }

            delay(currentDelay)
            currentDelay = (currentDelay * factor).toLong().coerceAtMost(maxDelay)
        }

        return block() // Last attempt - let exception propagate
    }

    suspend fun fetchUserData(userId: String): User {
        return retryWithExponentialBackoff {
            api.getUser(userId)
        }
    }
}
```

**Advanced Retry with Conditional Logic**:
```kotlin
suspend fun <T> retryIO(
    retryCondition: (Exception) -> Boolean = { it is IOException },
    block: suspend () -> T
): T {
    var currentDelay = 1000L
    var lastException: Exception? = null

    repeat(3) {
        try {
            return block()
        } catch (e: Exception) {
            lastException = e
            if (!retryCondition(e)) {
                throw e  // Don't retry 4xx errors, auth failures, etc.
            }
            delay(currentDelay)
            currentDelay *= 2
        }
    }

    throw lastException!!
}

// Usage
val user = retryIO(
    retryCondition = {
        it is IOException || (it as? HttpException)?.code() == 503
    }
) {
    api.fetchUser(userId)
}
```
