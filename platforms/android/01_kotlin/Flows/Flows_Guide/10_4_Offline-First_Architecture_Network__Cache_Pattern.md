## **4. Offline-First Architecture (Network + Cache Pattern)**

### **Problem**: Show cached data immediately, update from network in background

```kotlin
class ArticleRepository(
    private val api: ArticleApi,
    private val database: ArticleDao
) {
    // Single source of truth pattern
    fun getArticle(id: String): Flow<Resource<Article>> = flow {
        // First, emit cached data
        emit(Resource.Loading(data = database.getArticle(id)))

        try {
            // Fetch fresh data from network
            val freshArticle = api.fetchArticle(id)

            // Update cache
            database.insertArticle(freshArticle)

            // Emit fresh data (database will emit through Room's Flow)
        } catch (e: IOException) {
            // Network error - emit error but keep showing cached data
            emit(Resource.Error(
                message = "Network error",
                data = database.getArticle(id)
            ))
        }
    }.flatMapLatest {
        // Observe database for any updates
        database.observeArticle(id).map { article ->
            Resource.Success(article)
        }
    }

    // For list of articles
    fun getArticles(): Flow<Resource<List<Article>>> = flow {
        emit(Resource.Loading(data = database.getAllArticles()))

        try {
            val freshArticles = api.fetchArticles()
            database.insertArticles(freshArticles)
        } catch (e: IOException) {
            emit(Resource.Error(
                message = "Cannot fetch fresh data",
                data = database.getAllArticles()
            ))
        }
    }.flatMapLatest {
        database.observeAllArticles().map { articles ->
            Resource.Success(articles)
        }
    }
}

sealed class Resource<T>(
    val data: T? = null,
    val message: String? = null
) {
    class Success<T>(data: T) : Resource<T>(data)
    class Loading<T>(data: T? = null) : Resource<T>(data)
    class Error<T>(message: String, data: T? = null) : Resource<T>(data, message)
}

// Usage in ViewModel
class ArticleViewModel : ViewModel() {
    fun loadArticle(id: String) {
        viewModelScope.launch {
            repository.getArticle(id).collect { resource ->
                when (resource) {
                    is Resource.Loading -> {
                        _uiState.value = UiState.Loading(resource.data)
                    }
                    is Resource.Success -> {
                        _uiState.value = UiState.Success(resource.data!!)
                    }
                    is Resource.Error -> {
                        _uiState.value = UiState.Error(
                            message = resource.message!!,
                            cachedData = resource.data
                        )
                    }
                }
            }
        }
    }
}
```
