## **7. Converting Callbacks to Flows**

### **Problem**: Legacy callback APIs need to work with Flows

**Using `callbackFlow`**:
```kotlin
class LocationRepository(private val locationManager: LocationManager) {

    fun observeLocation(): Flow<Location> = callbackFlow {
        val callback = object : LocationListener {
            override fun onLocationChanged(location: Location) {
                trySend(location)  // Send to flow
            }

            override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {}
            override fun onProviderEnabled(provider: String) {}
            override fun onProviderDisabled(provider: String) {
                close(Exception("Location provider disabled"))
            }
        }

        // Register callback
        locationManager.requestLocationUpdates(
            LocationManager.GPS_PROVIDER,
            1000L,
            10f,
            callback
        )

        // Cleanup when flow is canceled
        awaitClose {
            locationManager.removeUpdates(callback)
        }
    }
}

// Firebase Firestore example
fun observeDocument(docId: String): Flow<Document> = callbackFlow {
    val listener = firestore.collection("docs")
        .document(docId)
        .addSnapshotListener { snapshot, error ->
            if (error != null) {
                close(error)
                return@addSnapshotListener
            }

            snapshot?.let { trySend(it.toObject(Document::class.java)!!) }
        }

    awaitClose { listener.remove() }
}
```
