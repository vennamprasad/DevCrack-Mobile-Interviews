## **10. Real-World Production Patterns**

### **Pattern 1: Loading States with Flows**
```kotlin
sealed class UiState<out T> {
    object Idle : UiState<Nothing>()
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}

class NewsViewModel : ViewModel() {
    private val _newsState = MutableStateFlow<UiState<List<News>>>(UiState.Idle)
    val newsState = _newsState.asStateFlow()

    fun loadNews() {
        viewModelScope.launch {
            _newsState.value = UiState.Loading

            repository.getNews()
                .catch { e ->
                    _newsState.value = UiState.Error(e.message ?: "Unknown error")
                }
                .collect { news ->
                    _newsState.value = UiState.Success(news)
                }
        }
    }
}
```

### **Pattern 2: One-Time Events with SharedFlow**
```kotlin
class CheckoutViewModel : ViewModel() {
    private val _checkoutEvents = MutableSharedFlow<CheckoutEvent>()
    val checkoutEvents = _checkoutEvents.asSharedFlow()

    fun processPayment() {
        viewModelScope.launch {
            try {
                val result = paymentRepository.charge()
                _checkoutEvents.emit(CheckoutEvent.PaymentSuccess(result))
            } catch (e: Exception) {
                _checkoutEvents.emit(CheckoutEvent.PaymentFailed(e.message))
            }
        }
    }
}

sealed class CheckoutEvent {
    data class PaymentSuccess(val orderId: String) : CheckoutEvent()
    data class PaymentFailed(val error: String?) : CheckoutEvent()
}
```

### **Pattern 3: Form Validation with Flows**
```kotlin
class LoginViewModel : ViewModel() {
    val email = MutableStateFlow("")
    val password = MutableStateFlow("")

    val isLoginEnabled: StateFlow<Boolean> = combine(
        email,
        password
    ) { email, password ->
        email.isValidEmail() && password.length >= 8
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = false
    )

    val emailError: StateFlow<String?> = email
        .debounce(500)
        .map { if (it.isNotEmpty() && !it.isValidEmail()) "Invalid email" else null }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), null)
}
```
