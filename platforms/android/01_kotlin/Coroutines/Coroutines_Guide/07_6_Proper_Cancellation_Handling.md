## **6. Proper Cancellation Handling**

### **Problem**: Coroutines doing work after they're canceled

**❌ Ignores Cancellation**:
```kotlin
suspend fun processImages(images: List<Bitmap>) {
    images.forEach { image ->
        processImage(image)  // Continues even if canceled!
    }
}
```

**✅ Respects Cancellation**:
```kotlin
suspend fun processImages(images: List<Bitmap>) {
    images.forEach { image ->
        ensureActive()  // Throws if canceled
        processImage(image)
    }
}

// Or use yield()
suspend fun processLargeList(items: List<Item>) {
    items.forEach { item ->
        yield()  // Checks for cancellation and allows other coroutines
        processItem(item)
    }
}
```

**Cleanup on Cancellation**:
```kotlin
suspend fun downloadFile(url: String): File {
    val tempFile = File.createTempFile("download", ".tmp")

    try {
        return withContext(Dispatchers.IO) {
            // Download logic
            tempFile
        }
    } catch (e: CancellationException) {
        tempFile.delete()  // Cleanup on cancellation
        throw e  // Re-throw CancellationException
    }
}
```

**Using invokeOnCompletion**:
```kotlin
val job = viewModelScope.launch {
    try {
        heavyOperation()
    } finally {
        cleanup()  // Always runs, even on cancellation
    }
}

job.invokeOnCompletion { exception ->
    when (exception) {
        is CancellationException -> Log.d("Job", "Canceled")
        null -> Log.d("Job", "Completed successfully")
        else -> Log.e("Job", "Failed with exception", exception)
    }
}
```
