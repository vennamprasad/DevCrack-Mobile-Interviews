## **HTTP Methods & Status Codes**

### Q5. Explain HTTP methods and when to use each one.

**Answer:**

**HTTP Methods (CRUD Operations):**

```kotlin
interface ApiService {

    // GET - Retrieve data (READ)
    @GET("users")
    suspend fun getUsers(): List<User>

    @GET("users/{id}")
    suspend fun getUser(@Path("id") id: Int): User

    @GET("users/{id}/posts")
    suspend fun getUserPosts(@Path("id") userId: Int): List<Post>

    // POST - Create new resource (CREATE)
    @POST("users")
    suspend fun createUser(@Body user: CreateUserRequest): User

    @POST("posts")
    suspend fun createPost(@Body post: CreatePostRequest): Post

    // PUT - Replace entire resource (UPDATE)
    @PUT("users/{id}")
    suspend fun updateUser(@Path("id") id: Int, @Body user: User): User

    // PATCH - Update partial resource (PARTIAL UPDATE)
    @PATCH("users/{id}")
    suspend fun patchUser(@Path("id") id: Int, @Body updates: Map<String, Any>): User

    // DELETE - Remove resource (DELETE)
    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") id: Int): Response<Unit>

    // HEAD - Get headers only (metadata)
    @HEAD("users/{id}")
    suspend fun checkUserExists(@Path("id") id: Int): Response<Unit>

    // OPTIONS - Get supported methods
    @OPTIONS("users")
    suspend fun getUsersOptions(): Response<Unit>
}
```

**Properties:**

| Method | Safe | Idempotent | Cacheable | Body |
|--------|------|------------|-----------|------|
| **GET** |  Yes |  Yes |  Yes | L No |
| **POST** | L No | L No | � Rarely |  Yes |
| **PUT** | L No |  Yes | L No |  Yes |
| **PATCH** | L No |  Yes* | L No |  Yes |
| **DELETE** | L No |  Yes | L No | L No |
| **HEAD** |  Yes |  Yes |  Yes | L No |

*PATCH should be idempotent but isn't guaranteed

**Real-World Examples:**
```kotlin
// GET - Fetch user profile
val profile = apiService.getUser(userId)

// POST - Register new user
val newUser = apiService.createUser(CreateUserRequest("John", "john@example.com"))

// PUT - Update entire profile
val updated = apiService.updateUser(userId, completeUserObject)

// PATCH - Update avatar only
val patched = apiService.patchUser(userId, mapOf("avatar" to newAvatarUrl))

// DELETE - Remove account
apiService.deleteUser(userId)

// HEAD - Check if user exists
val exists = apiService.checkUserExists(userId).code() == 200
```

---

### Q6. What are HTTP status codes and what do they mean?

**Answer:**

**Status Code Categories:**

**1xx - Informational:**
- `100 Continue` - Server received request headers

**2xx - Success:**
```kotlin
// 200 OK - Request successful
@GET("users/{id}")
suspend fun getUser(@Path("id") id: Int): Response<User>

if (response.code() == 200) {
    val user = response.body()
    // Success
}

// 201 Created - Resource created successfully
@POST("users")
suspend fun createUser(@Body user: User): Response<User>

if (response.code() == 201) {
    val createdUser = response.body()
    val location = response.headers()["Location"] // URL of created resource
}

// 204 No Content - Success but no response body
@DELETE("users/{id}")
suspend fun deleteUser(@Path("id") id: Int): Response<Unit>

if (response.code() == 204) {
    // Deleted successfully, no body returned
}
```

**3xx - Redirection:**
```kotlin
// 301 Moved Permanently - Resource moved
// 302 Found - Temporary redirect
// 304 Not Modified - Use cached version

when (response.code()) {
    304 -> {
        // Use cached data
        val cachedData = cache.get(url)
    }
}
```

**4xx - Client Errors:**
```kotlin
// 400 Bad Request - Invalid request format
// 401 Unauthorized - Authentication required
// 403 Forbidden - No permission
// 404 Not Found - Resource doesn't exist
// 409 Conflict - Resource conflict
// 422 Unprocessable Entity - Validation error
// 429 Too Many Requests - Rate limit exceeded

sealed class ApiError : Exception() {
    data class BadRequest(val errors: List<String>) : ApiError()
    object Unauthorized : ApiError()
    object Forbidden : ApiError()
    data class NotFound(val resource: String) : ApiError()
    data class ValidationError(val fields: Map<String, String>) : ApiError()
    object RateLimitExceeded : ApiError()
    data class ServerError(val message: String) : ApiError()
}

suspend fun <T> safeApiCall(apiCall: suspend () -> Response<T>): Result<T> {
    return try {
        val response = apiCall()
        when (response.code()) {
            200, 201 -> Result.Success(response.body()!!)
            204 -> Result.Success(null as T)
            400 -> Result.Error(ApiError.BadRequest(parseErrors(response)))
            401 -> Result.Error(ApiError.Unauthorized)
            403 -> Result.Error(ApiError.Forbidden)
            404 -> Result.Error(ApiError.NotFound("Resource"))
            422 -> Result.Error(ApiError.ValidationError(parseValidation(response)))
            429 -> Result.Error(ApiError.RateLimitExceeded)
            in 500..599 -> Result.Error(ApiError.ServerError("Server error"))
            else -> Result.Error(ApiError.ServerError("Unknown error"))
        }
    } catch (e: Exception) {
        Result.Error(e)
    }
}
```

**5xx - Server Errors:**
```kotlin
// 500 Internal Server Error - Server crashed
// 502 Bad Gateway - Invalid response from upstream
// 503 Service Unavailable - Server down/maintenance
// 504 Gateway Timeout - Upstream timeout

when (response.code()) {
    500 -> showError("Server error, please try again")
    503 -> showError("Service unavailable, maintenance in progress")
    504 -> showError("Request timeout, please try again")
}
```

**Common Status Codes in Mobile:**

| Code | Name | Meaning | Action |
|------|------|---------|--------|
| **200** | OK | Success | Process data |
| **201** | Created | Resource created | Get created resource |
| **204** | No Content | Success, no data | Update UI state |
| **400** | Bad Request | Invalid request | Show validation errors |
| **401** | Unauthorized | Not logged in | Redirect to login |
| **403** | Forbidden | No permission | Show error |
| **404** | Not Found | Resource missing | Show "not found" |
| **422** | Validation Error | Data validation failed | Show field errors |
| **429** | Rate Limited | Too many requests | Retry with backoff |
| **500** | Server Error | Server crashed | Show error, retry |
| **503** | Unavailable | Maintenance | Show maintenance screen |
