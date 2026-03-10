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
