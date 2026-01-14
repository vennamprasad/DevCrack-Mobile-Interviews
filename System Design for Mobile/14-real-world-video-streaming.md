# 🎬 Design a Video Streaming App
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** Adaptive video streaming, offline downloading, and player management.

![Video Streaming](https://img.shields.io/badge/Real_World-Video_Streaming-E50914?style=for-the-badge&logo=netflix&logoColor=white)
![Level](https://img.shields.io/badge/Level-Senior-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Streaming Architecture](#architecture)
- [2. File Structure & Entity](#1-video-entity)
- [3. Player Management (ExoPlayer)](#2-video-player-manager)
- [4. Downloading Logic](#6-video-download-manager)
- [5. Optimization Strategies](#performance-optimizations)

---

### Q19. How would you design a video streaming app like YouTube or Netflix?

**Answer:**

**Requirements:**
- Stream videos smoothly
- Adaptive bitrate streaming
- Offline downloads
- Playback controls (play, pause, seek)
- Continue watching (resume playback)
- Recommendations
- Low buffer time

**Architecture:**

```
┌─────────────────────────────────────────────┐
│ Video Player (ExoPlayer)                    │
│ - Adaptive streaming (HLS/DASH)            │
│ - Buffer management                         │
│ - Quality selection                         │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ CDN (Content Delivery Network)              │
│ - Video segments cached globally            │
│ - Low latency delivery                      │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Origin Server                                │
│ - Video encoding (multiple qualities)       │
│ - Metadata storage                          │
└─────────────────────────────────────────────┘
```

**Implementation:**

```kotlin
// 1. Video Entity
@Entity(tableName = "videos")
data class VideoEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "title") val title: String,
    @ColumnInfo(name = "description") val description: String,
    @ColumnInfo(name = "thumbnail_url") val thumbnailUrl: String,
    @ColumnInfo(name = "duration") val duration: Long,
    @ColumnInfo(name = "views_count") val viewsCount: Long,
    @ColumnInfo(name = "upload_date") val uploadDate: Long,
    @ColumnInfo(name = "channel_name") val channelName: String,
    @ColumnInfo(name = "channel_avatar") val channelAvatar: String,
    
    // Video URLs (different qualities)
    @ColumnInfo(name = "hls_manifest_url") val hlsManifestUrl: String,
    @ColumnInfo(name = "quality_360p") val quality360p: String?,
    @ColumnInfo(name = "quality_720p") val quality720p: String?,
    @ColumnInfo(name = "quality_1080p") val quality1080p: String?,
    
    // Playback state
    @ColumnInfo(name = "last_played_position") val lastPlayedPosition: Long = 0,
    @ColumnInfo(name = "is_downloaded") val isDownloaded: Boolean = false,
    @ColumnInfo(name = "download_path") val downloadPath: String? = null
)

// 2. Video Player Manager
class VideoPlayerManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val downloadManager: DownloadManager
) {
    private var player: ExoPlayer? = null

    fun createPlayer(): ExoPlayer {
        return ExoPlayer.Builder(context)
            .setLoadControl(
                DefaultLoadControl.Builder()
                    .setBufferDurationsMs(
                        minBufferMs = 15_000,      // Minimum buffer
                        maxBufferMs = 50_000,      // Maximum buffer
                        bufferForPlaybackMs = 2_500,  // Start playback
                        bufferForPlaybackAfterRebufferMs = 5_000  // Resume after rebuffer
                    )
                    .build()
            )
            .build()
            .also { player = it }
    }

    fun playVideo(videoUrl: String, startPosition: Long = 0) {
        player?.apply {
            val mediaItem = MediaItem.Builder()
                .setUri(videoUrl)
                .build()

            setMediaItem(mediaItem)
            seekTo(startPosition)
            prepare()
            playWhenReady = true
        }
    }

    fun playDownloadedVideo(downloadPath: String, startPosition: Long = 0) {
        player?.apply {
            val mediaItem = MediaItem.fromUri(Uri.fromFile(File(downloadPath)))
            setMediaItem(mediaItem)
            seekTo(startPosition)
            prepare()
            playWhenReady = true
        }
    }

    fun getCurrentPosition(): Long {
        return player?.currentPosition ?: 0
    }

    fun release() {
        player?.release()
        player = null
    }
}

// 3. Video Repository
class VideoRepository @Inject constructor(
    private val apiService: ApiService,
    private val videoDao: VideoDao,
    private val downloadManager: VideoDownloadManager
) {
    fun getVideos(): Flow<PagingData<Video>> {
        return Pager(
            config = PagingConfig(pageSize = 20),
            pagingSourceFactory = { VideoPagingSource(apiService, videoDao) }
        ).flow
    }

    suspend fun getVideoById(videoId: String): Result<Video> {
        return try {
            val video = apiService.getVideo(videoId)
            videoDao.insert(video.toEntity())
            Result.Success(video)
        } catch (e: Exception) {
            videoDao.getVideoById(videoId)?.let {
                Result.Success(it.toDomain())
            } ?: Result.Error(e)
        }
    }

    suspend fun savePlaybackPosition(videoId: String, position: Long) {
        videoDao.updatePlaybackPosition(videoId, position)
    }

    suspend fun downloadVideo(video: Video): Flow<DownloadProgress> = flow {
        emit(DownloadProgress.Starting)

        try {
            // Download video file
            downloadManager.download(
                url = video.quality720p ?: video.hlsManifestUrl,
                videoId = video.id
            ).collect { progress ->
                emit(progress)

                if (progress is DownloadProgress.Completed) {
                    // Mark as downloaded in database
                    videoDao.markAsDownloaded(video.id, progress.filePath)
                }
            }
        } catch (e: Exception) {
            emit(DownloadProgress.Failed(e.message ?: "Download failed"))
        }
    }

    suspend fun getDownloadedVideos(): Flow<List<Video>> {
        return videoDao.getDownloadedVideos()
            .map { entities -> entities.map { it.toDomain() } }
    }

    suspend fun recordView(videoId: String) {
        try {
            apiService.recordView(videoId)
            videoDao.incrementViews(videoId)
        } catch (e: Exception) {
            // Failed to record view
        }
    }
}

sealed class DownloadProgress {
    object Starting : DownloadProgress()
    data class Downloading(val progress: Int) : DownloadProgress()
    data class Completed(val filePath: String) : DownloadProgress()
    data class Failed(val error: String) : DownloadProgress()
}

// 4. Video Player ViewModel
@HiltViewModel
class VideoPlayerViewModel @Inject constructor(
    private val videoRepository: VideoRepository,
    private val playerManager: VideoPlayerManager,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val videoId: String = savedStateHandle["videoId"]!!

    private val _videoState = MutableStateFlow<VideoState>(VideoState.Loading)
    val videoState = _videoState.asStateFlow()

    private val _playerState = MutableStateFlow(PlayerState())
    val playerState = _playerState.asStateFlow()

    val player: ExoPlayer = playerManager.createPlayer()

    init {
        loadVideo()

        // Save playback position periodically
        viewModelScope.launch {
            while (true) {
                delay(5000)  // Every 5 seconds
                savePlaybackPosition()
            }
        }

        // Listen to player events
        player.addListener(object : Player.Listener {
            override fun onPlaybackStateChanged(playbackState: Int) {
                _playerState.value = _playerState.value.copy(
                    isPlaying = player.isPlaying,
                    isBuffering = playbackState == Player.STATE_BUFFERING
                )
            }

            override fun onPlayerError(error: PlaybackException) {
                _videoState.value = VideoState.Error(error.message ?: "Playback error")
            }
        })
    }

    private fun loadVideo() {
        viewModelScope.launch {
            when (val result = videoRepository.getVideoById(videoId)) {
                is Result.Success -> {
                    val video = result.data
                    _videoState.value = VideoState.Success(video)

                    // Record view
                    videoRepository.recordView(videoId)

                    // Start playback
                    if (video.isDownloaded && video.downloadPath != null) {
                        playerManager.playDownloadedVideo(
                            downloadPath = video.downloadPath,
                            startPosition = video.lastPlayedPosition
                        )
                    } else {
                        playerManager.playVideo(
                            videoUrl = video.hlsManifestUrl,
                            startPosition = video.lastPlayedPosition
                        )
                    }
                }
                is Result.Error -> {
                    _videoState.value = VideoState.Error(result.exception.message)
                }
            }
        }
    }

    fun togglePlayPause() {
        player.playWhenReady = !player.playWhenReady
    }

    fun seekTo(positionMs: Long) {
        player.seekTo(positionMs)
    }

    private fun savePlaybackPosition() {
        viewModelScope.launch {
            videoRepository.savePlaybackPosition(
                videoId = videoId,
                position = playerManager.getCurrentPosition()
            )
        }
    }

    fun downloadVideo() {
        viewModelScope.launch {
            val video = (_videoState.value as? VideoState.Success)?.video ?: return@launch

            videoRepository.downloadVideo(video).collect { progress ->
                _playerState.value = _playerState.value.copy(downloadProgress = progress)
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        savePlaybackPosition()
        playerManager.release()
    }
}

sealed class VideoState {
    object Loading : VideoState()
    data class Success(val video: Video) : VideoState()
    data class Error(val message: String?) : VideoState()
}

data class PlayerState(
    val isPlaying: Boolean = false,
    val isBuffering: Boolean = false,
    val downloadProgress: DownloadProgress? = null
)

// 5. Video Player UI
@Composable
fun VideoPlayerScreen(
    videoId: String,
    viewModel: VideoPlayerViewModel = hiltViewModel()
) {
    val videoState by viewModel.videoState.collectAsState()
    val playerState by viewModel.playerState.collectAsState()

    DisposableEffect(Unit) {
        onDispose {
            viewModel.player.release()
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Video player
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(16f / 9f)
                .background(Color.Black)
        ) {
            AndroidView(
                factory = { context ->
                    PlayerView(context).apply {
                        player = viewModel.player
                        useController = true
                        controllerShowTimeoutMs = 3000
                    }
                },
                modifier = Modifier.fillMaxSize()
            )

            // Buffering indicator
            if (playerState.isBuffering) {
                CircularProgressIndicator(
                    modifier = Modifier.align(Alignment.Center),
                    color = Color.White
                )
            }

            // Download progress
            playerState.downloadProgress?.let { progress ->
                when (progress) {
                    is DownloadProgress.Downloading -> {
                        LinearProgressIndicator(
                            progress = progress.progress / 100f,
                            modifier = Modifier
                                .align(Alignment.BottomCenter)
                                .fillMaxWidth()
                        )
                    }
                    else -> {}
                }
            }
        }

        // Video info
        when (val state = videoState) {
            is VideoState.Success -> {
                VideoInfoSection(
                    video = state.video,
                    onDownloadClick = { viewModel.downloadVideo() }
                )
            }
            is VideoState.Loading -> {
                CircularProgressIndicator(
                    modifier = Modifier
                        .padding(16.dp)
                        .align(Alignment.CenterHorizontally)
                )
            }
            is VideoState.Error -> {
                Text(
                    text = "Error: ${state.message}",
                    color = Color.Red,
                    modifier = Modifier.padding(16.dp)
                )
            }
        }
    }
}

@Composable
fun VideoInfoSection(
    video: Video,
    onDownloadClick: () -> Unit
) {
    Column(modifier = Modifier.padding(16.dp)) {
        // Title
        Text(
            text = video.title,
            style = MaterialTheme.typography.h6,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(8.dp))

        // Views and date
        Text(
            text = "${formatViews(video.viewsCount)} views • ${formatDate(video.uploadDate)}",
            style = MaterialTheme.typography.body2,
            color = Color.Gray
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Channel info
        Row(verticalAlignment = Alignment.CenterVertically) {
            AsyncImage(
                model = video.channelAvatar,
                contentDescription = null,
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
            )

            Spacer(modifier = Modifier.width(12.dp))

            Text(
                text = video.channelName,
                style = MaterialTheme.typography.subtitle1,
                modifier = Modifier.weight(1f)
            )

            // Download button
            if (!video.isDownloaded) {
                IconButton(onClick = onDownloadClick) {
                    Icon(
                        imageVector = Icons.Default.Download,
                        contentDescription = "Download"
                    )
                }
            } else {
                Icon(
                    imageVector = Icons.Default.CheckCircle,
                    contentDescription = "Downloaded",
                    tint = Color.Green
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Description
        Text(
            text = video.description,
            style = MaterialTheme.typography.body2,
            maxLines = 3,
            overflow = TextOverflow.Ellipsis
        )
    }
}

// 6. Video Download Manager
class VideoDownloadManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val okHttpClient: OkHttpClient
) {
    fun download(url: String, videoId: String): Flow<DownloadProgress> = flow {
        emit(DownloadProgress.Starting)

        val request = Request.Builder().url(url).build()
        val response = okHttpClient.newCall(request).execute()

        if (!response.isSuccessful) {
            emit(DownloadProgress.Failed("Download failed: ${response.code}"))
            return@flow
        }

        val body = response.body ?: run {
            emit(DownloadProgress.Failed("Empty response"))
            return@flow
        }

        val contentLength = body.contentLength()
        val file = File(context.getExternalFilesDir(null), "$videoId.mp4")

        body.byteStream().use { input ->
            file.outputStream().use { output ->
                val buffer = ByteArray(8192)
                var totalBytesRead = 0L
                var bytesRead: Int

                while (input.read(buffer).also { bytesRead = it } != -1) {
                    output.write(buffer, 0, bytesRead)
                    totalBytesRead += bytesRead

                    val progress = ((totalBytesRead * 100) / contentLength).toInt()
                    emit(DownloadProgress.Downloading(progress))
                }
            }
        }

        emit(DownloadProgress.Completed(file.absolutePath))
    }
}
```

**Key Features:**

1. **Adaptive Streaming**: HLS/DASH for quality switching
2. **Buffering**: Smart buffering for smooth playback
3. **Offline Downloads**: Save videos locally
4. **Resume Playback**: Continue where you left off
5. **CDN Delivery**: Fast video loading worldwide

**Performance Optimizations:**

```kotlin
// Preload next video
class VideoPreloader @Inject constructor(
    private val exoPlayer: ExoPlayer
) {
    fun preloadNextVideo(videoUrl: String) {
        val mediaItem = MediaItem.fromUri(videoUrl)
        exoPlayer.addMediaItem(mediaItem)
        exoPlayer.prepare()
    }
}

// Quality selector based on network
class AdaptiveQualitySelector @Inject constructor(
    private val networkMonitor: NetworkMonitor
) {
    fun getOptimalQuality(video: Video): String {
        return when (networkMonitor.getNetworkType()) {
            NetworkType.WIFI -> video.quality1080p ?: video.quality720p ?: video.hlsManifestUrl
            NetworkType.MOBILE_4G -> video.quality720p ?: video.quality360p ?: video.hlsManifestUrl
            NetworkType.MOBILE_3G -> video.quality360p ?: video.hlsManifestUrl
            else -> video.quality360p ?: video.hlsManifestUrl
        }
    }
}
```

---
