# 💾 Data Storage Security & At-Rest Encryption

> **Safeguarding persistent data on Android using Android KeyStore, EncryptedSharedPreferences, SQLCipher, and memory zeroization techniques.**

---

## 🔒 1. Storage Security Hierarchy

```
+-----------------------------------------------------------------+
| Level 3: Android KeyStore (StrongBox / Hardware TEE)           |
|          - Stores ONLY Master Encryption Keys (AES-256-GCM)     |
+-----------------------------------------------------------------+
                               │ (Decrypts at runtime)
                               ▼
+-----------------------------------------------------------------+
| Level 2: Application Data Vaults                                |
|          - EncryptedSharedPreferences (Jetpack Security)        |
|          - SQLCipher 4 / Room with SQLite Encryption            |
|          - EncryptedFile (for downloaded PDFs, bank statements) |
+-----------------------------------------------------------------+
                               │ (Never plaintext on disk)
                               ▼
+-----------------------------------------------------------------+
| Level 1: App Sandbox (/data/user/0/com.bank.app/)               |
|          - Protected by Linux UID/GID isolation & SELinux       |
+-----------------------------------------------------------------+
```

---

## 💻 2. Production EncryptedSharedPreferences Implementation

```kotlin
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

fun getSecurePreferences(context: Context): SharedPreferences {
    val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .setRequestStrongBoxed(true) // Hardware StrongBox where supported
        .build()

    return EncryptedSharedPreferences.create(
        context,
        "secure_bank_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )
}
```

---

## 📋 Data Storage Security Checklist

- [ ] **No Unencrypted Sensitive Data**: No PII, account numbers, JWT tokens, or credit cards in plain `SharedPreferences`, Realm, or default SQLite.
- [ ] **External Storage Prohibition**: Never save sensitive files to `/sdcard/` or external shared storage where other apps with storage permissions could read them.
- [ ] **Clipboard Sanitization**: Mark sensitive input fields (e.g. passwords/card details) with `ClipDescription.MIMETYPE_TEXT_PLAIN` or clear clipboard history after pasting.
- [ ] **Memory Zeroization**: PINs and passwords stored in `CharArray` or `ByteArray` and explicitly zeroed out with `Arrays.fill(pin, '0')` in a `finally` block.
