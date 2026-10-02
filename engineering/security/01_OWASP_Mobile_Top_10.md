# 🛡 OWASP Mobile Top 10 & Security Essentials
> **Focus:** Common Vulnerabilities, Secure Storage, and Networking.

![Security](https://img.shields.io/badge/Topic-Security-red?style=for-the-badge)
![OWASP](https://img.shields.io/badge/Standard-OWASP-black?style=for-the-badge)

---

## 📖 Table of Contents
- [1. OWASP Mobile Top 10 (Summary)](#1-owasp-mobile-top-10)
- [2. M1: Improper Platform Usage](#2-m1-improper-platform-usage)
- [3. M2: Insecure Data Storage](#3-m2-insecure-data-storage)
- [4. M3: Insecure Communication](#4-m3-insecure-communication)
- [5. M4: Insecure Authentication](#5-m4-insecure-authentication)

---

## 1. OWASP Mobile Top 10

The Open Web Application Security Project (OWASP) list of top mobile risks (Updated periodically):

1.  **M1: Improper Platform Usage:** Misusing Intents, Keychain, Permissions.
2.  **M2: Insecure Data Storage:** Saving passwords in SharedPrefs/UserDefaults.
3.  **M3: Insecure Communication:** No SSL, Invalid Certs.
4.  **M4: Insecure Authentication:** Leaking Logic, Weak FaceID implementation.
5.  **M5: Insufficient Cryptography:** Hardcoded Keys, Weak Algos (MD5).

---

## 2. M1: Improper Platform Usage

**Risk:** Misusing Android Intents, iOS URL Schemes, or Permissions.
*   **Example:** Making an Activity `exported="true"` that accepts sensitive data, allowing a malicious app to trigger it.
*   **Fix:**
    *   Set `exported="false"` unless necessary.
    *   Validate input from Intents.
    *   Don't request unnecessary permissions.

---

## 3. M2: Insecure Data Storage

**Risk:** Storing sensitive data (Tokens, Passwords, PII) in plain text.
*   **Vulnerability:**
    *   Android `SharedPreferences` (XML).
    *   iOS `UserDefaults` (Plist).
    *   Internal/External SD Card storage.
    *   Hardcoded Strings in Code.

**Fix:**
*   **Android:** Use `EncryptedSharedPreferences` or `Keystore`.
*   **iOS:** Use `Keychain` (Encrypted wrapper).
*   **Database:** Use SQLCipher for Realm/Room encryption.

---

## 4. M3: Insecure Communication

**Risk:** Man-in-the-Middle (MITM) attacks.
*   **Example:** Accepting any SSL certificate (Self-signed) in production code to make testing easier.

**Fix:**
1.  **HTTPS Everywhere:** Never use HTTP.
2.  **SSL Pinning:** Hardcode the hash of the server's certificate public key in the app. If the cert changes (hacker intercept), connection drops.
    *   *Android:* Network Security Config (`res/xml/network_security_config.xml`).
    *   *iOS:* Check `SecTrust` in URLSession delegate or use TrustKit.

---

## 5. M4: Insecure Authentication

**Risk:** Trusting the client-side too much.
*   **Example:** "Unlock App with FaceID".
    *   *Bad:* App checks FaceID -> Returns `True` -> App unlocks. (Hacker can hook the boolean return).
    *   *Good:* FaceID releases a generic encryption key from the hardware enclave that decrypts the local session token.

**Best Practice:**
*   Never store PINs locally if possible.
*   Biometrics should unlock credentials, not just bypass UI screens.
