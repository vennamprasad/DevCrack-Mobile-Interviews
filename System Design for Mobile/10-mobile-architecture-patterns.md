# Part 2: Mobile-Specific Design
## Mobile Architecture Patterns

### Q11. What are the common mobile architecture patterns?

**Answer:**

Mobile architecture patterns help organize code for maintainability, testability, and scalability.

**Popular Patterns:**

```
1. MVC (Model-View-Controller) - Legacy, not recommended
2. MVP (Model-View-Presenter) - Better separation
3. MVVM (Model-View-ViewModel) - Recommended for Android
4. MVI (Model-View-Intent) - Unidirectional data flow
5. Clean Architecture - Layered, highly testable
```

**MVVM + Clean Architecture (Recommended):**

```kotlin
// Domain Layer - Business Logic
data class User(
    val id: String,
    val name: String,
    val email: String
)

interface UserRepository {
    suspend fun getUser(id: String): Result<User>
}

class GetUserUseCase @Inject constructor(
    private val repository: UserRepository
) {
    suspend operator fun invoke(userId: String): Result<User> {
        return repository.getUser(userId)
    }
}

// Data Layer - Data Sources
class UserRepositoryImpl @Inject constructor(
    private val remoteDataSource: UserRemoteDataSource,
    private val localDataSource: UserLocalDataSource
) : UserRepository {
    override suspend fun getUser(id: String): Result<User> {
        // Implementation details hidden from other layers
        return remoteDataSource.getUser(id)
            .also { localDataSource.cacheUser(it) }
    }
}

// Domain Layer - Business logic
class GetUserUseCase @Inject constructor(
    private val repository: UserRepository
) {
    suspend operator fun invoke(id: String): Result<User> {
        return repository.getUser(id)
    }
}

// Presentation Layer - ViewModel
@HiltViewModel
class UserViewModel @Inject constructor(
    private val getUserUseCase: GetUserUseCase
) : ViewModel() {
    fun loadUser(id: String) {
        viewModelScope.launch {
            when (val result = getUserUseCase(id)) {
                is Result.Success -> updateUi(result.data)
                is Result.Error -> showError(result.error)
            }
        }
    }
}
```

---

## Offline-First Design

### Q12. How do you design an offline-first mobile application?

**Answer:**

Offline-first means the app works without internet, syncing when connected.

**Strategy:**

```kotlin
class OfflineFirstRepository @Inject constructor(
    private val apiService: ApiService,
    private val database: PostDao,
    private val networkMonitor: NetworkMonitor
) {
    fun getPosts(): Flow<List<Post>> = flow {
        // 1. Emit cached data immediately (offline-first)
        val cached = database.getAllPosts().first()
        if (cached.isNotEmpty()) {
            emit(cached)
        }

        // 2. Fetch from network if online
        if (networkMonitor.isOnline()) {
            try {
                val fresh = apiService.getPosts()
                database.insertAll(fresh)
                emit(fresh)  // Emit fresh data
            } catch (e: Exception) {
                // Use cache on error
                if (cached.isEmpty()) throw e
            }
        }
    }

    suspend fun createPost(post: Post): Result<Post> {
        // Save locally immediately
        val localPost = post.copy(
            id = UUID.randomUUID().toString(),
            syncStatus = SyncStatus.PENDING
        )
        database.insert(localPost)

        // Try to sync if online
        if (networkMonitor.isOnline()) {
            return syncPost(localPost)
        }

        // Will sync later when online
        return Result.Success(localPost)
    }

    private suspend fun syncPost(post: Post): Result<Post> {
        return try {
            val serverPost = apiService.createPost(post)
            database.update(serverPost.copy(syncStatus = SyncStatus.SYNCED))
            Result.Success(serverPost)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}
```

---

