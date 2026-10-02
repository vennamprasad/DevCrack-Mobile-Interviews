# 🔒 iOS Security Architecture: Secure Enclave, Keychain, CryptoKit & Biometrics

> **Hardening enterprise iOS applications: Hardware-backed Secure Enclave encryption, Keychain Services access controls, biometric authentication (Face ID / Touch ID), CryptoKit, and runtime anti-tampering.**

---

## 📌 Executive Summary

Building enterprise, banking, and healthcare iOS applications requires moving far beyond basic HTTPS and local storage. 

A high-security iOS architecture relies on Apple's **hardware-rooted security model**:
1. **The Secure Enclave Processor (SEP)**: A dedicated coprocessor isolated from the main application processor (CPU). Private keys generated inside the Secure Enclave **never enter application memory or the iOS kernel**.
2. **Keychain Services with Access Control**: Protecting tokens with hardware encryption and ensuring keys cannot be transferred to other devices via iCloud backups (`ThisDeviceOnly`).
3. **Biometric Invalidation Protection**: Preventing unauthorized access if a thief adds their face to an iPhone whose passcode was compromised.
4. **App Attest & DeviceCheck**: Cryptographically proving to backend servers that a request originated from an authentic, unmodified app on genuine Apple hardware.

---

## 🏗️ Hardware Security Architecture: Application Processor vs. Secure Enclave

```
┌──────────────────────────────────────┐     Hardware Mailbox / Shared Memory     ┌──────────────────────────────────────┐
│       Application Processor (CPU)    │ <======================================> │         Secure Enclave (SEP)         │
│                                      │                                          │                                      │
│ • Runs iOS Kernel & Apps             │                                          │ • Runs its own secure microkernel    │
│ • Swift Application Code             │                                          │ • Dedicated hardware TRNG & AES unit │
│ • Request: "Sign this hash using     │                                          │ • Private Key stays locked in silicon│
│             Key ID #482"             │                                          │ • Computes signature in hardware and │
│                                      │                                          │   returns ONLY the signature bytes!  │
└──────────────────────────────────────┘                                          └──────────────────────────────────────┘
```

---

## 🔑 Keychain Services: Cryptographic Access Controls

Never store sensitive data (JWTs, session tokens, refresh tokens, encryption keys) in `UserDefaults` or plaintext files! `UserDefaults` is stored as an unencrypted `.plist` on disk, easily extractable from device backups.

Always store secrets in the **iOS Keychain**.

### Choosing the Correct Accessibility Level

| Accessibility Attribute | Storage Behavior & Security Profile | Best Used For |
| :--- | :--- | :--- |
| `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` | **Most Secure.** Data is decrypted only while the device is actively unlocked by the user. Bound to hardware; never restored to other devices via iCloud or iTunes backups. | **Financial auth tokens, payment credentials, biometric secrets.** |
| `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` | Data is decrypted after the user unlocks the phone once after booting, and remains accessible even when locked (e.g. for background sync). | Background sync tokens, VoIP push tokens. |
| `kSecAttrAccessibleAlways` | **DEPRECATED.** Highly insecure. | ❌ Never use in modern iOS development. |

---

## 🧬 Biometric Authentication with Invalidation Protection

### The "Passcode Shoulder-Surfing" Attack
If an attacker discovers a user's 6-digit phone passcode, steals the iPhone, and enrolls their own face into Face ID in Settings, a naive biometric check (`LAContext.evaluatePolicy`) will **happily authenticate the thief!**

### The Enterprise Defense: `biometryCurrentSet`
When saving the private key or token into Keychain, bind it to the **current biometric set**:
- If any face or fingerprint is added or removed from iOS settings, the OS **permanently invalidates the Keychain item**, rendering the stolen credentials completely useless!

```swift
import Foundation
import Security
import LocalAuthentication

final class SecureKeyStore {

    func saveBiometricSecuredToken(key: String, data: Data) throws {
        // 1. Create Access Control bound to the CURRENT biometric enrollment
        var error: Unmanaged<CFError>?
        guard let accessControl = SecAccessControlCreateWithFlags(
            kCFAllocatorDefault,
            kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
            [.biometryCurrentSet, .userPresence], // Invalidated if new face added!
            &error
        ) else {
            throw error!.takeRetainedValue() as Error
        }

        // 2. Build Keychain Query
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            kSecAttrAccessControl as String: accessControl
        ]

        // 3. Atomically write to Keychain
        SecItemDelete(query as CFDictionary) // Delete any existing entry first
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else {
            throw KeychainError(status: status)
        }
    }
}
```

---

## 🛡️ Modern Cryptography with Apple CryptoKit & Secure Enclave

Generate hardware-bound Elliptic Curve P-256 keys directly inside the Secure Enclave:

```swift
import CryptoKit

final class DeviceSigner {

    // Generates a private key directly inside hardware silicon
    func createHardwareKey() throws -> SecureEnclave.P256.Signing.PrivateKey {
        guard SecureEnclave.isAvailable else {
            throw SecurityError.secureEnclaveUnavailable
        }

        // Generate P-256 key locked to Secure Enclave
        let privateKey = try SecureEnclave.P256.Signing.PrivateKey(
            compactRepresentable: false,
            accessControl: SecAccessControlCreateWithFlags(
                nil,
                kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
                [.privateKeyUsage],
                nil
            )!
        )

        return privateKey
    }

    // Sign transaction payload with hardware key
    func signTransaction(payload: Data, privateKey: SecureEnclave.P256.Signing.PrivateKey) throws -> Data {
        let signature = try privateKey.signature(for: payload)
        return signature.rawRepresentation
    }
}
```

---

## 🕵️ Runtime Security & Anti-Tampering Defenses

### 1. Jailbreak Detection
Check for common jailbreak artifacts, broken sandboxes, and suspicious dynamic linker hooks:
```swift
final class JailbreakDetector {
    static func isDeviceCompromised() -> Bool {
        #if targetEnvironment(simulator)
        return false // Don't flag development simulators
        #else
        // 1. Check for common jailbreak binaries
        let suspiciousPaths = [
            "/Applications/Cydia.app",
            "/Library/MobileSubstrate/MobileSubstrate.dylib",
            "/bin/bash",
            "/usr/sbin/sshd",
            "/etc/apt"
        ]
        for path in suspiciousPaths {
            if FileManager.default.fileExists(atPath: path) {
                return true
            }
        }

        // 2. Check for sandbox write violation
        do {
            let testString = "JailbreakSandboxTest"
            let testPath = "/private/jailbreak_test.txt"
            try testString.write(toFile: testPath, atomically: true, encoding: .utf8)
            try FileManager.default.removeItem(atPath: testPath)
            return true // Sandbox broken!
        } catch {
            // Expected failure: sandbox is intact
        }

        return false
        #endif
    }
}
```

### 2. Preventing Data Leaks in App Switcher
When a user swipes up to the iOS App Switcher, the operating system takes an automatic snapshot of the current window and caches it to disk:
- If the screen displays bank account numbers or credit cards, that snapshot is a security vulnerability.
- **Defense**: Obscure the window with a blur overlay when entering background:
  ```swift
  .onChange(of: scenePhase) { _, phase in
      if phase == .background || phase == .inactive {
          showPrivacyBlurOverlay = true
      } else {
          showPrivacyBlurOverlay = false
      }
  }
  ```

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "What is Apple App Attest (DeviceCheck), and how does it prevent API replay attacks from botnets?"
* **Answer**:
  - `DCAppAttestService` is an Apple service that validates that an API request originated from **your genuine, unmodified application running on a real, non-jailbroken Apple device**.
  - **Handshake Flow**:
    1. The app generates a cryptographic key pair inside the Secure Enclave.
    2. The app requests an Attestation Object from Apple's Attestation servers.
    3. The client sends the attestation and an initial challenge nonce to your backend.
    4. Your backend validates the certificate chain against Apple’s App Attest root CA.
    5. All subsequent API calls are signed with the Secure Enclave key and verified on the server, completely eliminating automated scripts, Postman spoofing, and reverse-engineered API abuse.

### Q2: "Why should you pin Subject Public Key Info (SPKI) instead of the Leaf Certificate in SSL Pinning?"
* **Answer**:
  - **Leaf Certificate Pinning**: Pins the exact binary certificate. When the certificate expires (typically every 90 to 365 days), you **must release an emergency app update**; otherwise, older app versions will fail all network requests and break.
  - **Public Key (SPKI) Pinning**: Pins only the cryptographic public key hash inside the certificate. When renewing your SSL certificate, you can generate the new certificate using the **same public key / CSR**, allowing the app to accept the renewed certificate without requiring a client-side update!
