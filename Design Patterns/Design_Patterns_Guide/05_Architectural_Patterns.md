## **Architectural Patterns**

### Q13. What is MVVM (Model-View-ViewModel)?

**Answer:**
MVVM separates UI logic from business logic using ViewModel as a mediator.

**Complete Implementation:**
```kotlin
// Model - Data layer
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Repository
class UserRepository(
    private val apiService: ApiService,
    private val userDao: UserDao
) {
    suspend fun getUsers(): List<User> {
        return try {
            val users = apiService.getUsers()
            userDao.insertAll(users)
            users
        } catch (e: Exception) {
            userDao.getAllUsers()
        }
    }

    suspend fun getUserById(id: Int): User? {
        return userDao.getUserById(id)
    }
}

// ViewModel
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    sealed class UiState {
        object Loading : UiState()
        data class Success(val users: List<User>) : UiState()
        data class Error(val message: String) : UiState()
    }

    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            try {
                val users = repository.getUsers()
                _uiState.value = UiState.Success(users)
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Unknown error")
            }
        }
    }

    fun retry() {
        loadUsers()
    }
}

// View (Activity/Fragment)
@AndroidEntryPoint
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    private lateinit var binding: FragmentUserBinding
    private val adapter = UserAdapter()

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentUserBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupRecyclerView()
        observeUiState()
        viewModel.loadUsers()
    }

    private fun setupRecyclerView() {
        binding.recyclerView.adapter = adapter
    }

    private fun observeUiState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.uiState.collect { state ->
                when (state) {
                    is UserViewModel.UiState.Loading -> showLoading()
                    is UserViewModel.UiState.Success -> showUsers(state.users)
                    is UserViewModel.UiState.Error -> showError(state.message)
                }
            }
        }
    }

    private fun showLoading() {
        binding.progressBar.visibility = View.VISIBLE
        binding.recyclerView.visibility = View.GONE
        binding.errorLayout.visibility = View.GONE
    }

    private fun showUsers(users: List<User>) {
        binding.progressBar.visibility = View.GONE
        binding.recyclerView.visibility = View.VISIBLE
        binding.errorLayout.visibility = View.GONE
        adapter.submitList(users)
    }

    private fun showError(message: String) {
        binding.progressBar.visibility = View.GONE
        binding.recyclerView.visibility = View.GONE
        binding.errorLayout.visibility = View.VISIBLE
        binding.errorText.text = message
        binding.retryButton.setOnClickListener {
            viewModel.retry()
        }
    }
}
```

**Benefits:**
- Clear separation of concerns
- Testable business logic
- Lifecycle awareness
- Reactive data flow

**When to use:**
- Modern Android apps (recommended by Google)
- Complex UI logic
- Need for testability

---

### Q14. What is MVP (Model-View-Presenter)?

**Answer:**
MVP separates UI from logic where Presenter acts as a middleman between View and Model.

**Implementation:**
```kotlin
// Contract
interface UserContract {
    interface View {
        fun showLoading()
        fun hideLoading()
        fun showUsers(users: List<User>)
        fun showError(message: String)
    }

    interface Presenter {
        fun attach(view: View)
        fun detach()
        fun loadUsers()
    }
}

// Model
class UserModel(private val apiService: ApiService) {
    suspend fun getUsers(): List<User> {
        return apiService.getUsers()
    }
}

// Presenter
class UserPresenter(
    private val model: UserModel,
    private val coroutineScope: CoroutineScope
) : UserContract.Presenter {

    private var view: UserContract.View? = null

    override fun attach(view: UserContract.View) {
        this.view = view
    }

    override fun detach() {
        view = null
    }

    override fun loadUsers() {
        view?.showLoading()
        coroutineScope.launch {
            try {
                val users = model.getUsers()
                view?.hideLoading()
                view?.showUsers(users)
            } catch (e: Exception) {
                view?.hideLoading()
                view?.showError(e.message ?: "Unknown error")
            }
        }
    }
}

// View (Activity)
class UserActivity : AppCompatActivity(), UserContract.View {
    private lateinit var binding: ActivityUserBinding
    private lateinit var presenter: UserContract.Presenter
    private val adapter = UserAdapter()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityUserBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val model = UserModel(apiService)
        presenter = UserPresenter(model, lifecycleScope)
        presenter.attach(this)

        binding.recyclerView.adapter = adapter
        presenter.loadUsers()
    }

    override fun onDestroy() {
        super.onDestroy()
        presenter.detach()
    }

    override fun showLoading() {
        binding.progressBar.visibility = View.VISIBLE
    }

    override fun hideLoading() {
        binding.progressBar.visibility = View.GONE
    }

    override fun showUsers(users: List<User>) {
        adapter.submitList(users)
    }

    override fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
```

**MVP vs MVVM:**

| Feature | MVP | MVVM |
|---------|-----|------|
| **View-Logic coupling** | View interface | Data binding |
| **Lifecycle** | Manual attach/detach | Automatic |
| **Testing** | Mock View interface | No View needed |
| **Boilerplate** | More (interfaces) | Less |
| **Learning curve** | Easier | Moderate |

**When to use:**
- Legacy Android apps
- Don't want data binding
- More control over View updates

---

### Q15. What is MVI (Model-View-Intent)?

**Answer:**
MVI is a unidirectional data flow pattern where user intents trigger state changes.

**Implementation:**
```kotlin
// Intent - User actions
sealed class UserIntent {
    object LoadUsers : UserIntent()
    data class SearchUsers(val query: String) : UserIntent()
    data class DeleteUser(val userId: Int) : UserIntent()
    object Refresh : UserIntent()
}

// State - UI state
data class UserViewState(
    val isLoading: Boolean = false,
    val users: List<User> = emptyList(),
    val error: String? = null,
    val searchQuery: String = ""
)

// ViewModel
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _state = MutableStateFlow(UserViewState())
    val state: StateFlow<UserViewState> = _state.asStateFlow()

    fun processIntent(intent: UserIntent) {
        when (intent) {
            is UserIntent.LoadUsers -> loadUsers()
            is UserIntent.SearchUsers -> searchUsers(intent.query)
            is UserIntent.DeleteUser -> deleteUser(intent.userId)
            is UserIntent.Refresh -> refresh()
        }
    }

    private fun loadUsers() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, error = null) }
            try {
                val users = repository.getUsers()
                _state.update {
                    it.copy(
                        isLoading = false,
                        users = users,
                        error = null
                    )
                }
            } catch (e: Exception) {
                _state.update {
                    it.copy(
                        isLoading = false,
                        error = e.message
                    )
                }
            }
        }
    }

    private fun searchUsers(query: String) {
        _state.update { it.copy(searchQuery = query) }
        viewModelScope.launch {
            val filteredUsers = repository.searchUsers(query)
            _state.update { it.copy(users = filteredUsers) }
        }
    }

    private fun deleteUser(userId: Int) {
        viewModelScope.launch {
            repository.deleteUser(userId)
            val updatedUsers = _state.value.users.filter { it.id != userId }
            _state.update { it.copy(users = updatedUsers) }
        }
    }

    private fun refresh() {
        loadUsers()
    }
}

// View
@AndroidEntryPoint
class UserFragment : Fragment() {
    private val viewModel: UserViewModel by viewModels()
    private lateinit var binding: FragmentUserBinding
    private val adapter = UserAdapter { user ->
        viewModel.processIntent(UserIntent.DeleteUser(user.id))
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        setupViews()
        observeState()
        sendIntent(UserIntent.LoadUsers)
    }

    private fun setupViews() {
        binding.recyclerView.adapter = adapter

        binding.searchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextChange(newText: String): Boolean {
                sendIntent(UserIntent.SearchUsers(newText))
                return true
            }

            override fun onQueryTextSubmit(query: String) = true
        })

        binding.refreshLayout.setOnRefreshListener {
            sendIntent(UserIntent.Refresh)
        }
    }

    private fun observeState() {
        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.state.collect { state ->
                render(state)
            }
        }
    }

    private fun render(state: UserViewState) {
        binding.progressBar.isVisible = state.isLoading
        binding.refreshLayout.isRefreshing = false

        if (state.error != null) {
            showError(state.error)
        } else {
            adapter.submitList(state.users)
        }
    }

    private fun sendIntent(intent: UserIntent) {
        viewModel.processIntent(intent)
    }

    private fun showError(message: String) {
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
    }
}
```

**Key Principles:**
1. **Intent** - User actions
2. **State** - Single source of truth
3. **Unidirectional flow** - Intent � Process � State � Render

**Benefits:**
- Predictable state changes
- Easy to debug (state history)
- Testable
- Time-travel debugging possible

**When to use:**
- Complex state management
- Need predictability
- Large teams
