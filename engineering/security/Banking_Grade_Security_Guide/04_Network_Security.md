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
