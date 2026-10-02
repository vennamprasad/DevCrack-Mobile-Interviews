# 🕵️ Reverse Engineering Defense
> **Focus:** Root/Jailbreak Detection, Obfuscation, and Tamper Resistance.

![Defense](https://img.shields.io/badge/Topic-Defense-blue?style=for-the-badge)
![Hacking](https://img.shields.io/badge/Risk-High-red?style=for-the-badge)

---

## 📖 Table of Contents
- [1. ProGuard / R8 (Obfuscation)](#1-proguard--r8-obfuscation)
- [2. Root & Jailbreak Detection](#2-root--jailbreak-detection)
- [3. SSL Pinning (Deep Dive)](#3-ssl-pinning)
- [4. Anti-Debugging Techniques](#4-anti-debugging-techniques)

---

## 1. ProGuard / R8 (Obfuscation)

**What:** Renames classes/methods to `a`, `b`, `c`. Removes unused code.
**Why:** Makes decompiled code hard to read.
**Configuration:**
*   `proguard-rules.pro`: Keep code that is accessed via Reflection (e.g., Data classes in Gson/Retrofit).

**Limitations:**
*   Does not encrypt strings. Strings are still visible in `strings.xml` or byte code.
*   **Fix:** Use NDK (C++) to hide keys (harder to reverse) or DexGuard (Commercial) for string encryption.

---

## 2. Root & Jailbreak Detection

**Goal:** Detect if the device is compromised (security sandbox broken).

**Techniques:**
1.  **File Checks:** Look for known binaries (`/system/bin/su`, `/Library/MobileSubstrate`).
2.  **Directory Permissions:** Can the app write to system folders? (If yes -> Rooted).
3.  **Package Methods:** Check for installed apps like "SuperSU", "Cydia", "Magisk".
4.  **Google Play Integrity API (SafetyNet):** Google's server-side check. Returns a verdict signed by Google. *Recommended standard.*

**Cat and Mouse Game:**
*   Hackers use "Magisk Hide" to bypass detection.
*   **Strategy:** Don't just crash. Fail silently or disable sensitive features (e.g., Banking).

---

## 3. SSL Pinning (Deep Dive)

**How it works:**
The app contains the "fingerprint" (SHA-256) of the server's certificate.

**Android (Network Security Config):**
```xml
<network-security-config>
    <domain-config>
        <domain includeSubdomains="true">api.bank.com</domain>
        <pin-set>
            <pin digest="SHA-256">7HIpactkIAq...</pin>
            <pin digest="SHA-256">backupPinForRotation...</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

**Risk:**
If certificate expires/rotates and app isn't updated, the app **bricks**.
**Mitigation:** Always pin the **PublicKey** (SubjectPublicKeyInfo), not the Leaf Certificate, and have backup pins.

---

## 4. Anti-Debugging Techniques

**Goal:** Prevent an attacker from attaching a debugger (GDB/LLDB) to step through your app at runtime.

**Techniques:**
*   **Android:** `android:debuggable="false"` in Manifest (default in Release). Check `Debug.isDebuggerConnected()`.
*   **iOS:** `ptrace` system call with `PT_DENY_ATTACH`.

**Note:** skilled attackers can patch these checks out. "Security through obscurity" is just a speed bump, not a wall.
