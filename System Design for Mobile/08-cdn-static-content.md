# 🌎 CDN & Static Content
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Improve performance by serving content from the edge.

![CDN](https://img.shields.io/badge/Performance-CDN-blueviolet?style=for-the-badge&logo=cloudflare&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Architecture & Benefits](#cdn-architecture)
- [2. Image Delivery Strategy](#1-image-delivery-via-cdn)
- [3. Progressive Loading](#2-progressive-image-loading)

---

### Q9. What is a CDN and how does it improve mobile app performance?

**Answer:**

A Content Delivery Network (CDN) is a geographically distributed network of servers that delivers static content (images, videos, CSS, JS) from locations closest to users.

**CDN Architecture:**

```
┌─────────────────────────────────────────────┐
│ CDN Edge Servers                           │
│ - Cache static content                     │
│ - Serve from nearest location              │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Origin Server (API)                        │
│ - Dynamic content                          │
│ - Business logic                           │
└─────────────────────────────────────────────┘
```

**Benefits:**

| Benefit | Impact | Example |
|---------|--------|---------|
| **Reduced Latency** | Content served from nearest edge location | Image loads in 50ms instead of 200ms |
| **Lower Bandwidth** | Cached content reduces origin server load | Saves 70% of bandwidth during peak times |
| **Improved Availability** | Content served from multiple locations | High availability even during server maintenance |
| **DDoS Protection** | Distributed nature absorbs attacks | Protects origin server from being overwhelmed |

**1. Image Delivery via CDN:**

```kotlin
// Image URLs with CDN
data class Post(
    val id: String,
    val content: String,
    // Original URL (stored in database)
    val originalImageUrl: String,
    // CDN URL (what mobile app uses)
    val cdnImageUrl: String
)

// Example URLs
/*
Original: https://api.example.com/uploads/images/12345.jpg
CDN:      https://cdn.example.com/images/12345.jpg

Benefits:
- CDN serves from nearest location
- Origin server not hit for every image request
- Can transform images on-the-fly
*/

// CDN with image transformations
class ImageUrlBuilder {
    private val cdnBase = "https://cdn.example.com"

    fun buildImageUrl(
        imageId: String,
        width: Int? = null,
        height: Int? = null,
        quality: Int = 80,
        format: String = "webp"
    ): String {
        val params = buildList {
            width?.let { add("w=$it") }
            height?.let { add("h=$it") }
            add("q=$quality")
            add("f=$format")
        }.joinToString("&")

        return "$cdnBase/images/$imageId?$params"
    }
}

// Usage in Compose
@Composable
fun UserAvatar(imageUrl: String) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(imageUrl)
            .crossfade(true)
            .memoryCachePolicy(CachePolicy.ENABLED)
            .diskCachePolicy(CachePolicy.ENABLED)
            .build(),
        contentDescription = "Avatar"
    )
}
```

**2. Progressive Image Loading:**

```kotlin
@Composable
fun ProgressiveImage(imageUrl: String) {
    val lowQualityUrl = "$imageUrl?q=20&blur=5"  // Tiny, blurred placeholder
    val highQualityUrl = "$imageUrl?q=85"        // Full quality

    var isHighQualityLoaded by remember { mutableStateOf(false) }

    Box {
        // Show low quality immediately
        AsyncImage(
            model = lowQualityUrl,
            contentDescription = null,
            modifier = Modifier.fillMaxSize()
        )

        // Load high quality in background
        AsyncImage(
            model = highQualityUrl,
            contentDescription = null,
            modifier = Modifier
                .fillMaxSize()
                .alpha(if (isHighQualityLoaded) 1f else 0f),
            onSuccess = { isHighQualityLoaded = true }
        )
    }
}
```

---
