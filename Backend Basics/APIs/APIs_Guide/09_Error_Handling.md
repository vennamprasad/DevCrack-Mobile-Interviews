## **Error Handling**

### Q14. How do you handle API errors in Android?

**Answer:**

**Comprehensive Error Handling:**

**1. Error Types:**
```kotlin
sealed class ApiError : Exception() {
    data class NetworkError(override val message: String = "No internet connection") : ApiError()
    data class ServerError(val code: Int, override val message: String) : ApiError()
    data class ValidationError(val errors: Map<String, String>) : ApiError()
    object Unauthorized : ApiError() {
        override val message = "Please login again"
    }
    object Forbidden : ApiError() {
        override val message = "You don't have permission"
    }
    data class NotFound(val resource: String) : ApiError() {
        override val message = "$resource not found"
    }
    object RateLimitExceeded : ApiError() {
        override val message = "Too many requests, please try again later"
    }
    data class Unknown(override val message: String = "Something went wrong") : ApiError()
}

sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val error: ApiError) : Result<Nothing>()
    object Loading : Result<Nothing>()
}
```

**2. Safe API Call Wrapper:**
```kotlin
suspend fun <T> safeApiCall(apiCall: suspend () -> T): Result<T> {
    return try {
        Result.Success(apiCall())
    } catch (e: Exception) {
        Result.Error(mapException(e))
    }
}

private fun mapException(exception: Exception): ApiError {
    return when (exception) {
        is HttpException -> {
            when (exception.code()) {
                400 -> ApiError.ValidationError(parseValidationErrors(exception))
                401 -> ApiError.Unauthorized
                403 -> ApiError.Forbidden
                404 -> ApiError.NotFound("Resource")
                429 -> ApiError.RateLimitExceeded
                in 500..599 -> ApiError.ServerError(
                    exception.code(),
                    "Server error: ${exception.message()}"
                )
                else -> ApiError.Unknown(exception.message())
            }
        }
        is IOException -> ApiError.NetworkError()
        is SocketTimeoutException -> ApiError.NetworkError("Request timeout")
        is UnknownHostException -> ApiError.NetworkError("No internet connection")
        else -> ApiError.Unknown(exception.message ?: "Unknown error")
    }
}

private fun parseValidationErrors(exception: HttpException): Map<String, String> {
    return try {
        val errorBody = exception.response()?.errorBody()?.string()
        val errorResponse = Gson().fromJson(errorBody, ValidationErrorResponse::class.java)
        errorResponse.errors ?: emptyMap()
    } catch (e: Exception) {
        emptyMap()
    }
}

data class ValidationErrorResponse(
    val message: String,
    val errors: Map<String, String>?
)
```

**3. Repository with Error Handling:**
```kotlin
class UserRepository @Inject constructor(
    private val apiService: ApiService,
    private val networkChecker: NetworkChecker
) {

    suspend fun getUser(userId: Int): Result<User> {
        if (!networkChecker.isConnected()) {
            return Result.Error(ApiError.NetworkError())
        }

        return safeApiCall {
            apiService.getUser(userId)
        }
    }

    suspend fun createUser(request: CreateUserRequest): Result<User> {
        return safeApiCall {
            apiService.createUser(request)
        }
    }

    suspend fun updateUser(userId: Int, request: UpdateUserRequest): Result<User> {
        return safeApiCall {
            apiService.updateUser(userId, request)
        }
    }
}
```

**4. ViewModel with Error States:**
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState>(UiState.Initial)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    sealed class UiState {
        object Initial : UiState()
        object Loading : UiState()
        data class Success(val users: List<User>) : UiState()
        data class Error(val error: ApiError) : UiState()
    }

    fun loadUser(userId: Int) {
        viewModelScope.launch {
            _uiState.value = UiState.Loading

            when (val result = repository.getUser(userId)) {
                is Result.Success -> {
                    _uiState.value = UiState.Success(listOf(result.data))
                }
                is Result.Error -> {
                    _uiState.value = UiState.Error(result.error)
                    handleError(result.error)
                }
                else -> {}
            }
        }
    }

    private fun handleError(error: ApiError) {
        when (error) {
            is ApiError.Unauthorized -> {
                // Redirect to login
                _navigationEvent.value = NavigationEvent.Login
            }
            is ApiError.NetworkError -> {
                // Show retry option
            }
            is ApiError.RateLimitExceeded -> {
                // Implement exponential backoff
            }
            else -> {
                // Show generic error
            }
        }
    }
}
```

**5. UI Layer Error Handling:**
```kotlin
@Composable
fun UserScreen(viewModel: UserViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    when (val state = uiState) {
        is UserViewModel.UiState.Loading -> {
            LoadingIndicator()
        }
        is UserViewModel.UiState.Success -> {
            UserList(users = state.users)
        }
        is UserViewModel.UiState.Error -> {
            ErrorScreen(
                error = state.error,
                onRetry = { viewModel.loadUser(userId) }
            )
        }
        else -> {}
    }
}

@Composable
fun ErrorScreen(error: ApiError, onRetry: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        val (icon, title, message) = when (error) {
            is ApiError.NetworkError -> Triple(
                Icons.Default.CloudOff,
                "No Connection",
                error.message
            )
            is ApiError.ServerError -> Triple(
                Icons.Default.Error,
                "Server Error",
                error.message
            )
            is ApiError.Unauthorized -> Triple(
                Icons.Default.Lock,
                "Unauthorized",
                error.message
            )
            is ApiError.NotFound -> Triple(
                Icons.Default.SearchOff,
                "Not Found",
                error.message
            )
            else -> Triple(
                Icons.Default.Error,
                "Error",
                error.message ?: "Something went wrong"
            )
        }

        Icon(
            imageVector = icon,
            contentDescription = null,
            modifier = Modifier.size(64.dp)
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(text = title, style = MaterialTheme.typography.h6)
        Text(text = message, style = MaterialTheme.typography.body2)

        Spacer(modifier = Modifier.height(24.dp))

        if (error !is ApiError.Unauthorized) {
            Button(onClick = onRetry) {
                Text("Retry")
            }
        }
    }
}
```

**6. Retry Logic with Exponential Backoff:**
```kotlin
class RetryInterceptor(
    private val maxRetries: Int = 3,
    private val initialDelay: Long = 1000L
) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        var attempt = 0
        var response: Response? = null
        var exception: IOException? = null

        while (attempt < maxRetries) {
            try {
                response = chain.proceed(chain.request())

                if (response.isSuccessful || !shouldRetry(response.code)) {
                    return response
                }

                response.close()
            } catch (e: IOException) {
                exception = e
            }

            attempt++
            if (attempt < maxRetries) {
                val delay = initialDelay * (1 shl (attempt - 1)) // Exponential backoff
                Thread.sleep(delay)
            }
        }

        return response ?: throw (exception ?: IOException("Max retries exceeded"))
    }

    private fun shouldRetry(code: Int): Boolean {
        return code in listOf(408, 429, 500, 502, 503, 504)
    }
}
```
