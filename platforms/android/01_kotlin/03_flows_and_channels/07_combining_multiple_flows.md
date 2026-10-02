## **5. Combining Multiple Flows**

### **Problem**: Need data from multiple sources

**Using `combine` (waits for all flows)**:
```kotlin
class DashboardViewModel : ViewModel() {
    private val userFlow = repository.observeUser()
    private val notificationsFlow = repository.observeNotifications()
    private val settingsFlow = repository.observeSettings()

    val dashboardState = combine(
        userFlow,
        notificationsFlow,
        settingsFlow
    ) { user, notifications, settings ->
        DashboardState(
            user = user,
            unreadCount = notifications.count { !it.isRead },
            isDarkMode = settings.isDarkMode
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = DashboardState.Loading
    )
}
```

**Using `zip` (pairs emissions)**:
```kotlin
val flow1 = flowOf(1, 2, 3)
val flow2 = flowOf("A", "B", "C")

flow1.zip(flow2) { num, letter ->
    "$num$letter"
}.collect { println(it) }
// Output: 1A, 2B, 3C
```

**Using `merge` (merges all emissions)**:
```kotlin
val localFlow = database.observeArticles()
val remoteFlow = api.fetchArticlesFlow()

merge(localFlow, remoteFlow)
    .collect { articles ->
        updateUI(articles)
    }
```
