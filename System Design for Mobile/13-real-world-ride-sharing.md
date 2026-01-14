# 🚗 Design a Ride-Sharing App
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Real-time driver tracking, matching, and payment processing.

![Ride Sharing](https://img.shields.io/badge/Real_World-Ride_Sharing-black?style=for-the-badge&logo=uber&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Architecture](#architecture)
- [2. Request Ride Flow](#2-ride-repository)
- [3. Real-time Tracking](#4-ride-request-ui)

---

### Q18. How would you design a ride-sharing app like Uber?

**Answer:**

**Requirements:**
- Real-time driver location tracking
- Request ride
- Match driver with rider
- Live ETA updates
- Payment processing
- Ride history

**Architecture:**

```
┌─────────────────────────────────────────────┐
│ Mobile App                                   │
│ - Map Screen                                │
│ - Ride Request Screen                       │
│ - Ride Tracking Screen                      │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Location Tracking Service                    │
│ - Track user and driver locations          │
│ - Update ride status in real-time         │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Ride Management Service                      │
│ - Match riders with drivers                 │
│ - Calculate ETA and fare                   │
│ - Handle ride requests and cancellations   │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Payment Service                             │
│ - Process payments                          │
│ - Handle tips and discounts                 │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Notification Service                        │
│ - Send ride updates to users                │
│ - Notify drivers of new ride requests      │
└─────────────────────────────────────────────┘
```

**Implementation:**

```kotlin
// 1. Ride Request Entity
@Entity(tableName = "ride_requests")
data class RideRequestEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "rider_id") val riderId: String,
    @ColumnInfo(name = "driver_id") val driverId: String?,
    @ColumnInfo(name = "pickup_location") val pickupLocation: LatLng,
    @ColumnInfo(name = "dropoff_location") val dropoffLocation: LatLng,
    @ColumnInfo(name = "status") val status: RideStatus,
    @ColumnInfo(name = "requested_at") val requestedAt: Long,
    @ColumnInfo(name = "updated_at") val updatedAt: Long
)

enum class RideStatus {
    PENDING, ACCEPTED, PICKED_UP, DROPPED_OFF, CANCELLED
}

// 2. Ride Repository
class RideRepository @Inject constructor(
    private val apiService: ApiService,
    private val rideDao: RideDao,
    private val locationTracker: LocationTracker
) {
    fun requestRide(
        pickup: LatLng,
        dropoff: LatLng
    ): Flow<Result<RideRequest>> = flow {
        val rideRequest = RideRequestEntity(
            id = UUID.randomUUID().toString(),
            riderId = currentUserId,
            driverId = null,
            pickupLocation = pickup,
            dropoffLocation = dropoff,
            status = RideStatus.PENDING,
            requestedAt = System.currentTimeMillis(),
            updatedAt = System.currentTimeMillis()
        )

        // Save locally
        rideDao.insert(rideRequest)

        emit(Result.Success(rideRequest.toDomain()))

        // Request ride from API
        try {
            val response = apiService.requestRide(rideRequest)
            emit(Result.Success(response))
        } catch (e: Exception) {
            emit(Result.Error(e))
        }
    }

    fun observeRideRequests(): Flow<List<RideRequest>> {
        return rideDao.getAllRideRequests()
            .map { entities -> entities.map { it.toDomain() } }
    }
}

// 3. Ride ViewModel
@HiltViewModel
class RideViewModel @Inject constructor(
    private val rideRepository: RideRepository
) : ViewModel() {

    val rideRequests: StateFlow<List<RideRequest>> = rideRepository
        .observeRideRequests()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    fun requestRide(pickup: LatLng, dropoff: LatLng) {
        viewModelScope.launch {
            rideRepository.requestRide(pickup, dropoff).collect { result ->
                // Handle result (show UI updates, errors, etc.)
            }
        }
    }
}

// 4. Ride Request UI
@Composable
fun RideRequestScreen(
    viewModel: RideViewModel = hiltViewModel()
) {
    val rideRequests by viewModel.rideRequests.collectAsState()

    Column(modifier = Modifier.fillMaxSize()) {
        // Header
        TopAppBar(
            title = { Text("Ride Requests") },
            actions = {
                IconButton(onClick = { /* Refresh */ }) {
                    Icon(Icons.Default.Refresh, contentDescription = "Refresh")
                }
            }
        )

        // Ride requests list
        LazyColumn {
            items(rideRequests) { request ->
                RideRequestItem(request)
            }
        }
    }
}

@Composable
fun RideRequestItem(request: RideRequest) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable { /* Navigate to ride details */ }
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(
                text = "Ride from ${request.pickupLocation} to ${request.dropoffLocation}",
                style = MaterialTheme.typography.subtitle1
            )

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = "Status: ${request.status}",
                style = MaterialTheme.typography.body2,
                color = Color.Gray
            )
        }
    }
}
```

**Key Features:**

1. **Real-time Tracking**: Driver and rider locations
2. **WebSocket**: Live updates for ride status
3. **Offline Support**: Cached ride requests
4. **Push Notifications**: For ride updates
5. **Payment Integration**: Secure payment processing

---
