## Design a Social Media Feed

### Q17. How would you design a social media feed like Instagram or Twitter?

**Answer:**

**Requirements:**
- Infinite scroll of posts
- Like, comment, share
- Real-time updates
- Image/video posts
- Personalized feed (algorithm)
- Pull-to-refresh

**Feed Architecture:**

```kotlin
// 1. Post Entity
@Entity(tableName = "posts")
data class PostEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "user_id") val userId: String,
    @ColumnInfo(name = "user_name") val userName: String,
    @ColumnInfo(name = "user_avatar") val userAvatar: String,
    @ColumnInfo(name = "content") val content: String,
    @ColumnInfo(name = "image_url") val imageUrl: String?,
    @ColumnInfo(name = "likes_count") val likesCount: Int,
    @ColumnInfo(name = "comments_count") val commentsCount: Int,
    @ColumnInfo(name = "is_liked") val isLiked: Boolean,
    @ColumnInfo(name = "created_at") val createdAt: Long,
    @ColumnInfo(name = "page") val page: Int
)

// 2. Paging Source
class FeedPagingSource(
    private val apiService: ApiService,
    private val postDao: PostDao
) : PagingSource<Int, Post>() {

    override suspend fun load(params: LoadParams<Int>): LoadResult<Int, Post> {
        val page = params.key ?: 1

        return try {
            // Fetch from API
            val response = apiService.getFeed(page = page, limit = params.loadSize)

            // Cache in database
            if (page == 1) {
                postDao.clearAll()  // Clear old cache on refresh
            }
            postDao.insertAll(response.posts.map { it.toEntity(page) })

            LoadResult.Page(
                data = response.posts,
                prevKey = if (page == 1) null else page - 1,
                nextKey = if (response.posts.isEmpty()) null else page + 1
            )
        } catch (e: IOException) {
            // Network error: load from cache
            val cached = postDao.getPostsByPage(page)
            if (cached.isNotEmpty()) {
                LoadResult.Page(
                    data = cached.map { it.toDomain() },
                    prevKey = null,
                    nextKey = page + 1
                )
            } else {
                LoadResult.Error(e)
            }
        } catch (e: Exception) {
            LoadResult.Error(e)
        }
    }

    override fun getRefreshKey(state: PagingState<Int, Post>): Int? {
        return state.anchorPosition?.let { anchorPosition ->
            state.closestPageToPosition(anchorPosition)?.prevKey?.plus(1)
                ?: state.closestPageToPosition(anchorPosition)?.nextKey?.minus(1)
        }
    }
}

// 3. Feed Repository
class FeedRepository @Inject constructor(
    private val apiService: ApiService,
    private val postDao: PostDao
) {
    fun getFeed(): Flow<PagingData<Post>> {
        return Pager(
            config = PagingConfig(
                pageSize = 20,
                prefetchDistance = 5,  // Prefetch when 5 items from bottom
                enablePlaceholders = false,
                initialLoadSize = 20
            ),
            pagingSourceFactory = { FeedPagingSource(apiService, postDao) }
        ).flow
    }

    suspend fun likePost(postId: String): Result<Unit> {
        return try {
            apiService.likePost(postId)

            // Update local cache
            postDao.incrementLikes(postId)
            postDao.setLiked(postId, true)

            Result.Success(Unit)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }

    suspend fun unlikePost(postId: String): Result<Unit> {
        return try {
            apiService.unlikePost(postId)

            // Update local cache
            postDao.decrementLikes(postId)
            postDao.setLiked(postId, false)

            Result.Success(Unit)
        } catch (e: Exception) {
            Result.Error(e)
        }
    }
}

// 4. Feed ViewModel
@HiltViewModel
class FeedViewModel @Inject constructor(
    private val feedRepository: FeedRepository
) : ViewModel() {

    val feedPagingData: Flow<PagingData<Post>> = feedRepository
        .getFeed()
        .cachedIn(viewModelScope)

    fun toggleLike(post: Post) {
        viewModelScope.launch {
            if (post.isLiked) {
                feedRepository.unlikePost(post.id)
            } else {
                feedRepository.likePost(post.id)
            }
        }
    }
}

// 5. Feed UI
@Composable
fun FeedScreen(
    viewModel: FeedViewModel = hiltViewModel()
) {
    val feedPagingItems = viewModel.feedPagingData.collectAsLazyPagingItems()

    val pullRefreshState = rememberPullRefreshState(
        refreshing = feedPagingItems.loadState.refresh is LoadState.Loading,
        onRefresh = { feedPagingItems.refresh() }
    )

    Box(modifier = Modifier.pullRefresh(pullRefreshState)) {
        LazyColumn {
            items(
                count = feedPagingItems.itemCount,
                key = { index -> feedPagingItems[index]?.id ?: index }
            ) { index ->
                val post = feedPagingItems[index]
                post?.let {
                    PostItem(
                        post = it,
                        onLikeClick = { viewModel.toggleLike(it) }
                    )
                }
            }

            // Loading indicator
            item {
                when (feedPagingItems.loadState.append) {
                    is LoadState.Loading -> {
                        CircularProgressIndicator(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp)
                        )
                    }
                    is LoadState.Error -> {
                        Text(
                            text = "Error loading more posts",
                            modifier = Modifier.padding(16.dp)
                        )
                    }
                    else -> {}
                }
            }
        }

        PullRefreshIndicator(
            refreshing = feedPagingItems.loadState.refresh is LoadState.Loading,
            state = pullRefreshState,
            modifier = Modifier.align(Alignment.TopCenter)
        )
    }
}

@Composable
fun PostItem(
    post: Post,
    onLikeClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
            .clickable { /* Navigate to restaurant detail */ }
    ) {
        Column {
            // User header
            Row(
                modifier = Modifier.padding(12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                AsyncImage(
                    model = post.userAvatar,
                    contentDescription = null,
                    modifier = Modifier
                        .size(40.dp)
                        .clip(CircleShape)
                )

                Spacer(modifier = Modifier.width(12.dp))

                Column {
                    Text(
                        text = post.userName,
                        style = MaterialTheme.typography.subtitle1,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        text = formatTimeAgo(post.createdAt),
                        style = MaterialTheme.typography.caption,
                        color = Color.Gray
                    )
                }
            }

            // Post image
            post.imageUrl?.let { imageUrl ->
                AsyncImage(
                    model = ImageRequest.Builder(LocalContext.current)
                        .data(imageUrl)
                        .crossfade(true)
                        .build(),
                    contentDescription = null,
                    modifier = Modifier
                        .fillMaxWidth()
                        .aspectRatio(1f),
                    contentScale = ContentScale.Crop
                )
            }

            // Post content
            if (post.content.isNotEmpty()) {
                Text(
                    text = post.content,
                    modifier = Modifier.padding(12.dp),
                    style = MaterialTheme.typography.body1
                )
            }

            // Actions
            Row(
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp)
            ) {
                // Like button
                IconButton(onClick = onLikeClick) {
                    Icon(
                        imageVector = if (post.isLiked) Icons.Filled.Favorite else Icons.Outlined.FavoriteBorder,
                        contentDescription = "Like",
                        tint = if (post.isLiked) Color.Red else Color.Gray
                    )
                }

                Text(
                    text = "${post.likesCount}",
                    modifier = Modifier.align(Alignment.CenterVertically)
                )

                Spacer(modifier = Modifier.width(16.dp))

                // Comment button
                IconButton(onClick = { /* Navigate to comments */ }) {
                    Icon(
                        imageVector = Icons.Outlined.ChatBubbleOutline,
                        contentDescription = "Comment",
                        tint = Color.Gray
                    )
                }

                Text(
                    text = "${post.commentsCount}",
                    modifier = Modifier.align(Alignment.CenterVertically)
                )

                Spacer(modifier = Modifier.weight(1f))

                // Share button
                IconButton(onClick = { /* Share */ }) {
                    Icon(
                        imageVector = Icons.Outlined.Share,
                        contentDescription = "Share",
                        tint = Color.Gray
                    )
                }
            }
        }
    }
}
```

**Key Features:**

1. **Pagination**: Efficient loading with Paging 3
2. **Offline Support**: Cached feed from database
3. **Pull-to-Refresh**: Update feed manually
4. **Optimistic Updates**: Instant like/unlike
5. **Image Loading**: Coil with caching

---

