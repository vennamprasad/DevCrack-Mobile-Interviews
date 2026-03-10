## **Common Production Bugs & Fixes**

### **Bug 1**: Memory leak from GlobalScope
```kotlin
// ❌ BAD - leaks if Activity is destroyed
GlobalScope.launch {
    val data = fetchData()
    updateUI(data)
}

// ✅ GOOD - auto-canceled with lifecycle
lifecycleScope.launch {
    val data = fetchData()
    updateUI(data)
}
```

### **Bug 2**: ANR from blocking main thread
```kotlin
// ❌ BAD - blocks UI
viewModelScope.launch(Dispatchers.Main) {
    val result = blockingIOOperation()  // ANR!
}

// ✅ GOOD - use IO dispatcher
viewModelScope.launch {
    val result = withContext(Dispatchers.IO) {
        blockingIOOperation()
    }
    updateUI(result)  // Back to Main
}
```

### **Bug 3**: Race condition in shared state
```kotlin
// ❌ BAD - multiple coroutines modify state
var count = 0
repeat(1000) {
    viewModelScope.launch { count++ }  // Final count unpredictable!
}

// ✅ GOOD - use atomic or single-threaded dispatcher
val count = AtomicInteger(0)
repeat(1000) {
    viewModelScope.launch { count.incrementAndGet() }
}
```
