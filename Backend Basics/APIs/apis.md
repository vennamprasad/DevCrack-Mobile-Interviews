# ðŸ”Œ Mobile API Implementation & Networking
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Retrofit, OkHttp, Authentication scenarios, and Error Handling.

![API](https://img.shields.io/badge/Android-Networking-green?style=for-the-badge&logo=android&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---
## **Table of Contents**
1. [API Fundamentals](#api-fundamentals)
2. [REST APIs](#rest-apis)
3. [HTTP Methods & Status Codes](#http-methods--status-codes)
4. [API Design & Best Practices](#api-design--best-practices)
5. [Authentication & Authorization](#authentication--authorization)
6. [GraphQL](#graphql)
7. [Android Implementation](#android-implementation)
8. [Error Handling](#error-handling)
9. [Networking Libraries](#networking-libraries)
10. [Performance & Optimization](#performance--optimization)
11. [Security Best Practices](#security-best-practices)
12. [Testing APIs](#testing-apis)

---

## **API Fundamentals**

### Q1. What is an API and why is it important for mobile apps?

**Answer:**
API (Application Programming Interface) is a set of protocols and tools that allows different software applications to communicate with each other.

**Key Components:**
- **Endpoints**: URLs that clients can call
- **Request**: What the client sends (method, headers, body)
- **Response**: What the server returns (status, headers, body)
- **Authentication**: Verifying client identity
- **Rate Limiting**: Controlling request frequency

**Why Important for Mobile:**
```kotlin
// Mobile apps rely on APIs for:
// 1. Data fetching
viewModelScope.launch {
    val users = apiService.getUsers() // Fetch from server
    _users.value = users
}

// 2. User authentication
suspend fun login(email: String, password: String): AuthResponse {
    return apiService.login(LoginRequest(email, password))
}

// 3. Real-time updates
fun observeMessages(): Flow<Message> {
    return webSocket.receiveAsFlow()
}

// 4. Content synchronization
suspend fun syncData() {
    val localData = database.getData()
    val remoteData = apiService.getData()
    // Merge and sync
}
```

**Benefits:**
- Separation of concerns (frontend/backend)
- Platform independence
- Scalability
- Centralized business logic
- Easy updates without app releases

---

### Q2. What are the different types of APIs?

**Answer:**

**1. REST (Representational State Transfer):**
```kotlin
interface ApiService {
    @GET("users")
    suspend fun getUsers(): List<User>

    @POST("users")
    suspend fun createUser(@Body user: User): User

    @PUT("users/{id}")
    suspend fun updateUser(@Path("id") id: Int, @Body user: User): User

    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") id: Int): Response<Unit>
}
```

**2. GraphQL:**
```kotlin
// Single endpoint, flexible queries
const val QUERY = """
    query GetUser(${'$'}id: ID!) {
        user(id: ${'$'}id) {
            id
            name
            email
            posts {
                title
                content
            }
        }
    }
"""
```

**3. WebSocket:**
```kotlin
// Real-time bidirectional communication
val webSocket = client.newWebSocket(request, object : WebSocketListener() {
    override fun onMessage(webSocket: WebSocket, text: String) {
        // Handle real-time message
    }
})
```

**4. gRPC:**
```kotlin
// High-performance RPC framework
val stub = UserServiceGrpc.newBlockingStub(channel)
val response = stub.getUser(GetUserRequest.newBuilder().setId(1).build())
```

**Comparison:**

| Type | Use Case | Pros | Cons |
|------|----------|------|------|
| **REST** | Standard CRUD operations | Simple, widely adopted | Over-fetching, multiple requests |
| **GraphQL** | Complex data requirements | Flexible, single request | Learning curve, complex caching |
| **WebSocket** | Real-time updates | Bidirectional, low latency | Connection management |
| **gRPC** | Microservices, high performance | Fast, type-safe | Limited browser support |

---

## **REST APIs**

### Q3. What are the principles of REST?

**Answer:**

**6 REST Principles:**

**1. Client-Server Architecture:**
```kotlin
// Client (Mobile App)
class UserViewModel(private val repository: UserRepository) : ViewModel() {
    fun loadUsers() {
        viewModelScope.launch {
            val users = repository.getUsers() // Request to server
            _users.value = users
        }
    }
}

// Server provides the API
// GET https://api.example.com/users
```

**2. Stateless:**
```kotlin
// Each request contains all necessary information
@Headers(
    "Authorization: Bearer eyJhbGc...",
    "Content-Type: application/json"
)
@GET("users/profile")
suspend fun getUserProfile(): UserProfile

// Server doesn't store client state between requests
```

**3. Cacheable:**
```kotlin
// Responses indicate if they can be cached
@Headers("Cache-Control: max-age=3600")
@GET("users")
suspend fun getUsers(): List<User>

// Client can cache for 1 hour
```

**4. Uniform Interface:**
```kotlin
// Consistent endpoint structure
interface ApiService {
    @GET("users")           // Get all users
    @GET("users/{id}")      // Get specific user
    @POST("users")          // Create user
    @PUT("users/{id}")      // Update user
    @DELETE("users/{id}")   // Delete user
}
```

**5. Layered System:**
```
Client ’ Load Balancer ’ API Gateway ’ Auth Service ’ Business Logic ’ Database
```

**6. Code on Demand (Optional):**
```kotlin
// Server can send executable code
// Rarely used in mobile apps
```

---

### Q4. What is the difference between PUT and PATCH?

**Answer:**

**PUT - Full Update (Replace entire resource):**
```kotlin
@PUT("users/{id}")
suspend fun updateUser(
    @Path("id") id: Int,
    @Body user: User  // Complete user object required
): User

// Usage
val updatedUser = User(
    id = 1,
    name = "John Doe",
    email = "john@example.com",
    phone = "123-456-7890",
    address = "123 Main St",
    age = 30
)
apiService.updateUser(1, updatedUser)

// Request Body (ALL fields)
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "address": "123 Main St",
    "age": 30
}
```

**PATCH - Partial Update (Modify specific fields):**
```kotlin
@PATCH("users/{id}")
suspend fun patchUser(
    @Path("id") id: Int,
    @Body updates: Map<String, Any>  // Only changed fields
): User

// Usage - Update only email
apiService.patchUser(1, mapOf("email" to "newemail@example.com"))

// Request Body (ONLY changed fields)
{
    "email": "newemail@example.com"
}
```

**Real-World Example:**
```kotlin
// User profile update
data class UserProfileUpdate(
    val name: String? = null,
    val bio: String? = null,
    val avatarUrl: String? = null
)

@PATCH("users/profile")
suspend fun updateProfile(@Body update: UserProfileUpdate): UserProfile

// Usage - Update only bio
viewModel.updateProfile(UserProfileUpdate(bio = "New bio"))
```

**Key Differences:**

| Feature | PUT | PATCH |
|---------|-----|-------|
| **Updates** | Full replacement | Partial update |
| **Fields** | All required | Only changed |
| **Idempotent** | Yes | Yes |
| **Bandwidth** | More data | Less data |
| **Use case** | Complete update | Small changes |

---

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
| **POST** | L No | L No |   Rarely |  Yes |
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

---

## **API Design & Best Practices**

### Q7. What are API versioning strategies?

**Answer:**

**1. URL Path Versioning (Most Common):**
```kotlin
// Version in URL path
interface ApiService {
    @GET("v1/users")
    suspend fun getUsersV1(): List<UserV1>

    @GET("v2/users")
    suspend fun getUsersV2(): List<UserV2>
}

// Base URL includes version
const val BASE_URL_V1 = "https://api.example.com/v1/"
const val BASE_URL_V2 = "https://api.example.com/v2/"
```

**2. Query Parameter Versioning:**
```kotlin
@GET("users")
suspend fun getUsers(@Query("version") version: String = "1"): List<User>

// Usage
apiService.getUsers(version = "2")
// GET https://api.example.com/users?version=2
```

**3. Header Versioning:**
```kotlin
@GET("users")
suspend fun getUsers(@Header("API-Version") version: String = "1"): List<User>

// Usage
apiService.getUsers(version = "2")
// Headers: API-Version: 2
```

**4. Content Negotiation:**
```kotlin
@Headers("Accept: application/vnd.example.v2+json")
@GET("users")
suspend fun getUsersV2(): List<User>
```

**Best Practice - Multiple Version Support:**
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    @Named("ApiV1")
    fun provideApiV1(retrofit: Retrofit): ApiService {
        return retrofit.newBuilder()
            .baseUrl("https://api.example.com/v1/")
            .build()
            .create(ApiService::class.java)
    }

    @Provides
    @Singleton
    @Named("ApiV2")
    fun provideApiV2(retrofit: Retrofit): ApiService {
        return retrofit.newBuilder()
            .baseUrl("https://api.example.com/v2/")
            .build()
            .create(ApiService::class.java)
    }
}

// Repository handles version
class UserRepository @Inject constructor(
    @Named("ApiV2") private val apiV2: ApiService,
    @Named("ApiV1") private val apiV1: ApiService
) {
    suspend fun getUsers(): List<User> {
        return try {
            apiV2.getUsers() // Try v2 first
        } catch (e: Exception) {
            apiV1.getUsers() // Fallback to v1
        }
    }
}
```

**Recommendations:**
-  **URL Path**: Most explicit, easy to cache
- L **Query Parameter**: Can cause caching issues
-   **Header**: Clean URLs but less visible
-   **Content Negotiation**: Complex but RESTful

---

### Q8. What are best practices for API endpoint design?

**Answer:**

**1. Use Nouns, Not Verbs:**
```kotlin
// L Bad
@GET("getUsers")
@POST("createUser")
@DELETE("deleteUser")

//  Good
@GET("users")          // GET for retrieve
@POST("users")         // POST for create
@DELETE("users/{id}")  // DELETE for remove
```

**2. Use Plural Nouns:**
```kotlin
// L Bad
@GET("user/{id}")
@GET("post/{id}")

//  Good
@GET("users/{id}")
@GET("posts/{id}")
```

**3. Use Resource Hierarchy:**
```kotlin
//  Good structure
@GET("users/{userId}/posts")                    // Get user's posts
@GET("users/{userId}/posts/{postId}")           // Get specific post
@GET("users/{userId}/posts/{postId}/comments")  // Get post comments
@POST("users/{userId}/posts")                   // Create post for user
```

**4. Use Query Parameters for Filtering:**
```kotlin
@GET("users")
suspend fun getUsers(
    @Query("page") page: Int = 1,
    @Query("limit") limit: Int = 20,
    @Query("sort") sort: String = "name",
    @Query("order") order: String = "asc",
    @Query("status") status: String? = null,
    @Query("search") search: String? = null
): List<User>

// Usage
// GET /users?page=2&limit=50&sort=createdAt&order=desc&status=active&search=john
```

**5. Use Standard Status Codes:**
```kotlin
// Create
@POST("users")
suspend fun createUser(@Body user: User): Response<User>
// Return 201 Created with Location header

// Update
@PUT("users/{id}")
suspend fun updateUser(@Path("id") id: Int, @Body user: User): Response<User>
// Return 200 OK

// Delete
@DELETE("users/{id}")
suspend fun deleteUser(@Path("id") id: Int): Response<Unit>
// Return 204 No Content

// Not Found
// Return 404 Not Found
```

**6. Use Consistent Naming:**
```kotlin
//  Good - Consistent snake_case in JSON
data class User(
    @SerializedName("user_id") val userId: Int,
    @SerializedName("first_name") val firstName: String,
    @SerializedName("last_name") val lastName: String,
    @SerializedName("created_at") val createdAt: String
)

// OR camelCase (be consistent)
data class User(
    val userId: Int,
    val firstName: String,
    val lastName: String,
    val createdAt: String
)
```

**7. Pagination:**
```kotlin
data class PaginatedResponse<T>(
    val data: List<T>,
    val page: Int,
    val totalPages: Int,
    val totalItems: Int,
    val hasNext: Boolean,
    val hasPrevious: Boolean
)

@GET("users")
suspend fun getUsers(
    @Query("page") page: Int,
    @Query("limit") limit: Int
): PaginatedResponse<User>
```

**8. Error Response Format:**
```kotlin
data class ErrorResponse(
    val error: String,
    val message: String,
    val statusCode: Int,
    val timestamp: String,
    val path: String,
    val details: Map<String, String>? = null
)

// Example error response:
{
    "error": "Validation Error",
    "message": "Invalid user data",
    "statusCode": 422,
    "timestamp": "2025-01-10T12:00:00Z",
    "path": "/users",
    "details": {
        "email": "Invalid email format",
        "age": "Must be greater than 0"
    }
}
```

---

## **Authentication & Authorization**

### Q9. What are different authentication methods for APIs?

**Answer:**

**1. Basic Authentication:**
```kotlin
// Username:Password in Base64
val credentials = "username:password"
val encodedCredentials = Base64.encodeToString(credentials.toByteArray(), Base64.NO_WRAP)

@Headers("Authorization: Basic $encodedCredentials")
@GET("users/profile")
suspend fun getProfile(): UserProfile

//   Not recommended - credentials sent with every request
// Only use with HTTPS
```

**2. API Key Authentication:**
```kotlin
@GET("users")
suspend fun getUsers(@Header("X-API-Key") apiKey: String): List<User>

// Or in query parameter
@GET("users")
suspend fun getUsers(@Query("api_key") apiKey: String): List<User>

// Usage
const val API_KEY = "your_api_key_here"
apiService.getUsers(API_KEY)
```

**3. Bearer Token (JWT - Most Common):**
```kotlin
// Login to get token
data class LoginRequest(val email: String, val password: String)
data class AuthResponse(val token: String, val refreshToken: String)

interface AuthService {
    @POST("auth/login")
    suspend fun login(@Body request: LoginRequest): AuthResponse

    @POST("auth/refresh")
    suspend fun refreshToken(@Body refreshToken: String): AuthResponse

    @POST("auth/logout")
    suspend fun logout(@Header("Authorization") token: String): Response<Unit>
}

// Add token to requests
class AuthInterceptor(private val tokenManager: TokenManager) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokenManager.getAccessToken()
        val request = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer $token")
            .build()
        return chain.proceed(request)
    }
}

// Token storage
class TokenManager @Inject constructor(
    private val encryptedPrefs: EncryptedSharedPreferences
) {
    fun saveTokens(accessToken: String, refreshToken: String) {
        encryptedPrefs.edit {
            putString("access_token", accessToken)
            putString("refresh_token", refreshToken)
        }
    }

    fun getAccessToken(): String? {
        return encryptedPrefs.getString("access_token", null)
    }

    fun getRefreshToken(): String? {
        return encryptedPrefs.getString("refresh_token", null)
    }

    fun clearTokens() {
        encryptedPrefs.edit { clear() }
    }
}
```

**4. OAuth 2.0:**
```kotlin
// Authorization Code Flow
// 1. Redirect user to authorization server
val authUrl = "https://auth.example.com/authorize?" +
        "client_id=$CLIENT_ID&" +
        "redirect_uri=$REDIRECT_URI&" +
        "response_type=code&" +
        "scope=read write"

// Open in browser or WebView
startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(authUrl)))

// 2. Handle redirect with authorization code
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    intent?.data?.let { uri ->
        val code = uri.getQueryParameter("code")
        if (code != null) {
            exchangeCodeForToken(code)
        }
    }
}

// 3. Exchange code for access token
suspend fun exchangeCodeForToken(code: String) {
    val response = authService.exchangeCode(
        code = code,
        clientId = CLIENT_ID,
        clientSecret = CLIENT_SECRET,
        redirectUri = REDIRECT_URI
    )
    tokenManager.saveTokens(response.accessToken, response.refreshToken)
}
```

**5. Token Refresh Strategy:**
```kotlin
class TokenAuthenticator(
    private val tokenManager: TokenManager,
    private val authService: AuthService
) : Authenticator {

    override fun authenticate(route: Route?, response: Response): Request? {
        // Don't retry if already tried once
        if (response.request.header("Authorization")?.contains("Bearer") == true) {
            if (responseCount(response) >= 2) {
                return null // Give up after 2 failed retries
            }
        }

        // Get new access token using refresh token
        return runBlocking {
            try {
                val refreshToken = tokenManager.getRefreshToken() ?: return@runBlocking null
                val newTokens = authService.refreshToken(refreshToken)

                tokenManager.saveTokens(newTokens.accessToken, newTokens.refreshToken)

                // Retry request with new token
                response.request.newBuilder()
                    .header("Authorization", "Bearer ${newTokens.accessToken}")
                    .build()
            } catch (e: Exception) {
                // Refresh failed, clear tokens and redirect to login
                tokenManager.clearTokens()
                null
            }
        }
    }

    private fun responseCount(response: Response): Int {
        var result = 1
        var current = response.priorResponse
        while (current != null) {
            result++
            current = current.priorResponse
        }
        return result
    }
}

// Configure OkHttpClient
val client = OkHttpClient.Builder()
    .addInterceptor(AuthInterceptor(tokenManager))
    .authenticator(TokenAuthenticator(tokenManager, authService))
    .build()
```

**Comparison:**

| Method | Security | Use Case | Complexity |
|--------|----------|----------|------------|
| **Basic Auth** | Low | Simple APIs | Very Low |
| **API Key** | Medium | Server-to-server | Low |
| **Bearer Token** | High | Modern mobile apps | Medium |
| **OAuth 2.0** | Very High | Third-party access | High |

---

### Q10. How do you securely store API tokens in Android?

**Answer:**

**1. EncryptedSharedPreferences (Recommended):**
```kotlin
class SecureTokenStorage @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val encryptedPrefs = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveToken(token: String) {
        encryptedPrefs.edit {
            putString("auth_token", token)
        }
    }

    fun getToken(): String? {
        return encryptedPrefs.getString("auth_token", null)
    }

    fun clearToken() {
        encryptedPrefs.edit { remove("auth_token") }
    }
}
```

**2. Android Keystore (For Sensitive Data):**
```kotlin
class KeystoreManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }
    private val keyAlias = "auth_token_key"

    init {
        createKeyIfNeeded()
    }

    private fun createKeyIfNeeded() {
        if (!keyStore.containsAlias(keyAlias)) {
            val keyGenerator = KeyGenerator.getInstance(
                KeyProperties.KEY_ALGORITHM_AES,
                "AndroidKeyStore"
            )

            val spec = KeyGenParameterSpec.Builder(
                keyAlias,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
            )
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setUserAuthenticationRequired(false)
                .build()

            keyGenerator.init(spec)
            keyGenerator.generateKey()
        }
    }

    fun encryptToken(token: String): ByteArray {
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, keyStore.getKey(keyAlias, null))
        val iv = cipher.iv
        val encrypted = cipher.doFinal(token.toByteArray())

        // Combine IV and encrypted data
        return iv + encrypted
    }

    fun decryptToken(encryptedData: ByteArray): String {
        val iv = encryptedData.copyOfRange(0, 12)
        val encrypted = encryptedData.copyOfRange(12, encryptedData.size)

        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        val spec = GCMParameterSpec(128, iv)
        cipher.init(Cipher.DECRYPT_MODE, keyStore.getKey(keyAlias, null), spec)

        return String(cipher.doFinal(encrypted))
    }
}
```

**3. Security Best Practices:**
```kotlin
class TokenManager @Inject constructor(
    private val secureStorage: SecureTokenStorage,
    private val encryptionManager: KeystoreManager
) {

    // Save with encryption
    fun saveToken(token: String) {
        val encrypted = encryptionManager.encryptToken(token)
        secureStorage.saveToken(Base64.encodeToString(encrypted, Base64.DEFAULT))
    }

    // Retrieve and decrypt
    fun getToken(): String? {
        val encrypted = secureStorage.getToken() ?: return null
        val encryptedBytes = Base64.decode(encrypted, Base64.DEFAULT)
        return encryptionManager.decryptToken(encryptedBytes)
    }

    // Clear on logout
    fun clearToken() {
        secureStorage.clearToken()
    }

    // Check if token is valid (not expired)
    fun isTokenValid(): Boolean {
        val token = getToken() ?: return false
        return try {
            val jwt = JWT(token)
            val expiresAt = jwt.expiresAt ?: return false
            expiresAt.after(Date())
        } catch (e: Exception) {
            false
        }
    }
}
```

**L Never Do This:**
```kotlin
// L DON'T store in regular SharedPreferences
val prefs = context.getSharedPreferences("prefs", Context.MODE_PRIVATE)
prefs.edit { putString("token", token) } // NOT ENCRYPTED!

// L DON'T hardcode in code
const val API_KEY = "my_secret_key_12345" // VISIBLE IN APK!

// L DON'T log sensitive data
Log.d("Auth", "Token: $token") // VISIBLE IN LOGS!

// L DON'T store in external storage
File("/sdcard/token.txt").writeText(token) // READABLE BY ALL APPS!
```

** Best Practices:**
-  Use EncryptedSharedPreferences for tokens
-  Use Android Keystore for encryption keys
-  Clear tokens on logout
-  Implement token expiration
-  Use HTTPS only
-  Implement certificate pinning
-  Obfuscate code with ProGuard/R8

---

## **GraphQL**

### Q11. What is GraphQL and how does it differ from REST?

**Answer:**

**GraphQL Overview:**
GraphQL is a query language for APIs that allows clients to request exactly the data they need.

**REST vs GraphQL:**

**REST Example:**
```kotlin
// Multiple requests needed
// 1. Get user
@GET("users/{id}")
suspend fun getUser(@Path("id") id: Int): User

// 2. Get user's posts
@GET("users/{id}/posts")
suspend fun getUserPosts(@Path("id") id: Int): List<Post>

// 3. Get post comments
@GET("posts/{id}/comments")
suspend fun getPostComments(@Path("id") id: Int): List<Comment>

// Usage - Multiple network calls
val user = apiService.getUser(1)
val posts = apiService.getUserPosts(1)
val comments = posts.flatMap { apiService.getPostComments(it.id) }

// Over-fetching: Get more data than needed
// Under-fetching: Need multiple requests
```

**GraphQL Example:**
```kotlin
// Single request with exact data needed
const val GET_USER_WITH_POSTS = """
    query GetUserWithPosts(${'$'}userId: ID!) {
        user(id: ${'$'}userId) {
            id
            name
            email
            posts {
                id
                title
                content
                comments {
                    id
                    text
                    author {
                        name
                    }
                }
            }
        }
    }
"""

// Single network call gets everything
val response = apolloClient.query(GetUserWithPostsQuery(userId = "1")).execute()
```

**Key Differences:**

| Feature | REST | GraphQL |
|---------|------|----------|
| **Endpoints** | Multiple endpoints | Single endpoint |
| **Data fetching** | Fixed structure | Flexible queries |
| **Over-fetching** | Common | No over-fetching |
| **Under-fetching** | Multiple requests | Single request |
| **Versioning** | URL versioning | Schema evolution |
| **Learning curve** | Easy | Moderate |
| **Caching** | HTTP caching | Custom caching |
| **Tooling** | Mature | Growing |

---

### Q12. How do you implement GraphQL in Android?

**Answer:**

**Using Apollo Client (Recommended):**

**1. Setup:**
```groovy
// build.gradle (app)
plugins {
    id("com.apollographql.apollo3") version "3.8.2"
}

dependencies {
    implementation("com.apollographql.apollo3:apollo-runtime:3.8.2")
    implementation("com.apollographql.apollo3:apollo-normalized-cache:3.8.2")
}

apollo {
    service("api") {
        packageName.set("com.example.app")
        schemaFile.set(file("src/main/graphql/schema.graphqls"))
    }
}
```

**2. Define Queries:**
```graphql
# src/main/graphql/GetUsers.graphql
query GetUsers {
    users {
        id
        name
        email
        avatar
    }
}

# GetUser.graphql
query GetUser($id: ID!) {
    user(id: $id) {
        id
        name
        email
        posts {
            id
            title
            content
            createdAt
        }
    }
}

# CreateUser.graphql
mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
        id
        name
        email
    }
}

# UserSubscription.graphql
subscription OnUserUpdated($userId: ID!) {
    userUpdated(userId: $userId) {
        id
        name
        email
        status
    }
}
```

**3. Configure Apollo Client:**
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object GraphQLModule {

    @Provides
    @Singleton
    fun provideApolloClient(
        okHttpClient: OkHttpClient,
        tokenManager: TokenManager
    ): ApolloClient {
        return ApolloClient.Builder()
            .serverUrl("https://api.example.com/graphql")
            .okHttpClient(okHttpClient)
            .addInterceptor(object : ApolloInterceptor {
                override fun <D : Operation.Data> intercept(
                    request: ApolloRequest<D>,
                    chain: ApolloInterceptorChain
                ): Flow<ApolloResponse<D>> {
                    val token = tokenManager.getAccessToken()
                    val newRequest = request.newBuilder()
                        .addHttpHeader("Authorization", "Bearer $token")
                        .build()
                    return chain.proceed(newRequest)
                }
            })
            .normalizedCache(
                normalizedCacheFactory = MemoryCacheFactory(maxSizeBytes = 10 * 1024 * 1024)
            )
            .build()
    }
}
```

**4. Repository Layer:**
```kotlin
class UserRepository @Inject constructor(
    private val apolloClient: ApolloClient
) {

    // Query
    suspend fun getUsers(): Result<List<User>> {
        return try {
            val response = apolloClient.query(GetUsersQuery()).execute()

            if (response.hasErrors()) {
                Result.Error(Exception(response.errors?.first()?.message))
            } else {
                val users = response.data?.users?.map { it.toUser() } ?: emptyList()
                Result.Success(users)
            }
        } catch (e: ApolloException) {
            Result.Error(e)
        }
    }

    suspend fun getUser(id: String): Result<User> {
        return try {
            val response = apolloClient.query(GetUserQuery(id)).execute()

            response.data?.user?.let {
                Result.Success(it.toUser())
            } ?: Result.Error(Exception("User not found"))
        } catch (e: ApolloException) {
            Result.Error(e)
        }
    }

    // Mutation
    suspend fun createUser(name: String, email: String): Result<User> {
        return try {
            val input = CreateUserInput(name = name, email = email)
            val response = apolloClient.mutation(CreateUserMutation(input)).execute()

            response.data?.createUser?.let {
                Result.Success(it.toUser())
            } ?: Result.Error(Exception("Failed to create user"))
        } catch (e: ApolloException) {
            Result.Error(e)
        }
    }

    // Subscription
    fun observeUserUpdates(userId: String): Flow<User> {
        return apolloClient
            .subscription(OnUserUpdatedSubscription(userId))
            .toFlow()
            .mapNotNull { response ->
                response.data?.userUpdated?.toUser()
            }
    }

    // Cache-first query
    suspend fun getUserCached(id: String): Result<User> {
        val response = apolloClient
            .query(GetUserQuery(id))
            .fetchPolicy(FetchPolicy.CacheFirst)
            .execute()

        return response.data?.user?.let {
            Result.Success(it.toUser())
        } ?: Result.Error(Exception("User not found"))
    }
}

// Extension function to map GraphQL to domain model
private fun GetUsersQuery.User.toUser() = User(
    id = id,
    name = name,
    email = email,
    avatar = avatar
)
```

**5. ViewModel:**
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _users = MutableStateFlow<UiState<List<User>>>(UiState.Loading)
    val users: StateFlow<UiState<List<User>>> = _users.asStateFlow()

    fun loadUsers() {
        viewModelScope.launch {
            _users.value = UiState.Loading
            when (val result = repository.getUsers()) {
                is Result.Success -> _users.value = UiState.Success(result.data)
                is Result.Error -> _users.value = UiState.Error(result.exception.message ?: "Error")
            }
        }
    }

    fun createUser(name: String, email: String) {
        viewModelScope.launch {
            when (repository.createUser(name, email)) {
                is Result.Success -> loadUsers() // Refresh list
                is Result.Error -> {
                    // Handle error
                }
            }
        }
    }

    // Real-time updates
    fun observeUserUpdates(userId: String) {
        viewModelScope.launch {
            repository.observeUserUpdates(userId).collect { user ->
                // Update UI with real-time data
            }
        }
    }
}
```

**6. Fragments with Type-Safe Arguments:**
```graphql
# UserFragment.graphql
fragment UserFields on User {
    id
    name
    email
    avatar
}

# GetUsers.graphql (using fragment)
query GetUsers {
    users {
        ...UserFields
    }
}
```

**Benefits of Apollo Client:**
-  Type-safe code generation
-  Automatic caching
-  Optimistic updates
-  Subscription support
-  Error handling
-  Pagination support

---

## **Android Implementation**

### Q13. How do you implement Retrofit for API calls in Android?

**Answer:**

**Complete Retrofit Implementation:**

**1. Dependencies:**
```groovy
// build.gradle (app)
dependencies {
    // Retrofit
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")

    // OkHttp
    implementation("com.squareup.okhttp3:okhttp:4.11.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.11.0")

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
}
```

**2. Data Models:**
```kotlin
data class User(
    @SerializedName("id") val id: Int,
    @SerializedName("name") val name: String,
    @SerializedName("email") val email: String,
    @SerializedName("avatar_url") val avatarUrl: String?,
    @SerializedName("created_at") val createdAt: String
)

data class CreateUserRequest(
    val name: String,
    val email: String,
    val password: String
)

data class UpdateUserRequest(
    val name: String?,
    val email: String?
)

data class ApiResponse<T>(
    val success: Boolean,
    val data: T?,
    val message: String?
)

data class PaginatedResponse<T>(
    val data: List<T>,
    val page: Int,
    val total_pages: Int,
    val total_items: Int
)
```

**3. API Service Interface:**
```kotlin
interface ApiService {

    // GET requests
    @GET("users")
    suspend fun getUsers(): List<User>

    @GET("users")
    suspend fun getUsersPaginated(
        @Query("page") page: Int,
        @Query("limit") limit: Int = 20
    ): PaginatedResponse<User>

    @GET("users/{id}")
    suspend fun getUser(@Path("id") userId: Int): User

    @GET("users/search")
    suspend fun searchUsers(
        @Query("q") query: String,
        @Query("page") page: Int = 1
    ): List<User>

    // POST requests
    @POST("users")
    suspend fun createUser(@Body request: CreateUserRequest): User

    @FormUrlEncoded
    @POST("auth/login")
    suspend fun login(
        @Field("email") email: String,
        @Field("password") password: String
    ): AuthResponse

    // PUT request
    @PUT("users/{id}")
    suspend fun updateUser(
        @Path("id") userId: Int,
        @Body request: UpdateUserRequest
    ): User

    // PATCH request
    @PATCH("users/{id}")
    suspend fun patchUser(
        @Path("id") userId: Int,
        @Body updates: Map<String, Any>
    ): User

    // DELETE request
    @DELETE("users/{id}")
    suspend fun deleteUser(@Path("id") userId: Int): Response<Unit>

    // Multipart upload
    @Multipart
    @POST("users/{id}/avatar")
    suspend fun uploadAvatar(
        @Path("id") userId: Int,
        @Part avatar: MultipartBody.Part
    ): User

    // Headers
    @Headers("Accept: application/json")
    @GET("users/profile")
    suspend fun getProfile(): User

    // Dynamic headers
    @GET("users/profile")
    suspend fun getProfile(@Header("Authorization") token: String): User

    // URL with base URL override
    @GET
    suspend fun getUserFromUrl(@Url url: String): User
}
```

**4. Network Module with Hilt:**
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    private const val BASE_URL = "https://api.example.com/v1/"
    private const val TIMEOUT = 30L

    @Provides
    @Singleton
    fun provideLoggingInterceptor(): HttpLoggingInterceptor {
        return HttpLoggingInterceptor().apply {
            level = if (BuildConfig.DEBUG) {
                HttpLoggingInterceptor.Level.BODY
            } else {
                HttpLoggingInterceptor.Level.NONE
            }
        }
    }

    @Provides
    @Singleton
    fun provideAuthInterceptor(tokenManager: TokenManager): Interceptor {
        return Interceptor { chain ->
            val request = chain.request()
            val token = tokenManager.getAccessToken()

            val newRequest = if (token != null) {
                request.newBuilder()
                    .addHeader("Authorization", "Bearer $token")
                    .addHeader("Accept", "application/json")
                    .build()
            } else {
                request
            }

            chain.proceed(newRequest)
        }
    }

    @Provides
    @Singleton
    fun provideOkHttpClient(
        loggingInterceptor: HttpLoggingInterceptor,
        authInterceptor: Interceptor,
        tokenAuthenticator: TokenAuthenticator
    ): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .addInterceptor(loggingInterceptor)
            .authenticator(tokenAuthenticator)
            .connectTimeout(TIMEOUT, TimeUnit.SECONDS)
            .readTimeout(TIMEOUT, TimeUnit.SECONDS)
            .writeTimeout(TIMEOUT, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideGson(): Gson {
        return GsonBuilder()
            .setLenient()
            .setDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'")
            .create()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient, gson: Gson): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build()
    }

    @Provides
    @Singleton
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}
```

**5. Repository Implementation:**
```kotlin
class UserRepository @Inject constructor(
    private val apiService: ApiService,
    private val userDao: UserDao,
    private val networkChecker: NetworkChecker
) {

    suspend fun getUsers(forceRefresh: Boolean = false): Result<List<User>> {
        return try {
            if (networkChecker.isConnected() || forceRefresh) {
                val users = apiService.getUsers()
                // Cache in database
                userDao.insertAll(users)
                Result.Success(users)
            } else {
                // Load from cache
                val cached = userDao.getAllUsers()
                if (cached.isNotEmpty()) {
                    Result.Success(cached)
                } else {
                    Result.Error(Exception("No internet connection"))
                }
            }
        } catch (e: HttpException) {
            handleHttpException(e)
        } catch (e: IOException) {
            Result.Error(Exception("Network error: ${e.message}"))
        } catch (e: Exception) {
            Result.Error(e)
        }
    }

    suspend fun createUser(name: String, email: String, password: String): Result<User> {
        return try {
            val request = CreateUserRequest(name, email, password)
            val user = apiService.createUser(request)
            userDao.insert(user)
            Result.Success(user)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }

    suspend fun uploadAvatar(userId: Int, imageUri: Uri, context: Context): Result<User> {
        return try {
            val file = getFileFromUri(context, imageUri)
            val requestFile = file.asRequestBody("image/*".toMediaType())
            val body = MultipartBody.Part.createFormData("avatar", file.name, requestFile)

            val user = apiService.uploadAvatar(userId, body)
            Result.Success(user)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }

    private fun handleHttpException(e: HttpException): Result.Error {
        return when (e.code()) {
            401 -> Result.Error(Exception("Unauthorized"))
            403 -> Result.Error(Exception("Forbidden"))
            404 -> Result.Error(Exception("Not found"))
            422 -> {
                val errorBody = e.response()?.errorBody()?.string()
                val errorMessage = parseValidationErrors(errorBody)
                Result.Error(Exception(errorMessage))
            }
            in 500..599 -> Result.Error(Exception("Server error"))
            else -> Result.Error(Exception("HTTP ${e.code()}: ${e.message()}"))
        }
    }
}
```

**6. ViewModel:**
```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _users = MutableStateFlow<UiState<List<User>>>(UiState.Loading)
    val users: StateFlow<UiState<List<User>>> = _users.asStateFlow()

    init {
        loadUsers()
    }

    fun loadUsers(forceRefresh: Boolean = false) {
        viewModelScope.launch {
            _users.value = UiState.Loading
            when (val result = repository.getUsers(forceRefresh)) {
                is Result.Success -> _users.value = UiState.Success(result.data)
                is Result.Error -> _users.value = UiState.Error(result.exception.message ?: "Error")
            }
        }
    }

    fun createUser(name: String, email: String, password: String) {
        viewModelScope.launch {
            when (repository.createUser(name, email, password)) {
                is Result.Success -> loadUsers(forceRefresh = true)
                is Result.Error -> {
                    // Handle error
                }
            }
        }
    }
}
```

---

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

---

## **Performance & Optimization**

### Q15. How do you optimize API calls and reduce network usage?

**Answer:**

**1. Caching Strategy:**
```kotlin
// OkHttp Cache
val cacheSize = 10 * 1024 * 1024 // 10 MB
val cache = Cache(context.cacheDir, cacheSize.toLong())

val client = OkHttpClient.Builder()
    .cache(cache)
    .addNetworkInterceptor(CacheInterceptor())
    .build()

class CacheInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()

        // Add cache control headers
        val newRequest = request.newBuilder()
            .header("Cache-Control", "public, max-age=3600")
            .build()

        return chain.proceed(newRequest)
    }
}

// Retrofit with cache
@Headers("Cache-Control: max-age=3600") // Cache for 1 hour
@GET("users")
suspend fun getUsers(): List<User>
```

**2. Request Debouncing (Search):**
```kotlin
@HiltViewModel
class SearchViewModel @Inject constructor(
    private val repository: SearchRepository
) : ViewModel() {

    private val searchQuery = MutableStateFlow("")

    val searchResults: StateFlow<List<SearchResult>> = searchQuery
        .debounce(300) // Wait 300ms after user stops typing
        .distinctUntilChanged() // Only if query changed
        .filter { it.length >= 3 } // Min 3 characters
        .flatMapLatest { query ->
            flow {
                emit(repository.search(query))
            }
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    fun onSearchQueryChanged(query: String) {
        searchQuery.value = query
    }
}
```

**3. Pagination:**
```kotlin
// Paging 3 implementation
class UserPagingSource(
    private val apiService: ApiService
) : PagingSource<Int, User>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, User> {
        return try {
            val page = params.key ?: 1
            val response = apiService.getUsersPaginated(page, params.loadSize)

            LoadResult.Page(
                data = response.data,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (response.data.isEmpty()) null else page + 1
            )
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, User>): Int? {
        return state.anchorPosition?.let { position ->
            state.closestPageToPosition(position)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(position)?.nextKey?.minus(1)
        }
    }
}

// Repository
class UserRepository @Inject constructor(
    private val apiService: ApiService
) {
    fun getUsersPaged(): Flow<PagingData<User>> {
        return Pager(
            config = PagingConfig(
                pageSize = 20,
                enablePlaceholders = false,
                prefetchDistance = 3
            ),
            pagingSourceFactory = { UserPagingSource(apiService) }
        ).flow
    }
}

// ViewModel
@HiltViewModel
class UserViewModel @Inject constructor(
    repository: UserRepository
) : ViewModel() {

    val users: Flow<PagingData<User>> = repository.getUsersPaged()
        .cachedIn(viewModelScope)
}

// UI
@Composable
fun UserListScreen(viewModel: UserViewModel = hiltViewModel()) {
    val users = viewModel.users.collectAsLazyPagingItems()

    LazyColumn {
        items(users.itemCount) { index ->
            users[index]?.let { user ->
                UserItem(user = user)
            }
        }

        when (users.loadState.append) {
            is LoadState.Loading -> {
                item { LoadingItem() }
            }
            is LoadState.Error -> {
                item { ErrorItem { users.retry() } }
            }
            else -> {}
        }
    }
}
```

**4. Image Loading Optimization:**
```kotlin
// Using Coil
@Composable
fun UserAvatar(avatarUrl: String) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(avatarUrl)
            .crossfade(true)
            .memoryCachePolicy(CachePolicy.ENABLED)
            .diskCachePolicy(CachePolicy.ENABLED)
            .size(Size.ORIGINAL) // or specific size
            .build(),
        contentDescription = "Avatar",
        modifier = Modifier.size(48.dp)
    )
}

// Preload images
val imageLoader = ImageLoader(context)
viewModelScope.launch {
    users.forEach { user ->
        val request = ImageRequest.Builder(context)
            .data(user.avatarUrl)
            .build()
        imageLoader.enqueue(request)
    }
}
```

**5. Request Batching:**
```kotlin
// Instead of multiple requests
val user1 = apiService.getUser(1)
val user2 = apiService.getUser(2)
val user3 = apiService.getUser(3)

// Use batch endpoint
@POST("users/batch")
suspend fun getUsersBatch(@Body ids: List<Int>): List<User>

val users = apiService.getUsersBatch(listOf(1, 2, 3))
```

**6. Compression:**
```kotlin
val client = OkHttpClient.Builder()
    .addInterceptor { chain ->
        val request = chain.request().newBuilder()
            .header("Accept-Encoding", "gzip")
            .build()
        chain.proceed(request)
    }
    .build()
```

**7. Connection Pooling:**
```kotlin
val client = OkHttpClient.Builder()
    .connectionPool(ConnectionPool(
        maxIdleConnections = 5,
        keepAliveDuration = 5,
        timeUnit = TimeUnit.MINUTES
    ))
    .build()
```

**8. Selective Field Fetching (GraphQL or REST with fields param):**
```kotlin
// GraphQL - request only needed fields
query GetUsers {
    users {
        id
        name
        # Don't fetch unnecessary fields like description, metadata, etc.
    }
}

// REST with fields parameter
@GET("users")
suspend fun getUsers(@Query("fields") fields: String = "id,name,email"): List<User>
```

---

## **Security Best Practices**

### Q16. What are security best practices for API integration in mobile apps?

**Answer:**

**1. Use HTTPS Only:**
```kotlin
// Network Security Config (res/xml/network_security_config.xml)
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>

// AndroidManifest.xml
<application
    android:networkSecurityConfig="@xml/network_security_config">
</application>
```

**2. Certificate Pinning:**
```kotlin
// Pin specific certificates
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .add("api.example.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=") // Backup pin
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()

// Get certificate hash:
// openssl s_client -servername api.example.com -connect api.example.com:443 | openssl x509 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64
```

**3. Don't Store Sensitive Data in Logs:**
```kotlin
// L Bad
Log.d("API", "Token: $token")
Log.d("API", "Password: $password")

//  Good - Remove in production
class DebugLoggingInterceptor : HttpLoggingInterceptor() {
    init {
        level = if (BuildConfig.DEBUG) {
            Level.BODY
        } else {
            Level.NONE
        }

        // Redact sensitive headers
        redactHeader("Authorization")
        redactHeader("Cookie")
        redactHeader("Set-Cookie")
    }
}
```

**4. Implement Request Signing:**
```kotlin
class RequestSigningInterceptor(private val apiSecret: String) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()
        val timestamp = System.currentTimeMillis().toString()

        // Create signature
        val signatureData = "${original.method}${original.url}$timestamp"
        val signature = createHmacSha256(signatureData, apiSecret)

        val signed = original.newBuilder()
            .header("X-Timestamp", timestamp)
            .header("X-Signature", signature)
            .build()

        return chain.proceed(signed)
    }

    private fun createHmacSha256(data: String, secret: String): String {
        val mac = Mac.getInstance("HmacSHA256")
        mac.init(SecretKeySpec(secret.toByteArray(), "HmacSHA256"))
        return Base64.encodeToString(mac.doFinal(data.toByteArray()), Base64.NO_WRAP)
    }
}
```

**5. Validate SSL Certificates:**
```kotlin
class SSLCertificateValidator {
    fun createSecureOkHttpClient(context: Context): OkHttpClient {
        try {
            // Load custom trust store if needed
            val trustManagerFactory = TrustManagerFactory.getInstance(
                TrustManagerFactory.getDefaultAlgorithm()
            )
            trustManagerFactory.init(null as KeyStore?)

            val sslContext = SSLContext.getInstance("TLS")
            sslContext.init(null, trustManagerFactory.trustManagers, SecureRandom())

            return OkHttpClient.Builder()
                .sslSocketFactory(
                    sslContext.socketFactory,
                    trustManagerFactory.trustManagers[0] as X509TrustManager
                )
                .build()
        } catch (e: Exception) {
            throw RuntimeException(e)
        }
    }
}
```

**6. Obfuscate API Keys:**
```kotlin
// L Never hardcode
const val API_KEY = "sk_live_123456789"

//  Use BuildConfig (still visible in APK)
buildConfigField("String", "API_KEY", "\"${project.properties["API_KEY"]}\"")
val apiKey = BuildConfig.API_KEY

//  Better: Use NDK to hide keys
external fun getApiKey(): String

// C++ implementation
extern "C" JNIEXPORT jstring JNICALL
Java_com_example_NativeLib_getApiKey(JNIEnv* env, jobject) {
    return env->NewStringUTF("your_api_key_here");
}
```

**7. Implement Rate Limiting on Client:**
```kotlin
class RateLimitInterceptor(
    private val maxRequests: Int = 10,
    private val windowMs: Long = 1000L
) : Interceptor {

    private val timestamps = mutableListOf<Long>()

    @Synchronized
    override fun intercept(chain: Interceptor.Chain): Response {
        val now = System.currentTimeMillis()

        // Remove old timestamps
        timestamps.removeAll { now - it > windowMs }

        if (timestamps.size >= maxRequests) {
            val oldestRequest = timestamps.first()
            val waitTime = windowMs - (now - oldestRequest)
            if (waitTime > 0) {
                Thread.sleep(waitTime)
            }
        }

        timestamps.add(now)
        return chain.proceed(chain.request())
    }
}
```

**8. Validate Response Data:**
```kotlin
fun validateUser(user: User): Result<User> {
    return when {
        user.id <= 0 -> Result.Error(Exception("Invalid user ID"))
        user.email.isBlank() -> Result.Error(Exception("Email is required"))
        !Patterns.EMAIL_ADDRESS.matcher(user.email).matches() ->
            Result.Error(Exception("Invalid email format"))
        else -> Result.Success(user)
    }
}
```

**9. Use ProGuard/R8:**
```groovy
// build.gradle
buildTypes {
    release {
        minifyEnabled true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
}
```

**10. Secure Data in Transit:**
```kotlin
// Enforce TLS 1.2+
val spec = ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
    .tlsVersions(TlsVersion.TLS_1_2, TlsVersion.TLS_1_3)
    .cipherSuites(
        CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
        CipherSuite.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
        CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        CipherSuite.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    )
    .build()

val client = OkHttpClient.Builder()
    .connectionSpecs(listOf(spec))
    .build()
```

---

## **Testing APIs**

### Q17. How do you test API calls in Android?

**Answer:**

**1. Unit Tests with MockWebServer:**
```kotlin
class UserRepositoryTest {

    private lateinit var mockWebServer: MockWebServer
    private lateinit var apiService: ApiService
    private lateinit var repository: UserRepository

    @Before
    fun setup() {
        mockWebServer = MockWebServer()
        mockWebServer.start()

        val retrofit = Retrofit.Builder()
            .baseUrl(mockWebServer.url("/"))
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        apiService = retrofit.create(ApiService::class.java)
        repository = UserRepository(apiService)
    }

    @After
    fun teardown() {
        mockWebServer.shutdown()
    }

    @Test
    fun `getUsers should return list of users`() = runTest {
        // Given
        val mockResponse = """
            [
                {"id": 1, "name": "John Doe", "email": "john@example.com"},
                {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
            ]
        """.trimIndent()

        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setBody(mockResponse)
        )

        // When
        val result = repository.getUsers()

        // Then
        assertThat(result).isInstanceOf(Result.Success::class.java)
        val users = (result as Result.Success).data
        assertThat(users).hasSize(2)
        assertThat(users[0].name).isEqualTo("John Doe")

        // Verify request
        val request = mockWebServer.takeRequest()
        assertThat(request.path).isEqualTo("/users")
        assertThat(request.method).isEqualTo("GET")
    }

    @Test
    fun `getUsers should return error on network failure`() = runTest {
        // Given
        mockWebServer.enqueue(
            MockResponse()
                .setResponseCode(500)
                .setBody("Internal Server Error")
        )

        // When
        val result = repository.getUsers()

        // Then
        assertThat(result).isInstanceOf(Result.Error::class.java)
        val error = (result as Result.Error).error
        assertThat(error).isInstanceOf(ApiError.ServerError::class.java)
    }

    @Test
    fun `getUsers should return unauthorized error`() = runTest {
        // Given
        mockWebServer.enqueue(
            MockResponse().setResponseCode(401)
        )

        // When
        val result = repository.getUsers()

        // Then
        assertThat(result).isInstanceOf(Result.Error::class.java)
        assertThat((result as Result.Error).error).isInstanceOf(ApiError.Unauthorized::class.java)
    }
}
```

**2. Testing with Fake Repository:**
```kotlin
class FakeUserRepository : UserRepository {
    private val users = mutableListOf<User>()
    var shouldReturnError = false

    override suspend fun getUsers(): Result<List<User>> {
        return if (shouldReturnError) {
            Result.Error(ApiError.ServerError(500, "Test error"))
        } else {
            Result.Success(users.toList())
        }
    }

    override suspend fun createUser(request: CreateUserRequest): Result<User> {
        val user = User(
            id = users.size + 1,
            name = request.name,
            email = request.email,
            avatarUrl = null,
            createdAt = ""
        )
        users.add(user)
        return Result.Success(user)
    }

    fun addUser(user: User) {
        users.add(user)
    }
}

// ViewModel test
class UserViewModelTest {

    private lateinit var fakeRepository: FakeUserRepository
    private lateinit var viewModel: UserViewModel

    @Before
    fun setup() {
        fakeRepository = FakeUserRepository()
        viewModel = UserViewModel(fakeRepository)
    }

    @Test
    fun `loadUsers should update state to success`() = runTest {
        // Given
        fakeRepository.addUser(User(1, "John", "john@example.com", null, ""))

        // When
        viewModel.loadUsers()
        advanceUntilIdle()

        // Then
        val state = viewModel.uiState.value
        assertThat(state).isInstanceOf(UserViewModel.UiState.Success::class.java)
        assertThat((state as UserViewModel.UiState.Success).users).hasSize(1)
    }

    @Test
    fun `loadUsers should update state to error on failure`() = runTest {
        // Given
        fakeRepository.shouldReturnError = true

        // When
        viewModel.loadUsers()
        advanceUntilIdle()

        // Then
        assertThat(viewModel.uiState.value).isInstanceOf(UserViewModel.UiState.Error::class.java)
    }
}
```

**3. Integration Tests:**
```kotlin
@RunWith(AndroidJUnit4::class)
class UserApiIntegrationTest {

    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private lateinit var apiService: ApiService

    @Before
    fun setup() {
        val okHttpClient = OkHttpClient.Builder()
            .addInterceptor(MockInterceptor())
            .build()

        val retrofit = Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        apiService = retrofit.create(ApiService::class.java)
    }

    @Test
    fun testFullUserFlow() = runTest {
        // Create user
        val createRequest = CreateUserRequest("John", "john@example.com", "password123")
        val createdUser = apiService.createUser(createRequest)
        assertThat(createdUser.name).isEqualTo("John")

        // Get user
        val user = apiService.getUser(createdUser.id)
        assertThat(user.id).isEqualTo(createdUser.id)

        // Update user
        val updateRequest = UpdateUserRequest(name = "John Updated", email = null)
        val updatedUser = apiService.updateUser(user.id, updateRequest)
        assertThat(updatedUser.name).isEqualTo("John Updated")

        // Delete user
        val deleteResponse = apiService.deleteUser(user.id)
        assertThat(deleteResponse.code()).isEqualTo(204)
    }
}
```

**4. UI Tests with Hilt:**
```kotlin
@HiltAndroidTest
@RunWith(AndroidJUnit4::class)
class UserListScreenTest {

    @get:Rule(order = 0)
    val hiltRule = HiltAndroidRule(this)

    @get:Rule(order = 1)
    val composeRule = createAndroidComposeRule<MainActivity>()

    @BindValue
    @JvmField
    val repository: UserRepository = FakeUserRepository()

    @Test
    fun displayUsers() {
        // Given
        (repository as FakeUserRepository).addUser(
            User(1, "John Doe", "john@example.com", null, "")
        )

        // When
        composeRule.setContent {
            UserListScreen()
        }

        // Then
        composeRule.onNodeWithText("John Doe").assertIsDisplayed()
        composeRule.onNodeWithText("john@example.com").assertIsDisplayed()
    }
}
```

---

## **Summary**

**Essential API Concepts for Mobile Developers:**

**1. API Fundamentals:**
- Understanding REST principles
- HTTP methods and status codes
- Request/Response structure
- Authentication mechanisms

**2. Android Implementation:**
- Retrofit for REST APIs
- Apollo Client for GraphQL
- OkHttp for networking
- Coroutines for async operations

**3. Best Practices:**
- Error handling with sealed classes
- Repository pattern for data layer
- Caching strategies
- Pagination for large datasets
- Request debouncing for search

**4. Security:**
- HTTPS only
- Certificate pinning
- Secure token storage (EncryptedSharedPreferences)
- Request signing
- Data validation

**5. Performance:**
- Caching (HTTP, Memory, Disk)
- Image optimization
- Request batching
- Compression
- Connection pooling

**6. Testing:**
- Unit tests with MockWebServer
- Fake repositories
- Integration tests
- UI tests with Hilt

**Interview Tips:**
1. Understand REST vs GraphQL trade-offs
2. Explain authentication flows (OAuth, JWT)
3. Discuss caching strategies
4. Show error handling patterns
5. Demonstrate security knowledge
6. Explain testing approaches
7. Discuss performance optimizations
8. Understand pagination techniques

**Common Mistakes to Avoid:**
- L Not handling network errors
- L Blocking main thread with API calls
- L Storing tokens in plain SharedPreferences
- L Not implementing retry logic
- L Over-fetching data
- L Not caching responses
- L Logging sensitive information
- L Not validating SSL certificates

**Resources:**
- Retrofit Documentation
- OkHttp Documentation
- Apollo GraphQL Documentation
- Android Network Security Config
- HTTP Status Codes Reference
- REST API Design Guidelines
