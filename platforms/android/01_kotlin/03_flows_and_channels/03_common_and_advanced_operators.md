## **9. Advanced Flow Operators in Real Scenarios**

### **flatMapConcat** (Sequential processing)
```kotlin
// Process users one by one, in order
fun processUsers(userIds: List<String>): Flow<User> {
    return userIds.asFlow()
        .flatMapConcat { id ->
            flow { emit(api.fetchUser(id)) }
        }
}
```

### **flatMapMerge** (Parallel processing)
```kotlin
// Process multiple users concurrently
fun processUsersInParallel(userIds: List<String>): Flow<User> {
    return userIds.asFlow()
        .flatMapMerge(concurrency = 3) { id ->
            flow { emit(api.fetchUser(id)) }
        }
}
```

### **transformLatest** (Cancel previous when new arrives)
```kotlin
fun searchWithTransformLatest(query: String): Flow<List<Result>> {
    return flowOf(query)
        .transformLatest { q ->
            emit(emptyList())  // Clear previous results
            delay(300)
            emit(api.search(q))
        }
}
```

### **scan** (Accumulate emissions)
```kotlin
// Calculate running total of cart items
fun cartTotal(items: Flow<Item>): Flow<Double> {
    return items
        .map { it.price }
        .scan(0.0) { total, price -> total + price }
}
```

### **buffer** (Handle backpressure)
```kotlin
fun processLargeDataset(): Flow<Data> = flow {
    repeat(100) {
        emit(fetchData(it))
    }
}
.buffer(capacity = 10)  // Buffer up to 10 items
.map { processData(it) }  // Slow processing
```
