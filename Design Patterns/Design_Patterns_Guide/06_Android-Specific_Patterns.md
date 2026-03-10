## **Android-Specific Patterns**

### Q16. What is the Repository Pattern?

**Answer:**
Repository Pattern abstracts data sources and provides a clean API for data access.

**Implementation:**
```kotlin
// Data sources
interface UserRemoteDataSource {
    suspend fun getUsers(): List<User>
    suspend fun getUserById(id: Int): User
}

interface UserLocalDataSource {
    suspend fun getUsers(): List<User>
    suspend fun getUserById(id: Int): User?
    suspend fun insertUsers(users: List<User>)
    suspend fun deleteAll()
}

// Remote implementation
class UserRemoteDataSourceImpl(
    private val apiService: ApiService
) : UserRemoteDataSource {
    override suspend fun getUsers() = apiService.getUsers()
    override suspend fun getUserById(id: Int) = apiService.getUser(id)
}

// Local implementation
class UserLocalDataSourceImpl(
    private val userDao: UserDao
) : UserLocalDataSource {
    override suspend fun getUsers() = userDao.getAllUsers()
    override suspend fun getUserById(id: Int) = userDao.getUserById(id)
    override suspend fun insertUsers(users: List<User>) = userDao.insertAll(users)
    override suspend fun deleteAll() = userDao.deleteAll()
}

// Repository
class UserRepository(
    private val remoteDataSource: UserRemoteDataSource,
    private val localDataSource: UserLocalDataSource,
    private val networkChecker: NetworkChecker
) {
    suspend fun getUsers(forceRefresh: Boolean = false): Result<List<User>> {
        return try {
            if (networkChecker.isConnected() || forceRefresh) {
                // Fetch from network
                val users = remoteDataSource.getUsers()
                // Cache in database
                localDataSource.deleteAll()
                localDataSource.insertUsers(users)
                Result.Success(users)
            } else {
                // Load from cache
                val cachedUsers = localDataSource.getUsers()
                if (cachedUsers.isNotEmpty()) {
                    Result.Success(cachedUsers)
                } else {
                    Result.Error(Exception("No cached data"))
                }
            }
        } catch (e: Exception) {
            // Fallback to cache
            val cachedUsers = localDataSource.getUsers()
            if (cachedUsers.isNotEmpty()) {
                Result.Success(cachedUsers)
            } else {
                Result.Error(e)
            }
        }
    }

    suspend fun getUserById(id: Int): Result<User> {
        return try {
            // Try cache first
            localDataSource.getUserById(id)?.let {
                return Result.Success(it)
            }

            // Fetch from network
            val user = remoteDataSource.getUserById(id)
            localDataSource.insertUsers(listOf(user))
            Result.Success(user)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}

// Result sealed class
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Exception) : Result<Nothing>()
}
```

**With Hilt:**
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {
    @Provides
    @Singleton
    fun provideUserRepository(
        remoteDataSource: UserRemoteDataSource,
        localDataSource: UserLocalDataSource,
        networkChecker: NetworkChecker
    ): UserRepository {
        return UserRepository(remoteDataSource, localDataSource, networkChecker)
    }
}
```

**Benefits:**
- Centralized data access
- Abstraction from data sources
- Easy to test and mock
- Single source of truth

**When to use:**
- Multiple data sources
- Complex data operations
- Need caching strategy

---

### Q17. What is the ViewHolder Pattern?

**Answer:**
ViewHolder Pattern caches view references to improve RecyclerView performance.

**Implementation:**
```kotlin
data class User(val id: Int, val name: String, val email: String, val avatarUrl: String)

class UserAdapter(
    private val onItemClick: (User) -> Unit
) : ListAdapter<User, UserAdapter.UserViewHolder>(UserDiffCallback()) {

    inner class UserViewHolder(
        private val binding: ItemUserBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        init {
            binding.root.setOnClickListener {
                val position = bindingAdapterPosition
                if (position != RecyclerView.NO_POSITION) {
                    onItemClick(getItem(position))
                }
            }
        }

        fun bind(user: User) {
            binding.apply {
                tvName.text = user.name
                tvEmail.text = user.email

                Glide.with(ivAvatar)
                    .load(user.avatarUrl)
                    .placeholder(R.drawable.ic_placeholder)
                    .circleCrop()
                    .into(ivAvatar)
            }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): UserViewHolder {
        val binding = ItemUserBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return UserViewHolder(binding)
    }

    override fun onBindViewHolder(holder: UserViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    private class UserDiffCallback : DiffUtil.ItemCallback<User>() {
        override fun areItemsTheSame(oldItem: User, newItem: User): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: User, newItem: User): Boolean {
            return oldItem == newItem
        }
    }
}

// Usage
val adapter = UserAdapter { user ->
    Toast.makeText(context, "Clicked: ${user.name}", Toast.LENGTH_SHORT).show()
}

recyclerView.apply {
    layoutManager = LinearLayoutManager(context)
    this.adapter = adapter
    setHasFixedSize(true)
}

adapter.submitList(userList)
```

**Multiple ViewTypes:**
```kotlin
sealed class ListItem {
    data class Header(val title: String) : ListItem()
    data class UserItem(val user: User) : ListItem()
    data class Footer(val text: String) : ListItem()
}

class MultiTypeAdapter : ListAdapter<ListItem, RecyclerView.ViewHolder>(DiffCallback()) {

    inner class HeaderViewHolder(private val binding: ItemHeaderBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(header: ListItem.Header) {
            binding.tvHeader.text = header.title
        }
    }

    inner class UserViewHolder(private val binding: ItemUserBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(item: ListItem.UserItem) {
            binding.tvName.text = item.user.name
        }
    }

    inner class FooterViewHolder(private val binding: ItemFooterBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(footer: ListItem.Footer) {
            binding.tvFooter.text = footer.text
        }
    }

    override fun getItemViewType(position: Int): Int {
        return when (getItem(position)) {
            is ListItem.Header -> TYPE_HEADER
            is ListItem.UserItem -> TYPE_USER
            is ListItem.Footer -> TYPE_FOOTER
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        return when (viewType) {
            TYPE_HEADER -> HeaderViewHolder(
                ItemHeaderBinding.inflate(LayoutInflater.from(parent.context), parent, false)
            )
            TYPE_USER -> UserViewHolder(
                ItemUserBinding.inflate(LayoutInflater.from(parent.context), parent, false)
            )
            TYPE_FOOTER -> FooterViewHolder(
                ItemFooterBinding.inflate(LayoutInflater.from(parent.context), parent, false)
            )
            else -> throw IllegalArgumentException("Unknown view type")
        }
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        when (val item = getItem(position)) {
            is ListItem.Header -> (holder as HeaderViewHolder).bind(item)
            is ListItem.UserItem -> (holder as UserViewHolder).bind(item)
            is ListItem.Footer -> (holder as FooterViewHolder).bind(item)
        }
    }

    private class DiffCallback : DiffUtil.ItemCallback<ListItem>() {
        override fun areItemsTheSame(oldItem: ListItem, newItem: ListItem): Boolean {
            return oldItem == newItem
        }

        override fun areContentsTheSame(oldItem: ListItem, newItem: ListItem): Boolean {
            return oldItem == newItem
        }
    }

    companion object {
        private const val TYPE_HEADER = 0
        private const val TYPE_USER = 1
        private const val TYPE_FOOTER = 2
    }
}
```

**Benefits:**
- Improved performance (no findViewById)
- Cleaner code
- Efficient recycling

---

### Q18. What is the Service Locator Pattern?

**Answer:**
Service Locator provides a centralized registry for obtaining services/dependencies.

**Implementation:**
```kotlin
object ServiceLocator {
    private val services = mutableMapOf<Class<*>, Any>()

    fun <T : Any> registerService(serviceClass: Class<T>, service: T) {
        services[serviceClass] = service
    }

    @Suppress("UNCHECKED_CAST")
    fun <T : Any> getService(serviceClass: Class<T>): T {
        return services[serviceClass] as? T
            ?: throw IllegalStateException("Service ${serviceClass.name} not registered")
    }

    inline fun <reified T : Any> getService(): T {
        return getService(T::class.java)
    }
}

// Usage
// Register services
ServiceLocator.registerService(ApiService::class.java, apiService)
ServiceLocator.registerService(Database::class.java, database)

// Get services
val api = ServiceLocator.getService<ApiService>()
val db = ServiceLocator.getService<Database>()
```

**Android Example:**
```kotlin
class AppServiceLocator {
    private val apiService: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .build()
            .create(ApiService::class.java)
    }

    private var database: AppDatabase? = null

    fun getApiService(): ApiService = apiService

    fun getDatabase(context: Context): AppDatabase {
        return database ?: Room.databaseBuilder(
            context.applicationContext,
            AppDatabase::class.java,
            "app_database"
        ).build().also { database = it }
    }

    fun getUserRepository(context: Context): UserRepository {
        return UserRepository(
            getApiService(),
            getDatabase(context).userDao()
        )
    }
}

// In Application class
class MyApplication : Application() {
    val serviceLocator = AppServiceLocator()
}

// Usage in Activity/Fragment
val app = requireActivity().application as MyApplication
val repository = app.serviceLocator.getUserRepository(requireContext())
```

**Service Locator vs Dependency Injection:**

| Feature | Service Locator | DI (Hilt/Dagger) |
|---------|-----------------|------------------|
| **Dependencies** | Pulled actively | Pushed/Injected |
| **Testability** | Hard to mock | Easy to mock |
| **Compile-time safety** | No | Yes |
| **Boilerplate** | Less | More |
| **Recommended** | No | Yes |

**When to use:**
- Small projects
- Prototyping
- Legacy code (migrate to DI)
