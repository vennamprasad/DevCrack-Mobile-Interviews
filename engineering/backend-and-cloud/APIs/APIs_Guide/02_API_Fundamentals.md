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
