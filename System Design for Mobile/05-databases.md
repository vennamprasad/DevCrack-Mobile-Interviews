## Databases

### Q6. What are different types of databases and when to use each?

**Answer:**

**Database Types Overview (clean):**
- Relational (SQL): PostgreSQL, MySQL, SQLite — structured data, strong consistency, joins.
- Document (NoSQL): Firestore, MongoDB — flexible schema, good for nested data.
- Key-Value: Redis, DynamoDB — very fast lookups, caching, session storage.
- Graph: Neo4j — relationships and traversals.
- Time-series: InfluxDB, TimescaleDB — metrics and time-based data.

**1. Relational Database (SQL) - Mobile: SQLite/Room:**

```kotlin
// Schema design for user and posts
@Entity(
    tableName = "users",
    indices = [Index(value = ["email"], unique = true)]
)
data class UserEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "email") val email: String,
    @ColumnInfo(name = "name") val name: String,
    @ColumnInfo(name = "avatar_url") val avatarUrl: String?,
    @ColumnInfo(name = "created_at") val createdAt: Long
)

@Entity(
    tableName = "posts",
    foreignKeys = [
        ForeignKey(
            entity = UserEntity::class,
            parentColumns = ["id"],
            childColumns = ["user_id"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index("user_id"), Index("created_at")]
)
data class PostEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "user_id") val userId: String,
    @ColumnInfo(name = "content") val content: String,
    @ColumnInfo(name = "image_url") val imageUrl: String?,
    @ColumnInfo(name = "likes_count") val likesCount: Int,
    @ColumnInfo(name = "created_at") val createdAt: Long
)

// Many-to-many relationship: Post Likes
@Entity(
    tableName = "post_likes",
    primaryKeys = ["post_id", "user_id"],
    foreignKeys = [
        ForeignKey(
            entity = PostEntity::class,
            parentColumns = ["id"],
            childColumns = ["post_id"],
            onDelete = ForeignKey.CASCADE
        ),
        ForeignKey(
            entity = UserEntity::class,
            parentColumns = ["id"],
            childColumns = ["user_id"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class PostLikeEntity(
    @ColumnInfo(name = "post_id") val postId: String,
    @ColumnInfo(name = "user_id") val userId: String,
    @ColumnInfo(name = "created_at") val createdAt: Long
)

@Dao
interface PostDao {
    @Query("SELECT * FROM posts ORDER BY timestamp DESC")
    fun getAllPosts(): Flow<List<PostEntity>>

    @Query("SELECT * FROM posts WHERE id = :postId")
    suspend fun getPost(postId: String): PostEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(posts: List<PostEntity>)

    @Query("DELETE FROM posts WHERE cachedAt < :threshold")
    suspend fun deleteOldCache(threshold: Long)

    @Query("DELETE FROM posts")
    suspend fun clearCache()
}

// Use case: E-commerce orders (ACID compliance)
@Entity(tableName = "orders")
data class OrderEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "user_id") val userId: String,
    @ColumnInfo(name = "total_amount") val totalAmount: Double,
    @ColumnInfo(name = "status") val status: OrderStatus,
    @ColumnInfo(name = "created_at") val createdAt: Long
)

@Entity(tableName = "order_items")
data class OrderItemEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "order_id") val orderId: String,
    @ColumnInfo(name = "product_id") val productId: String,
    @ColumnInfo(name = "quantity") val quantity: Int,
    @ColumnInfo(name = "price") val price: Double
)

@Dao
interface OrderDao {
    @Transaction
    suspend fun createOrder(order: OrderEntity, items: List<OrderItemEntity>) {
        // Atomic transaction - all or nothing
        insertOrder(order)
        insertOrderItems(items)
        // If any fails, entire transaction rolls back
    }
}
```

**Pros:**
-  ACID compliance (Atomicity, Consistency, Isolation, Durability)
-  Complex queries with JOINs
-  Data integrity with foreign keys
-  Well-understood, mature technology

**Cons:**
- L Schema changes require migrations
- L Horizontal scaling is difficult
- L Not ideal for hierarchical data

**Use Cases:**
- User accounts and profiles
- E-commerce (orders, inventory)
- Financial transactions
- Structured data with relationships

---

**2. NoSQL Document Database - Mobile: Firestore:**

```kotlin
// Flexible schema with nested data
data class Post(
    val id: String = "",
    val userId: String = "",
    val content: String = "",
    val imageUrls: List<String> = emptyList(),  // Array
    val author: Author = Author(),  // Nested object
    val likes: Map<String, Boolean> = emptyMap(),  // Map
    val comments: List<Comment> = emptyList(),  // Nested array
    val tags: List<String> = emptyList(),
    val location: GeoPoint? = null,
    val metadata: Map<String, Any> = emptyMap(),  // Flexible fields
    val createdAt: Timestamp = Timestamp.now()
)

data class Author(
    val id: String = "",
    val name: String = "",
    val avatarUrl: String = ""
)

data class Comment(
    val id: String = "",
    val userId: String = "",
    val text: String = "",
    val createdAt: Timestamp = Timestamp.now()
)

// Firestore operations
class PostRepository @Inject constructor(
    private val firestore: FirebaseFirestore
) {
    private val postsCollection = firestore.collection("posts")

    // Create
    suspend fun createPost(post: Post): Result<Post> = suspendCoroutine { continuation ->
        val docRef = postsCollection.document()
        val postWithId = post.copy(id = docRef.id)

        docRef.set(postWithId)
            .addOnSuccessListener { continuation.resume(Result.Success(postWithId)) }
            .addOnFailureListener { continuation.resume(Result.Error(it)) }
    }

    // Read with complex query
    fun getPostsByUser(userId: String): Flow<List<Post>> = callbackFlow {
        val listener = postsCollection
            .whereEqualTo("userId", userId)
            .orderBy("createdAt", Query.Direction.DESCENDING)
            .limit(50)
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    close(error)
                    return@addSnapshotListener
                }

                val posts = snapshot?.documents?.mapNotNull {
                    it.toObject(Post::class.java)
                } ?: emptyList()

                trySend(posts)
            }

        awaitClose { listener.remove() }
    }

    // Update specific field
    suspend fun likePost(postId: String, userId: String) {
        postsCollection.document(postId)
            .update("likes.$userId", true)
            .await()
    }

    // Add to array
    suspend fun addComment(postId: String, comment: Comment) {
        postsCollection.document(postId)
            .update("comments", FieldValue.arrayUnion(comment))
            .await()
    }

    // Query with multiple conditions
    fun searchPosts(tag: String, location: GeoPoint, radius: Double): Flow<List<Post>> {
        // Note: Firestore has limitations on complex queries
        return callbackFlow {
            val listener = postsCollection
                .whereArrayContains("tags", tag)
                // Geo queries require third-party library or custom logic
                .addSnapshotListener { snapshot, error ->
                    if (error != null) {
                        close(error)
                        return@addSnapshotListener
                    }

                    val posts = snapshot?.documents?.mapNotNull {
                        it.toObject(Post::class.java)
                    }?.filter { post ->
                        post.location?.let { loc ->
                            calculateDistance(loc, location) <= radius
                        } ?: false
                    } ?: emptyList()

                    trySend(posts)
                }

            awaitClose { listener.remove() }
        }
    }
}

// Subcollections for better organization
/*
Structure:
/users/{userId}/posts/{postId}
/users/{userId}/posts/{postId}/comments/{commentId}
/users/{userId}/followers/{followerId}
*/

class UserRepository @Inject constructor(
    private val firestore: FirebaseFirestore
) {
    fun getUserPosts(userId: String): Flow<List<Post>> = callbackFlow {
        val listener = firestore.collection("users")
            .document(userId)
            .collection("posts")
            .orderBy("createdAt", Query.Direction.DESCENDING)
            .addSnapshotListener { snapshot, error ->
                // Handle updates
            }

        awaitClose { listener.remove() }
    }
}
```

**Pros:**
-  Flexible schema (add fields without migration)
-  Easy to scale horizontally
-  Good for hierarchical data
-  Real-time updates built-in

**Cons:**
- L Limited JOIN capabilities
- L Eventual consistency
- L Complex queries can be expensive
- L Data duplication for performance

**Use Cases:**
- Social media posts and comments
- User-generated content
- Activity logs
- Product catalogs with varying attributes

---

**3. Key-Value Store - Mobile: DataStore/SharedPreferences:**

```kotlin
// Simple key-value storage for preferences
class UserPreferences @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(
        name = "user_preferences"
    )

    companion object {
        val THEME_KEY = stringPreferencesKey("theme")
        val NOTIFICATION_ENABLED = booleanPreferencesKey("notifications_enabled")
        val LAST_SYNC = longPreferencesKey("last_sync_timestamp")
        val USER_ID = stringPreferencesKey("user_id")
    }

    // Write
    suspend fun setTheme(theme: String) {
        context.dataStore.edit { preferences ->
            preferences[THEME_KEY] = theme
        }
    }

    // Read
    val theme: Flow<String> = context.dataStore.data
        .map { preferences ->
            preferences[THEME_KEY] ?: "system"
        }

    // Complex object (serialize to JSON)
    suspend fun saveUserSession(session: UserSession) {
        val json = Json.encodeToString(session)
        context.dataStore.edit { preferences ->
            preferences[stringPreferencesKey("user_session")] = json
        }
    }
}

// Backend: Redis for caching and sessions
/*
Redis use cases on backend:
- Session storage: SET session:user123 "session_data" EX 3600
- Rate limiting: INCR rate:user123:endpoint TTL 60
- Leaderboard: ZADD leaderboard score user_id
- Pub/Sub: PUBLISH channel "message"
*/
```

**Pros:**
-  Extremely fast (in-memory)
-  Simple API
-  Perfect for caching
-  Atomic operations

**Cons:**
- L No complex queries
- L Limited data structures
- L No relationships
- L Memory-bound (expensive for large data)

**Use Cases:**
- User sessions and preferences
- Caching layer
- Rate limiting
- Real-time leaderboards

---

**4. Graph Database - Backend: Neo4j:**

```kotlin
// Social network relationships
/*
Graph Structure:
(User:Alice) -[:FOLLOWS]-> (User:Bob)
(User:Alice) -[:LIKES]-> (Post:123)
(User:Bob) -[:COMMENTED_ON]-> (Post:123)
(User:Alice) -[:FRIENDS_WITH]-> (User:Charlie)

Cypher Query Examples:

1. Find friends of friends:
MATCH (user:User {id: 'alice'})-[:FRIENDS_WITH]->(friend)-[:FRIENDS_WITH]->(fof)
WHERE NOT (user)-[:FRIENDS_WITH]->(fof) AND user <> fof
RETURN fof.name, COUNT(*) as mutual_friends

2. Recommend users to follow:
MATCH (user:User {id: 'alice'})-[:FOLLOWS]->(followed)-[:FOLLOWS]->(recommendation)
WHERE NOT (user)-[:FOLLOWS]->(recommendation) AND user <> recommendation
RETURN recommendation.name, COUNT(*) as score
ORDER BY score DESC
LIMIT 10

3. Find shortest path:
MATCH path = shortestPath(
  (alice:User {id: 'alice'})-[:FRIENDS_WITH*]-(bob:User {id: 'bob'})
)
RETURN path, length(path)
*/

// Android client for graph database
interface SocialGraphApi {
    @GET("users/{userId}/friends-of-friends")
    suspend fun getFriendsOfFriends(@Path("userId") userId: String): List<User>

    @GET("users/{userId}/recommendations")
    suspend fun getFollowRecommendations(
        @Path("userId") userId: String,
        @Query("limit") limit: Int = 10
    ): List<UserRecommendation>

    @GET("users/{userId}/connection-path/{targetId}")
    suspend fun getConnectionPath(
        @Path("userId") userId: String,
        @Path("targetId") targetId: String
    ): ConnectionPath
}

data class UserRecommendation(
    val user: User,
    val mutualFriends: Int,
    val commonInterests: List<String>
)

data class ConnectionPath(
    val users: List<User>,
    val relationships: List<Relationship>,
    val degreeOfSeparation: Int
)
```

**Pros:**
-  Excellent for relationship queries
-  Fast traversal of connections
-  Natural representation of networks
-  Pattern matching

**Cons:**
- L Specialized use case
- L Complex to set up
- L Overkill for simple data
- L Expensive for non-graph queries

**Use Cases:**
- Social networks (friends, followers)
- Recommendation engines
- Fraud detection (connection patterns)
- Knowledge graphs

---

**Database Selection Matrix:**

| Requirement | SQL | NoSQL Document | Key-Value | Graph |
|-------------|-----|----------------|-----------|-------|
| **Complex queries** |  Best | � Limited | L No | � For relationships |
| **Flexible schema** | L No |  Yes |  Yes | � Somewhat |
| **Scalability** | � Vertical |  Horizontal |  Horizontal | � Depends |
| **ACID compliance** |  Yes | � Limited | L No |  Yes |
| **Relationships** |  Joins | L Embed/Ref | L No |  Native |
| **Speed** | � Good |  Fast |  Fastest | � For graphs |
| **Cost** | =� Low | =� Medium | =� High (memory) | =� High |

**Mobile App Database Strategy:**

```kotlin
// Hybrid approach: Use different databases for different needs
class DataManager @Inject constructor(
    // Local SQL for structured data
    private val roomDatabase: AppDatabase,

    // Remote NoSQL for flexible data
    private val firestore: FirebaseFirestore,

    // Key-value for preferences
    private val dataStore: DataStore<Preferences>,

    // Memory cache for hot data
    private val memoryCache: MemoryCache
) {
    // Use Room for:
    // - User profiles (structured)
    // - Messages (queryable)
    // - Orders (transactional)

    // Use Firestore for:
    // - Posts (flexible schema)
    // - Comments (nested data)
    // - Activity logs

    // Use DataStore for:
    // - User preferences
    // - App settings
    // - Feature flags

    // Use Memory Cache for:
    // - Current user data
    // - Recently viewed items
    // - Temporary state
}
```

---

