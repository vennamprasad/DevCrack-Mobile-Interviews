# 📨 Message Queues
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Decouple services and handle asynchronous tasks efficiently.

![Message Queues](https://img.shields.io/badge/Architecture-Queues-orange?style=for-the-badge&logo=apachekafka&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Async Processing](#1-asynchronous-processing)
- [2. Push Notifications](#2-push-notifications-via-queue)
- [3. Retry Mechanism](#3-retry-mechanism)
- [4. Event-Driven Patterns](#4-event-driven-architecture)

---

### Q8. What are message queues and how do they work with mobile apps?

**Answer:**

Message queues enable asynchronous communication between services, improving scalability and reliability.

**Message Queue Architecture:**

```
Mobile App
    ↓ (Publish)
┌─────────────────────┐
│  Message Queue      │
│  (RabbitMQ, Kafka)  │
└─────────────────────┘
    ↓ (Subscribe)
┌─────────────────────┐
│  Workers/Consumers  │
│  - Email Service    │
│  - Push Service     │
│  - Analytics        │
└─────────────────────┘
```

**Use Cases:**

**1. Asynchronous Processing:**

```kotlin
// Mobile app sends request, doesn't wait for processing
class PostRepository @Inject constructor(
    private val apiService: ApiService,
    private val database: PostDao
) {
    suspend fun createPost(post: Post): Result<Post> {
        return try {
            // API publishes to queue and returns immediately
            val response = apiService.createPost(post)

            // Post is queued for:
            // - Image processing (resize, compress)
            // - Content moderation (AI checks)
            // - Notifications (to followers)
            // - Search indexing
            // - Analytics logging

            // User sees post immediately (optimistic update)
            database.insert(response.copy(status = PostStatus.PROCESSING))

            Result.Success(response)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}

// Backend processing flow
/*
1. User creates post → API saves to DB
2. API publishes message to queue: "new_post_created"
3. API returns success to mobile app
4. Workers consume messages asynchronously:
   - Image worker: Process images
   - Notification worker: Send push notifications
   - Search worker: Update search index
   - Analytics worker: Log event
   - Content moderation worker: Check for violations

Each worker can scale independently based on the queue size and processing time.
*/
```

**2. Push Notifications via Queue:**

```kotlin
// Mobile app triggers action
class FollowRepository @Inject constructor(
    private val apiService: ApiService
) {
    suspend fun followUser(userId: String): Result<Unit> {
        return try {
            apiService.followUser(userId)
            // Backend publishes to "user_followed" queue
            // Notification worker consumes and sends push to followed user
            Result.Success(Unit)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}

// Backend queue structure
/*
Queue: "user_followed"
Message: {
    "follower_id": "user123",
    "followed_id": "user456",
    "timestamp": 1234567890
}

Notification Worker:
1. Consumes message from queue
2. Fetches user preferences
3. Sends FCM push notification
4. Logs notification sent
5. Acknowledges message (removes from queue)
*/
```

**3. Retry Mechanism:**

```kotlin
// Dead Letter Queue (DLQ) pattern
/*
Normal Flow:
Mobile App → API → Queue → Worker → Success

Failed Flow:
Mobile App → API → Queue → Worker → Failure
                            ↓
                    Retry Queue (with delay)
                            ↓
                    Worker → Failure (after 3 retries)
                            ↓
                    Dead Letter Queue (for investigation)

DLQ Processing:
- Admin dashboard shows failed messages
- Option to replay or delete
- Alerts on critical failures
*/
```

**4. Event-Driven Architecture:**

```kotlin
// Mobile app publishes events, backend processes asynchronously
sealed class UserEvent {
    data class ProfileUpdated(val userId: String, val changes: Map<String, Any>) : UserEvent()
    data class PostCreated(val postId: String, val userId: String) : UserEvent()
    data class PostLiked(val postId: String, val userId: String) : UserEvent()
    data class UserFollowed(val followerId: String, val followedId: String) : UserEvent()
}

class EventPublisher @Inject constructor(
    private val apiService: ApiService
) {
    suspend fun publishEvent(event: UserEvent) {
        // Backend publishes to event bus/queue
        apiService.publishEvent(event)
    }
}

// Backend event processing
/*
Event: "post_liked"

Subscribers:
1. Notification Service → Send push to post author
2. Analytics Service → Update engagement metrics
3. Recommendation Service → Update user preferences
4. Newsfeed Service → Update followers' feeds
5. Cache Service → Invalidate cached like count

Each service processes independently and asynchronously
*/
```

**Benefits for Mobile:**

| Benefit | Description |
|---------|-------------|
| **Fast response** | API returns quickly, processing happens async |
| **Reliability** | Failed operations retry automatically |
| **Scalability** | Workers scale based on queue size |
| **Decoupling** | Mobile app doesn't need to know about backend services |
| **Offline support** | Queue stores operations until workers are ready |

**Queue vs Direct API Call:**

```kotlin
// Direct API call (synchronous)
suspend fun uploadVideo(video: Video): Result<Video> {
    // ✗ Mobile waits for:
    // 1. Upload (30 seconds)
    // 2. Transcoding (2 minutes)
    // 3. Thumbnail generation (10 seconds)
    // 4. CDN distribution (20 seconds)
    // Total: 3+ minutes!

    return apiService.uploadVideo(video)  // User waits...
}

// Queue-based (asynchronous)
suspend fun uploadVideo(video: Video): Result<Video> {
    // ✓ Mobile waits for:
    // 1. Upload (30 seconds)
    // API queues rest of processing

    val response = apiService.uploadVideo(video)
    // Returns immediately with status: PROCESSING

    // Workers process in background:
    // - Transcoding
    // - Thumbnail generation
    // - CDN distribution

    // Mobile polls or receives push when complete

    return Result.Success(response)
}
```

---
