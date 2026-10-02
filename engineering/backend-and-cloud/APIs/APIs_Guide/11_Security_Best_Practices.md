## **Security Best Practices**

### Q16. What are security best practices for API integration in mobile apps?

**Answer:**

**1. Use HTTPS Only:**
```kotlin
// Network Security Config (res/xml/network_security_config.xml)
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system" />
        </trust-anchors>
    </base-config>
</network-security-config>

// AndroidManifest.xml
<application
    android:networkSecurityConfig="@xml/network_security_config">
</application>
```

**2. Certificate Pinning:**
```kotlin
// Pin specific certificates
val certificatePinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .add("api.example.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=") // Backup pin
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()

// Get certificate hash:
// openssl s_client -servername api.example.com -connect api.example.com:443 | openssl x509 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64
```

**3. Don't Store Sensitive Data in Logs:**
```kotlin
// L Bad
Log.d("API", "Token: $token")
Log.d("API", "Password: $password")

//  Good - Remove in production
class DebugLoggingInterceptor : HttpLoggingInterceptor() {
    init {
        level = if (BuildConfig.DEBUG) {
            Level.BODY
        } else {
            Level.NONE
        }

        // Redact sensitive headers
        redactHeader("Authorization")
        redactHeader("Cookie")
        redactHeader("Set-Cookie")
    }
}
```

**4. Implement Request Signing:**
```kotlin
class RequestSigningInterceptor(private val apiSecret: String) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val original = chain.request()
        val timestamp = System.currentTimeMillis().toString()

        // Create signature
        val signatureData = "${original.method}${original.url}$timestamp"
        val signature = createHmacSha256(signatureData, apiSecret)

        val signed = original.newBuilder()
            .header("X-Timestamp", timestamp)
            .header("X-Signature", signature)
            .build()

        return chain.proceed(signed)
    }

    private fun createHmacSha256(data: String, secret: String): String {
        val mac = Mac.getInstance("HmacSHA256")
        mac.init(SecretKeySpec(secret.toByteArray(), "HmacSHA256"))
        return Base64.encodeToString(mac.doFinal(data.toByteArray()), Base64.NO_WRAP)
    }
}
```

**5. Validate SSL Certificates:**
```kotlin
class SSLCertificateValidator {
    fun createSecureOkHttpClient(context: Context): OkHttpClient {
        try {
            // Load custom trust store if needed
            val trustManagerFactory = TrustManagerFactory.getInstance(
                TrustManagerFactory.getDefaultAlgorithm()
            )
            trustManagerFactory.init(null as KeyStore?)

            val sslContext = SSLContext.getInstance("TLS")
            sslContext.init(null, trustManagerFactory.trustManagers, SecureRandom())

            return OkHttpClient.Builder()
                .sslSocketFactory(
                    sslContext.socketFactory,
                    trustManagerFactory.trustManagers[0] as X509TrustManager
                )
                .build()
        } catch (e: Exception) {
            throw RuntimeException(e)
        }
    }
}
```

**6. Obfuscate API Keys:**
```kotlin
// L Never hardcode
const val API_KEY = "sk_live_123456789"

//  Use BuildConfig (still visible in APK)
buildConfigField("String", "API_KEY", "\"${project.properties["API_KEY"]}\"")
val apiKey = BuildConfig.API_KEY

//  Better: Use NDK to hide keys
external fun getApiKey(): String

// C++ implementation
extern "C" JNIEXPORT jstring JNICALL
Java_com_example_NativeLib_getApiKey(JNIEnv* env, jobject) {
    return env->NewStringUTF("your_api_key_here");
}
```

**7. Implement Rate Limiting on Client:**
```kotlin
class RateLimitInterceptor(
    private val maxRequests: Int = 10,
    private val windowMs: Long = 1000L
) : Interceptor {

    private val timestamps = mutableListOf<Long>()

    @Synchronized
    override fun intercept(chain: Interceptor.Chain): Response {
        val now = System.currentTimeMillis()

        // Remove old timestamps
        timestamps.removeAll { now - it > windowMs }

        if (timestamps.size >= maxRequests) {
            val oldestRequest = timestamps.first()
            val waitTime = windowMs - (now - oldestRequest)
            if (waitTime > 0) {
                Thread.sleep(waitTime)
            }
        }

        timestamps.add(now)
        return chain.proceed(chain.request())
    }
}
```

**8. Validate Response Data:**
```kotlin
fun validateUser(user: User): Result<User> {
    return when {
        user.id <= 0 -> Result.Error(Exception("Invalid user ID"))
        user.email.isBlank() -> Result.Error(Exception("Email is required"))
        !Patterns.EMAIL_ADDRESS.matcher(user.email).matches() ->
            Result.Error(Exception("Invalid email format"))
        else -> Result.Success(user)
    }
}
```

**9. Use ProGuard/R8:**
```groovy
// build.gradle
buildTypes {
    release {
        minifyEnabled true
        proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
    }
}
```

**10. Secure Data in Transit:**
```kotlin
// Enforce TLS 1.2+
val spec = ConnectionSpec.Builder(ConnectionSpec.MODERN_TLS)
    .tlsVersions(TlsVersion.TLS_1_2, TlsVersion.TLS_1_3)
    .cipherSuites(
        CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
        CipherSuite.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
        CipherSuite.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
        CipherSuite.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    )
    .build()

val client = OkHttpClient.Builder()
    .connectionSpecs(listOf(spec))
    .build()
```
