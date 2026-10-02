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
