# 🔒 Security Best Practices
> **Targeted for iOS Developers**
> **Note:** HTTPS, Certificates, and API Keys.

![Security](https://img.shields.io/badge/Networking-Security-black?style=for-the-badge&logo=swift&logoColor=white)

---

## 📖 Table of Contents
- [1. App Transport Security (ATS)](#1-ats)
- [2. SSL Pinning](#2-ssl-pinning)
- [3. Avoiding Man-in-the-Middle](#3-mitm)

---

### Q1. What is ATS?

**Answer:**
App Transport Security. Apple's requirement that all network connections use **HTTPS** with TLS 1.2+. It blocks insecure HTTP connections by default.
**Exception**: You can add `NSAppTransportSecurity` in Info.plist to allow arbitrary loads (not recommended).

### Q2. How to implement SSL Pinning?

**Answer:**
Pinning verifies the server's identity by checking its certificate or public key against a local copy.
- **Why?**: Prevents attackers from intercepting traffic even if they install a custom root certificate on the user's device (MITM).
- **Implementation**:
    - **URLSession**: Implement `urlSession(_:didReceive:completionHandler:)`.
    - **Alamofire**: Use `ServerTrustManager`.

### Q3. Where to store API Keys?

**Answer:**
**NEVER** in code or plist.
1.  Use **Keychain**.
2.  Ideally, don't have keys in the app. Route traffic through your own Backend Proxy which holds the real secrets.
3.  Obfuscate keys using salt/split strings to make reverse engineering harder.
