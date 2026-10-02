# 🔍 Static Analysis & Decompilation Auditing

> **A comprehensive runbook for performing static security audits, automated scanning, and source-level decompilation vulnerability assessments on Android binaries (APK/AAB).**

---

## 🛠️ Essential Tooling for Static Auditing

| Tool | Purpose | Key Command |
|:---|:---|:---|
| **[JADX](https://github.com/skylot/jadx)** | Decompile APK/DEX to readable Java code | `jadx-gui target.apk` |
| **[MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF)** | Automated Static & Manifest vulnerability analysis | `docker run -it -p 8000:8000 opensecurity/mobsf` |
| **[Apktool](https://ibotpeaches.github.io/Apktool/)** | Disassemble resources and Smali bytecode | `apktool d target.apk -o output_dir` |
| **[Semgrep](https://semgrep.dev/)** | Automated SAST rule matching for Android security smells | `semgrep --config p/android src/` |

---

## 📋 Comprehensive Static Audit Checklist

### 1. Manifest Security (`AndroidManifest.xml`)
- [ ] **Exported Components**: Verify all Activities, Services, BroadcastReceivers, and ContentProviders have `android:exported="false"` unless explicitly designed for external IPC.
- [ ] **Custom Permissions**: If exported, verify strong signature-level protection:
  ```xml
  <permission android:name="com.bank.permission.PAYMENT_IPC" android:protectionLevel="signature" />
  ```
- [ ] **Debuggable & Backup Flags**: Ensure production manifests disable backups and debugging:
  ```xml
  <application
      android:allowBackup="false"
      android:debuggable="false"
      android:networkSecurityConfig="@xml/network_security_config">
  ```
- [ ] **Cleartext Traffic**: Verify `android:usesCleartextTraffic="false"` is strictly enforced.

### 2. Hardcoded Secrets & Cryptographic Keys
- [ ] Scan decompiled sources for API tokens, AWS keys, Stripe secret keys, and encryption salts.
- [ ] Check `.so` native libraries using `strings libnative.so | grep -E "(API|KEY|SECRET|PASSWORD)"`.

### 3. Obfuscation & R8 / ProGuard Audit
- [ ] Verify that sensitive class names, method names, and package hierarchies are fully mangled.
- [ ] Verify that sensitive string literals are encrypted or resolved dynamically via native JNI.
