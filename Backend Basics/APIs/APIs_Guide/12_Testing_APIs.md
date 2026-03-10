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
