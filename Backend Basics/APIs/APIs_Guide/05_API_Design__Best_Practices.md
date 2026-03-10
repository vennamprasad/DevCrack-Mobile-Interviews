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
- � **Header**: Clean URLs but less visible
- � **Content Negotiation**: Complex but RESTful

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
