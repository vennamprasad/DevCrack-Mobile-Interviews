# Jetpack Android Interview Questions (Basic & Advanced)

## Basic Questions

### 1. What is Android Jetpack?
**Answer:**  
Android Jetpack is a suite of libraries, tools, and guidance to help developers write high-quality apps easier. It includes components for architecture, UI, behavior, and foundation.

---

### 2. Name some Jetpack components.
**Answer:**  
- Navigation
- LiveData
- ViewModel
- Room
- WorkManager
- DataBinding
- Paging
- Lifecycle

---

### 3. What is LiveData?
**Answer:**  
LiveData is an observable data holder class. It respects the lifecycle of app components, such as activities and fragments.

**Example:**
```kotlin
val users: LiveData<List<User>> = userRepository.getUsers()
```

---

### 4. What is ViewModel?
**Answer:**  
ViewModel stores and manages UI-related data in a lifecycle conscious way. It survives configuration changes.

**Example:**
```kotlin
class MyViewModel : ViewModel() {
    val user = MutableLiveData<User>()
}
```

---

### 5. What is Room?
**Answer:**  
Room is a persistence library that provides an abstraction layer over SQLite to allow fluent database access.

**Example:**
```kotlin
@Entity
data class User(val uid: Int, val name: String)

@Dao
interface UserDao {
    @Query("SELECT * FROM user")
    fun getAll(): List<User>
}
```

---

### 6. What is DataBinding?
**Answer:**  
DataBinding binds UI components in layouts to data sources in your app using a declarative format.

---

### 7. What is Navigation Component?
**Answer:**  
Navigation Component helps manage app navigation, including fragment transactions, deep linking, and navigation graphs.

---

### 8. What is Lifecycle-aware component?
**Answer:**  
Lifecycle-aware components perform actions in response to lifecycle changes of activities and fragments.

---

### 9. What is WorkManager?
**Answer:**  
WorkManager is a library for managing deferrable, guaranteed background work.

**Example:**
```kotlin
val workRequest = OneTimeWorkRequestBuilder<MyWorker>().build()
WorkManager.getInstance(context).enqueue(workRequest)
```

---

### 10. What is Paging?
**Answer:**  
Paging helps load and display large data sets efficiently by loading data in chunks.

---

### 11. What is the difference between LiveData and StateFlow?
**Answer:**  
LiveData is lifecycle-aware and used in Jetpack; StateFlow is a Kotlin Flow for state management, not lifecycle-aware.

---

### 12. How does ViewModel survive configuration changes?
**Answer:**  
ViewModel is tied to the lifecycle of the activity/fragment and is not destroyed on configuration changes.

---

### 13. What is the use of SavedStateHandle in ViewModel?
**Answer:**  
SavedStateHandle allows ViewModel to save and restore UI state during process death.

---

### 14. How do you observe LiveData in a Fragment?
**Answer:**
```kotlin
viewModel.user.observe(viewLifecycleOwner) { user ->
    // Update UI
}
```

---

### 15. What is the role of Repository in Jetpack architecture?
**Answer:**  
Repository abstracts the data sources and provides a clean API for data access.

---

### 16. What is the difference between @Insert and @Update in Room?
**Answer:**  
@Insert adds new records; @Update modifies existing records.

---

### 17. How do you handle database migrations in Room?
**Answer:**  
By providing a Migration object to Room's database builder.

---

### 18. What is the use of Navigation Graph?
**Answer:**  
Navigation Graph visually represents all navigation paths in the app.

---

### 19. How do you pass data between fragments using Navigation Component?
**Answer:**
```kotlin
val action = FirstFragmentDirections.actionToSecondFragment(data)
findNavController().navigate(action)
```

---

