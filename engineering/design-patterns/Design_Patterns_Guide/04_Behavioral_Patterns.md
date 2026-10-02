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
