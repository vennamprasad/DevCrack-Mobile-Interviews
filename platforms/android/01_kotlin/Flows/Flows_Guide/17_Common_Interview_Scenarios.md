## **Common Interview Scenarios**

### **Scenario 1**: Implement a real-time chat message flow
```kotlin
class ChatRepository {
    fun observeMessages(chatId: String): Flow<List<Message>> = callbackFlow {
        val listener = firestore.collection("chats")
            .document(chatId)
            .collection("messages")
            .orderBy("timestamp")
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    close(error)
                    return@addSnapshotListener
                }

                val messages = snapshot?.documents?.map { it.toObject(Message::class.java)!! }
                    ?: emptyList()
                trySend(messages)
            }

        awaitClose { listener.remove() }
    }
}
```

### **Scenario 2**: Handle multiple data sources (remote + local + cache)
```kotlin
fun getArticles(): Flow<List<Article>> = channelFlow {
    // Emit from memory cache immediately
    memoryCache.get()?.let { send(it) }

    // Then emit from database
    launch {
        database.getArticles().collect { send(it) }
    }

    // Finally fetch from network
    launch {
        try {
            val fresh = api.fetchArticles()
            database.saveArticles(fresh)
            memoryCache.save(fresh)
            send(fresh)
        } catch (e: Exception) {
            // Already sent cached data
        }
    }
}
```

### **Scenario 3**: Implement infinite scroll pagination
```kotlin
class PagingViewModel : ViewModel() {
    private val _pagingFlow = MutableStateFlow(PagingData(items = emptyList(), page = 0))

    val items: StateFlow<List<Item>> = _pagingFlow
        .flatMapLatest { pagingData ->
            flow {
                emit(pagingData.items)

                if (!pagingData.isLoading) {
                    val newItems = repository.fetchPage(pagingData.page)
                    emit(pagingData.items + newItems)
                }
            }
        }
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun loadMore() {
        val current = _pagingFlow.value
        _pagingFlow.value = current.copy(page = current.page + 1, isLoading = true)
    }
}
```
