# ⚖️ Load Balancing
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Distribute scale and ensuring fast response times.

![Load Balancing](https://img.shields.io/badge/Concept-Load_Balancing-blue?style=for-the-badge&logo=nginx&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Algorithms (Round Robin, etc.)](#load-balancing-algorithms)
- [2. Mobile Strategies (Sticky Sessions, Failover)](#mobile-implications)

---

### Q4. What is load balancing and how does it affect mobile apps?

**Answer:**

Load balancing distributes incoming traffic across servers to avoid overload.

**Load Balancing Architecture (simple):**
- Mobile Clients → Load Balancer → Backend Servers (S1, S2, S3)
- Backend Servers → Shared Database / Replicas

**Load Balancing Algorithms:**

```
1. Round Robin
   Request 1 → Server 1
   Request 2 → Server 2
   Request 3 → Server 3
   Request 4 → Server 1 (cycle repeats)

2. Least Connections
   Server 1: 10 connections  →    New request goes here
   Server 2: 15 connections
   Server 3: 20 connections

3. IP Hash
   Client IP → Hash → Server
   Same client always gets same server (sticky sessions)

4. Weighted Round Robin
   Server 1 (2x capacity): Gets 50% of requests
   Server 2 (1x capacity): Gets 25% of requests
   Server 3 (1x capacity): Gets 25% of requests
```

**Mobile Implications:**

**1. Session Management:**
```kotlin
// L Bad: Server-side sessions break with load balancing
class LoginViewModel {
    fun login(email: String, password: String) {
        // Server creates session, stores in memory
        apiService.login(email, password)
        // Next request might go to different server → session lost
    }
}

//   Good: Stateless authentication with tokens
class LoginViewModel @Inject constructor(
    private val apiService: ApiService,
    private val tokenManager: TokenManager
) : ViewModel() {
    fun login(email: String, password: String) {
        viewModelScope.launch {
            val response = apiService.login(email, password)

            // Store token locally
            tokenManager.saveToken(response.accessToken)
            tokenManager.saveRefreshToken(response.refreshToken)

            // Token sent with every request, works with any server
        }
    }
}

// All requests include token
class AuthInterceptor @Inject constructor(
    private val tokenManager: TokenManager
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val token = tokenManager.getAccessToken()
        val request = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer $token")
            .build()
        return chain.proceed(request)
    }
}
```

**2. Sticky Sessions (When Needed):**
```kotlin
// Use case: Real-time chat, WebSocket connections
class ChatWebSocketManager @Inject constructor(
    private val okHttpClient: OkHttpClient
) {
    private var webSocket: WebSocket? = null

    fun connect(chatRoomId: String) {
        // WebSocket needs to stay connected to same server
        val request = Request.Builder()
            .url("wss://chat.example.com/room/$chatRoomId")
            .build()

        webSocket = okHttpClient.newWebSocket(request, object : WebSocketListener() {
            override fun onMessage(webSocket: WebSocket, text: String) {
                handleMessage(text)
            }

            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                // Reconnect on connection loss
                reconnect(chatRoomId)
            }
        })
    }

    private fun reconnect(chatRoomId: String) {
        // May connect to different server, need to re-establish state
        delay(1000)
        connect(chatRoomId)

        // Re-sync messages
        syncMissedMessages(chatRoomId)
    }
}

// Load balancer configuration for sticky sessions:
/*
Load Balancer Config:
- Algorithm: IP Hash or Cookie-based
- Session Affinity: Enabled
- Health Checks: Active (remove failed servers)
*/
```

**3. Health Checks & Failover:**
```kotlin
// Mobile client should handle server failures gracefully
class ApiServiceWithFailover @Inject constructor(
    private val apiService: ApiService
) {
    suspend fun <T> executeWithFailover(
        block: suspend () -> T
    ): Result<T> {
        return retryPolicy.executeWithRetry(
            maxRetries = 3,
            shouldRetry = { exception ->
                // Retry on server errors (load balancer will route to healthy server)
                exception is IOException ||
                (exception is HttpException && exception.code() in 500..599)
            }
        ) {
            block()
        }
    }
}

// Usage
class UserRepository @Inject constructor(
    private val apiServiceWithFailover: ApiServiceWithFailover,
    private val apiService: ApiService
) {
    suspend fun getUser(userId: String): Result<User> {
        return apiServiceWithFailover.executeWithFailover {
            apiService.getUser(userId)
        }
    }
}
```

**4. Geographic Load Balancing:**
```
Global Users
      ↓
     ↓
                    ↓
   Global DNS         →    Routes based on user location
         ,          ↓
          ↓
        <     ↘
               ↓
    ↓    ↓    ↓
US Region  EU Region  Asia Region
                          ↓
    ↓         ↓          ↓
Load Balancer in each region
                          ↓
    ↓         ↓          ↓
Local Servers in each region
```

**Mobile Implementation:**
```kotlin
class ApiEndpointSelector @Inject constructor(
    private val locationProvider: LocationProvider,
    private val preferences: Preferences
) {
    fun getOptimalEndpoint(): String {
        // Get user's region
        val region = locationProvider.getCurrentRegion()

        // Use closest server
        return when (region) {
            Region.NORTH_AMERICA -> "https://api-us.example.com"
            Region.EUROPE -> "https://api-eu.example.com"
            Region.ASIA -> "https://api-asia.example.com"
            else -> "https://api.example.com"  // Default
        }
    }

    // Or measure latency and cache result
    suspend fun getMeasuredOptimalEndpoint(): String {
        val cachedEndpoint = preferences.getString("optimal_endpoint")
        if (cachedEndpoint != null) return cachedEndpoint

        val endpoints = listOf(
            "https://api-us.example.com",
            "https://api-eu.example.com",
            "https://api-asia.example.com"
        )

        val optimal = endpoints.minByOrNull { endpoint ->
            measureLatency(endpoint)
        } ?: endpoints.first()

        preferences.putString("optimal_endpoint", optimal)
        return optimal
    }
}

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideRetrofit(
        okHttpClient: OkHttpClient,
        endpointSelector: ApiEndpointSelector
    ): Retrofit {
        return Retrofit.Builder()
            .baseUrl(endpointSelector.getOptimalEndpoint())
            .client(okHttpClient)
            .build()
    }
}
```

**5. Load Balancer Awareness in Mobile:**
```kotlin
// Add request ID for debugging across servers
class RequestIdInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val requestId = UUID.randomUUID().toString()

        val request = chain.request().newBuilder()
            .addHeader("X-Request-ID", requestId)
            .build()

        val response = chain.proceed(request)

        // Log which server handled request
        val serverId = response.headers["X-Server-ID"]
        Log.d("API", "Request $requestId handled by server $serverId")

        return response

    }
}

// Track server performance
class ServerPerformanceTracker @Inject constructor(
    private val analytics: Analytics
) {
    fun trackResponse(serverId: String?, duration: Long, success: Boolean) {
        analytics.logEvent("api_response") {
            param("server_id", serverId ?: "unknown")
            param("duration_ms", duration)
            param("success", success)
        }

        // Identify problematic servers
        if (duration > 3000) {
            analytics.logEvent("slow_server") {
                param("server_id", serverId ?: "unknown")
                param("duration_ms", duration)
            }
        }
    }
}
```
