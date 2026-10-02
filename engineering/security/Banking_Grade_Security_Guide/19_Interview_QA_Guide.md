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
