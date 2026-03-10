## **8. Performance Optimizations**

### **Batch Processing with Channels**:
```kotlin
fun CoroutineScope.batchProcessor(
    batchSize: Int = 10,
    delayMs: Long = 1000L
): SendChannel<Item> = Channel<Item>(Channel.UNLIMITED).also { channel ->
    launch {
        val batch = mutableListOf<Item>()

        while (!channel.isClosedForReceive) {
            select<Unit> {
                channel.onReceive { item ->
                    batch.add(item)
                    if (batch.size >= batchSize) {
                        processBatch(batch.toList())
                        batch.clear()
                    }
                }

                onTimeout(delayMs) {
                    if (batch.isNotEmpty()) {
                        processBatch(batch.toList())
                        batch.clear()
                    }
                }
            }
        }
    }
}

// Usage
val processor = viewModelScope.batchProcessor()
processor.send(item1)
processor.send(item2)  // Batched together for efficiency
```

**Limiting Concurrent Operations**:
```kotlin
suspend fun downloadImages(urls: List<String>) {
    val semaphore = Semaphore(3)  // Max 3 concurrent downloads

    coroutineScope {
        urls.map { url ->
            async {
                semaphore.withPermit {
                    downloadImage(url)
                }
            }
        }.awaitAll()
    }
}
```
