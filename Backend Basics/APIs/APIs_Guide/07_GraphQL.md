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
