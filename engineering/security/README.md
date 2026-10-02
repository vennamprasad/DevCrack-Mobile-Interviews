# 🛡️ Mobile Security & Reverse Engineering Defense

> **A Comprehensive Guide to Mobile Application Security, OWASP Mobile Top 10, Banking-Grade Hardening, and Pentesting.**

![Security](https://img.shields.io/badge/Security-OWASP_Mobile_Top_10-red?style=for-the-badge&logo=shield)
![Hardening](https://img.shields.io/badge/Hardening-Banking_Grade-blue?style=for-the-badge)
![AntiTamper](https://img.shields.io/badge/Protection-Anti_Tamper-orange?style=for-the-badge)

---

## 📖 Module Contents

| Guide | Description | Target Level |
| :--- | :--- | :--- |
| **[01. OWASP Mobile Top 10](./01_OWASP_Mobile_Top_10.md)** | Core vulnerabilities (M1–M10), improper platform usage, insecure storage, cryptography flaws. | Mid / Senior |
| **[02. Reverse Engineering Defense](./02_Reverse_Engineering_Defense.md)** | R8/ProGuard obfuscation, root/jailbreak detection, Frida/Xposed hooks, dynamic instrumentation defense. | Senior / Staff |
| **[03. OWASP Implementation Checklist](./03_OWASP_Implementation_Checklist.md)** | Step-by-step developer implementation audit checklist for MASVS / OWASP Mobile 2024. | All Levels |
| **[04. Penetration Testing Checklist](./04_Penetration_Testing_Checklist.md)** | Static analysis, dynamic analysis, APK decompilation, network intercept testing, and report generation. | Senior / Lead |
| **[05. Screen Recording & Screenshot Defense](./05_Screen_Record_and_Screenshot_Defense.md)** | `FLAG_SECURE`, Jetpack Compose window flags, PCI DSS compliance, banking-grade screen obfuscation. | Mid / Senior |
| **[Banking-Grade Security Guide](./Banking_Grade_Security_Guide/README.md)** | 22-chapter deep-dive into enterprise mobile security: Keystore, hardware-backed keys, network security, and compliance. | Staff / Architect |

---

## 🏛️ The Defense-in-Depth Security Matrix

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  - FLAG_SECURE (Prevent screenshots & recents leaks)         │
│  - Screen tapjacking / Overlay protection (filterTouches)   │
│  - BiometricPrompt with CryptoObject (Keystore-backed)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    Application & Runtime                     │
│  - Root & Jailbreak detection (SafetyNet / Play Integrity)  │
│  - Hook detection (Frida, Xposed, Substrate, ptrace)         │
│  - R8 Name Obfuscation + String/Flow obfuscation (DexGuard) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                     Data at Rest (Storage)                   │
│  - EncryptedSharedPreferences / Jetpack Security            │
│  - SQLCipher for SQLite / Room Database                     │
│  - Android Keystore / iOS Keychain (Secure Enclave)         │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                    Data in Transit (Network)                │
│  - TLS 1.3 strict enforcement (disable plaintext HTTP)     │
│  - SSL / Certificate Pinning (HPKP / Network Security Config)│
│  - Mutual TLS (mTLS) for high-security enterprise endpoints │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Top Interview Focus Areas

1. **Hardware-Backed Keystore vs SharedPreferences:** How keys are generated, stored in TEE/StrongBox, and never exposed in plaintext RAM.
2. **Frida Dynamic Hooking:** How attackers hook methods at runtime to bypass checks, and how native C/C++ checks detect hooked pointers and debuggers.
3. **SSL Pinning & Pin Rotation:** Public key hashes (`sha256/`) vs leaf certificates, backup pins, and handling expired certificates without app store updates.
4. **Android 14/15 Security Updates:** Stricter intent filters, restricted background broadcasts, and safer dynamic code loading requirements.
