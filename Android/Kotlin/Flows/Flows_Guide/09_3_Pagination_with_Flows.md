## **3. Pagination with Flows**

### **Problem**: Load items incrementally as user scrolls

```kotlin
class PaginatedRepository {
    private var currentPage = 0
    private val _items = mutableListOf<Item>()

    fun getItems(): Flow<PagingState<Item>> = flow {
        emit(PagingState.Loading)

        try {
            val newItems = api.fetchItems(page = currentPage, pageSize = 20)
            _items.addAll(newItems)
            currentPage++

            emit(PagingState.Success(
                items = _items.toList(),
                hasMore = newItems.size == 20
            ))
        } catch (e: Exception) {
            emit(PagingState.Error(e.message ?: "Unknown error"))
        }
    }

    fun reset() {
        currentPage = 0
        _items.clear()
    }
}

class FeedViewModel : ViewModel() {
    private val _feedState = MutableStateFlow<PagingState<Item>>(PagingState.Initial)
    val feedState = _feedState.asStateFlow()

    fun loadMore() {
        viewModelScope.launch {
            repository.getItems().collect { state ->
                _feedState.value = state
            }
        }
    }

    fun refresh() {
        repository.reset()
        loadMore()
    }
}

sealed class PagingState<out T> {
    object Initial : PagingState<Nothing>()
    object Loading : PagingState<Nothing>()
    data class Success<T>(val items: List<T>, val hasMore: Boolean) : PagingState<T>()
    data class Error(val message: String) : PagingState<Nothing>()
}
```
