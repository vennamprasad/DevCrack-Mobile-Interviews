## API Design

### Q7. How do you design RESTful APIs for mobile applications?

**Answer:**

API design is crucial for mobile apps as it affects performance, battery life, and user experience.

**RESTful API Principles:**

```
HTTP Methods:
GET    - Retrieve data (safe, idempotent)
POST   - Create new resource
PUT    - Update entire resource (idempotent)
PATCH  - Partial update
DELETE - Remove resource (idempotent)

Status Codes:
2xx - Success (200 OK, 201 Created, 204 No Content)
3xx - Redirection
4xx - Client errors (400 Bad Request, 401 Unauthorized, 404 Not Found)
5xx - Server errors (500 Internal Server Error, 503 Service Unavailable)
```

**1. API Endpoint Design:**

```kotlin
// ✓ Good: RESTful, resource-oriented
interface UserApi {
    // Get user profile
    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: String): User

    // Get user's posts (nested resource)
    @GET("users/{id}/posts")
    suspend fun getUserPosts(
        @Path("id") userId: String,
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20
    ): PostsResponse

    // Create a post
    @POST("posts")
    suspend fun createPost(@Body post: CreatePostRequest): Post

    // Update user profile (full update)
    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") userId: String,
        @Body user: UpdateUserRequest
    ): User

    // Partial update (specific fields)
    @PATCH("users/{id}")
    suspend fun patchUser(
        @Path("id") userId: String,
        @Body updates: Map<String, Any>
    ): User

    // Delete post
    @DELETE("posts/{id}")
    suspend fun deletePost(@Path("id") postId: String): Response<Unit>
}

// ✗ Bad: Non-RESTful, action-oriented
interface BadApi {
    @GET("getUserById")  // ✗ Should be GET /users/{id}
    suspend fun getUserById(@Query("id") id: String): User

    @POST("deletePost")  // ✗ Should be DELETE /posts/{id}
    suspend fun deletePost(@Body postId: String): Response<Unit>

    @GET("getAllUserPostsAndComments")  // ✗ Too specific, not scalable
    suspend fun getAllData(@Query("userId") userId: String): Response<Any>
}
```

**2. Request/Response Design:**

```kotlin
// Request DTOs
data class CreatePostRequest(
    val content: String,
    val imageUrls: List<String> = emptyList(),
    val tags: List<String> = emptyList(),
    val visibility: PostVisibility = PostVisibility.PUBLIC
)

data class UpdateUserRequest(
    val name: String,
    val bio: String,
    val avatarUrl: String?,
    val location: String?
)

// Response wrapper for consistency
data class ApiResponse<T>(
    val data: T?,
    val error: ErrorResponse?,
    val metadata: Metadata?
)

data class ErrorResponse(
    val code: String,
    val message: String,
    val details: Map<String, Any> = emptyMap()
)

data class Metadata(
    val timestamp: Long,
    val requestId: String,
    val version: String = "1.0"
)

// Pagination response
data class PaginatedResponse<T>(
    val data: List<T>,
    val pagination: PaginationInfo
)

data class PaginationInfo(
    val page: Int,
    val limit: Int,
    val totalPages: Int,
    val totalCount: Int,
    val hasNext: Boolean,
    val hasPrevious: Boolean
)

// Usage
interface PostApi {
    @GET("posts")
    suspend fun getPosts(
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20,
        @Query("sort") sort: String = "createdAt",
        @Query("order") order: String = "desc"
    ): PaginatedResponse<Post>
}
```

**3. API Versioning:**

```kotlin
// Strategy 1: URL versioning (most common for mobile)
interface ApiServiceV1 {
    @GET("v1/users/{id}")
    suspend fun getUser(@Path("id") userId: String): User
}

interface ApiServiceV2 {
    @GET("v2/users/{id}")  // Breaking changes in V2
    suspend fun getUser(@Path("id") userId: String): UserV2
}

// Strategy 2: Header versioning
class VersionInterceptor(private val version: String) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request().newBuilder()
            .addHeader("API-Version", version)
            .build()
        return chain.proceed(request)
    }
}

// Handle multiple versions in app
class ApiVersionManager @Inject constructor(
    private val apiV1: ApiServiceV1,
    private val apiV2: ApiServiceV2,
    private val preferences: AppPreferences
) {
    suspend fun getUser(userId: String): User {
        return when (preferences.getApiVersion()) {
            "v1" -> apiV1.getUser(userId).toUser()
            "v2" -> apiV2.getUser(userId).toUser()
            else -> apiV2.getUser(userId).toUser()  // Default to latest
        }
    }
}
```

**4. Efficient Data Transfer:**

```kotlin
// Use field filtering to reduce payload size
interface UserApi {
    // Full user object
    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: String): User

    // Partial response with specific fields
    @GET("users/{id}")
    suspend fun getUserBasic(
        @Path("id") userId: String,
        @Query("fields") fields: String = "id,name,avatarUrl"
    ): UserBasic

    // Batch requests to reduce roundtrips
    @POST("users/batch")
    suspend fun getUsersBatch(@Body userIds: List<String>): List<User>
}

// Response compression
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            // Request compression
            .addInterceptor { chain ->
                chain.proceed(
                    chain.request().newBuilder()
                        .header("Accept-Encoding", "gzip, deflate")
                        .build()
                )
            }
            .build()
    }
}

// GraphQL for flexible queries (alternative to REST)
data class GraphQLRequest(
    val query: String,
    val variables: Map<String, Any> = emptyMap()
)

interface GraphQLApi {
    @POST("graphql")
    suspend fun query(@Body request: GraphQLRequest): GraphQLResponse
}

// Usage
class UserRepository @Inject constructor(
    private val graphQLApi: GraphQLApi
) {
    suspend fun getUser(userId: String): User {
        val query = """
            query GetUser(${"$"}id: ID!) {
                user(id: ${"$"}id) {
                    id
                    name
                    avatarUrl
                    posts(limit: 10) {
                        id
                        content
                        createdAt
                    }
                }
            }
        """.trimIndent()

        val response = graphQLApi.query(
            GraphQLRequest(
                query = query,
                variables = mapOf("id" to userId)
            )
        )

        return response.data.user
    }
}
```

**5. Error Handling:**

```kotlin
// Standardized error responses
sealed class ApiError {
    data class NetworkError(val exception: IOException) : ApiError()
    data class HttpError(val code: Int, val message: String) : ApiError()
    data class ValidationError(val errors: Map<String, List<String>>) : ApiError()
    data class ServerError(val message: String) : ApiError()
    data class UnknownError(val exception: Throwable) : ApiError()
}

// Error interceptor
class ErrorHandlingInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()

        try {
            val response = chain.proceed(request)

            // Log errors
            if (!response.isSuccessful) {
                val errorBody = response.body?.string()
                Log.e("API", "Error ${response.code}: $errorBody")
            }

            return response
        } catch (e: IOException) {
            Log.e("API", "Network error", e)
            throw e
        }
    }
}

// Repository error handling
class UserRepository @Inject constructor(
    private val apiService: ApiService
) {
    suspend fun getUser(userId: String): Result<User> {
        return try {
            val user = apiService.getUser(userId)
            Result.Success(user)
        } catch (e: IOException) {
            Result.Error(ApiError.NetworkError(e))
        } catch (e: HttpException) {
            when (e.code()) {
                400 -> {
                    val error = parseErrorBody(e.response()?.errorBody())
                    Result.Error(ApiError.ValidationError(error.validationErrors))
                }
                401 -> Result.Error(ApiError.HttpError(401, "Unauthorized"))
                404 -> Result.Error(ApiError.HttpError(404, "User not found"))
                in 500..599 -> Result.Error(ApiError.ServerError(e.message()))
                else -> Result.Error(ApiError.UnknownError(e))
            }
        } catch (e: Exception) {
            Result.Error(ApiError.UnknownError(e))
        }
    }
}
```

**6. Rate Limiting & Throttling:**

```kotlin
// Respect rate limits from server
class RateLimitInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val response = chain.proceed(chain.request())

        if (response.code == 429) {  // Too Many Requests
            val retryAfter = response.header("Retry-After")?.toLongOrNull() ?: 60
            Log.w("API", "Rate limited. Retry after $retryAfter seconds")

            // Store rate limit info
            // App should show user-friendly message
        }

        // Track remaining quota
        val rateLimitRemaining = response.header("X-RateLimit-Remaining")?.toIntOrNull()
        val rateLimitReset = response.header("X-RateLimit-Reset")?.toLongOrNull()

        if (rateLimitRemaining != null && rateLimitRemaining < 10) {
            Log.w("API", "Rate limit low: $rateLimitRemaining requests remaining")
        }

        return response
    }
}

// Client-side request throttling
class RequestThrottler {
    private val requestTimestamps = mutableListOf<Long>()
    private val maxRequestsPerMinute = 60

    suspend fun throttle() {
        val now = System.currentTimeMillis()
        val oneMinuteAgo = now - 60_000

        // Remove old timestamps
        requestTimestamps.removeAll { it < oneMinuteAgo }

        if (requestTimestamps.size >= maxRequestsPerMinute) {
            val oldestRequest = requestTimestamps.first()
            val delayMs = 60_000 - (now - oldestRequest)
            if (delayMs > 0) {
                delay(delayMs)
            }
        }

        requestTimestamps.add(now)
    }
}
```

**7. API Security:**

```kotlin
// Authentication interceptor
class AuthInterceptor @Inject constructor(
    private val tokenManager: TokenManager
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()

        // Add auth token
        val token = tokenManager.getAccessToken()
        val authenticatedRequest = if (token != null) {
            originalRequest.newBuilder()
                .header("Authorization", "Bearer $token")
                .build()
        } else {
            originalRequest
        }

        val response = chain.proceed(authenticatedRequest)

        // Handle token expiration
        if (response.code == 401) {
            response.close()

            // Try to refresh token
            val newToken = tokenManager.refreshToken()

            if (newToken != null) {
                // Retry with new token
                val retryRequest = originalRequest.newBuilder()
                    .header("Authorization", "Bearer $newToken")
                    .build()
                return chain.proceed(retryRequest)
            }
        }

        return response
    }
}

// Token management
class TokenManager @Inject constructor(
    private val secureStorage: SecureStorage,
    private val authApi: AuthApi
) {
    suspend fun refreshToken(): String? {
        val refreshToken = secureStorage.getRefreshToken() ?: return null

        return try {
            val response = authApi.refreshToken(RefreshTokenRequest(refreshToken))
            secureStorage.saveAccessToken(response.accessToken)
            secureStorage.saveRefreshToken(response.refreshToken)
            response.accessToken
        } catch (e: Exception) {
            // Refresh failed, user needs to login again
            secureStorage.clear()
            null
        }
    }
}
```

**Best Practices Summary:**

| Practice | Implementation | Benefit |
|----------|----------------|---------|
| **Pagination** | Limit results, use cursor-based | Reduces payload size |
| **Field filtering** | `?fields=id,name` | Only fetch needed data |
| **Compression** | gzip, Brotli | Smaller network transfer |
| **Caching** | ETag, Cache-Control headers | Avoid unnecessary requests |
| **Batch requests** | Single call for multiple resources | Reduce roundtrips |
| **Versioning** | URL or header-based | Backward compatibility |
| **Error codes** | Standard HTTP status codes | Consistent error handling |

---

