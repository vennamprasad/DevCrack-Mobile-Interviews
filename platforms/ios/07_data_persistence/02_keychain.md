# 🔑 Keychain Services
> **Targeted for Senior iOS Developers**
> **Note:** Secure secure storage for secrets.

![Keychain](https://img.shields.io/badge/Storage-Keychain-black?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Security](#1-security)
- [2. Access Control](#2-access-control)
- [3. Sharing Data](#3-sharing-data)

---

### Q1. How is Keychain different from UserDefaults?

**Answer:**
- **Encrypted**: Data is encrypted by the OS.
- **Persistent**: Can persist even after the app is uninstalled (if configured).
- **Secure**: Designed for Passwords, Certificates, and Tokens.

### Q2. How to use it?

**Answer:**
The native C-API is complex (`SecItemAdd`, `SecItemCopyMatching`).
Most developers use wrappers like `Valet`, `KeychainAccess`, or `KeychainSwift` for a Swift-friendly API.

### Q3. Sharing Keychain between apps?

**Answer:**
Yes, via **Keychain Groups**.
If two apps share the same App ID Prefix (Team ID) and have the entitlement for the same Keychain Group, they can read each other's secrets. Essential for SSO (Single Sign On) between a suite of apps.

### Q4. Biometric Protection?

**Answer:**
You can set an access control flag `.userPresence` or `.biometryCurrentSet`.
The Keychain will **require** FaceID/TouchID before revealing the item to your app.
