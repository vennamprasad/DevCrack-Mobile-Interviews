## **2. Search with Debouncing (Real-Time Search)**

### **Problem**: Don't want to search on every keystroke

```kotlin
class SearchViewModel : ViewModel() {
    private val _searchQuery = MutableStateFlow("")

    val searchResults: StateFlow<List<Result>> = _searchQuery
        .debounce(300)  // Wait 300ms after user stops typing
        .filter { it.length >= 3 }  // Only search if 3+ characters
        .distinctUntilChanged()  // Don't search if query hasn't changed
        .flatMapLatest { query ->
            searchRepository.search(query)
                .catch { emit(emptyList()) }  // Handle errors gracefully
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = emptyList()
        )

    fun onSearchQueryChanged(query: String) {
        _searchQuery.value = query
    }
}

// In UI
class SearchActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        searchEditText.addTextChangedListener { text ->
            viewModel.onSearchQueryChanged(text.toString())
        }

        lifecycleScope.launch {
            viewModel.searchResults.collect { results ->
                adapter.submitList(results)
            }
        }
    }
}
```

**Why It Works**:
- `debounce(300)`: Waits 300ms after last emission
- `filter`: Prevents unnecessary API calls for short queries
- `distinctUntilChanged`: Avoids duplicate searches
- `flatMapLatest`: Cancels previous search if new one starts
- `catch`: Handles errors without breaking the flow
