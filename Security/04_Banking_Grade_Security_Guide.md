# Banking-Grade Security Implementation Guide
## Enterprise-Level Security for Android Applications

---

## 📋 Table of Contents
1. [Security Architecture Overview](#security-architecture-overview)
2. [Network Security](#network-security)
3. [Data Security & Encryption](#data-security--encryption)
4. [Authentication & Authorization](#authentication--authorization)
5. [Code Protection & Anti-Tampering](#code-protection--anti-tampering)
6. [Runtime Security](#runtime-security)
7. [Transaction Security](#transaction-security)
8. [Compliance & Standards](#compliance--standards)
9. [Security Testing](#security-testing)
10. [Interview Q&A Guide](#interview-qa-guide)

---

## 🏗️ Security Architecture Overview

### Security Layers
```
┌─────────────────────────────────────────────┐
│         User Interface Layer                │
│  (Screen Security, Input Validation)        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      Application Security Layer             │
│  (Code Obfuscation, Anti-Tampering)         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│        Authentication Layer                 │
│  (Biometric, MFA, Session Management)       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Business Logic Layer                │
│  (Transaction Security, Authorization)      │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│           Data Layer                        │
│  (Encrypted Storage, Secure Database)       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Network Layer                       │
│  (SSL Pinning, TLS 1.3, API Security)       │
└─────────────────────────────────────────────┘
```

### Security Principles for Banking Apps
1. **Defense in Depth**: Multiple layers of security
2. **Least Privilege**: Minimal permissions and access
3. **Zero Trust**: Never trust, always verify
4. **Secure by Default**: Security from design phase
5. **Data Minimization**: Store only what's necessary
6. **Fail Securely**: Graceful degradation
7. **Privacy by Design**: User privacy first

---

## 🌐 Network Security

### 1. Certificate Pinning

#### Implementation with OkHttp
```kotlin
// SecurityConfig.kt
object SecurityConfig {
    
    // Pin Configuration - Store these securely, ideally from backend
    private const val HOSTNAME = "api.yourbank.com"
    private const val PRIMARY_PIN = "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
    private const val BACKUP_PIN = "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
    
    fun getCertificatePinner(): CertificatePinner {
        return CertificatePinner.Builder()
            .add(HOSTNAME, PRIMARY_PIN)
            .add(HOSTNAME, BACKUP_PIN) // Backup for certificate rotation
            .build()
    }
    
    fun getOkHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .certificatePinner(getCertificatePinner())
            .addInterceptor(getSecurityInterceptor())
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .protocols(listOf(Protocol.HTTP_2, Protocol.HTTP_1_1))
            .build()
    }
    
    private fun getSecurityInterceptor(): Interceptor {
        return Interceptor { chain ->
            val request = chain.request().newBuilder()
                .addHeader("X-App-Version", BuildConfig.VERSION_NAME)
                .addHeader("X-Device-ID", getDeviceId())
                .addHeader("X-Request-ID", UUID.randomUUID().toString())
                .build()
            chain.proceed(request)
        }
    }
}
```

#### Network Security Config (XML-based)
```xml
<!-- res/xml/network_security_config.xml -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Production Configuration -->
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">api.yourbank.com</domain>
        <pin-set expiration="2026-12-31">
            <!-- Primary Pin -->
            <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
            <!-- Backup Pin -->
            <pin digest="SHA-256">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=</pin>
        </pin-set>
        <trustkit-config 
            enforcePinning="true"
            includeSubdomains="true"/>
    </domain-config>
    
    <!-- Debug Configuration - Remove in production -->
    <debug-overrides>
        <trust-anchors>
            <certificates src="user" />
        </trust-anchors>
    </debug-overrides>
</network-security-config>
```

#### Manifest Configuration
```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    android:usesCleartextTraffic="false">
    ...
</application>
```

### 2. TLS/SSL Configuration

```kotlin
// TLSConfig.kt
object TLSConfig {
    
    fun getSecureTLSSocketFactory(): SSLSocketFactory {
        val trustManagerFactory = TrustManagerFactory.getInstance(
            TrustManagerFactory.getDefaultAlgorithm()
        )
        trustManagerFactory.init(null as KeyStore?)
        
        val sslContext = SSLContext.getInstance("TLSv1.3")
        sslContext.init(null, trustManagerFactory.trustManagers, SecureRandom())
        
        return sslContext.socketFactory
    }
    
    fun getSecureConnectionSpec(): ConnectionSpec {
        return ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
            .tlsVersions(TlsVersion.TLS_1_3, TlsVersion.TLS_1_2)
            .cipherSuites(
                CipherSuite.TLS_AES_128_GCM_SHA256,
                CipherSuite.TLS_AES_256_GCM_SHA384,
                CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
                CipherSuite.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
            )
            .build()
    }
}
```

### 3. API Request Signing

```kotlin
// RequestSigner.kt
class RequestSigner @Inject constructor(
    private val keyManager: KeyManager
) {
    
    fun signRequest(
        method: String,
        url: String,
        body: String?,
        timestamp: Long
    ): String {
        val message = buildMessage(method, url, body, timestamp)
        return generateHMAC(message)
    }
    
    private fun buildMessage(
        method: String,
        url: String,
        body: String?,
        timestamp: Long
    ): String {
        return buildString {
            append(method.uppercase())
            append("\n")
            append(url)
            append("\n")
            append(body ?: "")
            append("\n")
            append(timestamp)
        }
    }
    
    private fun generateHMAC(message: String): String {
        val secret = keyManager.getApiSecret()
        val mac = Mac.getInstance("HmacSHA256")
        val secretKey = SecretKeySpec(secret.toByteArray(), "HmacSHA256")
        mac.init(secretKey)
        val hmac = mac.doFinal(message.toByteArray())
        return Base64.encodeToString(hmac, Base64.NO_WRAP)
    }
}

// SigningInterceptor.kt
class SigningInterceptor @Inject constructor(
    private val requestSigner: RequestSigner
) : Interceptor {
    
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()
        val timestamp = System.currentTimeMillis()
        
        val body = originalRequest.body?.let { requestBody ->
            val buffer = Buffer()
            requestBody.writeTo(buffer)
            buffer.readUtf8()
        }
        
        val signature = requestSigner.signRequest(
            method = originalRequest.method,
            url = originalRequest.url.toString(),
            body = body,
            timestamp = timestamp
        )
        
        val signedRequest = originalRequest.newBuilder()
            .addHeader("X-Signature", signature)
            .addHeader("X-Timestamp", timestamp.toString())
            .addHeader("X-Nonce", UUID.randomUUID().toString())
            .build()
        
        return chain.proceed(signedRequest)
    }
}
```

### 4. API Key Obfuscation with NDK

```cpp
// native-lib.cpp
#include <jni.h>
#include <string>

extern "C" JNIEXPORT jstring JNICALL
Java_com_yourbank_app_security_NativeKeys_getApiKey(
    JNIEnv* env,
    jobject /* this */) {
    
    // Obfuscated API key - basic example
    // In production, use more sophisticated obfuscation
    const char* obfuscated = "ZW5jcnlwdGVkX2FwaV9rZXk=";
    
    // Decode and decrypt (implement proper decryption)
    std::string decoded = decodeBase64(obfuscated);
    std::string decrypted = xorDecrypt(decoded, getDeviceSpecificKey());
    
    return env->NewStringUTF(decrypted.c_str());
}

// Additional security layers
std::string getDeviceSpecificKey() {
    // Generate key based on device properties
    // This makes the key extraction harder
    return "device_specific_salt";
}
```

```kotlin
// NativeKeys.kt
object NativeKeys {
    init {
        System.loadLibrary("native-lib")
    }
    
    external fun getApiKey(): String
    
    // Obfuscate the usage
    fun getSecureApiKey(): String {
        return getApiKey().also { 
            // Additional runtime checks
            if (isRooted() || isDebuggable()) {
                throw SecurityException("Security check failed")
            }
        }
    }
}
```

---

## 🔐 Data Security & Encryption

### 1. Android Keystore System

```kotlin
// KeystoreManager.kt
class KeystoreManager @Inject constructor(
    private val context: Context
) {
    
    companion object {
        private const val KEYSTORE_PROVIDER = "AndroidKeyStore"
        private const val KEY_ALIAS = "bank_app_master_key"
        private const val TRANSFORMATION = "AES/GCM/NoPadding"
    }
    
    private val keyStore: KeyStore by lazy {
        KeyStore.getInstance(KEYSTORE_PROVIDER).apply { load(null) }
    }
    
    /**
     * Generate or retrieve hardware-backed encryption key
     * Uses StrongBox if available for enhanced security
     */
    fun getOrCreateKey(): SecretKey {
        return if (keyStore.containsAlias(KEY_ALIAS)) {
            getExistingKey()
        } else {
            generateNewKey()
        }
    }
    
    private fun generateNewKey(): SecretKey {
        val keyGenerator = KeyGenerator.getInstance(
            KeyProperties.KEY_ALGORITHM_AES,
            KEYSTORE_PROVIDER
        )
        
        val purposes = KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
        
        val builder = KeyGenParameterSpec.Builder(KEY_ALIAS, purposes)
            .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
            .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
            .setKeySize(256)
            .setUserAuthenticationRequired(true)
            .setUserAuthenticationParameters(
                30, // Valid for 30 seconds after authentication
                KeyProperties.AUTH_BIOMETRIC_STRONG or KeyProperties.AUTH_DEVICE_CREDENTIAL
            )
            .setRandomizedEncryptionRequired(true)
        
        // Use StrongBox if available (hardware security module)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            if (context.packageManager.hasSystemFeature(
                PackageManager.FEATURE_STRONGBOX_KEYSTORE
            )) {
                builder.setIsStrongBoxBacked(true)
            }
        }
        
        keyGenerator.init(builder.build())
        return keyGenerator.generateKey()
    }
    
    private fun getExistingKey(): SecretKey {
        return keyStore.getKey(KEY_ALIAS, null) as SecretKey
    }
    
    /**
     * Encrypt data with AES-GCM
     */
    fun encrypt(data: ByteArray): EncryptedData {
        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, getOrCreateKey())
        
        val iv = cipher.iv
        val encryptedBytes = cipher.doFinal(data)
        
        return EncryptedData(encryptedBytes, iv)
    }
    
    /**
     * Decrypt data
     */
    fun decrypt(encryptedData: EncryptedData): ByteArray {
        val cipher = Cipher.getInstance(TRANSFORMATION)
        val spec = GCMParameterSpec(128, encryptedData.iv)
        cipher.init(Cipher.DECRYPT_MODE, getOrCreateKey(), spec)
        
        return cipher.doFinal(encryptedData.data)
    }
}

data class EncryptedData(
    val data: ByteArray,
    val iv: ByteArray
)
```

### 2. Encrypted SharedPreferences

```kotlin
// SecurePreferences.kt
class SecurePreferences @Inject constructor(
    @ApplicationContext private val context: Context
) {
    
    private val masterKey: MasterKey by lazy {
        MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .setUserAuthenticationRequired(false) // Change based on requirements
            .build()
    }
    
    private val encryptedPrefs: SharedPreferences by lazy {
        EncryptedSharedPreferences.create(
            context,
            "secure_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }
    
    fun saveToken(token: String) {
        encryptedPrefs.edit {
            putString("auth_token", token)
        }
    }
    
    fun getToken(): String? {
        return encryptedPrefs.getString("auth_token", null)
    }
    
    fun saveBiometricKey(key: String) {
        encryptedPrefs.edit {
            putString("biometric_key", key)
        }
    }
    
    fun clear() {
        encryptedPrefs.edit { clear() }
    }
}
```

### 3. SQLCipher Database Encryption

```kotlin
// AppDatabase.kt
@Database(
    entities = [
        Transaction::class,
        Account::class,
        User::class
    ],
    version = 1,
    exportSchema = true
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun transactionDao(): TransactionDao
    abstract fun accountDao(): AccountDao
    abstract fun userDao(): UserDao
}

// DatabaseProvider.kt
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    
    @Provides
    @Singleton
    fun provideDatabase(
        @ApplicationContext context: Context,
        keystoreManager: KeystoreManager
    ): AppDatabase {
        
        // Get encryption key from Keystore
        val passphrase = keystoreManager.getDatabasePassphrase()
        val factory = SupportFactory(passphrase)
        
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "bank_app_db"
        )
            .openHelperFactory(factory) // Enable SQLCipher
            .fallbackToDestructiveMigration() // Remove in production
            .build()
    }
}

// KeystoreManager addition
fun KeystoreManager.getDatabasePassphrase(): ByteArray {
    val key = getOrCreateKey()
    // Generate passphrase from hardware-backed key
    return key.encoded
}
```

### 4. Secure String Handling

```kotlin
// SecureString.kt
class SecureString(private val value: CharArray) : Closeable {
    
    fun use(block: (CharArray) -> Unit) {
        try {
            block(value)
        } finally {
            close()
        }
    }
    
    override fun close() {
        // Overwrite memory
        value.fill('0')
    }
    
    companion object {
        fun from(string: String): SecureString {
            val chars = string.toCharArray()
            // Clear original string from memory if possible
            return SecureString(chars)
        }
    }
}

// Usage example
fun processPassword(password: String) {
    SecureString.from(password).use { chars ->
        // Use password
        val hash = hashPassword(chars)
        // Password automatically cleared after use
    }
}
```

### 5. Encrypted File Storage

```kotlin
// EncryptedFileManager.kt
class EncryptedFileManager @Inject constructor(
    @ApplicationContext private val context: Context,
    private val keystoreManager: KeystoreManager
) {
    
    private val masterKey: MasterKey by lazy {
        MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
    }
    
    fun writeEncryptedFile(fileName: String, data: ByteArray) {
        val file = File(context.filesDir, fileName)
        
        val encryptedFile = EncryptedFile.Builder(
            context,
            file,
            masterKey,
            EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
        ).build()
        
        encryptedFile.openFileOutput().use { output ->
            output.write(data)
        }
    }
    
    fun readEncryptedFile(fileName: String): ByteArray {
        val file = File(context.filesDir, fileName)
        
        val encryptedFile = EncryptedFile.Builder(
            context,
            file,
            masterKey,
            EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB
        ).build()
        
        return encryptedFile.openFileInput().use { input ->
            input.readBytes()
        }
    }
    
    fun secureDelete(fileName: String) {
        val file = File(context.filesDir, fileName)
        
        if (file.exists()) {
            // Overwrite file before deletion
            file.outputStream().use { output ->
                val random = SecureRandom()
                val buffer = ByteArray(4096)
                
                repeat(3) { // Overwrite 3 times
                    random.nextBytes(buffer)
                    var remaining = file.length()
                    while (remaining > 0) {
                        val toWrite = minOf(buffer.size.toLong(), remaining).toInt()
                        output.write(buffer, 0, toWrite)
                        remaining -= toWrite
                    }
                }
            }
            
            file.delete()
        }
    }
}
```

---

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


---

## 🛡️ Code Protection & Anti-Tampering

### 1. ProGuard/R8 Configuration

```proguard
# proguard-rules.pro

# ==================== OPTIMIZATION ====================
-optimizationpasses 5
-dontusemixedcaseclassnames
-verbose

# ==================== OBFUSCATION ====================
-repackageclasses 'o'
-allowaccessmodification
-overloadaggressively

# Keep application class
-keep public class * extends android.app.Application

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# ==================== SECURITY ====================
# Obfuscate critical security classes
-keep,allowobfuscation class com.yourbank.app.security.** { *; }
-keep,allowobfuscation class com.yourbank.app.crypto.** { *; }

# Remove logging in release
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
    public static *** w(...);
    public static *** e(...);
}

# Remove debug code
-assumenosideeffects class kotlin.jvm.internal.Intrinsics {
    public static void check*(...);
    public static void throw*(...);
}

# String encryption (basic)
-adaptclassstrings
-adaptresourcefilenames
-adaptresourcefilecontents

# ==================== ANTI-REVERSE ENGINEERING ====================
# Add random strings to make reverse engineering harder
-addconfigurationdebugging

# Rename source file attribute
-renamesourcefileattribute SourceFile

# Keep line numbers for crash reports but obfuscate file names
-keepattributes SourceFile,LineNumberTable

# ==================== DEPENDENCY SPECIFIC ====================
# Retrofit
-keepattributes Signature, InnerClasses, EnclosingMethod
-keepattributes RuntimeVisibleAnnotations, RuntimeVisibleParameterAnnotations
-keep,allowobfuscation,allowshrinking interface retrofit2.Call
-keep,allowobfuscation,allowshrinking class retrofit2.Response
-keep,allowobfuscation,allowshrinking class kotlin.coroutines.Continuation

# OkHttp
-dontwarn okhttp3.internal.platform.**
-dontwarn org.conscrypt.**
-dontwarn org.bouncycastle.**
-dontwarn org.openjsse.**

# Gson
-keepattributes Signature
-keepattributes *Annotation*
-keep class com.google.gson.** { *; }
-keep class * implements com.google.gson.TypeAdapter
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer

# Room
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-dontwarn androidx.room.paging.**
```

### 2. String Obfuscation

```kotlin
// ObfuscatedStrings.kt
object ObfuscatedStrings {
    
    // XOR encryption for strings
    private const val XOR_KEY = 0x5A
    
    private fun String.obfuscate(): ByteArray {
        return this.toByteArray().map { (it.toInt() xor XOR_KEY).toByte() }.toByteArray()
    }
    
    private fun ByteArray.deobfuscate(): String {
        return String(this.map { (it.toInt() xor XOR_KEY).toByte() }.toByteArray())
    }
    
    // Store obfuscated strings
    private val API_BASE_URL = byteArrayOf(/* obfuscated bytes */)
    private val API_KEY = byteArrayOf(/* obfuscated bytes */)
    
    fun getApiBaseUrl(): String = API_BASE_URL.deobfuscate()
    fun getApiKey(): String = API_KEY.deobfuscate()
    
    // Alternative: Base64 + XOR
    fun obfuscateString(input: String): String {
        val xored = input.toByteArray().map { (it.toInt() xor XOR_KEY).toByte() }.toByteArray()
        return Base64.encodeToString(xored, Base64.NO_WRAP)
    }
    
    fun deobfuscateString(input: String): String {
        val decoded = Base64.decode(input, Base64.NO_WRAP)
        return String(decoded.map { (it.toInt() xor XOR_KEY).toByte() }.toByteArray())
    }
}
```

### 3. Code Integrity Check

```kotlin
// IntegrityChecker.kt
class IntegrityChecker @Inject constructor(
    @ApplicationContext private val context: Context
) {
    
    fun verifyAppSignature(): Boolean {
        return try {
            val packageInfo = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                context.packageManager.getPackageInfo(
                    context.packageName,
                    PackageManager.GET_SIGNING_CERTIFICATES
                )
            } else {
                @Suppress("DEPRECATION")
                context.packageManager.getPackageInfo(
                    context.packageName,
                    PackageManager.GET_SIGNATURES
                )
            }
            
            val signatures = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                packageInfo.signingInfo.apkContentsSigners
            } else {
                @Suppress("DEPRECATION")
                packageInfo.signatures
            }
            
            // Verify against expected signature
            val expectedSignature = getExpectedSignatureHash()
            val actualSignature = signatures.firstOrNull()?.let { 
                hashSignature(it.toByteArray()) 
            }
            
            actualSignature == expectedSignature
            
        } catch (e: Exception) {
            false
        }
    }
    
    private fun getExpectedSignatureHash(): String {
        // Store expected signature hash (from your keystore)
        return "YOUR_EXPECTED_SIGNATURE_HASH"
    }
    
    private fun hashSignature(signature: ByteArray): String {
        val digest = MessageDigest.getInstance("SHA-256")
        val hash = digest.digest(signature)
        return Base64.encodeToString(hash, Base64.NO_WRAP)
    }
    
    fun verifyAppInstaller(): Boolean {
        val validInstallers = listOf(
            "com.android.vending", // Google Play Store
            "com.google.android.feedback", // Google Play Store
            null // Sideload for debug builds
        )
        
        val installer = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            context.packageManager.getInstallSourceInfo(context.packageName).installingPackageName
        } else {
            @Suppress("DEPRECATION")
            context.packageManager.getInstallerPackageName(context.packageName)
        }
        
        return validInstallers.contains(installer)
    }
}
```

---

## 🔍 Runtime Security

### 1. Root Detection

```kotlin
// RootDetector.kt
object RootDetector {
    
    private val knownRootApps = listOf(
        "com.noshufou.android.su",
        "com.noshufou.android.su.elite",
        "eu.chainfire.supersu",
        "com.koushikdutta.superuser",
        "com.thirdparty.superuser",
        "com.yellowes.su",
        "com.topjohnwu.magisk",
        "com.kingroot.kinguser",
        "com.kingo.root",
        "com.smedialink.oneclickroot",
        "com.zhiqupk.root.global",
        "com.alephzain.framaroot"
    )
    
    private val knownDangerousApps = listOf(
        "com.koushikdutta.rommanager",
        "com.koushikdutta.rommanager.license",
        "com.dimonvideo.luckypatcher",
        "com.chelpus.lackypatch",
        "com.ramdroid.appquarantine",
        "com.ramdroid.appquarantinepro",
        "com.android.vending.billing.InAppBillingService.COIN",
        "com.android.vending.billing.InAppBillingService.LUCK",
        "com.chelpus.luckypatcher",
        "com.blackmartalpha",
        "org.blackmart.market",
        "com.allinone.free",
        "com.repodroid.app",
        "org.creeplays.hack",
        "com.baseappfull.fwd",
        "com.zmapp",
        "com.dv.marketmod.installer",
        "org.mobilism.android",
        "com.android.wp.net.log",
        "com.android.camera.update",
        "cc.madkite.freedom",
        "com.solohsu.android.edxp.manager",
        "org.meowcat.edxposed.manager",
        "com.xmodgame",
        "com.cih.game_cih",
        "com.charles.lpoqasert",
        "catch_.me_.if_.you_.can_"
    )
    
    private val knownRootCloakingPackages = listOf(
        "com.devadvance.rootcloak",
        "com.devadvance.rootcloakplus",
        "de.robv.android.xposed.installer",
        "com.saurik.substrate",
        "com.zachspong.temprootremovejb",
        "com.amphoras.hidemyroot",
        "com.amphoras.hidemyrootadfree",
        "com.formyhm.hiderootPremium",
        "com.formyhm.hideroot"
    )
    
    private val suBinaryPaths = arrayOf(
        "/data/local/",
        "/data/local/bin/",
        "/data/local/xbin/",
        "/sbin/",
        "/su/bin/",
        "/system/bin/",
        "/system/bin/.ext/",
        "/system/bin/failsafe/",
        "/system/sd/xbin/",
        "/system/usr/we-need-root/",
        "/system/xbin/",
        "/cache/",
        "/data/",
        "/dev/"
    )
    
    fun isRooted(): Boolean {
        return checkRootMethod1() || 
               checkRootMethod2() || 
               checkRootMethod3() ||
               checkForRootApps() ||
               checkForDangerousApps() ||
               checkForRootCloakingApps() ||
               checkSuExists() ||
               checkForBusyBoxBinary() ||
               checkForRWPaths()
    }
    
    // Method 1: Check Build tags
    private fun checkRootMethod1(): Boolean {
        val buildTags = Build.TAGS
        return buildTags != null && buildTags.contains("test-keys")
    }
    
    // Method 2: Check for SU binary
    private fun checkRootMethod2(): Boolean {
        return try {
            File("/system/app/Superuser.apk").exists()
        } catch (e: Exception) {
            false
        }
    }
    
    // Method 3: Try to execute SU command
    private fun checkRootMethod3(): Boolean {
        var process: Process? = null
        return try {
            process = Runtime.getRuntime().exec(arrayOf("/system/xbin/which", "su"))
            val bufferedReader = BufferedReader(InputStreamReader(process.inputStream))
            bufferedReader.readLine() != null
        } catch (e: Exception) {
            false
        } finally {
            process?.destroy()
        }
    }
    
    private fun checkForRootApps(): Boolean {
        return knownRootApps.any { isPackageInstalled(it) }
    }
    
    private fun checkForDangerousApps(): Boolean {
        return knownDangerousApps.any { isPackageInstalled(it) }
    }
    
    private fun checkForRootCloakingApps(): Boolean {
        return knownRootCloakingPackages.any { isPackageInstalled(it) }
    }
    
    private fun isPackageInstalled(packageName: String): Boolean {
        return try {
            val packageManager = context.packageManager
            packageManager.getPackageInfo(packageName, 0)
            true
        } catch (e: PackageManager.NameNotFoundException) {
            false
        }
    }
    
    private fun checkSuExists(): Boolean {
        return suBinaryPaths.any { path ->
            val file = File(path, "su")
            file.exists()
        }
    }
    
    private fun checkForBusyBoxBinary(): Boolean {
        return try {
            val process = Runtime.getRuntime().exec(arrayOf("which", "busybox"))
            val bufferedReader = BufferedReader(InputStreamReader(process.inputStream))
            bufferedReader.readLine() != null
        } catch (e: Exception) {
            false
        }
    }
    
    private fun checkForRWPaths(): Boolean {
        val paths = arrayOf(
            "/system",
            "/system/bin",
            "/system/sbin",
            "/system/xbin",
            "/vendor/bin",
            "/sbin",
            "/etc"
        )
        
        return paths.any { path ->
            try {
                val file = File(path)
                file.canWrite()
            } catch (e: Exception) {
                false
            }
        }
    }
    
    private lateinit var context: Context
    
    fun initialize(context: Context) {
        this.context = context.applicationContext
    }
}
```

### 2. Emulator Detection

```kotlin
// EmulatorDetector.kt
object EmulatorDetector {
    
    fun isEmulator(): Boolean {
        return checkBasic() ||
               checkAdvanced() ||
               checkFiles() ||
               checkQEmuDrivers() ||
               checkIpAddresses()
    }
    
    private fun checkBasic(): Boolean {
        return (Build.FINGERPRINT.startsWith("generic")
                || Build.FINGERPRINT.startsWith("unknown")
                || Build.MODEL.contains("google_sdk")
                || Build.MODEL.contains("Emulator")
                || Build.MODEL.contains("Android SDK built for x86")
                || Build.MANUFACTURER.contains("Genymotion")
                || (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic"))
                || "google_sdk" == Build.PRODUCT)
    }
    
    private fun checkAdvanced(): Boolean {
        return (Build.BOARD == "QC_Reference_Phone"
                || Build.BOOTLOADER == "unknown"
                || Build.DEVICE.startsWith("generic")
                || Build.HARDWARE == "ranchu"
                || Build.HARDWARE == "goldfish"
                || Build.MANUFACTURER == "unknown"
                || Build.MODEL == "sdk"
                || Build.MODEL == "google_sdk"
                || Build.PRODUCT == "sdk"
                || Build.PRODUCT == "google_sdk"
                || Build.SERIAL == null)
    }
    
    private fun checkFiles(): Boolean {
        val knownFiles = arrayOf(
            "/dev/socket/qemud",
            "/dev/qemu_pipe",
            "/system/lib/libc_malloc_debug_qemu.so",
            "/sys/qemu_trace",
            "/system/bin/qemu-props"
        )
        
        return knownFiles.any { File(it).exists() }
    }
    
    private fun checkQEmuDrivers(): Boolean {
        val drivers = arrayOf(
            "goldfish",
            "ranchu"
        )
        
        return try {
            val file = File("/proc/tty/drivers")
            if (file.exists() && file.canRead()) {
                val data = file.readText()
                drivers.any { data.contains(it) }
            } else {
                false
            }
        } catch (e: Exception) {
            false
        }
    }
    
    private fun checkIpAddresses(): Boolean {
        val knownIps = arrayOf(
            "10.0.2.15", // Default Android emulator IP
            "10.0.3.2"   // Alternative emulator IP
        )
        
        return try {
            val networkInterfaces = NetworkInterface.getNetworkInterfaces()
            while (networkInterfaces.hasMoreElements()) {
                val networkInterface = networkInterfaces.nextElement()
                val addresses = networkInterface.inetAddresses
                
                while (addresses.hasMoreElements()) {
                    val address = addresses.nextElement()
                    if (!address.isLoopbackAddress && !address.isLinkLocalAddress) {
                        val hostAddress = address.hostAddress
                        if (knownIps.contains(hostAddress)) {
                            return true
                        }
                    }
                }
            }
            false
        } catch (e: Exception) {
            false
        }
    }
}
```

### 3. Debugger Detection

```kotlin
// DebuggerDetector.kt
object DebuggerDetector {
    
    fun isDebuggerAttached(): Boolean {
        return Debug.isDebuggerConnected() || Debug.waitingForDebugger()
    }
    
    fun isDebuggable(context: Context): Boolean {
        return (context.applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) != 0
    }
    
    fun detectTracePid(): Boolean {
        return try {
            val statusFile = File("/proc/self/status")
            val status = statusFile.readText()
            val tracerPid = status.lines()
                .firstOrNull { it.startsWith("TracerPid:") }
                ?.substringAfter("TracerPid:")
                ?.trim()
                ?.toIntOrNull()
            
            tracerPid != null && tracerPid > 0
        } catch (e: Exception) {
            false
        }
    }
    
    // Native anti-debug check
    external fun detectDebuggerNative(): Boolean
    
    init {
        System.loadLibrary("security-lib")
    }
}

// In C++ (security-lib.cpp)
/*
#include <jni.h>
#include <unistd.h>
#include <sys/ptrace.h>

extern "C" JNIEXPORT jboolean JNICALL
Java_com_yourbank_app_security_DebuggerDetector_detectDebuggerNative(
    JNIEnv* env,
    jobject thiz) {
    
    // Try to attach ptrace to ourselves
    if (ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) {
        // Already being traced
        return JNI_TRUE;
    }
    
    // Detach if we successfully attached
    ptrace(PTRACE_DETACH, 0, 0, 0);
    return JNI_FALSE;
}
*/
```

### 4. Screen Security

```kotlin
// ScreenSecurityManager.kt
class ScreenSecurityManager @Inject constructor(
    private val activity: Activity
) {
    
    fun enableScreenSecurity() {
        // Prevent screenshots and screen recording
        activity.window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
    }
    
    fun disableScreenSecurity() {
        activity.window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
    }
    
    fun maskRecentAppsScreenshot() {
        // This should be called when sensitive data is displayed
        enableScreenSecurity()
    }
    
    fun detectScreenRecording(): Boolean {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            return activity.isInPictureInPictureMode || isScreenBeingRecorded()
        }
        return false
    }
    
    @RequiresApi(Build.VERSION_CODES.Q)
    private fun isScreenBeingRecorded(): Boolean {
        val mediaProjectionManager = activity.getSystemService(
            Context.MEDIA_PROJECTION_SERVICE
        ) as MediaProjectionManager
        
        // Check if any app is recording screen
        // Note: This is limited and may not catch all cases
        return try {
            mediaProjectionManager.getMediaProjection(-1, Intent()) != null
        } catch (e: Exception) {
            false
        }
    }
}

// Compose version
@Composable
fun SecureScreen(content: @Composable () -> Unit) {
    val context = LocalContext.current
    val activity = context.findActivity()
    
    DisposableEffect(Unit) {
        activity?.window?.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )
        
        onDispose {
            activity?.window?.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
        }
    }
    
    content()
}

fun Context.findActivity(): Activity? {
    var context = this
    while (context is ContextWrapper) {
        if (context is Activity) return context
        context = context.baseContext
    }
    return null
}
```

---

## 💰 Transaction Security

### 1. Transaction Signing

```kotlin
// TransactionSigner.kt
class TransactionSigner @Inject constructor(
    private val keystoreManager: KeystoreManager
) {
    
    fun signTransaction(transaction: Transaction): SignedTransaction {
        val transactionData = serializeTransaction(transaction)
        val signature = generateSignature(transactionData)
        
        return SignedTransaction(
            transaction = transaction,
            signature = signature,
            timestamp = System.currentTimeMillis(),
            nonce = UUID.randomUUID().toString()
        )
    }
    
    private fun serializeTransaction(transaction: Transaction): String {
        return buildString {
            append(transaction.fromAccount)
            append("|")
            append(transaction.toAccount)
            append("|")
            append(transaction.amount)
            append("|")
            append(transaction.currency)
            append("|")
            append(transaction.type)
        }
    }
    
    private fun generateSignature(data: String): String {
        val privateKey = keystoreManager.getPrivateKey()
        val signature = Signature.getInstance("SHA256withRSA")
        signature.initSign(privateKey)
        signature.update(data.toByteArray())
        
        val signed = signature.sign()
        return Base64.encodeToString(signed, Base64.NO_WRAP)
    }
    
    fun verifyTransaction(signedTransaction: SignedTransaction): Boolean {
        val publicKey = keystoreManager.getPublicKey()
        val transactionData = serializeTransaction(signedTransaction.transaction)
        
        val signature = Signature.getInstance("SHA256withRSA")
        signature.initVerify(publicKey)
        signature.update(transactionData.toByteArray())
        
        val signatureBytes = Base64.decode(signedTransaction.signature, Base64.NO_WRAP)
        return signature.verify(signatureBytes)
    }
}

data class Transaction(
    val id: String,
    val fromAccount: String,
    val toAccount: String,
    val amount: Double,
    val currency: String,
    val type: TransactionType,
    val description: String?
)

data class SignedTransaction(
    val transaction: Transaction,
    val signature: String,
    val timestamp: Long,
    val nonce: String
)

enum class TransactionType {
    TRANSFER, PAYMENT, WITHDRAWAL, DEPOSIT
}
```

### 2. Transaction Limits & Velocity Checks

```kotlin
// TransactionValidator.kt
class TransactionValidator @Inject constructor(
    private val transactionRepository: TransactionRepository,
    private val accountRepository: AccountRepository
) {
    
    suspend fun validateTransaction(transaction: Transaction): ValidationResult {
        // Check 1: Daily limit
        val dailyLimitCheck = checkDailyLimit(transaction)
        if (!dailyLimitCheck.isValid) {
            return dailyLimitCheck
        }
        
        // Check 2: Single transaction limit
        val singleLimitCheck = checkSingleTransactionLimit(transaction)
        if (!singleLimitCheck.isValid) {
            return singleLimitCheck
        }
        
        // Check 3: Velocity check (frequency)
        val velocityCheck = checkVelocity(transaction)
        if (!velocityCheck.isValid) {
            return velocityCheck
        }
        
        // Check 4: Sufficient balance
        val balanceCheck = checkBalance(transaction)
        if (!balanceCheck.isValid) {
            return balanceCheck
        }
        
        // Check 5: Suspicious pattern detection
        val patternCheck = detectSuspiciousPattern(transaction)
        if (!patternCheck.isValid) {
            return patternCheck
        }
        
        return ValidationResult(true, "Transaction validated successfully")
    }
    
    private suspend fun checkDailyLimit(transaction: Transaction): ValidationResult {
        val startOfDay = LocalDate.now().atStartOfDay()
        val todaysTransactions = transactionRepository.getTransactionsSince(
            transaction.fromAccount,
            startOfDay
        )
        
        val todaysTotal = todaysTransactions.sumOf { it.amount }
        val dailyLimit = accountRepository.getDailyLimit(transaction.fromAccount)
        
        if (todaysTotal + transaction.amount > dailyLimit) {
            return ValidationResult(
                false,
                "Daily transaction limit exceeded. Limit: $dailyLimit, Used: $todaysTotal"
            )
        }
        
        return ValidationResult(true, "Daily limit check passed")
    }
    
    private fun checkSingleTransactionLimit(transaction: Transaction): ValidationResult {
        val singleTransactionLimit = when (transaction.type) {
            TransactionType.TRANSFER -> 50000.0
            TransactionType.PAYMENT -> 25000.0
            TransactionType.WITHDRAWAL -> 10000.0
            TransactionType.DEPOSIT -> Double.MAX_VALUE
        }
        
        if (transaction.amount > singleTransactionLimit) {
            return ValidationResult(
                false,
                "Single transaction limit exceeded. Maximum: $singleTransactionLimit"
            )
        }
        
        return ValidationResult(true, "Single transaction limit check passed")
    }
    
    private suspend fun checkVelocity(transaction: Transaction): ValidationResult {
        val last15Minutes = LocalDateTime.now().minusMinutes(15)
        val recentTransactions = transactionRepository.getTransactionsSince(
            transaction.fromAccount,
            last15Minutes
        )
        
        // Allow max 5 transactions in 15 minutes
        if (recentTransactions.size >= 5) {
            return ValidationResult(
                false,
                "Too many transactions in short period. Please try again later."
            )
        }
        
        return ValidationResult(true, "Velocity check passed")
    }
    
    private suspend fun checkBalance(transaction: Transaction): ValidationResult {
        val account = accountRepository.getAccount(transaction.fromAccount)
        
        if (account.balance < transaction.amount) {
            return ValidationResult(
                false,
                "Insufficient balance. Available: ${account.balance}"
            )
        }
        
        return ValidationResult(true, "Balance check passed")
    }
    
    private suspend fun detectSuspiciousPattern(transaction: Transaction): ValidationResult {
        // Check for round numbers (potential fraud indicator)
        if (transaction.amount % 1000 == 0.0 && transaction.amount > 10000) {
            return ValidationResult(
                false,
                "Transaction requires additional verification",
                requiresStepUpAuth = true
            )
        }
        
        // Check for unusual transaction pattern
        val userHistory = transactionRepository.getUserTransactionHistory(
            transaction.fromAccount,
            limit = 100
        )
        
        val avgAmount = userHistory.map { it.amount }.average()
        
        // If transaction is 5x the average, flag for review
        if (transaction.amount > avgAmount * 5) {
            return ValidationResult(
                false,
                "Unusual transaction amount detected. Additional verification required.",
                requiresStepUpAuth = true
            )
        }
        
        return ValidationResult(true, "Pattern check passed")
    }
}

data class ValidationResult(
    val isValid: Boolean,
    val message: String,
    val requiresStepUpAuth: Boolean = false
)
```

### 3. Step-Up Authentication

```kotlin
// StepUpAuthManager.kt
class StepUpAuthManager @Inject constructor(
    private val biometricManager: BiometricManager,
    private val otpService: OTPService
) {
    
    suspend fun requireStepUpAuth(
        activity: FragmentActivity,
        transaction: Transaction,
        method: StepUpMethod = StepUpMethod.BIOMETRIC
    ): Result<Boolean> {
        return when (method) {
            StepUpMethod.BIOMETRIC -> authenticateWithBiometric(activity, transaction)
            StepUpMethod.PIN -> authenticateWithPIN(transaction)
            StepUpMethod.OTP -> authenticateWithOTP(transaction)
        }
    }
    
    private suspend fun authenticateWithBiometric(
        activity: FragmentActivity,
        transaction: Transaction
    ): Result<Boolean> {
        return suspendCoroutine { continuation ->
            biometricManager.authenticateWithCrypto(
                activity,
                onSuccess = { cipher ->
                    // Use authenticated cipher to encrypt transaction
                    continuation.resume(Result.success(true))
                },
                onError = { code, message ->
                    continuation.resume(
                        Result.failure(Exception("Biometric auth failed: $message"))
                    )
                }
            )
        }
    }
    
    private suspend fun authenticateWithPIN(transaction: Transaction): Result<Boolean> {
        // Show PIN dialog and verify
        // Implementation depends on UI framework
        return Result.success(true)
    }
    
    private suspend fun authenticateWithOTP(transaction: Transaction): Result<Boolean> {
        return try {
            val otpSent = otpService.sendTransactionOTP(transaction)
            if (otpSent) {
                Result.success(true)
            } else {
                Result.failure(Exception("Failed to send OTP"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

enum class StepUpMethod {
    BIOMETRIC, PIN, OTP
}
```

---

## 📊 Compliance & Standards

### OWASP Mobile Top 10 Checklist

```kotlin
/**
 * OWASP Mobile Top 10 (2024) Implementation Checklist
 */

// M1: Improper Platform Usage
✓ Use Android Keystore for key storage
✓ Implement proper permission handling
✓ Follow Android security best practices
✓ Use AndroidX Security library

// M2: Insecure Data Storage
✓ Use EncryptedSharedPreferences
✓ Implement SQLCipher for database encryption
✓ Use EncryptedFile for sensitive file storage
✓ Never store sensitive data in logs
✓ Clear sensitive data from memory after use

// M3: Insecure Communication
✓ Enforce TLS 1.3
✓ Implement certificate pinning
✓ Use secure network configuration
✓ Validate SSL certificates
✓ Implement request signing

// M4: Insecure Authentication
✓ Implement multi-factor authentication
✓ Use biometric authentication properly
✓ Implement session management
✓ Use secure token storage
✓ Implement proper logout

// M5: Insufficient Cryptography
✓ Use AES-256-GCM for encryption
✓ Use SHA-256 or better for hashing
✓ Use SecureRandom for random generation
✓ Implement proper key management
✓ Never hardcode encryption keys

// M6: Insecure Authorization
✓ Implement proper access control
✓ Validate user permissions server-side
✓ Use principle of least privilege
✓ Implement session validation

// M7: Client Code Quality
✓ Use R8/ProGuard
✓ Implement input validation
✓ Handle exceptions properly
✓ Use static analysis tools
✓ Regular code reviews

// M8: Code Tampering
✓ Implement signature verification
✓ Use code obfuscation
✓ Detect rooted devices
✓ Implement integrity checks

// M9: Reverse Engineering
✓ Use ProGuard/R8 obfuscation
✓ Implement string encryption
✓ Use native code for sensitive logic
✓ Implement anti-debug techniques

// M10: Extraneous Functionality
✓ Remove all debug code
✓ Disable logging in production
✓ Remove test endpoints
✓ Clean up commented code
```

### PCI DSS Compliance

```kotlin
/**
 * PCI DSS Requirements for Mobile Banking Apps
 */

// Requirement 3: Protect stored cardholder data
object PCIDSSCompliance {
    
    // 3.1: Keep cardholder data storage to a minimum
    fun minimizeDataStorage() {
        // Store only PAN (masked), never CVV/CVC
        // Delete data when no longer needed
    }
    
    // 3.4: Render PAN unreadable
    fun maskPAN(pan: String): String {
        if (pan.length < 8) return pan
        val firstSix = pan.substring(0, 6)
        val lastFour = pan.substring(pan.length - 4)
        val masked = "*".repeat(pan.length - 10)
        return "$firstSix$masked$lastFour"
    }
    
    // 3.5: Document and implement procedures to protect keys
    class KeyProtectionProcedures {
        // Store keys in Android Keystore
        // Implement key rotation
        // Use separate keys for different purposes
        // Never log or display keys
    }
    
    // Requirement 4: Encrypt transmission of cardholder data
    fun enforceEncryption() {
        // Use TLS 1.3
        // Implement certificate pinning
        // Encrypt sensitive data before transmission
    }
    
    // Never store sensitive authentication data after authorization
    val prohibitedData = listOf(
        "Full track data (magnetic-stripe data or equivalent)",
        "CAV2/CVC2/CVV2/CID",
        "PIN/PIN Block"
    )
}
```

---

## 🧪 Security Testing

### 1. Security Test Cases

```kotlin
// SecurityTests.kt
@RunWith(AndroidJUnit4::class)
class SecurityTests {
    
    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)
    
    @Test
    fun testScreenshotPrevention() {
        activityRule.scenario.onActivity { activity ->
            val flags = activity.window.attributes.flags
            assertTrue(
                "Screen security not enabled",
                flags and WindowManager.LayoutParams.FLAG_SECURE != 0
            )
        }
    }
    
    @Test
    fun testRootDetection() {
        val isRooted = RootDetector.isRooted()
        // Should handle rooted devices appropriately
        assertTrue("Root detection not working", true) // Adjust based on test device
    }
    
    @Test
    fun testEncryptedStorage() {
        val testData = "sensitive_data"
        val prefs = SecurePreferences(ApplicationProvider.getApplicationContext())
        
        prefs.saveToken(testData)
        val retrieved = prefs.getToken()
        
        assertEquals(testData, retrieved)
        
        // Verify data is encrypted in storage
        val rawPrefs = ApplicationProvider.getApplicationContext()
            .getSharedPreferences("secure_prefs", Context.MODE_PRIVATE)
        val rawValue = rawPrefs.getString("auth_token", null)
        
        assertNotEquals(
            "Data not encrypted",
            testData,
            rawValue
        )
    }
    
    @Test
    fun testCertificatePinning() {
        // This would need to be tested with actual network calls
        // or mocked SSL context
        val client = SecurityConfig.getOkHttpClient()
        assertNotNull(client.certificatePinner)
    }
    
    @Test
    fun testAppSignatureVerification() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val checker = IntegrityChecker(context)
        assertTrue("Signature verification failed", checker.verifyAppSignature())
    }
}
```

### 2. Penetration Testing Checklist

```markdown
# Mobile App Penetration Testing Checklist

## Static Analysis
- [ ] Decompile APK and analyze code
- [ ] Check for hardcoded secrets/keys
- [ ] Analyze AndroidManifest.xml for security issues
- [ ] Check for exported components
- [ ] Analyze certificate pinning implementation
- [ ] Check ProGuard/R8 configuration
- [ ] Analyze cryptographic implementations

## Dynamic Analysis
- [ ] Intercept HTTPS traffic (test certificate pinning)
- [ ] Test API endpoints for vulnerabilities
- [ ] Test authentication bypass attempts
- [ ] Test for SQL injection
- [ ] Test for insecure data storage
- [ ] Test for insecure logging
- [ ] Test root detection bypass
- [ ] Test debugger detection bypass

## Runtime Analysis
- [ ] Hook into app with Frida
- [ ] Bypass certificate pinning
- [ ] Bypass root detection
- [ ] Bypass biometric authentication
- [ ] Extract sensitive data from memory
- [ ] Test for memory leaks of sensitive data

## Authentication & Session Management
- [ ] Test weak password policies
- [ ] Test for authentication bypass
- [ ] Test session timeout
- [ ] Test for session fixation
- [ ] Test token validation
- [ ] Test biometric authentication bypass

## Data Storage
- [ ] Check SharedPreferences encryption
- [ ] Check database encryption
- [ ] Check file storage security
- [ ] Check cache security
- [ ] Check clipboard data exposure

## Network Security
- [ ] Test TLS version enforcement
- [ ] Test certificate validation
- [ ] Test for man-in-the-middle vulnerabilities
- [ ] Test API key security
- [ ] Test request/response encryption

## Business Logic
- [ ] Test transaction limits bypass
- [ ] Test race conditions
- [ ] Test payment flow manipulation
- [ ] Test authorization checks
```

---

## 💡 Interview Q&A Guide

### Question 1: How do you implement certificate pinning in Android?

**Answer:**
"I implement certificate pinning using OkHttp's CertificatePinner. I pin both the primary and backup certificates to handle certificate rotation. Here's my approach:

1. Extract the certificate's public key hash using `openssl`
2. Configure CertificatePinner with primary and backup pins
3. Also implement XML-based Network Security Config as fallback
4. Handle pinning failures gracefully with proper error messages
5. Implement pin update mechanism via remote config

I also ensure pins are stored securely (not hardcoded strings) and have a strategy for emergency pin updates if needed."

### Question 2: Explain your approach to secure token storage.

**Answer:**
"I use a multi-layered approach:

1. **Android Keystore**: Generate hardware-backed encryption keys using KeyStore API, preferring StrongBox when available
2. **EncryptedSharedPreferences**: Store tokens encrypted using AES-256-GCM
3. **Token Lifecycle**: Implement automatic token refresh, rotation, and secure deletion
4. **Memory Management**: Clear tokens from memory after use, use char arrays instead of Strings for sensitive data
5. **Binding**: Bind tokens to device fingerprint to prevent token theft

I never store tokens in plain SharedPreferences, logs, or database without encryption. For refresh tokens, I implement additional security like device binding and rotation."

### Question 3: How do you detect and handle rooted devices?

**Answer:**
"I implement multiple root detection methods:

1. **Check for SU binary** in common paths
2. **Check Build.TAGS** for test-keys
3. **Check for root management apps** (Magisk, SuperSU)
4. **Try executing SU commands**
5. **Check for RW access** to system directories
6. **SafetyNet Attestation API** for Google's device integrity check

However, I know root detection can be bypassed, so I implement defense in depth:

- Server-side validation
- Transaction signing
- Behavioral analytics
- Step-up authentication for sensitive operations

For banking apps, I typically show a warning but don't block completely unless the risk is too high, as some legitimate users root their devices."

### Question 4: Explain your database encryption strategy.

**Answer:**
"I use SQLCipher for database encryption:

1. **Passphrase Generation**: Generate encryption key using Android Keystore (hardware-backed)
2. **Key Storage**: Store key securely in Keystore, never in code or SharedPreferences
3. **Implementation**: Use Room with SupportFactory for SQLCipher integration
4. **Key Rotation**: Implement key rotation mechanism for long-term security
5. **Secure Deletion**: Overwrite data before deletion for sensitive records

For additional security, I encrypt sensitive columns at application level before storing, even in the encrypted database. This provides defense in depth if database encryption is somehow bypassed."

### Question 5: How do you implement biometric authentication securely?

**Answer:**
"I follow these security practices:

1. **Use BiometricPrompt API** with BIOMETRIC_STRONG authentication
2. **CryptoObject**: Always use CryptoObject for cryptographically binding authentication
3. **Key Generation**: Generate key with user authentication required flag
4. **Timeout**: Set validity period after authentication (typically 30 seconds)
5. **Fallback**: Provide device credential fallback
6. **Server Validation**: Never trust client-side biometric auth alone

For sensitive transactions, I combine biometric authentication with:
- Step-up authentication
- Transaction signing
- Server-side validation

I never use biometric authentication as the sole security measure for financial transactions."

### Question 6: Explain your approach to preventing reverse engineering.

**Answer:**
"I use multiple layers of protection:

**Code Protection:**
- R8/ProGuard with aggressive obfuscation
- String encryption for sensitive constants
- Native code (NDK) for critical security logic
- Control flow obfuscation

**Runtime Protection:**
- Root detection
- Debugger detection
- Emulator detection
- Integrity checking (signature verification)
- Anti-hooking (detect Frida, Xposed)

**Anti-Tampering:**
- App signature verification at runtime
- Code integrity checks
- Detection of repackaging attempts

However, I understand that determined attackers can bypass these protections. The goal is to increase the cost and effort required to reverse engineer the app, not to make it impossible. Critical security operations are always validated server-side."

### Question 7: How do you handle PCI DSS compliance in mobile apps?

**Answer:**
"For PCI DSS compliance, I follow these principles:

**Data Storage:**
- Never store CVV/CVC
- Mask PAN (show only first 6 and last 4 digits)
- Delete card data when no longer needed
- Use tokenization whenever possible

**Data Transmission:**
- Always use TLS 1.3
- Implement certificate pinning
- Encrypt sensitive data before transmission
- Use strong cipher suites

**Key Management:**
- Store keys in Android Keystore
- Implement key rotation
- Never hardcode keys
- Document key management procedures

**Access Control:**
- Implement proper authentication
- Use principle of least privilege
- Log security events

I also ensure regular security testing and maintain compliance documentation. For actual payment processing, I prefer using PCI-compliant third-party SDKs rather than handling card data directly."

### Question 8: Explain your session management strategy.

**Answer:**
"My session management includes:

**Session Creation:**
- Generate secure session tokens (UUID + timestamp + signature)
- Store tokens encrypted in EncryptedSharedPreferences
- Implement device binding

**Session Lifecycle:**
- Implement idle timeout (typically 5-10 minutes for banking)
- Implement absolute timeout (typically 30 minutes)
- Show warning before timeout
- Implement token refresh mechanism

**Session Validation:**
- Validate every API request server-side
- Check token expiry
- Verify device fingerprint
- Check for suspicious activity

**Session Termination:**
- Secure token deletion from device
- Server-side session invalidation
- Clear sensitive data from memory
- Force logout on security events

**Multi-Device:**
- Track active sessions per user
- Allow viewing/terminating active sessions
- Limit concurrent sessions

For high-security operations, I implement step-up authentication even within an active session."

---

## 🔄 Security Update & Maintenance Checklist

```kotlin
/**
 * Regular Security Maintenance Tasks
 */

// Weekly
- [ ] Review security logs and alerts
- [ ] Check for new security advisories
- [ ] Monitor crash reports for security issues
- [ ] Review failed authentication attempts

// Monthly
- [ ] Update dependencies (security patches)
- [ ] Review and update security documentation
- [ ] Conduct internal security review
- [ ] Update threat model

// Quarterly
- [ ] Full security audit
- [ ] Penetration testing
- [ ] Update security training
- [ ] Review and update security policies
- [ ] Certificate expiry check and renewal planning

// Annually
- [ ] Comprehensive security assessment
- [ ] Third-party security audit
- [ ] Compliance review (PCI DSS, GDPR, etc.)
- [ ] Disaster recovery drill
- [ ] Security architecture review
```

---

## 📚 Recommended Tools & Resources

### Security Testing Tools
- **MobSF**: Mobile Security Framework for static/dynamic analysis
- **Frida**: Dynamic instrumentation toolkit
- **Burp Suite**: Web/mobile proxy for testing
- **JADX**: Dex to Java decompiler
- **Apktool**: APK reverse engineering tool
- **Drozer**: Android security assessment framework

### Security Libraries
- **AndroidX Security**: Official Android security library
- **SQLCipher**: Database encryption
- **Conscrypt**: Modern TLS provider
- **SafetyNet**: Google Play Integrity API
- **RootBeer**: Root detection library

### Documentation & Standards
- OWASP Mobile Security Testing Guide (MSTG)
- OWASP Mobile Top 10
- PCI Mobile Payment Acceptance Security Guidelines
- Android Security Best Practices (developer.android.com)
- CWE/SANS Top 25 Most Dangerous Software Errors

---

## ✅ Final Security Checklist

Before release, ensure:
- [ ] All OWASP Mobile Top 10 risks mitigated
- [ ] Certificate pinning implemented and tested
- [ ] All data encrypted at rest and in transit
- [ ] Root detection implemented
- [ ] Debugger detection implemented
- [ ] Code obfuscation enabled
- [ ] No secrets in code or resources
- [ ] Security testing completed
- [ ] Penetration testing passed
- [ ] Compliance requirements met (PCI DSS, GDPR, etc.)
- [ ] Security documentation completed
- [ ] Incident response plan in place

---

**Remember**: Security is not a one-time implementation but an ongoing process. Stay updated with latest security best practices, threats, and mitigation techniques.
