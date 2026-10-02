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

// � Not recommended - credentials sent with every request
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
