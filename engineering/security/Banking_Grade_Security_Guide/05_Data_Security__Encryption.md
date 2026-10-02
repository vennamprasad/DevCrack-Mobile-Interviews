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
