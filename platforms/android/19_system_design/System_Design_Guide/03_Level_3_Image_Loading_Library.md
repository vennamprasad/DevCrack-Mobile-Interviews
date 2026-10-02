# 🖼️ Level 3: Design an Image Loading Library from Scratch (Glide / Coil / Kingfisher)

> **High-performance mobile image loading architecture: Multi-tier caching (L1 RAM LRU, L2 BitmapPool, L3 Disk), preventing OOMs via inSampleSize downsampling, request coalescing, and lifecycle-aware cancellation.**

---

## 📌 Executive Summary & Interview Framing

**"Design an Image Loading Library like Glide, Picasso, Coil, or Kingfisher"** is a quintessential Senior and Staff Mobile System Design question asked by Meta, Google, Uber, and Pinterest.

The problem seems simple on the surface ("download a URL and put it into a View"), but at scale, it presents the most brutal performance traps in mobile development:
1. **Uncompressed Bitmap Memory (OOM Catastrophe)**: A single 12MP smartphone photo (4000 × 3000) takes **~48 MB of RAM** when decoded in `ARGB_8888`. Loading 3 such images in a feed will instantly crash the app with an `OutOfMemoryError`.
2. **Garbage Collection Thrashing & Jank**: Constantly allocating and destroying large bitmap byte arrays forces the GC to pause the main thread, dropping frame rates below 60fps.
3. **RecyclerView / LazyColumn Recycling Race Conditions**: Fast scrolling recycles views, causing images to flicker and show the wrong avatar on the wrong list row.

---

## 🏗️ End-to-End Pipeline Architecture

```
                                [ ImageRequest (URL, Target ImageView/Composable) ]
                                                        │
                                                        ▼
                                       ┌────────────────────────────────┐
                                       │ 1. Request Coalescing Manager  │
                                       │ (Deduplicates identical URLs)  │
                                       └────────────────┬───────────────┘
                                                        │
                                                        ▼
                        ┌────────────────────────────────────────────────────────┐
                        │              2. Multi-Tier Cache Engine                │
                        └───────┬───────────────────────┬────────────────┬───────┘
                                │                       │                │
                          (Cache Hit)             (Cache Hit)      (Cache Miss)
                                ▼                       ▼                ▼
                        [ L1 Memory Cache ]     [ L3 Disk Cache ]  [ L4 Network ]
                        (LRU in RAM: <2ms)     (DiskLruCache)      (OkHttp / CDN)
                                                        │                │
                                                        └────────┬───────┘
                                                                 │
                                                                 ▼
                                       ┌────────────────────────────────┐
                                       │ 3. Downsampler & BitmapPool    │
                                       │ • inJustDecodeBounds           │
                                       │ • inSampleSize (Resize to View)│
                                       │ • inBitmap (Reuses RAM buffer) │
                                       └────────────────┬───────────────┘
                                                        │
                                                        ▼
                                       ┌────────────────────────────────┐
                                       │ 4. Main-Thread UI Dispatcher   │
                                       │ • Crossfade animation          │
                                       │ • Lifecycle cancel verification│
                                       └────────────────────────────────┘
```

---

## 💾 Multi-Tier Caching Strategy

| Cache Tier | Storage Medium | Lookup Latency | Eviction Policy & Size Budget | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **L1: Memory Cache** | Heap RAM (`LruCache<String, Bitmap>`) | **< 2 ms** | Least Recently Used (LRU). Typically allocated **20% to 25% of available JVM heap**. | Instant display for currently visible and recently viewed images. |
| **L2: BitmapPool** | Reusable byte allocations | **0 ms allocation** | Reuses mutable byte buffers via `BitmapFactory.Options.inBitmap`. | Eliminates GC churn by preventing continuous memory re-allocation. |
| **L3: Disk Cache** | Flash Storage (`DiskLruCache`) | **10 – 30 ms** | LRU with storage quota (e.g., 250 MB). Keyed by `SHA-256(URL)`. | Persists images across app cold restarts without network calls. |
| **L4: Network / CDN** | Remote Edge Server | **100 – 1500 ms** | Controlled by HTTP `Cache-Control` / `ETag`. | Source of truth for new or modified media assets. |

---

## 🔬 Preventing OOMs: Mathematical Downsampling & BitmapPool

### 1. Downsampling with `inJustDecodeBounds`
Never decode the full raw image stream into memory! If the target view is 200×200 pixels, decode **only 200×200 pixels**:

```kotlin
fun decodeSampledBitmapFromStream(
    inputStreamProvider: () -> InputStream,
    reqWidth: Int,
    reqHeight: Int,
    bitmapPool: BitmapPool?
): Bitmap {
    val options = BitmapFactory.Options().apply {
        // Step 1: Read image dimensions ONLY without allocating pixel memory in RAM
        inJustDecodeBounds = true
    }
    
    inputStreamProvider().use { BitmapFactory.decodeStream(it, null, options) }

    // Step 2: Compute inSampleSize (power of 2)
    options.inSampleSize = calculateInSampleSize(options.outWidth, options.outHeight, reqWidth, reqHeight)

    // Step 3: Enable inJustDecodeBounds = false to actually decode pixels
    options.inJustDecodeBounds = false

    // Step 4: Recycle existing memory buffer from BitmapPool if available
    bitmapPool?.get(options.outWidth, options.outHeight, options.inPreferredConfig)?.let { reusableBitmap ->
        options.inBitmap = reusableBitmap
        options.inMutable = true
    }

    return inputStreamProvider().use { BitmapFactory.decodeStream(it, null, options) }!!
}

private fun calculateInSampleSize(rawWidth: Int, rawHeight: Int, reqWidth: Int, reqHeight: Int): Int {
    var inSampleSize = 1
    if (rawHeight > reqHeight || rawWidth > reqWidth) {
        val halfHeight = rawHeight / 2
        val halfWidth = rawWidth / 2
        while ((halfHeight / inSampleSize) >= reqHeight && (halfWidth / inSampleSize) >= reqWidth) {
            inSampleSize *= 2
        }
    }
    return inSampleSize
}
```

### 2. Memory Recycling with `BitmapPool` & `inBitmap`
In older architectures, when an image scrolls off-screen, it is dereferenced and garbage collected. When a new image scrolls in, a new 10 MB allocation occurs. This causes **GC thrashing**.

Using `inBitmap`:
- Instead of allocating new native memory, the JVM tells Android's decoder: **"Re-use this existing allocated byte array to draw the new image."**
- **Allocation overhead drops to 0 bytes.**

---

## ⚡ Request Coalescing (Deduplication)

If a user opens a screen containing a grid where 5 image views display the same creator avatar (`avatar_90.jpg`), a naive library makes 5 identical network calls.

### The Solution: Shared Deferred Jobs
Maintain an in-flight request map:
```kotlin
class RequestCoalescer {
    private val inFlightRequests = ConcurrentHashMap<String, Deferred<Bitmap>>()

    suspend fun load(url: String, fetcher: suspend () -> Bitmap): Bitmap {
        val deferred = inFlightRequests.computeIfAbsent(url) {
            CoroutineScope(Dispatchers.IO).async {
                try {
                    fetcher()
                } finally {
                    inFlightRequests.remove(url)
                }
            }
        }
        return deferred.await()
    }
}
```
All 5 views attach to the single `Deferred` job. When the network returns, all 5 views are populated simultaneously.

---

## 🛑 Lifecycle-Aware Cancellation & Fast Scrolling

When a user rapidly flings through a list of 100 items:
- Items 1 to 20 enter and leave the screen in **less than 500 milliseconds**.
- If network requests for items 1 to 20 continue downloading, they congest the network queue and delay item 21 (which the user is actually looking at!).

### Implementation:
1. Bind the loading Coroutine job to the view's lifecycle:
   ```kotlin
   // In Compose:
   @Composable
   fun AsyncImage(url: String, contentDescription: String?) {
       var bitmap by remember { mutableStateOf<Bitmap?>(null) }
       
       // LaunchedEffect automatically cancels the coroutine when this composable leaves composition!
       LaunchedEffect(url) {
           bitmap = ImageLoader.load(url)
       }
       
       bitmap?.let { Image(bitmap = it.asImageBitmap(), contentDescription = contentDescription) }
   }
   ```
2. When the job is cancelled:
   - Cancel the underlying OkHttp `Call` immediately.
   - Close the network socket stream.

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "What is `Bitmap.Config.HARDWARE` on Android, and what are its performance tradeoffs?"
* **Answer**:
  - Introduced in Android 8.0 (API 26), `HARDWARE` config allocates bitmap pixel memory directly in **GPU graphic memory (GraphicBuffer)** instead of JVM heap or native C++ heap.
  - **Advantages**:
    - **Zero JVM Heap Overhead**: Bitmaps cannot cause JVM OOM crashes.
    - **Fast Rendering**: The bitmap is already on the GPU; no CPU-to-GPU texture upload transfer overhead over PCIe/bus.
  - **Disadvantages**:
    - Immutable (cannot be edited or drawn onto via `Canvas` on the CPU).
    - Cannot be recycled into a standard `BitmapPool` via `inBitmap`.

### Q2: "How do you avoid thread starvation in an image loading library?"
* **Answer**:
  - Never use a single global thread pool for all tasks!
  - **Segregate Dispatchers by I/O and CPU profiles**:
    1. **Network Dispatcher**: Dedicated thread pool of 4 to 8 threads (I/O bound).
    2. **Disk Cache Dispatcher**: Dedicated thread pool of 2 threads (Disk bound; prevents disk head contention and flash bus saturation).
    3. **Decoding Dispatcher**: Dedicated thread pool sized to `Runtime.getRuntime().availableProcessors()` (CPU bound).
