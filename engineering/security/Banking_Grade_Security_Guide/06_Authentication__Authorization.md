## 🔑 Authentication & Authorization

### 1. Biometric Authentication

```kotlin
// BiometricManager.kt
class BiometricManager @Inject constructor(
    private val context: Context,
    private val keystoreManager: KeystoreManager
) {
    
    fun isBiometricAvailable(): BiometricStatus {
        val biometricManager = androidx.biometric.BiometricManager.from(context)
        
        return when (biometricManager.canAuthenticate(BIOMETRIC_STRONG)) {
            androidx.biometric.BiometricManager.BIOMETRIC_SUCCESS ->
                BiometricStatus.AVAILABLE
            androidx.biometric.BiometricManager.BIOMETRIC_ERROR_NO_HARDWARE ->
                BiometricStatus.NO_HARDWARE
            androidx.biometric.BiometricManager.BIOMETRIC_ERROR_HW_UNAVAILABLE ->
                BiometricStatus.HARDWARE_UNAVAILABLE
            androidx.biometric.BiometricManager.BIOMETRIC_ERROR_NONE_ENROLLED ->
                BiometricStatus.NOT_ENROLLED
            else -> BiometricStatus.UNKNOWN
        }
    }
    
    fun authenticate(
        activity: FragmentActivity,
        onSuccess: (BiometricPrompt.AuthenticationResult) -> Unit,
        onError: (Int, String) -> Unit
    ) {
        val executor = ContextCompat.getMainExecutor(context)
        
        val biometricPrompt = BiometricPrompt(
            activity,
            executor,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(
                    result: BiometricPrompt.AuthenticationResult
                ) {
                    super.onAuthenticationSucceeded(result)
                    onSuccess(result)
                }
                
                override fun onAuthenticationError(
                    errorCode: Int,
                    errString: CharSequence
                ) {
                    super.onAuthenticationError(errorCode, errString)
                    onError(errorCode, errString.toString())
                }
                
                override fun onAuthenticationFailed() {
                    super.onAuthenticationFailed()
                    onError(-1, "Authentication failed")
                }
            }
        )
        
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Biometric Authentication")
            .setSubtitle("Authenticate to access your account")
            .setDescription("Use your fingerprint or face to verify your identity")
            .setAllowedAuthenticators(BIOMETRIC_STRONG or DEVICE_CREDENTIAL)
            .build()
        
        biometricPrompt.authenticate(promptInfo)
    }
    
    /**
     * Biometric authentication with CryptoObject for cryptographically secured operations
     */
    fun authenticateWithCrypto(
        activity: FragmentActivity,
        onSuccess: (Cipher) -> Unit,
        onError: (Int, String) -> Unit
    ) {
        val cipher = getCipherForBiometric()
        val cryptoObject = BiometricPrompt.CryptoObject(cipher)
        
        val executor = ContextCompat.getMainExecutor(context)
        
        val biometricPrompt = BiometricPrompt(
            activity,
            executor,
            object : BiometricPrompt.AuthenticationCallback() {
                override fun onAuthenticationSucceeded(
                    result: BiometricPrompt.AuthenticationResult
                ) {
                    result.cryptoObject?.cipher?.let { authenticatedCipher ->
                        onSuccess(authenticatedCipher)
                    }
                }
                
                override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                    onError(errorCode, errString.toString())
                }
            }
        )
        
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Secure Transaction")
            .setSubtitle("Authenticate to proceed")
            .setNegativeButtonText("Cancel")
            .setAllowedAuthenticators(BIOMETRIC_STRONG)
            .build()
        
        biometricPrompt.authenticate(promptInfo, cryptoObject)
    }
    
    private fun getCipherForBiometric(): Cipher {
        val key = keystoreManager.getOrCreateKey()
        val cipher = Cipher.getInstance("AES/GCM/NoPadding")
        cipher.init(Cipher.ENCRYPT_MODE, key)
        return cipher
    }
}

enum class BiometricStatus {
    AVAILABLE,
    NO_HARDWARE,
    HARDWARE_UNAVAILABLE,
    NOT_ENROLLED,
    UNKNOWN
}
```

### 2. Multi-Factor Authentication (MFA)

```kotlin
// MFAManager.kt
class MFAManager @Inject constructor(
    private val apiService: AuthApiService,
    private val securePreferences: SecurePreferences
) {
    
    suspend fun initiateMFA(userId: String): Result<MFAResponse> {
        return try {
            val response = apiService.initiateMFA(userId)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun verifyMFACode(
        userId: String,
        code: String,
        mfaToken: String
    ): Result<AuthToken> {
        return try {
            val response = apiService.verifyMFA(
                VerifyMFARequest(userId, code, mfaToken)
            )
            
            // Store token securely
            securePreferences.saveToken(response.accessToken)
            
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun setupTOTP(userId: String): Result<TOTPSetup> {
        return try {
            val response = apiService.setupTOTP(userId)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

data class MFAResponse(
    val mfaToken: String,
    val expiresIn: Long,
    val method: MFAMethod
)

data class TOTPSetup(
    val secret: String,
    val qrCodeUrl: String,
    val backupCodes: List<String>
)

enum class MFAMethod {
    SMS, EMAIL, TOTP, PUSH
}
```

### 3. Session Management

```kotlin
// SessionManager.kt
@Singleton
class SessionManager @Inject constructor(
    private val securePreferences: SecurePreferences,
    private val apiService: AuthApiService,
    @ApplicationContext private val context: Context
) {
    
    private val _sessionState = MutableStateFlow<SessionState>(SessionState.Unknown)
    val sessionState: StateFlow<SessionState> = _sessionState.asStateFlow()
    
    private var sessionTimer: Job? = null
    private var lastActivityTime = System.currentTimeMillis()
    
    companion object {
        private const val SESSION_TIMEOUT_MS = 5 * 60 * 1000L // 5 minutes
        private const val WARNING_TIMEOUT_MS = 4 * 60 * 1000L // 4 minutes
    }
    
    fun startSession(token: String, refreshToken: String) {
        securePreferences.saveToken(token)
        securePreferences.saveRefreshToken(refreshToken)
        
        _sessionState.value = SessionState.Active
        startSessionTimer()
    }
    
    fun updateActivity() {
        lastActivityTime = System.currentTimeMillis()
    }
    
    private fun startSessionTimer() {
        sessionTimer?.cancel()
        sessionTimer = CoroutineScope(Dispatchers.Default).launch {
            while (isActive) {
                delay(10_000) // Check every 10 seconds
                
                val inactiveTime = System.currentTimeMillis() - lastActivityTime
                
                when {
                    inactiveTime >= SESSION_TIMEOUT_MS -> {
                        endSession()
                        break
                    }
                    inactiveTime >= WARNING_TIMEOUT_MS -> {
                        _sessionState.value = SessionState.Warning
                    }
                }
            }
        }
    }
    
    suspend fun refreshToken(): Result<Boolean> {
        val refreshToken = securePreferences.getRefreshToken() ?: return Result.failure(
            Exception("No refresh token")
        )
        
        return try {
            val response = apiService.refreshToken(RefreshTokenRequest(refreshToken))
            securePreferences.saveToken(response.accessToken)
            response.refreshToken?.let { securePreferences.saveRefreshToken(it) }
            
            lastActivityTime = System.currentTimeMillis()
            _sessionState.value = SessionState.Active
            
            Result.success(true)
        } catch (e: Exception) {
            endSession()
            Result.failure(e)
        }
    }
    
    fun endSession() {
        sessionTimer?.cancel()
        securePreferences.clear()
        _sessionState.value = SessionState.Expired
    }
    
    fun isSessionValid(): Boolean {
        return _sessionState.value == SessionState.Active
    }
}

sealed class SessionState {
    object Unknown : SessionState()
    object Active : SessionState()
    object Warning : SessionState()
    object Expired : SessionState()
}
```

### 4. Device Binding

```kotlin
// DeviceManager.kt
class DeviceManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val securePreferences: SecurePreferences
) {
    
    fun getDeviceId(): String {
        var deviceId = securePreferences.getDeviceId()
        
        if (deviceId == null) {
            deviceId = generateDeviceId()
            securePreferences.saveDeviceId(deviceId)
        }
        
        return deviceId
    }
    
    private fun generateDeviceId(): String {
        // Generate unique device identifier
        val androidId = Settings.Secure.getString(
            context.contentResolver,
            Settings.Secure.ANDROID_ID
        )
        
        val deviceInfo = buildString {
            append(androidId)
            append(Build.MANUFACTURER)
            append(Build.MODEL)
            append(Build.BRAND)
        }
        
        return hashString(deviceInfo)
    }
    
    fun getDeviceFingerprint(): DeviceFingerprint {
        return DeviceFingerprint(
            deviceId = getDeviceId(),
            manufacturer = Build.MANUFACTURER,
            model = Build.MODEL,
            osVersion = Build.VERSION.SDK_INT.toString(),
            appVersion = BuildConfig.VERSION_NAME,
            screenDensity = context.resources.displayMetrics.densityDpi.toString(),
            screenResolution = getScreenResolution(),
            isRooted = RootDetector.isRooted(),
            isEmulator = EmulatorDetector.isEmulator()
        )
    }
    
    private fun getScreenResolution(): String {
        val metrics = context.resources.displayMetrics
        return "${metrics.widthPixels}x${metrics.heightPixels}"
    }
    
    private fun hashString(input: String): String {
        val digest = MessageDigest.getInstance("SHA-256")
        val hash = digest.digest(input.toByteArray())
        return Base64.encodeToString(hash, Base64.NO_WRAP)
    }
}

data class DeviceFingerprint(
    val deviceId: String,
    val manufacturer: String,
    val model: String,
    val osVersion: String,
    val appVersion: String,
    val screenDensity: String,
    val screenResolution: String,
    val isRooted: Boolean,
    val isEmulator: Boolean
)
```
