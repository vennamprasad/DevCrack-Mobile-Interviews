## **1. Sequential vs Parallel API Calls**

### **Problem**: Fetching data from multiple APIs efficiently

**Sequential (Slower - takes sum of all times)**:
```kotlin
class UserRepository {
    suspend fun loadUserProfile(userId: String): UserProfile {
        // Takes 2s + 1.5s + 1s = 4.5s total
        val user = api.fetchUser(userId)        // 2 seconds
        val posts = api.fetchUserPosts(userId)  // 1.5 seconds
        val friends = api.fetchFriends(userId)  // 1 second

        return UserProfile(user, posts, friends)
    }
}
```

**Parallel (Faster - takes max of all times)**:
```kotlin
class UserRepository {
    suspend fun loadUserProfile(userId: String): UserProfile {
        // All run concurrently - takes ~2s (longest call)
        return coroutineScope {
            val userDeferred = async { api.fetchUser(userId) }
            val postsDeferred = async { api.fetchUserPosts(userId) }
            val friendsDeferred = async { api.fetchFriends(userId) }

            UserProfile(
                user = userDeferred.await(),
                posts = postsDeferred.await(),
                friends = friendsDeferred.await()
            )
        }
    }
}
```

**Key Insight**: Use `async` when calls are independent. If one depends on another, use sequential.

**Dependent Calls** (User ID needed for subsequent calls):
```kotlin
suspend fun loadUserDetails(username: String): UserDetails {
    val userId = api.getUserId(username)  // Must complete first

    // Now fetch in parallel using the userId
    return coroutineScope {
        val profile = async { api.getProfile(userId) }
        val settings = async { api.getSettings(userId) }
        UserDetails(profile.await(), settings.await())
    }
}
```
