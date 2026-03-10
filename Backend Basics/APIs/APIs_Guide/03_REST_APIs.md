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
Client � Load Balancer � API Gateway � Auth Service � Business Logic � Database
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
