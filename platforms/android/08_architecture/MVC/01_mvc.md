# 📦 MVC Architecture Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**

![MVC](https://img.shields.io/badge/Architecture-MVC-blue?style=for-the-badge)
![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)

---

## ✅ Overview

The **Model-View-Controller (MVC)** architecture is a design pattern commonly used in Android development to organize code in a modular, maintainable, and testable way.
MVC divides an application into three interconnected components:

### 1. Model Layer
- Responsible for managing the business logic and handling network or database APIs.
- The Model has **no knowledge** of the user interface.
- Stores the application data:
    - Data sources (e.g., Room database, SQLite, Firebase, APIs).
    - Repository classes that handle data operations.
    - Business logic (e.g., calculations, data transformations).

**Example:** A `User` class or a repository fetching user data.

```kotlin
class TaskRepository {
    private val tasks = mutableListOf<Task>()
    fun addTask(task: Task) { tasks.add(task) }
    fun getTasks(): List<Task> = tasks
}
```

### 2. View Layer
- Represents the UI layer, responsible for displaying data and capturing user input.
- In Android, this is typically **XML layouts**, custom Views, ViewGroups, and UI widgets.
- The View doesn’t handle any complex logic itself.

**Example:** An Activity displaying a list of users (The View is passive).

```xml
<LinearLayout ...>
    <RecyclerView android:id="@+id/recyclerView" ... />
    <Button android:id="@+id/addButton" android:text="Add Task" />
</LinearLayout>
```

### 3. Controller Layer
- Establishes the relationship between the View and the Model.
- Handles user input from the View, updates the Model, and refreshes the View with new data.
- **In Android:** Traditionally `Activities` or `Fragments` act as the Controller.
- It processes interactions (e.g., button clicks) and coordinates with the Model.

**Example:** An Activity that listens for a button click.

```kotlin
class MainActivity : AppCompatActivity() {
    private val repository = TaskRepository()
    private lateinit var recyclerView: RecyclerView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        recyclerView = findViewById(R.id.recyclerView)
        // Controller updates View with data from Model
        recyclerView.adapter = TaskAdapter(repository.getTasks())

        findViewById<Button>(R.id.addButton).setOnClickListener {
            // Controller updates Model based on View input
            val newTask = Task(id = tasks.size + 1, title = "New Task")
            repository.addTask(newTask)
            recyclerView.adapter?.notifyDataSetChanged()
        }
    }
}
```

---

## ⚖️ Pros & Cons of MVC

| Advantages | Disadvantages |
|------------|---------------|
| **Separation of Concerns:** Distinct roles improve organization. | **Complexity:** Can add unnecessary complexity for small apps. |
| **Maintainability:** Changes to UI don't affect Model. | **Tight Coupling:** Android Activities often act as both View & Controller. |
| **Testability:** Model can be tested independently. | **Boilerplate:** Requires more code than simple scripting. |
| **Reusability:** Models can be reused. | **God Components:** Controllers (Activities) tend to become massive. |

---

## ❓ Interview Questions (MVC Focus)

### 1. Conceptual Questions

#### Q1: What is the MVC architecture, and how is it implemented in Android?
* **Model:** Data & Business Logic (e.g., `Room`, `Retrofit`).
* **View:** UI (e.g., XML Layouts).
* **Controller:** Logic to link Model & View (e.g., `Activity`, `Fragment`).
* **Flow:** View accepts input -> Controller -> Model updates data -> Controller updates View.

#### Q2: What are the main disadvantages of MVC in Android?
* **Tight Coupling:** In standard Android, the `Activity` defines the layout *and* handles events, making it act as both View and Controller. This makes unit testing the "Controller" logic difficult because it is bound to Android, SDK.
* **Massive View Controller:** Activities tend to grow very large as they handle UI logic, business logic coordination, and lifecycle events.

#### Q3: How does MVC differ from MVVM and MVI?
* **MVC:** Controller drives the View.
* **MVVM:** View observes the ViewModel (Data Binding/LiveData). Decoupled.
* **MVI:** Unidirectional Data Flow. View receives immutable States.

#### Q4: How do you handle communication between Model and Controller?
* The Controller calls methods on the Model (e.g., `repository.getData()`).
* The Model can return data synchronously or asynchronously (via Callbacks/Coroutines) to the Controller.

---

### 2. Technical Implementation

#### Q1: How do you avoid tight coupling between View and Controller?
* Use **Dependency Injection** (Hilt/Dagger) to inject Repository instances.
* Abstract the View via **Interfaces** (similar to MVP) if you want strict separation, though standard MVC in Android usually implies Activity = Controller.

#### Q2: How do you handle asynchronous operations in MVC?
* The Controller launches a Coroutine or uses RxJava to call the Model.
* When data returns, the Controller runs code on the Main Thread to update the UI (View).

#### Q3: How would you refactor an MVC app to MVVM?
1. Extract business logic from the Activity (Controller) into a `ViewModel`.
2. Expose data as `LiveData` or `StateFlow` from the ViewModel.
3. Make the Activity (View) observe these streams.
4. Remove direct calls from Activity to Model; route everything through ViewModel.

---

### 3. Scenario-Based

#### Q1: How would you handle screen rotation in MVC?
* **Problem:** Activity (Controller) recreates on rotation.
* **Solution:**
    1. Use `onSaveInstanceState` to bundle data.
    2. Ideally, migrate to **ViewModel** which survives configuration changes (Architecture Components), effectively hybridizing MVC into MVVM.

#### Q2: How do you test the Controller logic?
* Since the Controller is often the Activity, standard JUnit tests are hard. You often need **Espresso** or **Robolectric** for UI tests.
* To make it unit-testable, you must extract logic into a separate plain Kotlin class that the Activity calls.

---

### 4. Advanced Questions

#### Q1: Comparison with other patterns?
* **vs MVP:** In MVP, the Presenter calls the View interface. In MVC, the Controller modifies the View directly (often tightly coupled in Android).
* **vs MVVM:** MVVM uses the Observer pattern. The View reacts to changes, rather than being told to change.

#### Q2: Thread safety in MVC?
* Ensure that the Model operations run on `Dispatchers.IO`.
* Ensure that the Controller updates the View hierarchy **only** on `Dispatchers.Main`.
