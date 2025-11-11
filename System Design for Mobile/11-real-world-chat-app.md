# Part 3: Real-World Examples

## Design a Chat Application

### Q16. How would you design a mobile chat application like WhatsApp or Telegram?

**Answer:**

**Requirements:**
- Send/receive messages in real-time
- Offline message sending
- Media sharing (images, videos, files)
- Read receipts
- Typing indicators
- Group chats
- End-to-end encryption

**High-Level Architecture:**

```
Mobile App
    ↓
┌─────────────────────────────────────────────┐
│ Presentation Layer                           │
│ - Chat List Screen                          │
│ - Chat Room Screen                          │
│ - Compose Message                           │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Domain Layer                                 │
│ - Send Message Use Case                     │
│ - Receive Message Use Case                  │
│ - Sync Messages Use Case                    │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ Data Layer                                   │
│ - WebSocket Manager                         │
│ - Message Repository                        │
│ - Local Database (Room)                     │
└─────────────────────────────────────────────┘
    ↓
Backend Services
    - WebSocket Server
    - Message Queue
    - Database
    - Media Storage (S3/CDN)
```

**Implementation:**

```kotlin
// 1. Message Entity
@Entity(tableName = "messages")
data class MessageEntity(
    @PrimaryKey val id: String,
    @ColumnInfo(name = "chat_id") val chatId: String,
    @ColumnInfo(name = "sender_id") val senderId: String,
    @ColumnInfo(name = "content") val content: String,
    @ColumnInfo(name = "type") val type: MessageType,
    @ColumnInfo(name = "media_url") val mediaUrl: String? = null,
    @ColumnInfo(name = "timestamp") val timestamp: Long,
    @ColumnInfo(name = "status") val status: MessageStatus,
    @ColumnInfo(name = "is_read") val isRead: Boolean = false
)

enum class MessageType { TEXT, IMAGE, VIDEO, FILE, AUDIO }
enum class MessageStatus { SENDING, SENT, DELIVERED, READ, FAILED }

// 2. WebSocket Manager
class ChatWebSocketManager @Inject constructor(
    private val okHttpClient: OkHttpClient
) {
    private var webSocket: WebSocket? = null
    private val messageFlow = MutableSharedFlow<ChatEvent>()

    fun connect(userId: String): Flow<ChatEvent> {
        val request = Request.Builder()
            .url("wss://chat.example.com/ws?userId=$userId")
            .build()

        webSocket = okHttpClient.newWebSocket(request, object : WebSocketListener() {
            override fun onMessage(webSocket: WebSocket, text: String) {
                val event = Json.decodeFromString<ChatEvent>(text)
                viewModelScope.launch {
                    messageFlow.emit(event)
                }
            }

            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                // Reconnect logic
                reconnect(userId)
            }
        })

        return messageFlow
    }

    fun sendMessage(message: Message) {
        val json = Json.encodeToString(message)
        webSocket?.send(json)
    }

    fun disconnect() {
        webSocket?.close(1000, "User logout")
    }
}

// 3. Message Repository (Offline-First)
class MessageRepository @Inject constructor(
    private val webSocketManager: ChatWebSocketManager,
    private val messageDao: MessageDao,
    private val apiService: ApiService,
    private val networkMonitor: NetworkMonitor
) {
    // Get messages for a chat
    fun getMessages(chatId: String): Flow<List<Message>> {
        return messageDao.getMessagesForChat(chatId)
            .map { entities -> entities.map { it.toDomain() } }
    }

    // Send message (offline-first)
    suspend fun sendMessage(message: Message): Result<Message> {
        // 1. Save locally with SENDING status
        val localMessage = message.copy(
            id = UUID.randomUUID().toString(),
            status = MessageStatus.SENDING,
            timestamp = System.currentTimeMillis()
        )
        messageDao.insert(localMessage.toEntity())

        // 2. Try to send via WebSocket if online
        if (networkMonitor.isOnline()) {
            return try {
                webSocketManager.sendMessage(localMessage)

                // Update status to SENT
                messageDao.updateStatus(localMessage.id, MessageStatus.SENT)

                Result.Success(localMessage.copy(status = MessageStatus.SENT))
            } catch (e: Exception) {
                // Mark as failed, will retry later
                messageDao.updateStatus(localMessage.id, MessageStatus.FAILED)
                Result.Error(e)
            }
        }

        // 3. Will send when online (queued)
        return Result.Success(localMessage)
    }

    // Receive real-time messages
    fun observeIncomingMessages(): Flow<Message> = flow {
        webSocketManager.connect(userId).collect { event ->
            when (event) {
                is ChatEvent.NewMessage -> {
                    messageDao.insert(event.message.toEntity())
                    emit(event.message)
                }
                is ChatEvent.MessageDelivered -> {
                    messageDao.updateStatus(event.messageId, MessageStatus.DELIVERED)
                }
                is ChatEvent.MessageRead -> {
                    messageDao.updateStatus(event.messageId, MessageStatus.READ)
                }
            }
        }
    }

    // Upload media (images, videos)
    suspend fun uploadMedia(
        file: File,
        type: MessageType
    ): Result<String> {
        return try {
            val requestBody = file.asRequestBody("image/*".toMediaTypeOrNull())
            val multipart = MultipartBody.Part.createFormData("file", file.name, requestBody)

            val response = apiService.uploadMedia(multipart)
            Result.Success(response.url)  // CDN URL
        } catch (e: Exception) {
            Result.Error(e)
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

// 4. Chat ViewModel
@HiltViewModel
class ChatViewModel @Inject constructor(
    private val messageRepository: MessageRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val chatId: String = savedStateHandle["chatId"]!!

    val messages: StateFlow<List<Message>> = messageRepository
        .getMessages(chatId)
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    private val _sendingState = MutableStateFlow<SendingState>(SendingState.Idle)
    val sendingState = _sendingState.asStateFlow()

    init {
        // Listen for incoming messages
        viewModelScope.launch {
            messageRepository.observeIncomingMessages().collect { message ->
                if (message.chatId == chatId) {
                    // Message automatically updates via Room Flow
                    // Send read receipt
                    markMessageAsRead(message.id)
                }
            }
        }
    }

    fun sendTextMessage(text: String) {
        viewModelScope.launch {
            val message = Message(
                chatId = chatId,
                senderId = currentUserId,
                content = text,
                type = MessageType.TEXT
            )

            _sendingState.value = SendingState.Sending

            when (messageRepository.sendMessage(message)) {
                is Result.Success -> _sendingState.value = SendingState.Success
                is Result.Error -> _sendingState.value = SendingState.Error("Failed to send")
            }
        }
    }

    fun sendImageMessage(imageFile: File) {
        viewModelScope.launch {
            _sendingState.value = SendingState.Sending

            // Upload image first
            when (val result = messageRepository.uploadMedia(imageFile, MessageType.IMAGE)) {
                is Result.Success -> {
                    val message = Message(
                        chatId = chatId,
                        senderId = currentUserId,
                        content = "",
                        type = MessageType.IMAGE,
                        mediaUrl = result.data
                    )

                    messageRepository.sendMessage(message)
                    _sendingState.value = SendingState.Success
                }
                is Result.Error -> {
                    _sendingState.value = SendingState.Error("Upload failed")
                }
            }
        }
    }

    private suspend fun markMessageAsRead(messageId: String) {
        messageRepository.markAsRead(messageId)
    }
}

// 5. Chat UI
@Composable
fun ChatScreen(
    chatId: String,
    viewModel: ChatViewModel = hiltViewModel()
) {
    val messages by viewModel.messages.collectAsState()
    val sendingState by viewModel.sendingState.collectAsState()

    var messageText by remember { mutableStateOf("") }

    Column(modifier = Modifier.fillMaxSize()) {
        // Messages list
        LazyColumn(
            modifier = Modifier.weight(1f),
            reverseLayout = true
        ) {
            items(messages.reversed()) { message ->
                MessageItem(message)
            }
        }

        // Input area
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
        ) {
            TextField(
                value = messageText,
                onValueChange = { messageText = it },
                modifier = Modifier.weight(1f),
                placeholder = { Text("Type a message") }
            )

            IconButton(
                onClick = {
                    viewModel.sendTextMessage(messageText)
                    messageText = ""
                }
            ) {
                Icon(Icons.Default.Send, contentDescription = "Send")
            }
        }

        // Sending status
        when (sendingState) {
            is SendingState.Sending -> LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
            is SendingState.Error -> Text(
                text = (sendingState as SendingState.Error).message,
                color = Color.Red
            )
            else -> {}
        }
    }
}

@Composable
fun MessageItem(message: Message) {
    val isOwnMessage = message.senderId == currentUserId

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        horizontalArrangement = if (isOwnMessage) Arrangement.End else Arrangement.Start
    ) {
        Card(
            backgroundColor = if (isOwnMessage) Color(0xFF DCF8C6) else Color.White
        ) {
            Column(modifier = Modifier.padding(12.dp)) {
                when (message.type) {
                    MessageType.TEXT -> Text(message.content)
                    MessageType.IMAGE -> AsyncImage(
                        model = message.mediaUrl,
                        contentDescription = null,
                        modifier = Modifier.size(200.dp)
                    )
                    else -> {}
                }

                Spacer(modifier = Modifier.height(4.dp))

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = formatTime(message.timestamp),
                        style = MaterialTheme.typography.caption,
                        color = Color.Gray
                    )

                    if (isOwnMessage) {
                        Spacer(modifier = Modifier.width(4.dp))
                        // Status icons
                        when (message.status) {
                            MessageStatus.SENDING -> Icon(
                                Icons.Default.Schedule,
                                contentDescription = null,
                                tint = Color.Gray,
                                modifier = Modifier.size(16.dp)
                            )
                            MessageStatus.SENT -> Icon(
                                Icons.Default.Done,
                                contentDescription = null,
                                tint = Color.Gray,
                                modifier = Modifier.size(16.dp)
                            )
                            MessageStatus.DELIVERED -> Icon(
                                Icons.Default.DoneAll,
                                contentDescription = null,
                                tint = Color.Gray,
                                modifier = Modifier.size(16.dp)
                            )
                            MessageStatus.READ -> Icon(
                                Icons.Default.DoneAll,
                                contentDescription = null,
                                tint = Color.Blue,
                                modifier = Modifier.size(16.dp)
                            )
                            MessageStatus.FAILED -> Icon(
                                Icons.Default.Error,
                                contentDescription = null,
                                tint = Color.Red,
                                modifier = Modifier.size(16.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}
```

**Key Features:**

1. **Offline-First**: Messages saved locally, sent when online
2. **Real-time**: WebSocket for instant delivery
3. **Read Receipts**: Status tracking (sent, delivered, read)
4. **Media Upload**: CDN-hosted images/videos
5. **Sync**: Background sync for failed messages

---

