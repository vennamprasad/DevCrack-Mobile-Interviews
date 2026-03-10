## **1. StateFlow vs SharedFlow vs Flow - When to Use What**

### **Flow (Cold Stream)**
**Use Case**: One-time operations, API calls, database queries

```kotlin
class UserRepository {
    // Returns fresh data each time it's collected
    fun getUser(id: String): Flow<User> = flow {
        val user = api.fetchUser(id)
        emit(user)
    }
}

// Each collector gets a NEW API call
viewModelScope.launch {
    repository.getUser("123").collect { user ->
        println("Collector 1: $user")
    }
}

viewModelScope.launch {
    repository.getUser("123").collect { user ->
        println("Collector 2: $user")  // Separate API call!
    }
}
```

### **StateFlow (Hot Stream with State)**
**Use Case**: UI state, configuration, single source of truth

```kotlin
class UserViewModel : ViewModel() {
    private val _userState = MutableStateFlow<UserState>(UserState.Loading)
    val userState: StateFlow<UserState> = _userState.asStateFlow()

    fun loadUser(id: String) {
        viewModelScope.launch {
            _userState.value = UserState.Loading
            try {
                val user = repository.fetchUser(id)
                _userState.value = UserState.Success(user)
            } catch (e: Exception) {
                _userState.value = UserState.Error(e.message)
            }
        }
    }
}

// In Activity/Fragment
lifecycleScope.launch {
    viewModel.userState.collect { state ->
        when (state) {
            is UserState.Loading -> showLoading()
            is UserState.Success -> showUser(state.user)
            is UserState.Error -> showError(state.message)
        }
    }
}
```

**Key Features**:
- Always has a current value (`.value`)
- New collectors immediately get the latest value
- Conflates updates (skips intermediate values if collector is slow)
- Perfect for UI state

### **SharedFlow (Hot Stream for Events)**
**Use Case**: Events, notifications, one-time actions

```kotlin
class EventViewModel : ViewModel() {
    private val _navigationEvents = MutableSharedFlow<NavigationEvent>()
    val navigationEvents = _navigationEvents.asSharedFlow()

    fun onLoginSuccess() {
        viewModelScope.launch {
            _navigationEvents.emit(NavigationEvent.GoToHome)
        }
    }
}

// Collectors only receive NEW events (no replay by default)
lifecycleScope.launch {
    viewModel.navigationEvents.collect { event ->
        when (event) {
            is NavigationEvent.GoToHome -> navigateToHome()
            is NavigationEvent.ShowError -> showErrorDialog()
        }
    }
}
```

**Key Features**:
- No initial value
- Can configure replay (buffer past events)
- Doesn't skip values (unless buffer is full)
- Perfect for one-time events

**Comparison Table**:
| Feature | Flow | StateFlow | SharedFlow |
|---------|------|-----------|------------|
| Hot/Cold | Cold | Hot | Hot |
| Initial Value | No | Yes | Optional (replay) |
| Multiple Collectors | Independent streams | Share same stream | Share same stream |
| Conflation | No | Yes | Configurable |
| Use Case | API calls | UI state | Events |
