## **3. Thread Safety & Race Conditions**

### **Problem**: Multiple coroutines accessing shared mutable state

**❌ Race Condition (Unsafe)**:
```kotlin
class Counter {
    private var count = 0

    fun increment() {
        viewModelScope.launch {
            count++  // NOT thread-safe! Can lose updates
        }
    }
}
```

**✅ Using Mutex (Thread-safe)**:
```kotlin
class Counter {
    private var count = 0
    private val mutex = Mutex()

    suspend fun increment() {
        mutex.withLock {
            count++  // Only one coroutine at a time
        }
    }

    suspend fun getCount(): Int = mutex.withLock { count }
}
```

**✅ Using AtomicInteger**:
```kotlin
class Counter {
    private val count = AtomicInteger(0)

    fun increment() {
        viewModelScope.launch {
            count.incrementAndGet()  // Thread-safe atomic operation
        }
    }
}
```

**✅ Using Single Dispatcher** (Confine to one thread):
```kotlin
class BankAccount {
    private var balance = 0
    private val accountDispatcher = Dispatchers.Default.limitedParallelism(1)

    suspend fun deposit(amount: Int) = withContext(accountDispatcher) {
        balance += amount  // Always runs on same thread
    }

    suspend fun getBalance(): Int = withContext(accountDispatcher) {
        balance
    }
}
```
