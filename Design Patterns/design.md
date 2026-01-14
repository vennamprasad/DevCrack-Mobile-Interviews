# ðŸŽ¨ Design Patterns for Mobile
> **Targeted for Senior Android Developers**
> **Note:** Creational, Structural, Behavioral patterns with Kotlin examples.

![Design Patterns](https://img.shields.io/badge/Architecture-Design_Patterns-orange?style=for-the-badge&logo=kotlin&logoColor=white)

---

## ðŸ“– Table of Contents
- [1. Creational Patterns](#creational-patterns)
- [2. Structural Patterns](#structural-patterns)
- [3. Behavioral Patterns](#behavioral-patterns)
- [4. Architectural Patterns](#architectural-patterns)
- [5. Android Specifics](#android-specific-patterns)

---

Design patterns are reusable solutions to commonly occurring problems in software design. They represent best practices evolved over time by experienced developers.

**Benefits:**
- Proven solutions to common problems
- Improved code readability and maintainability
- Facilitate communication among developers
- Speed up development process
- Reduce code complexity

**Categories:**
- **Creational**: Object creation mechanisms
- **Structural**: Object composition and relationships
- **Behavioral**: Object interaction and responsibility
- **Architectural**: High-level application structure

---

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

---

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

---

## **Behavioral Patterns**

### Q9. What is the Observer Pattern?

**Answer:**
Observer Pattern defines a one-to-many dependency where when one object changes state, all dependents are notified.

**Using LiveData:**
```kotlin
class UserViewModel : ViewModel() {
    private val _users = MutableLiveData<List<User>>()
    val users: LiveData<List<User>> = _users

    fun loadUsers() {
        viewModelScope.launch {
            val userList = repository.getUsers()
            _users.value = userList
        }
    }
}

// Observer (Activity/Fragment)
viewModel.users.observe(viewLifecycleOwner) { users ->
    // Update UI when users change
    adapter.submitList(users)
}
```

**Using Flow:**
```kotlin
class UserViewModel : ViewModel() {
    private val _users = MutableStateFlow<List<User>>(emptyList())
    val users: StateFlow<List<User>> = _users.asStateFlow()

    fun loadUsers() {
        viewModelScope.launch {
            repository.getUsers().collect { userList ->
                _users.value = userList
            }
        }
    }
}

// Observer
lifecycleScope.launch {
    viewModel.users.collect { users ->
        adapter.submitList(users)
    }
}
```

**Custom Observer Implementation:**
```kotlin
interface Observer<T> {
    fun onChanged(data: T)
}

class Observable<T> {
    private val observers = mutableListOf<Observer<T>>()
    private var data: T? = null

    fun addObserver(observer: Observer<T>) {
        observers.add(observer)
    }

    fun removeObserver(observer: Observer<T>) {
        observers.remove(observer)
    }

    fun setData(newData: T) {
        data = newData
        notifyObservers()
    }

    private fun notifyObservers() {
        data?.let { currentData ->
            observers.forEach { it.onChanged(currentData) }
        }
    }
}

// Usage
val userObservable = Observable<User>()

userObservable.addObserver(object : Observer<User> {
    override fun onChanged(data: User) {
        println("User changed: ${data.name}")
    }
})

userObservable.setData(User(1, "John"))
```

**Android Examples:**
- LiveData/MutableLiveData
- Flow/StateFlow
- RxJava Observable
- OnClickListener
- BroadcastReceiver

**When to use:**
- One-to-many relationships
- Loosely coupled communication
- Event handling systems

---

### Q10. What is the Strategy Pattern?

**Answer:**
Strategy Pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

**Implementation:**
```kotlin
// Strategy interface
interface PriceStrategy {
    fun calculatePrice(basePrice: Double): Double
}

class RegularPrice : PriceStrategy {
    override fun calculatePrice(basePrice: Double) = basePrice
}

class HappyHourPrice : PriceStrategy {
    override fun calculatePrice(basePrice: Double) = basePrice * 0.5
}

class MemberPrice : PriceStrategy {
    override fun calculatePrice(basePrice: Double) = basePrice * 0.9
}

// Context
class ShoppingCart(private var priceStrategy: PriceStrategy) {
    private val items = mutableListOf<Double>()

    fun addItem(price: Double) {
        items.add(price)
    }

    fun setPriceStrategy(strategy: PriceStrategy) {
        priceStrategy = strategy
    }

    fun calculateTotal(): Double {
        return items.sumOf { priceStrategy.calculatePrice(it) }
    }
}

// Usage
val cart = ShoppingCart(RegularPrice())
cart.addItem(100.0)
cart.addItem(50.0)
println("Regular: ${cart.calculateTotal()}") // 150.0

cart.setPriceStrategy(HappyHourPrice())
println("Happy Hour: ${cart.calculateTotal()}") // 75.0
```

**Android Sorting Example:**
```kotlin
interface SortStrategy {
    fun sort(users: List<User>): List<User>
}

class SortByName : SortStrategy {
    override fun sort(users: List<User>) = users.sortedBy { it.name }
}

class SortByAge : SortStrategy {
    override fun sort(users: List<User>) = users.sortedBy { it.age }
}

class SortByDate : SortStrategy {
    override fun sort(users: List<User>) = users.sortedBy { it.createdAt }
}

class UserListManager {
    private var sortStrategy: SortStrategy = SortByName()

    fun setSortStrategy(strategy: SortStrategy) {
        sortStrategy = strategy
    }

    fun getSortedUsers(users: List<User>): List<User> {
        return sortStrategy.sort(users)
    }
}

// Usage
val manager = UserListManager()
manager.setSortStrategy(SortByAge())
val sortedUsers = manager.getSortedUsers(userList)
```

**Navigation Strategy:**
```kotlin
interface NavigationStrategy {
    fun navigate(from: Fragment, to: Fragment)
}

class SlideNavigation : NavigationStrategy {
    override fun navigate(from: Fragment, to: Fragment) {
        from.parentFragmentManager.beginTransaction()
            .setCustomAnimations(R.anim.slide_in, R.anim.slide_out)
            .replace(R.id.container, to)
            .commit()
    }
}

class FadeNavigation : NavigationStrategy {
    override fun navigate(from: Fragment, to: Fragment) {
        from.parentFragmentManager.beginTransaction()
            .setCustomAnimations(R.anim.fade_in, R.anim.fade_out)
            .replace(R.id.container, to)
            .commit()
    }
}
```

**When to use:**
- Multiple algorithms for same task
- Runtime algorithm selection
- Avoid conditional statements

---

### Q11. What is the Command Pattern?

**Answer:**
Command Pattern encapsulates a request as an object, allowing parameterization and queuing of requests.

**Implementation:**
```kotlin
// Command interface
interface Command {
    fun execute()
    fun undo()
}

// Receiver
class TextEditor {
    private val text = StringBuilder()

    fun insertText(text: String) {
        this.text.append(text)
    }

    fun deleteText(length: Int) {
        val start = maxOf(0, text.length - length)
        text.delete(start, text.length)
    }

    fun getText() = text.toString()
}

// Concrete Commands
class InsertCommand(
    private val editor: TextEditor,
    private val text: String
) : Command {
    override fun execute() {
        editor.insertText(text)
    }

    override fun undo() {
        editor.deleteText(text.length)
    }
}

class DeleteCommand(
    private val editor: TextEditor,
    private val length: Int
) : Command {
    private var deletedText = ""

    override fun execute() {
        val current = editor.getText()
        deletedText = current.takeLast(length)
        editor.deleteText(length)
    }

    override fun undo() {
        editor.insertText(deletedText)
    }
}

// Invoker
class CommandManager {
    private val history = mutableListOf<Command>()
    private val undoStack = mutableListOf<Command>()

    fun executeCommand(command: Command) {
        command.execute()
        history.add(command)
        undoStack.clear()
    }

    fun undo() {
        if (history.isNotEmpty()) {
            val command = history.removeLast()
            command.undo()
            undoStack.add(command)
        }
    }

    fun redo() {
        if (undoStack.isNotEmpty()) {
            val command = undoStack.removeLast()
            command.execute()
            history.add(command)
        }
    }
}

// Usage
val editor = TextEditor()
val manager = CommandManager()

manager.executeCommand(InsertCommand(editor, "Hello "))
manager.executeCommand(InsertCommand(editor, "World"))
println(editor.getText()) // "Hello World"

manager.undo()
println(editor.getText()) // "Hello "

manager.redo()
println(editor.getText()) // "Hello World"
```

**Android Example - Undo/Redo:**
```kotlin
sealed class DrawCommand {
    abstract fun execute(canvas: Canvas)
    abstract fun undo()

    data class DrawLine(
        val startX: Float,
        val startY: Float,
        val endX: Float,
        val endY: Float,
        val paint: Paint
    ) : DrawCommand() {
        override fun execute(canvas: Canvas) {
            canvas.drawLine(startX, startY, endX, endY, paint)
        }

        override fun undo() {
            // Clear line
        }
    }

    data class DrawCircle(
        val cx: Float,
        val cy: Float,
        val radius: Float,
        val paint: Paint
    ) : DrawCommand() {
        override fun execute(canvas: Canvas) {
            canvas.drawCircle(cx, cy, radius, paint)
        }

        override fun undo() {
            // Clear circle
        }
    }
}

class DrawingView(context: Context) : View(context) {
    private val commands = mutableListOf<DrawCommand>()

    fun addCommand(command: DrawCommand) {
        commands.add(command)
        invalidate()
    }

    fun undo() {
        if (commands.isNotEmpty()) {
            commands.removeLast()
            invalidate()
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        commands.forEach { it.execute(canvas) }
    }
}
```

**When to use:**
- Implement undo/redo
- Queue operations
- Log/audit actions
- Macro recording

---

### Q12. What is the Chain of Responsibility Pattern?

**Answer:**
Chain of Responsibility passes requests along a chain of handlers until one handles it.

**Implementation:**
```kotlin
abstract class Handler {
    private var nextHandler: Handler? = null

    fun setNext(handler: Handler): Handler {
        nextHandler = handler
        return handler
    }

    abstract fun handle(request: Request): Boolean

    protected fun passToNext(request: Request): Boolean {
        return nextHandler?.handle(request) ?: false
    }
}

data class Request(
    val type: String,
    val priority: Int,
    val data: String
)

class LowPriorityHandler : Handler() {
    override fun handle(request: Request): Boolean {
        return if (request.priority <= 3) {
            println("LowPriorityHandler handled: ${request.data}")
            true
        } else {
            passToNext(request)
        }
    }
}

class MediumPriorityHandler : Handler() {
    override fun handle(request: Request): Boolean {
        return if (request.priority in 4..7) {
            println("MediumPriorityHandler handled: ${request.data}")
            true
        } else {
            passToNext(request)
        }
    }
}

class HighPriorityHandler : Handler() {
    override fun handle(request: Request): Boolean {
        return if (request.priority >= 8) {
            println("HighPriorityHandler handled: ${request.data}")
            true
        } else {
            passToNext(request)
        }
    }
}

// Usage
val lowHandler = LowPriorityHandler()
val medHandler = MediumPriorityHandler()
val highHandler = HighPriorityHandler()

lowHandler.setNext(medHandler).setNext(highHandler)

lowHandler.handle(Request("urgent", 9, "Critical bug"))
// HighPriorityHandler handled: Critical bug

lowHandler.handle(Request("normal", 5, "Feature request"))
// MediumPriorityHandler handled: Feature request
```

**Android Logging Chain:**
```kotlin
abstract class Logger(val level: Int) {
    private var nextLogger: Logger? = null

    fun setNext(logger: Logger): Logger {
        nextLogger = logger
        return logger
    }

    fun log(level: Int, message: String) {
        if (this.level <= level) {
            write(message)
        }
        nextLogger?.log(level, message)
    }

    protected abstract fun write(message: String)

    companion object {
        const val INFO = 1
        const val DEBUG = 2
        const val ERROR = 3
    }
}

class ConsoleLogger(level: Int) : Logger(level) {
    override fun write(message: String) {
        println("Console: $message")
    }
}

class FileLogger(level: Int) : Logger(level) {
    override fun write(message: String) {
        println("File: $message")
    }
}

class ErrorLogger(level: Int) : Logger(level) {
    override fun write(message: String) {
        println("Error: $message")
    }
}

// Usage
val loggerChain = ConsoleLogger(Logger.INFO)
    .setNext(FileLogger(Logger.DEBUG))
    .setNext(ErrorLogger(Logger.ERROR))

loggerChain.log(Logger.INFO, "This is info")
loggerChain.log(Logger.ERROR, "This is error")
```

**Android Touch Event Chain:**
```kotlin
// ViewGroup intercepts touch events
class CustomViewGroup(context: Context) : FrameLayout(context) {
    override fun onInterceptTouchEvent(ev: MotionEvent): Boolean {
        return when (ev.action) {
            MotionEvent.ACTION_DOWN -> {
                // Decide whether to intercept
                shouldInterceptTouch(ev)
            }
            else -> super.onInterceptTouchEvent(ev)
        }
    }

    private fun shouldInterceptTouch(ev: MotionEvent): Boolean {
        // Custom logic
        return false // Pass to child views
    }
}
```

**When to use:**
- Process requests in sequence
- Decouple sender from receiver
- Dynamic chain configuration

---

## **Architectural Patterns**

### Q13. What is MVVM (Model-View-ViewModel)?

**Answer:**
MVVM separates UI logic from business logic using ViewModel as a mediator.

**Complete Implementation:**
```kotlin
// Model - Data layer
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Repository
class UserRepository(
    private val apiService: ApiService,
    private val userDao: UserDao
) {
    suspend fun getUsers(): List<User> {
        return try {
            val users = apiService.getUsers()
            userDao.insertAll(users)
            users
        } catch (e: Exception) {
            userDao.getAllUsers()
        }
    }

    suspend fun getUserById(id: Int): User? {
        return userDao.getUserById(id)
    }
}

// ViewModel
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    sealed class UiState {
        object Loading : UiState()
        data class Success(val users: List<User>) : UiState()
        data class Error(val message: String) : UiState()
    }

    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            try {
                val users = repository.getUsers()
                _uiState.value = UiState.Success(users)
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Unknown error")
            }
        }
    }

    fun retry() {
        loadUsers()
    }
}

// View (Activity/Fragment)
@AndroidEntryPoint
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    private lateinit var binding: FragmentUserBinding
    private val adapter = UserAdapter()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentUserBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupRecyclerView()
        observeUiState()
        viewModel.loadUsers()
    }

    private fun setupRecyclerView() {
        binding.recyclerView.adapter = adapter
    }

    private fun observeUiState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.uiState.collect { state ->
                when (state) {
                    is UserViewModel.UiState.Loading -> showLoading()
                    is UserViewModel.UiState.Success -> showUsers(state.users)
                    is UserViewModel.UiState.Error -> showError(state.message)
                }
            }
        }
    }

    private fun showLoading() {
        binding.progressBar.visibility = View.VISIBLE
        binding.recyclerView.visibility = View.GONE
        binding.errorLayout.visibility = View.GONE
    }

    private fun showUsers(users: List<User>) {
        binding.progressBar.visibility = View.GONE
        binding.recyclerView.visibility = View.VISIBLE
        binding.errorLayout.visibility = View.GONE
        adapter.submitList(users)
    }

    private fun showError(message: String) {
        binding.progressBar.visibility = View.GONE
        binding.recyclerView.visibility = View.GONE
        binding.errorLayout.visibility = View.VISIBLE
        binding.errorText.text = message
        binding.retryButton.setOnClickListener {
            viewModel.retry()
        }
    }
}
```

**Benefits:**
- Clear separation of concerns
- Testable business logic
- Lifecycle awareness
- Reactive data flow

**When to use:**
- Modern Android apps (recommended by Google)
- Complex UI logic
- Need for testability

---

### Q14. What is MVP (Model-View-Presenter)?

**Answer:**
MVP separates UI from logic where Presenter acts as a middleman between View and Model.

**Implementation:**
```kotlin
// Contract
interface UserContract {
    interface View {
        fun showLoading()
        fun hideLoading()
        fun showUsers(users: List<User>)
        fun showError(message: String)
    }

    interface Presenter {
        fun attach(view: View)
        fun detach()
        fun loadUsers()
    }
}

// Model
class UserModel(private val apiService: ApiService) {
    suspend fun getUsers(): List<User> {
        return apiService.getUsers()
    }
}

// Presenter
class UserPresenter(
    private val model: UserModel,
    private val coroutineScope: CoroutineScope
) : UserContract.Presenter {

    private var view: UserContract.View? = null

    override fun attach(view: UserContract.View) {
        this.view = view
    }

    override fun detach() {
        view = null
    }

    override fun loadUsers() {
        view?.showLoading()
        coroutineScope.launch {
            try {
                val users = model.getUsers()
                view?.hideLoading()
                view?.showUsers(users)
            } catch (e: Exception) {
                view?.hideLoading()
                view?.showError(e.message ?: "Unknown error")
            }
        }
    }
}

// View (Activity)
class UserActivity : AppCompatActivity(), UserContract.View {
    private lateinit var binding: ActivityUserBinding
    private lateinit var presenter: UserContract.Presenter
    private val adapter = UserAdapter()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityUserBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val model = UserModel(apiService)
        presenter = UserPresenter(model, lifecycleScope)
        presenter.attach(this)

        binding.recyclerView.adapter = adapter
        presenter.loadUsers()
    }

    override fun onDestroy() {
        super.onDestroy()
        presenter.detach()
    }

    override fun showLoading() {
        binding.progressBar.visibility = View.VISIBLE
    }

    override fun hideLoading() {
        binding.progressBar.visibility = View.GONE
    }

    override fun showUsers(users: List<User>) {
        adapter.submitList(users)
    }

    override fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
```

**MVP vs MVVM:**

| Feature | MVP | MVVM |
|---------|-----|------|
| **View-Logic coupling** | View interface | Data binding |
| **Lifecycle** | Manual attach/detach | Automatic |
| **Testing** | Mock View interface | No View needed |
| **Boilerplate** | More (interfaces) | Less |
| **Learning curve** | Easier | Moderate |

**When to use:**
- Legacy Android apps
- Don't want data binding
- More control over View updates

---

### Q15. What is MVI (Model-View-Intent)?

**Answer:**
MVI is a unidirectional data flow pattern where user intents trigger state changes.

**Implementation:**
```kotlin
// Intent - User actions
sealed class UserIntent {
    object LoadUsers : UserIntent()
    data class SearchUsers(val query: String) : UserIntent()
    data class DeleteUser(val userId: Int) : UserIntent()
    object Refresh : UserIntent()
}

// State - UI state
data class UserViewState(
    val isLoading: Boolean = false,
    val users: List<User> = emptyList(),
    val error: String? = null,
    val searchQuery: String = ""
)

// ViewModel
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _state = MutableStateFlow(UserViewState())
    val state: StateFlow<UserViewState> = _state.asStateFlow()

    fun processIntent(intent: UserIntent) {
        when (intent) {
            is UserIntent.LoadUsers -> loadUsers()
            is UserIntent.SearchUsers -> searchUsers(intent.query)
            is UserIntent.DeleteUser -> deleteUser(intent.userId)
            is UserIntent.Refresh -> refresh()
        }
    }

    private fun loadUsers() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, error = null) }
            try {
                val users = repository.getUsers()
                _state.update {
                    it.copy(
                        isLoading = false,
                        users = users,
                        error = null
                    )
                }
            } catch (e: Exception) {
                _state.update {
                    it.copy(
                        isLoading = false,
                        error = e.message
                    )
                }
            }
        }
    }

    private fun searchUsers(query: String) {
        _state.update { it.copy(searchQuery = query) }
        viewModelScope.launch {
            val filteredUsers = repository.searchUsers(query)
            _state.update { it.copy(users = filteredUsers) }
        }
    }

    private fun deleteUser(userId: Int) {
        viewModelScope.launch {
            repository.deleteUser(userId)
            val updatedUsers = _state.value.users.filter { it.id != userId }
            _state.update { it.copy(users = updatedUsers) }
        }
    }

    private fun refresh() {
        loadUsers()
    }
}

// View
@AndroidEntryPoint
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    private lateinit var binding: FragmentUserBinding
    private val adapter = UserAdapter { user ->
        viewModel.processIntent(UserIntent.DeleteUser(user.id))
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        setupViews()
        observeState()
        sendIntent(UserIntent.LoadUsers)
    }

    private fun setupViews() {
        binding.recyclerView.adapter = adapter

        binding.searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextChange(newText: String): Boolean {
                sendIntent(UserIntent.SearchUsers(newText))
                return true
            }

            override fun onQueryTextSubmit(query: String) = true
        })

        binding.refreshLayout.setOnRefreshListener {
            sendIntent(UserIntent.Refresh)
        }
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.state.collect { state ->
                render(state)
            }
        }
    }

    private fun render(state: UserViewState) {
        binding.progressBar.isVisible = state.isLoading
        binding.refreshLayout.isRefreshing = false

        if (state.error != null) {
            showError(state.error)
        } else {
            adapter.submitList(state.users)
        }
    }

    private fun sendIntent(intent: UserIntent) {
        viewModel.processIntent(intent)
    }

    private fun showError(message: String) {
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
    }
}
```

**Key Principles:**
1. **Intent** - User actions
2. **State** - Single source of truth
3. **Unidirectional flow** - Intent ’ Process ’ State ’ Render

**Benefits:**
- Predictable state changes
- Easy to debug (state history)
- Testable
- Time-travel debugging possible

**When to use:**
- Complex state management
- Need predictability
- Large teams

---

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

---

## **Best Practices**

### Q19. When should you use which pattern?

**Answer:**

**Creational Patterns:**
- **Singleton**: Database, Network client, Logger
- **Factory**: Creating Views, Fragments, ViewHolders
- **Builder**: Complex objects with many optional parameters
- **Dependency Injection**: Everything! (Recommended)

**Structural Patterns:**
- **Adapter**: RecyclerView, integrating third-party libraries
- **Decorator**: Adding features to Views, OkHttp Interceptors
- **Facade**: Simplifying complex subsystems
- **Proxy**: Lazy loading, access control, caching

**Behavioral Patterns:**
- **Observer**: LiveData, Flow, event handling
- **Strategy**: Algorithms that change at runtime
- **Command**: Undo/Redo, queuing operations
- **Chain of Responsibility**: Touch event handling, logging

**Architectural Patterns:**
- **MVVM**: Modern Android apps (recommended)
- **MVP**: Legacy apps, more control
- **MVI**: Complex state management, predictability

---

### Q20. Common Interview Questions

**Q: What's the difference between Singleton and Static class?**
```kotlin
// Static class (object in Kotlin)
object StaticUtils {
    fun doSomething() { }
}

// Singleton
class Singleton private constructor() {
    companion object {
        @Volatile
        private var instance: Singleton? = null

        fun getInstance(): Singleton {
            return instance ?: synchronized(this) {
                instance ?: Singleton().also { instance = it }
            }
        }
    }
}
```
- Singleton can implement interfaces, extend classes
- Static class cannot have state that requires initialization
- Singleton can be lazy-loaded
- Static is initialized when class loads

**Q: How do you make Singleton thread-safe in Android?**
```kotlin
// Thread-safe lazy initialization
class ThreadSafeSingleton private constructor() {
    companion object {
        val instance: ThreadSafeSingleton by lazy(LazyThreadSafetyMode.SYNCHRONIZED) {
            ThreadSafeSingleton()
        }
    }
}

// Using object (thread-safe by default)
object SafeSingleton {
    // Thread-safe
}

// Double-checked locking
class DoubleCheckedSingleton private constructor() {
    companion object {
        @Volatile
        private var instance: DoubleCheckedSingleton? = null

        fun getInstance(): DoubleCheckedSingleton {
            return instance ?: synchronized(this) {
                instance ?: DoubleCheckedSingleton().also { instance = it }
            }
        }
    }
}
```

**Q: How does RecyclerView use design patterns?**
- **Adapter Pattern**: RecyclerView.Adapter adapts data to views
- **ViewHolder Pattern**: Caches view references
- **Observer Pattern**: notify methods update views
- **Strategy Pattern**: LayoutManager defines layout strategy

**Q: Explain dependency injection in Android**
- Provides dependencies from outside
- Improves testability
- Reduces coupling
- Hilt/Dagger are recommended frameworks

**Q: What's the difference between MVP and MVVM?**
- MVP: View interface, manual updates, more boilerplate
- MVVM: Data binding, lifecycle-aware, less boilerplate
- MVVM is Google's recommended pattern

---

## **Summary**

**Key Patterns for Android:**

**Creational:**
- Singleton (but use DI instead)
- Factory (ViewHolders, Fragments)
- Builder (AlertDialog, Notification)
- Dependency Injection (Hilt)

**Structural:**
- Adapter (RecyclerView)
- Decorator (Interceptors)
- Facade (Complex APIs)

**Behavioral:**
- Observer (LiveData, Flow)
- Strategy (Algorithms)
- Command (Undo/Redo)

**Architectural:**
- MVVM (Recommended)
- Repository Pattern
- Clean Architecture

**Interview Tips:**
1. Understand the problem each pattern solves
2. Know real Android examples
3. Explain pros/cons
4. Show code examples
5. Discuss when to use each pattern
6. Understand architectural patterns deeply
7. Be ready to compare patterns

**Resources:**
- Android Architecture Components
- Clean Architecture by Robert C. Martin
- Design Patterns by Gang of Four
- Android Developer Guide
- Refactoring.Guru

---

**Remember:** Patterns are tools, not rules. Use them when they solve a problem, not because you should use patterns!
