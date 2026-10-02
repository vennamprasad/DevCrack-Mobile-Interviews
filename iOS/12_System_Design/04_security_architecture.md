# 🔐 Security Architecture
> **Targeted for Senior iOS Developers**
> **Note:** Threat Modeling, Storage, and Jailbreak.

![Security](https://img.shields.io/badge/Design-Security-red?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Threat Model](#1-threat-model)
- [2. Data at Rest](#2-data-at-rest)
- [3. Data in Transit](#3-data-in-transit)

---

### Q1. Core iOS Security Features?

**Answer:**
- **Sandbox**: Isolates app data.
- **Code Signing**: Ensures code hasn't been tampered with.
- **ASLR**: Randomizes memory locations to prevent buffer overflow exploits.
- **Data Protection API**: Encrypts files on disk based on device passcode state.

### Q2. How to detect Jailbreak?

**Answer:**
Check for artifacts:
- File existence (`/bin/bash`, `/Applications/Cydia.app`).
- Can write to outside sandbox (`/private/jailbreak.txt`).
- Protocol handlers (`cydia://`).
**Note**: It's a cat-and-mouse game. Detection creates an "arms race".

### Q3. Secure user session management?

**Answer:**
- **Token**: Access Token (Short lived, 15m), Refresh Token (Long lived).
- **Storage**: Store Refresh Token in **Keychain** with Biometric Access Control.
- **SSL Pinning**: Prevent MITM attacks intercepting the token.

### Q4. Obfuscation?

**Answer:**
Tools like **SwiftShield** rename classes/methods to random strings (`a.b()`) to make reverse engineering the binary harder.
Not a silver bullet, but keeps honest people (and script kiddies) out.
