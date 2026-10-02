# 🌐 Network Security & Transport Layer Hardening

> **Defending against Man-in-the-Middle (MITM) attacks, rogue certificates, and protocol downgrade attacks using OkHttp Certificate Pinning, TLS 1.3, and mTLS.**

---

## 🔒 1. Dual-Layer Certificate Pinning Strategy

Certificate pinning ensures the app connects *only* to servers presenting exact known public keys, bypassing compromised system CA root certificates.

```kotlin
import okhttp3.CertificatePinner
import okhttp3.OkHttpClient

val certificatePinner = CertificatePinner.Builder()
    // 1. Primary Leaf Certificate Public Key Pin (SHA-256 SPKI)
    .add("api.bank.com", "sha256/k2v657xUM4MmNGummaoVuGMrktcTDdUjWKe2432epN0=")
    // 2. Backup Intermediate CA Pin (Prevents app outages during emergency cert rotations)
    .add("api.bank.com", "sha256/WoiWRyIOVNa9ihaBciRSC7XHjliYS9VwUGOIud4PB18=")
    .build()

val okHttpClient = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

---

## 🛡️ 2. Android Network Security Config (`network_security_config.xml`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Strictly disable cleartext HTTP traffic across entire app -->
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <!-- Trust ONLY official system CAs, never user-installed CAs -->
            <certificates src="system" />
        </trust-anchors>
    </base-config>

    <domain-config>
        <domain includeSubdomains="true">api.bank.com</domain>
        <pin-set expiration="2027-12-31">
            <pin digest="SHA-256">k2v657xUM4MmNGummaoVuGMrktcTDdUjWKe2432epN0=</pin>
            <!-- Backup Pin -->
            <pin digest="SHA-256">WoiWRyIOVNa9ihaBciRSC7XHjliYS9VwUGOIud4PB18=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

---

## 📋 Network Hardening Checklist

- [ ] **TLS 1.3 Minimum**: Restrict TLS cipher suites to modern authenticated encryption (AES-GCM / ChaCha20-Poly1305).
- [ ] **No Custom TrustManagers**: Never deploy code containing `TrustAllCerts` or empty `checkServerTrusted()` methods.
- [ ] **Mutual TLS (mTLS)**: Hardware-backed client certificate authentication for high-value banking APIs.
- [ ] **VPN & Proxy Detection**: Alert or restrict operations if unknown local proxy configs or VPNs are detected on device.
