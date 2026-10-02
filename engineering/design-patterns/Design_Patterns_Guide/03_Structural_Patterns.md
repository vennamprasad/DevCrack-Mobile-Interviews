## **Structural Patterns**

### Q5. What is the Adapter Pattern?

**Answer:**
Adapter Pattern allows incompatible interfaces to work together by wrapping an object with a compatible interface.

**RecyclerView Adapter:**
```kotlin
data class User(val id: Int, val name: String, val email: String)

class UserAdapter(
    private val users: List<User>,
    private val onItemClick: (User) -> Unit
) : RecyclerView.Adapter<UserAdapter.UserViewHolder>() {

    inner class UserViewHolder(private val binding: ItemUserBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(user: User) {
            binding.apply {
                tvName.text = user.name
                tvEmail.text = user.email
                root.setOnClickListener { onItemClick(user) }
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
        holder.bind(users[position])
    }

    override fun getItemCount() = users.size
}

// Usage
val adapter = UserAdapter(userList) { user ->
    Toast.makeText(context, "Clicked: ${user.name}", Toast.LENGTH_SHORT).show()
}
recyclerView.adapter = adapter
```

**Interface Adapter:**
```kotlin
// Third-party library with incompatible interface
class ThirdPartyImageLoader {
    fun fetchImage(url: String): Bitmap { /* ... */ }
}

// Our application interface
interface ImageLoader {
    suspend fun loadImage(url: String): Bitmap
}

// Adapter
class ImageLoaderAdapter(
    private val thirdPartyLoader: ThirdPartyImageLoader
) : ImageLoader {
    override suspend fun loadImage(url: String): Bitmap {
        return withContext(Dispatchers.IO) {
            thirdPartyLoader.fetchImage(url)
        }
    }
}

// Usage
val imageLoader: ImageLoader = ImageLoaderAdapter(ThirdPartyImageLoader())
val bitmap = imageLoader.loadImage("https://example.com/image.jpg")
```

**Android Examples:**
- RecyclerView.Adapter
- ViewPager2 Adapter
- Array Adapter
- Cursor Adapter

**When to use:**
- Integrate third-party libraries
- Make legacy code work with new code
- RecyclerView/ListView data binding

---

### Q6. What is the Decorator Pattern?

**Answer:**
Decorator Pattern adds new functionality to objects dynamically without altering their structure.

**Implementation:**
```kotlin
interface Coffee {
    fun cost(): Double
    fun description(): String
}

class SimpleCoffee : Coffee {
    override fun cost() = 2.0
    override fun description() = "Simple Coffee"
}

abstract class CoffeeDecorator(
    private val coffee: Coffee
) : Coffee {
    override fun cost() = coffee.cost()
    override fun description() = coffee.description()
}

class MilkDecorator(coffee: Coffee) : CoffeeDecorator(coffee) {
    override fun cost() = super.cost() + 0.5
    override fun description() = super.description() + ", Milk"
}

class SugarDecorator(coffee: Coffee) : CoffeeDecorator(coffee) {
    override fun cost() = super.cost() + 0.2
    override fun description() = super.description() + ", Sugar"
}

// Usage
var coffee: Coffee = SimpleCoffee()
coffee = MilkDecorator(coffee)
coffee = SugarDecorator(coffee)
println("${coffee.description()} costs $${coffee.cost()}")
// Simple Coffee, Milk, Sugar costs $2.7
```

**Android Context Wrapper:**
```kotlin
class CustomContextWrapper(base: Context) : ContextWrapper(base) {
    override fun getResources(): Resources {
        val res = super.getResources()
        val config = Configuration(res.configuration)
        config.fontScale = 1.2f // Increase font size
        return createConfigurationContext(config).resources
    }
}

// Usage in Activity
override fun attachBaseContext(newBase: Context) {
    super.attachBaseContext(CustomContextWrapper(newBase))
}
```

**Interceptor Pattern (OkHttp):**
```kotlin
class LoggingInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        Log.d("API", "Request: ${request.url}")

        val response = chain.proceed(request)
        Log.d("API", "Response: ${response.code}")

        return response
    }
}

class AuthInterceptor(private val token: String) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer $token")
            .build()
        return chain.proceed(request)
    }
}

// Usage
val client = OkHttpClient.Builder()
    .addInterceptor(LoggingInterceptor())
    .addInterceptor(AuthInterceptor(token))
    .build()
```

**When to use:**
- Add functionality without modifying original class
- Runtime behavior modification
- Alternative to subclassing

---

### Q7. What is the Facade Pattern?

**Answer:**
Facade Pattern provides a simplified interface to a complex subsystem.

**Implementation:**
```kotlin
// Complex subsystem classes
class ApiService {
    suspend fun fetchData(): String { /* ... */ }
}

class DatabaseManager {
    suspend fun saveData(data: String) { /* ... */ }
    suspend fun getData(): String { /* ... */ }
}

class CacheManager {
    fun cacheData(data: String) { /* ... */ }
    fun getCachedData(): String? { /* ... */ }
}

class PreferencesManager {
    fun savePreference(key: String, value: String) { /* ... */ }
}

// Facade
class DataManagerFacade(
    private val apiService: ApiService,
    private val database: DatabaseManager,
    private val cache: CacheManager,
    private val preferences: PreferencesManager
) {
    suspend fun getUserData(userId: String): String {
        // Check cache first
        cache.getCachedData()?.let { return it }

        // Try database
        val dbData = database.getData()
        if (dbData.isNotEmpty()) {
            cache.cacheData(dbData)
            return dbData
        }

        // Fetch from API
        val apiData = apiService.fetchData()
        database.saveData(apiData)
        cache.cacheData(apiData)
        preferences.savePreference("last_sync", System.currentTimeMillis().toString())

        return apiData
    }
}

// Usage (simple interface)
val facade = DataManagerFacade(api, db, cache, prefs)
val data = facade.getUserData("123")
```

**Real Android Example - Media Player Facade:**
```kotlin
class MediaPlayerFacade(private val context: Context) {
    private var mediaPlayer: MediaPlayer? = null
    private var isPrepared = false

    fun playAudio(url: String) {
        stop()
        mediaPlayer = MediaPlayer().apply {
            setDataSource(url)
            setOnPreparedListener {
                isPrepared = true
                start()
            }
            setOnErrorListener { _, _, _ ->
                Log.e("MediaPlayer", "Error playing audio")
                true
            }
            prepareAsync()
        }
    }

    fun pause() {
        if (isPrepared) {
            mediaPlayer?.pause()
        }
    }

    fun resume() {
        if (isPrepared) {
            mediaPlayer?.start()
        }
    }

    fun stop() {
        mediaPlayer?.apply {
            if (isPlaying) stop()
            release()
        }
        mediaPlayer = null
        isPrepared = false
    }

    fun seekTo(position: Int) {
        if (isPrepared) {
            mediaPlayer?.seekTo(position)
        }
    }
}

// Usage
val player = MediaPlayerFacade(context)
player.playAudio("https://example.com/audio.mp3")
player.pause()
player.resume()
```

**When to use:**
- Simplify complex APIs
- Provide high-level interface
- Reduce dependencies on subsystems

---

### Q8. What is the Proxy Pattern?

**Answer:**
Proxy Pattern provides a placeholder for another object to control access to it.

**Virtual Proxy (Lazy Loading):**
```kotlin
interface Image {
    fun display()
}

class RealImage(private val filename: String) : Image {
    init {
        loadFromDisk()
    }

    private fun loadFromDisk() {
        println("Loading $filename from disk...")
        Thread.sleep(1000) // Simulate expensive operation
    }

    override fun display() {
        println("Displaying $filename")
    }
}

class ProxyImage(private val filename: String) : Image {
    private var realImage: RealImage? = null

    override fun display() {
        if (realImage == null) {
            realImage = RealImage(filename)
        }
        realImage?.display()
    }
}

// Usage
val image: Image = ProxyImage("photo.jpg")
// Image not loaded yet
image.display() // Now loads and displays
image.display() // Just displays (already loaded)
```

**Protection Proxy:**
```kotlin
interface UserManager {
    fun deleteUser(userId: Int)
    fun updateUser(userId: Int, data: UserData)
}

class RealUserManager : UserManager {
    override fun deleteUser(userId: Int) {
        println("User $userId deleted")
    }

    override fun updateUser(userId: Int, data: UserData) {
        println("User $userId updated")
    }
}

class UserManagerProxy(
    private val realManager: UserManager,
    private val currentUserRole: String
) : UserManager {
    override fun deleteUser(userId: Int) {
        if (currentUserRole == "ADMIN") {
            realManager.deleteUser(userId)
        } else {
            throw SecurityException("Only admins can delete users")
        }
    }

    override fun updateUser(userId: Int, data: UserData) {
        if (currentUserRole in listOf("ADMIN", "MODERATOR")) {
            realManager.updateUser(userId, data)
        } else {
            throw SecurityException("Insufficient permissions")
        }
    }
}
```

**Android - Glide as Proxy:**
```kotlin
// Glide acts as a proxy for image loading
Glide.with(context)
    .load(imageUrl)
    .placeholder(R.drawable.placeholder) // Show while loading
    .error(R.drawable.error) // Show on error
    .into(imageView)
```

**When to use:**
- Lazy loading of expensive objects
- Access control
- Remote proxy for network objects
- Caching proxy
