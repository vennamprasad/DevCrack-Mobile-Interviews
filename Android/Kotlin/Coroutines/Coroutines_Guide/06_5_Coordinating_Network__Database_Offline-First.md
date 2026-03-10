## **5. Coordinating Network + Database (Offline-First)**

### **Problem**: Show cached data immediately, then update from network

```kotlin
class ArticleRepository(
    private val api: ArticleApi,
    private val database: ArticleDatabase
) {
    suspend fun getArticle(id: String): Article {
        // First, show cached data immediately
        val cached = database.getArticle(id)

        return try {
            // Then fetch fresh data in background
            val fresh = api.fetchArticle(id)
            database.saveArticle(fresh)
            fresh
        } catch (e: IOException) {
            // Network failed - return cached or throw if no cache
            cached ?: throw e
        }
    }

    // Flow-based approach (better for reactive UI)
    fun observeArticle(id: String): Flow<Article> = flow {
        // Emit cached first
        database.observeArticle(id).firstOrNull()?.let { emit(it) }

        // Then fetch and emit fresh data
        try {
            val fresh = api.fetchArticle(id)
            database.saveArticle(fresh)
            emit(fresh)
        } catch (e: Exception) {
            // Already emitted cache, so just log
            Log.e("Repo", "Failed to fetch fresh data", e)
        }
    }
}
```
