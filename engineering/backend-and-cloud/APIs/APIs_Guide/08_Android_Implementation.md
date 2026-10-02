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
