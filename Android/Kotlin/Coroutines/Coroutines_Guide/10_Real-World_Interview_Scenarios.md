## **Real-World Interview Scenarios**

### **Scenario 1**: Multiple API calls for a screen
**Question**: Load user profile, posts, and comments for a social media app.

```kotlin
class ProfileViewModel(private val repository: ProfileRepository) : ViewModel() {
    private val _uiState = MutableStateFlow<ProfileUiState>(ProfileUiState.Loading)
    val uiState = _uiState.asStateFlow()

    fun loadProfile(userId: String) {
        viewModelScope.launch {
            _uiState.value = ProfileUiState.Loading

            try {
                // Parallel fetch for speed
                coroutineScope {
                    val userDeferred = async { repository.fetchUser(userId) }
                    val postsDeferred = async { repository.fetchPosts(userId) }
                    val followersDeferred = async { repository.fetchFollowers(userId) }

                    _uiState.value = ProfileUiState.Success(
                        user = userDeferred.await(),
                        posts = postsDeferred.await(),
                        followers = followersDeferred.await()
                    )
                }
            } catch (e: Exception) {
                _uiState.value = ProfileUiState.Error(e.message ?: "Unknown error")
            }
        }
    }
}
```

### **Scenario 2**: Handle cancellation during screen rotation
**Answer**: Use `viewModelScope` - it automatically survives rotation and cancels when ViewModel is cleared.

### **Scenario 3**: Implement pull-to-refresh with proper cancellation
```kotlin
class FeedViewModel : ViewModel() {
    private var refreshJob: Job? = null

    fun refresh() {
        refreshJob?.cancel()  // Cancel previous refresh
        refreshJob = viewModelScope.launch {
            try {
                _isRefreshing.value = true
                val fresh = repository.fetchLatestFeed()
                _feedData.value = fresh
            } finally {
                _isRefreshing.value = false
            }
        }
    }
}
```
