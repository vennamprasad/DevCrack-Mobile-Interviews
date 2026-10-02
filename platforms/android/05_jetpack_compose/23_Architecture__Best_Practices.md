## **Architecture & Best Practices**

### 74. What is the recommended architecture for Compose apps?

**Answer:**

**Recommended: MVVM with UDF (Unidirectional Data Flow)**

```kotlin
// 1. UI State
data class HomeUiState(
    val isLoading: Boolean = false,
    val items: List<Item> = emptyList(),
    val error: String? = null,
    val selectedFilter: Filter = Filter.ALL
)

// 2. UI Events
sealed class HomeUiEvent {
    data class FilterChanged(val filter: Filter) : HomeUiEvent()
    object Refresh : HomeUiEvent()
    data class ItemClicked(val itemId: Int) : HomeUiEvent()
}

// 3. ViewModel
class HomeViewModel(
    private val repository: ItemRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    fun onEvent(event: HomeUiEvent) {
        when (event) {
            is HomeUiEvent.FilterChanged -> updateFilter(event.filter)
            is HomeUiEvent.Refresh -> refresh()
            is HomeUiEvent.ItemClicked -> navigateToDetail(event.itemId)
        }
    }

    private fun updateFilter(filter: Filter) {
        _uiState.update { it.copy(selectedFilter = filter) }
        loadItems()
    }

    private fun loadItems() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            try {
                val items = repository.getItems(_uiState.value.selectedFilter)
                _uiState.update { it.copy(items = items, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(error = e.message, isLoading = false)
                }
            }
        }
    }
}

// 4. Composable (Stateless)
@Composable
fun HomeScreen(
    viewModel: HomeViewModel = hiltViewModel(),
    onNavigateToDetail: (Int) -> Unit
) {
    val uiState by viewModel.uiState.collectAsState()

    HomeScreenContent(
        uiState = uiState,
        onEvent = viewModel::onEvent
    )
}

@Composable
private fun HomeScreenContent(
    uiState: HomeUiState,
    onEvent: (HomeUiEvent) -> Unit
) {
    Column {
        FilterChips(
            selectedFilter = uiState.selectedFilter,
            onFilterChange = { onEvent(HomeUiEvent.FilterChanged(it)) }
        )

        when {
            uiState.isLoading -> LoadingIndicator()
            uiState.error != null -> ErrorMessage(uiState.error)
            else -> ItemList(
                items = uiState.items,
                onItemClick = { onEvent(HomeUiEvent.ItemClicked(it)) }
            )
        }
    }
}
```

**Key Principles:**
1. **Single source of truth** - State in ViewModel
2. **Unidirectional data flow** - Events up, State down
3. **Separation of concerns** - UI logic vs Business logic
4. **Testability** - ViewModels easily testable

---

### 75. Best practices for production Compose apps?

**Answer:**

**1. State Management**
```kotlin
// ✅ DO: Hoist state to appropriate level
@Composable
fun Screen() {
    var sharedState by remember { mutableStateOf("") }
    ComponentA(sharedState) { sharedState = it }
    ComponentB(sharedState)
}

// ❌ DON'T: Keep state in multiple places
@Composable
fun BadScreen() {
    ComponentA() // Has its own state
    ComponentB() // Has duplicate state
}
```

**2. Composable Design**
```kotlin
// ✅ DO: Keep composables small and focused
@Composable
fun UserCard(user: User) {
    Card {
        UserAvatar(user.avatarUrl)
        UserInfo(user.name, user.email)
    }
}

// ❌ DON'T: Create god composables
@Composable
fun GiantScreen() {
    // 500 lines of code
}
```

**3. Performance**
```kotlin
// ✅ DO: Use keys in lists
LazyColumn {
    items(items, key = { it.id }) { item ->
        ItemCard(item)
    }
}

// ❌ DON'T: Skip keys
LazyColumn {
    items(items) { item -> // No key
        ItemCard(item)
    }
}
```

**4. Side Effects**
```kotlin
// ✅ DO: Use appropriate effect APIs
@Composable
fun Screen(userId: String) {
    LaunchedEffect(userId) {
        loadUser(userId)
    }
}

// ❌ DON'T: Perform side effects in composition
@Composable
fun BadScreen(userId: String) {
    loadUser(userId) // Runs on every recomposition!
}
```

**5. Testing**
```kotlin
// ✅ DO: Write tests
@Test
fun testUserScreen() {
    composeTestRule.setContent {
        UserScreen(user = testUser)
    }

    composeTestRule
        .onNodeWithText(testUser.name)
        .assertExists()
}
```

**6. Previews**
```kotlin
// ✅ DO: Create multiple previews
@Preview(name = "Light Mode")
@Preview(name = "Dark Mode", uiMode = Configuration.UI_MODE_NIGHT_YES)
@Preview(name = "Large Font", fontScale = 2f)
@Composable
fun UserCardPreview() {
    MyTheme {
        UserCard(sampleUser)
    }
}
```

**7. Modularization**
```kotlin
// Separate into modules
:feature:home
:feature:profile
:core:ui (shared components)
:core:design-system (theme, colors, typography)
```

**8. Accessibility**
```kotlin
// ✅ DO: Add semantics
Text(
    "Close",
    modifier = Modifier.semantics {
        contentDescription = "Close dialog"
        role = Role.Button
    }
)
```

**9. Error Handling**
```kotlin
// ✅ DO: Handle all states
when (uiState) {
    is Loading -> LoadingState()
    is Success -> SuccessState(uiState.data)
    is Error -> ErrorState(uiState.error)
    is Empty -> EmptyState()
}
```

**10. Documentation**
```kotlin
/**
 * Displays a user profile card with avatar and information.
 *
 * @param user The user data to display
 * @param onEditClick Callback when edit button is clicked
 * @param modifier Modifier to be applied to the card
 */
@Composable
fun UserProfileCard(
    user: User,
    onEditClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    // Implementation
}
```
