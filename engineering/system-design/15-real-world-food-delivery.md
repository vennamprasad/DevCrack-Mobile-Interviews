# 🍔 Design a Food Delivery App
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Restaurant listing, real-time order tracking, and cart management.

![Food Delivery](https://img.shields.io/badge/Real_World-Food_Delivery-orange?style=for-the-badge&logo=doordash&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Data Model](#1-restaurant-entity)
- [2. Cart System Logic](#6-cart-repository)
- [3. Order Tracking (WebSocket)](#4-order-repository)
- [4. UI Implementation](#11-restaurant-list-ui)

---

### Q20. How would you design a food delivery app like DoorDash or Uber Eats?

**Answer:**

**Requirements:**
- Browse restaurants
- Search and filter
- Menu with items
- Shopping cart
- Order tracking (real-time)
- Payment processing
- Delivery driver tracking
- Order history

**Architecture:**

```
┌─────────────────────────────────────────────┐
│ Mobile App                                   │
│ - Restaurant List Screen                    │
│ - Restaurant Detail Screen                  │
│ - Cart Screen                               │
│ - Order Tracking Screen                     │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Restaurant Service                          │
│ - Get nearby restaurants                   │
│ - Search restaurants                       │
│ - Get restaurant details                   │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Menu Service                               │
│ - Get menu for restaurant                  │
│ - Search menu items                        │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Cart Service                               │
│ - Add, update, remove items                │
│ - Get cart contents                        │
│ - Clear cart                               │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Order Service                              │
│ - Place new order                          │
│ - Get order status                         │
│ - Cancel order                             │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Payment Service                            │
│ - Process payments                          │
│ - Handle refunds                           │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Notification Service                        │
│ - Send order updates to users              │
│ - Notify drivers of new delivery requests  │
└─────────────────────────────────────────────┘
```

**Implementation:**

```kotlin
// 1. Restaurant Entity
@Entity(tableName = "restaurants")
data class RestaurantEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "name") val name: String,
    @ColumnInfo(name = "cuisine_type") val cuisineType: String,
    @ColumnInfo(name = "rating") val rating: Double,
    @ColumnInfo(name = "delivery_time") val deliveryTime: String,
    @ColumnInfo(name = "delivery_fee") val deliveryFee: Double,
    @ColumnInfo(name = "image_url") val imageUrl: String,
    @ColumnInfo(name = "latitude") val latitude: Double,
    @ColumnInfo(name = "longitude") val longitude: Double,
    @ColumnInfo(name = "is_open") val isOpen: Boolean,
    @ColumnInfo(name = "distance") val distance: Double // km
)

// 2. Menu Item Entity
@Entity(tableName = "menu_items")
data class MenuItemEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "restaurant_id") val restaurantId: String,
    @ColumnInfo(name = "name") val name: String,
    @ColumnInfo(name = "description") val description: String,
    @ColumnInfo(name = "price") val price: Double,
    @ColumnInfo(name = "image_url") val imageUrl: String,
    @ColumnInfo(name = "category") val category: String,
    @ColumnInfo(name = "is_available") val isAvailable: Boolean = true,
    @ColumnInfo(name = "customizations") val customizations: String // JSON
)

// 3. Cart Item Entity
@Entity(tableName = "cart_items")
data class CartItemEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    @ColumnInfo(name = "menu_item_id") val menuItemId: String,
    @ColumnInfo(name = "restaurant_id") val restaurantId: String,
    @ColumnInfo(name = "name") val name: String,
    @ColumnInfo(name = "price") val price: Double,
    @ColumnInfo(name = "quantity") val quantity: Int,
    @ColumnInfo(name = "special_instructions") val specialInstructions: String? = null,
    @ColumnInfo(name = "customizations") val customizations: String // JSON
)

// 4. Order Entity
@Entity(tableName = "orders")
data class OrderEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "user_id") val userId: String,
    @ColumnInfo(name = "restaurant_id") val restaurantId: String,
    @ColumnInfo(name = "items") val items: String, // JSON array of OrderItem
    @ColumnInfo(name = "total_amount") val totalAmount: Double,
    @ColumnInfo(name = "status") val status: OrderStatus,
    @ColumnInfo(name = "created_at") val createdAt: Long,
    @ColumnInfo(name = "updated_at") val updatedAt: Long
)

enum class OrderStatus {
    PENDING, CONFIRMED, PREPARING, READY_FOR_PICKUP, PICKED_UP, ON_THE_WAY, DELIVERED, CANCELLED
}

// 5. Restaurant Repository
class RestaurantRepository @Inject constructor(
    private val apiService: ApiService,
    private val restaurantDao: RestaurantDao,
    private val locationTracker: LocationTracker
) {
    fun getRestaurantsNearby(
        latitude: Double,
        longitude: Double,
        radius: Double = 5.0  // km
    ): Flow<PagingData<Restaurant>> {
        return Pager(
            config = PagingConfig(pageSize = 20),
            pagingSourceFactory = {
                RestaurantPagingSource(apiService, restaurantDao, latitude, longitude, radius)
            }
        ).flow
    }

    suspend fun searchRestaurants(query: String): Result<List<Restaurant>> {
        return try {
            val results = apiService.searchRestaurants(query)
            Result.Success(results)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }

    suspend fun getRestaurantById(restaurantId: String): Result<Restaurant> {
        return try {
            val restaurant = apiService.getRestaurant(restaurantId)
            restaurantDao.insert(restaurant.toEntity())
            Result.Success(restaurant)
        } catch (e: Exception) {
            restaurantDao.getRestaurantById(restaurantId)?.let {
                Result.Success(it.toDomain())
            } ?: Result.Error(e)
        }
    }

    suspend fun getMenu(restaurantId: String): Result<List<MenuItem>> {
        return try {
            val menu = apiService.getMenu(restaurantId)
            Result.Success(menu)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}

// 6. Cart Repository
class CartRepository @Inject constructor(
    private val cartDao: CartDao
) {
    fun getCartItems(): Flow<List<CartItem>> {
        return cartDao.getAllCartItems()
            .map { entities -> entities.map { it.toDomain() } }
    }

    suspend fun addToCart(item: MenuItem, quantity: Int, customizations: Map<String, String>) {
        val cartItem = CartItemEntity(
            menuItemId = item.id,
            restaurantId = item.restaurantId,
            name = item.name,
            price = item.price,
            quantity = quantity,
            customizations = Json.encodeToString(customizations)
        )
        cartDao.insert(cartItem)
    }

    suspend fun updateQuantity(cartItemId: Long, quantity: Int) {
        if (quantity <= 0) {
            cartDao.deleteById(cartItemId)
        } else {
            cartDao.updateQuantity(cartItemId, quantity)
        }
    }

    suspend fun clearCart() {
        cartDao.deleteAll()
    }

    fun getCartTotal(): Flow<Double> {
        return cartDao.getCartTotal()
    }
}

// 7. Order Repository
class OrderRepository @Inject constructor(
    private val apiService: ApiService,
    private val orderDao: OrderDao,
    private val webSocketManager: OrderWebSocketManager
) {
    suspend fun placeOrder(
        restaurantId: String,
        cartItems: List<CartItem>,
        deliveryAddress: Address,
        paymentMethodId: String
    ): Result<Order> {
        return try {
            val orderRequest = CreateOrderRequest(
                restaurantId = restaurantId,
                items = cartItems.map { it.toOrderItem() },
                deliveryAddress = deliveryAddress,
                paymentMethodId = paymentMethodId
            )

            val order = apiService.placeOrder(orderRequest)
            orderDao.insert(order.toEntity())

            Result.Success(order)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }

    fun getOrders(): Flow<List<Order>> {
        return orderDao.getAllOrders()
            .map { entities -> entities.map { it.toDomain() } }
    }

    fun observeOrderUpdates(orderId: String): Flow<OrderUpdate> {
        return webSocketManager.observeOrder(orderId)
    }

    fun observeDriverLocation(driverId: String): Flow<LatLng> {
        return webSocketManager.observeDriverLocation(driverId)
    }
}

// 8. Restaurant List ViewModel
@HiltViewModel
class RestaurantListViewModel @Inject constructor(
    private val restaurantRepository: RestaurantRepository,
    private val locationTracker: LocationTracker
) : ViewModel() {

    private val _currentLocation = MutableStateFlow<LatLng?>(null)

    val restaurants: Flow<PagingData<Restaurant>> = _currentLocation
        .filterNotNull()
        .flatMapLatest { location ->
            restaurantRepository.getRestaurantsNearby(
                latitude = location.latitude,
                longitude = location.longitude
            )
        }
        .cachedIn(viewModelScope)

    init {
        viewModelScope.launch {
            locationTracker.getCurrentLocation()?.let {
                _currentLocation.value = LatLng(it.latitude, it.longitude)
            }
        }
    }

    fun searchRestaurants(query: String) {
        // Implementation
    }
}

// 9. Cart ViewModel
@HiltViewModel
class CartViewModel @Inject constructor(
    private val cartRepository: CartRepository,
    private val orderRepository: OrderRepository
) : ViewModel() {

    val cartItems: StateFlow<List<CartItem>> = cartRepository
        .getCartItems()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    val cartTotal: StateFlow<Double> = cartRepository
        .getCartTotal()
        .stateIn(viewModelScope, SharingStarted.Lazily, 0.0)

    private val _checkoutState = MutableStateFlow<CheckoutState>(CheckoutState.Idle)
    val checkoutState = _checkoutState.asStateFlow()

    fun updateQuantity(cartItemId: Long, quantity: Int) {
        viewModelScope.launch {
            cartRepository.updateQuantity(cartItemId, quantity)
        }
    }

    fun checkout(deliveryAddress: Address, paymentMethodId: String) {
        viewModelScope.launch {
            _checkoutState.value = CheckoutState.Processing

            val items = cartItems.value
            if (items.isEmpty()) {
                _checkoutState.value = CheckoutState.Error("Cart is empty")
                return@launch
            }

            val restaurantId = items.first().restaurantId

            when (val result = orderRepository.placeOrder(
                restaurantId = restaurantId,
                cartItems = items,
                deliveryAddress = deliveryAddress,
                paymentMethodId = paymentMethodId
            )) {
                is Result.Success -> {
                    cartRepository.clearCart()
                    _checkoutState.value = CheckoutState.Success(result.data)
                }
                is Result.Error -> {
                    _checkoutState.value = CheckoutState.Error(result.exception.message)
                }
            }
        }
    }
}

sealed class CheckoutState {
    object Idle : CheckoutState()
    object Processing : CheckoutState()
    data class Success(val order: Order) : CheckoutState()
    data class Error(val message: String?) : CheckoutState()
}

// 10. Order Tracking ViewModel
@HiltViewModel
class OrderTrackingViewModel @Inject constructor(
    private val orderRepository: OrderRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val orderId: String = savedStateHandle["orderId"]!!

    private val _orderState = MutableStateFlow<OrderTrackingState>(OrderTrackingState.Loading)
    val orderState = _orderState.asStateFlow()

    private val _driverLocation = MutableStateFlow<LatLng?>(null)
    val driverLocation = _driverLocation.asStateFlow()

    init {
        trackOrder()
    }

    private fun trackOrder() {
        viewModelScope.launch {
            orderRepository.observeOrderUpdates(orderId).collect { update ->
                when (update) {
                    is OrderUpdate.StatusChanged -> {
                        _orderState.value = OrderTrackingState.Success(
                            order = update.order,
                            estimatedTime = update.estimatedTime
                        )

                        // Start tracking driver if picked up
                        if (update.order.status == OrderStatus.PICKED_UP) {
                            update.order.driverId?.let { driverId ->
                                trackDriver(driverId)
                            }
                        }
                    }
                }
            }
        }
    }

    private fun trackDriver(driverId: String) {
        viewModelScope.launch {
            orderRepository.observeDriverLocation(driverId).collect { location ->
                _driverLocation.value = location
            }
        }
    }
}

sealed class OrderTrackingState {
    object Loading : OrderTrackingState()
    data class Success(val order: Order, val estimatedTime: Long) : OrderTrackingState()
    data class Error(val message: String?) : OrderTrackingState()
}

// 11. Restaurant List UI
@Composable
fun RestaurantListScreen(
    viewModel: RestaurantListViewModel = hiltViewModel()
) {
    val restaurants = viewModel.restaurants.collectAsLazyPagingItems()

    LazyColumn {
        items(
            count = restaurants.itemCount,
            key = { index -> restaurants[index]?.id ?: index }
        ) { index ->
            restaurants[index]?.let { restaurant ->
                RestaurantCard(restaurant = restaurant)
            }
        }
    }
}

@Composable
fun RestaurantCard(restaurant: Restaurant) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable { /* Navigate to restaurant detail */ }
    ) {
        Row {
            AsyncImage(
                model = restaurant.imageUrl,
                contentDescription = null,
                modifier = Modifier
                    .size(100.dp)
                    .clip(RoundedCornerShape(8.dp)),
                contentScale = ContentScale.Crop
            )

            Column(modifier = Modifier.padding(12.dp)) {
                Text(
                    text = restaurant.name,
                    style = MaterialTheme.typography.subtitle1,
                    fontWeight = FontWeight.Bold
                )

                Text(
                    text = restaurant.cuisineType,
                    style = MaterialTheme.typography.body2,
                    color = Color.Gray
                )

                Spacer(modifier = Modifier.height(4.dp))

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.Star,
                        contentDescription = null,
                        tint = Color(0xFFFFC107),
                        modifier = Modifier.size(16.dp)
                    )
                    Text(
                        text = restaurant.rating.toString(),
                        style = MaterialTheme.typography.caption
                    )

                    Spacer(modifier = Modifier.width(8.dp))

                    Text(
                        text = restaurant.deliveryTime,
                        style = MaterialTheme.typography.caption,
                        color = Color.Gray
                    )

                    Spacer(modifier = Modifier.width(8.dp))

                    Text(
                        text = "$${restaurant.deliveryFee} delivery",
                        style = MaterialTheme.typography.caption,
                        color = Color.Gray
                    )
                }

                if (!restaurant.isOpen) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "Closed",
                        style = MaterialTheme.typography.caption,
                        color = Color.Red
                    )
                }
            }
        }
    }
}

// 12. Order Tracking UI
@Composable
fun OrderTrackingScreen(
    orderId: String,
    viewModel: OrderTrackingViewModel = hiltViewModel()
) {
    val orderState by viewModel.orderState.collectAsState()
    val driverLocation by viewModel.driverLocation.collectAsState()

    when (val state = orderState) {
        is OrderTrackingState.Success -> {
            Column(modifier = Modifier.fillMaxSize()) {
                // Map showing driver location
                if (driverLocation != null) {
                    GoogleMap(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f)
                    ) {
                        Marker(
                            state = MarkerState(position = driverLocation!!),
                            title = "Delivery Driver"
                        )
                    }
                }

                // Order status
                OrderStatusTimeline(order = state.order)

                // Estimated time
                Text(
                    text = "Estimated delivery: ${formatTime(state.estimatedTime)}",
                    modifier = Modifier.padding(16.dp),
                    style = MaterialTheme.typography.h6
                )
            }
        }
        is OrderTrackingState.Loading -> {
            CircularProgressIndicator()
        }
        is OrderTrackingState.Error -> {
            Text(text = "Error: ${state.message}")
        }
    }
}

@Composable
fun OrderStatusTimeline(order: Order) {
    val statuses = listOf(
        OrderStatus.CONFIRMED,
        OrderStatus.PREPARING,
        OrderStatus.READY_FOR_PICKUP,
        OrderStatus.PICKED_UP,
        OrderStatus.ON_THE_WAY,
        OrderStatus.DELIVERED
    )

    Column(modifier = Modifier.padding(16.dp)) {
        statuses.forEach { status ->
            Row(verticalAlignment = Alignment.CenterVertically) {
                val isCompleted = statuses.indexOf(status) <= statuses.indexOf(order.status)

                Icon(
                    imageVector = if (isCompleted) Icons.Default.CheckCircle else Icons.Outlined.Circle,
                    contentDescription = null,
                    tint = if (isCompleted) Color.Green else Color.Gray,
                    modifier = Modifier.size(24.dp)
                )

                Spacer(modifier = Modifier.width(12.dp))

                Text(
                    text = status.name.replace("_", " ").lowercase().capitalize(),
                    style = MaterialTheme.typography.body1,
                    color = if (isCompleted) Color.Black else Color.Gray
                )
            }

            if (status != statuses.last()) {
                Spacer(modifier = Modifier.height(8.dp))
            }
        }
    }
}

---

# Summary

This comprehensive guide covers:

**Part 1: Fundamentals**
- Scalability, Caching, Load Balancing
- Databases, APIs, Message Queues
- CDN, Monitoring

**Part 2: Mobile Patterns**
- MVVM, Clean Architecture
- Offline-First Design

**Part 3: Real-World Examples**
- Chat App (WhatsApp)
- Social Feed (Instagram)
- Ride-Sharing (Uber)
- Video Streaming (YouTube)
- Food Delivery (DoorDash)

Each example includes complete Kotlin code with:
- Data models and entities
- Repository pattern
- ViewModels with state management
- Composable UI components
- Real-time updates via WebSocket
- Offline support
- Performance optimizations

**Interview Tips:**
1. Start with requirements gathering
2. Draw high-level architecture
3. Discuss trade-offs
4. Mention scalability considerations
5. Talk about mobile-specific challenges
6. Provide code examples when relevant
