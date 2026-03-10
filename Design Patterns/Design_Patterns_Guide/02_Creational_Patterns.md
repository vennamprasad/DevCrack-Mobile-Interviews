## **Creational Patterns**

### Q1. What is the Singleton Pattern and how is it used in Android?

**Answer:**
Singleton ensures a class has only one instance and provides a global access point to it.

**Implementation in Kotlin:**
```kotlin
// Thread-safe Singleton
object DatabaseManager {
    private var database: Database? = null

    fun getDatabase(context: Context): Database {
        return database ?: synchronized(this) {
            database ?: Room.databaseBuilder(
                context.applicationContext,
                AppDatabase::class.java,
                "app_database"
            ).build().also { database = it }
        }
    }
}

// Usage
val db = DatabaseManager.getDatabase(context)
```

**Using Kotlin's object:**
```kotlin
object ApiClient {
    private val retrofit: Retrofit by lazy {
        Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val apiService: ApiService by lazy {
        retrofit.create(ApiService::class.java)
    }
}

// Usage
ApiClient.apiService.getUsers()
```

**Android Examples:**
- Application class (singleton per process)
- Retrofit instance
- Room Database instance
- Repository classes
- SharedPreferences wrapper

**Pros:**
- Controlled access to single instance
- Reduced memory footprint
- Lazy initialization
- Global access point

**Cons:**
- Global state (hard to test)
- Hidden dependencies
- Violates Single Responsibility Principle
- Threading issues if not careful

**When to use:**
- Database connections
- Network clients
- Logging systems
- Configuration managers

---

### Q2. What is the Factory Pattern?

**Answer:**
Factory Pattern provides an interface for creating objects without specifying their exact classes.

**Simple Factory:**
```kotlin
interface ViewHolder {
    fun bind(data: Any)
}

class TextViewHolder(view: View) : ViewHolder {
    override fun bind(data: Any) {
        // Bind text data
    }
}

class ImageViewHolder(view: View) : ViewHolder {
    override fun bind(data: Any) {
        // Bind image data
    }
}

class ViewHolderFactory {
    fun createViewHolder(viewType: Int, parent: ViewGroup): ViewHolder {
        return when (viewType) {
            VIEW_TYPE_TEXT -> {
                val view = LayoutInflater.from(parent.context)
                    .inflate(R.layout.item_text, parent, false)
                TextViewHolder(view)
            }
            VIEW_TYPE_IMAGE -> {
                val view = LayoutInflater.from(parent.context)
                    .inflate(R.layout.item_image, parent, false)
                ImageViewHolder(view)
            }
            else -> throw IllegalArgumentException("Unknown view type")
        }
    }

    companion object {
        const val VIEW_TYPE_TEXT = 0
        const val VIEW_TYPE_IMAGE = 1
    }
}
```

**Abstract Factory:**
```kotlin
interface UIFactory {
    fun createButton(): Button
    fun createTextView(): TextView
}

class MaterialUIFactory(private val context: Context) : UIFactory {
    override fun createButton(): Button {
        return Button(context).apply {
            // Material design styling
            setBackgroundColor(Color.BLUE)
        }
    }

    override fun createTextView(): TextView {
        return TextView(context).apply {
            // Material design styling
            textSize = 16f
        }
    }
}

class CustomUIFactory(private val context: Context) : UIFactory {
    override fun createButton(): Button {
        return Button(context).apply {
            // Custom styling
            setBackgroundColor(Color.GREEN)
        }
    }

    override fun createTextView(): TextView {
        return TextView(context).apply {
            // Custom styling
            textSize = 14f
        }
    }
}
```

**Android Examples:**
- LayoutInflater creates Views
- RecyclerView ViewHolder creation
- Fragment instantiation
- Intent creation

**When to use:**
- Creating related families of objects
- When exact type is determined at runtime
- To encapsulate object creation logic

---

### Q3. What is the Builder Pattern?

**Answer:**
Builder Pattern constructs complex objects step by step, allowing different representations.

**Implementation:**
```kotlin
data class User(
    val id: Int,
    val name: String,
    val email: String?,
    val phone: String?,
    val address: String?,
    val age: Int?
)

class UserBuilder {
    private var id: Int = 0
    private var name: String = ""
    private var email: String? = null
    private var phone: String? = null
    private var address: String? = null
    private var age: Int? = null

    fun id(id: Int) = apply { this.id = id }
    fun name(name: String) = apply { this.name = name }
    fun email(email: String) = apply { this.email = email }
    fun phone(phone: String) = apply { this.phone = phone }
    fun address(address: String) = apply { this.address = address }
    fun age(age: Int) = apply { this.age = age }

    fun build() = User(id, name, email, phone, address, age)
}

// Usage
val user = UserBuilder()
    .id(1)
    .name("John Doe")
    .email("john@example.com")
    .age(30)
    .build()
```

**Using Kotlin's apply/also:**
```kotlin
data class NetworkConfig(
    var baseUrl: String = "",
    var timeout: Long = 30,
    var retryCount: Int = 3,
    var enableLogging: Boolean = false
)

// Usage with apply
val config = NetworkConfig().apply {
    baseUrl = "https://api.example.com"
    timeout = 60
    enableLogging = true
}
```

**Android Examples:**
- AlertDialog.Builder
- Notification.Builder
- Intent building
- Retrofit.Builder
- OkHttpClient.Builder

```kotlin
// AlertDialog Builder
val dialog = AlertDialog.Builder(context)
    .setTitle("Confirmation")
    .setMessage("Are you sure?")
    .setPositiveButton("Yes") { _, _ -> }
    .setNegativeButton("No") { _, _ -> }
    .create()

// Notification Builder
val notification = NotificationCompat.Builder(context, CHANNEL_ID)
    .setContentTitle("New Message")
    .setContentText("You have a new message")
    .setSmallIcon(R.drawable.ic_notification)
    .setPriority(NotificationCompat.PRIORITY_HIGH)
    .build()
```

**When to use:**
- Objects with many optional parameters
- Step-by-step object construction
- Improving code readability

---

### Q4. What is Dependency Injection and how is it implemented?

**Answer:**
Dependency Injection is a design pattern where dependencies are provided to a class rather than the class creating them.

**Constructor Injection:**
```kotlin
class UserRepository(
    private val apiService: ApiService,
    private val database: UserDao
) {
    suspend fun getUser(id: Int): User {
        return try {
            val user = apiService.getUser(id)
            database.insert(user)
            user
        } catch (e: Exception) {
            database.getUser(id)
        }
    }
}

// Usage
val repository = UserRepository(apiService, database)
```

**Using Hilt (Recommended):**
```kotlin
// Module
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideApiService(): ApiService {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .build()
            .create(ApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }
}

// Repository with injection
@Singleton
class UserRepository @Inject constructor(
    private val apiService: ApiService,
    private val userDao: UserDao
) {
    // Implementation
}

// ViewModel with injection
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    // Implementation
}
```

**Manual DI (Poor man's DI):**
```kotlin
object ServiceLocator {
    private var apiService: ApiService? = null
    private var database: AppDatabase? = null

    fun provideApiService(): ApiService {
        return apiService ?: createApiService().also { apiService = it }
    }

    fun provideDatabase(context: Context): AppDatabase {
        return database ?: createDatabase(context).also { database = it }
    }

    private fun createApiService(): ApiService { /* ... */ }
    private fun createDatabase(context: Context): AppDatabase { /* ... */ }
}
```

**Benefits:**
- Loose coupling
- Easy testing (mock dependencies)
- Reusability
- Separation of concerns

**When to use:**
- Always! It's a best practice
- Complex dependency graphs
- Need for testability
