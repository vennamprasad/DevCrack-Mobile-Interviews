# 🔐 Authentication & Session Management Security

> **Implementing biometric hardware crypto binding, rotating token lifecycles, and secure session management for enterprise mobile applications.**

---

## 🏗️ 1. Biometric Authentication with `CryptoObject`

Standard biometric callbacks (e.g. checking `onAuthenticationSucceeded`) can be easily hooked by tools like Frida (`return true`). 

In **banking-grade security**, biometrics must be cryptographically bound to hardware:

```kotlin
// 1. Generate Asymmetric Key in Android KeyStore requiring biometric auth
val keyGenParameterSpec = KeyGenParameterSpec.Builder(
    "BANK_AUTH_KEY",
    KeyProperties.PURPOSE_SIGN or KeyProperties.PURPOSE_VERIFY
)
    .setDigests(KeyProperties.DIGEST_SHA256)
    .setSignaturePaddings(KeyProperties.SIGNATURE_PADDING_RSA_PKCS1)
    .setUserAuthenticationRequired(true)
    .setUserAuthenticationParameters(
        0, // 0 = requires biometric prompt per operation
        KeyProperties.AUTH_BIOMETRIC_STRONG
    )
    .build()

// 2. Initialize Signature with the Private Key
val signature = Signature.getInstance("SHA256withRSA")
val privateKey = keyStore.getKey("BANK_AUTH_KEY", null) as PrivateKey
signature.initSign(privateKey)

// 3. Pass to BiometricPrompt.CryptoObject
val cryptoObject = BiometricPrompt.CryptoObject(signature)
biometricPrompt.authenticate(promptInfo, cryptoObject)

// 4. In callback, sign server challenge:
override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
    val authenticatedSignature = result.cryptoObject?.signature
    authenticatedSignature?.update(serverChallengeNonce)
    val signedPayload = authenticatedSignature?.sign()
    // Send signed payload to backend for cryptographic verification
}
```

---

## 📋 Session Security Checklist

- [ ] **Dual Token Architecture**: Access Token (short-lived, 5–15 mins) + Refresh Token (long-lived, 30 days) with database token rotation.
- [ ] **Inactivity Timeouts**: Enforce automatic logout / session termination after 5 minutes of app backgrounding.
- [ ] **Concurrent Session Control**: Invalidate prior sessions when a new login occurs from a different device fingerprint.
- [ ] **Biometric Invalidation on New Enrollment**: Configure `setInvalidatedByBiometricEnrollment(true)` so private keys are destroyed if a new fingerprint/face is added to the device OS.
