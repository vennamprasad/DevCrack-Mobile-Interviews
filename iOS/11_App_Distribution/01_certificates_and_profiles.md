# 📜 Certificates & Profiles
> **Targeted for iOS Developers**
> **Note:** Signing, Entitlements, and Provisioning.

![Signing](https://img.shields.io/badge/Distribution-Signing-yellow?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Certificate (`.p12`)](#1-certificate)
- [2. App ID & Entitlements](#2-app-id)
- [3. Provisioning Profile](#3-provisioning-profile)

---

### Q1. The Triangle of Signing?

**Answer:**
1.  **Who** (Certificate): Identifies the Developer/Team. (Private Key).
2.  **What** (App ID): Identifies the App (Bundle ID).
3.  **Where** (Device): Identifies allowed devices (UDIDs) - *Only for Dev/AdHoc builds*.
The **Provisioning Profile** binds these three together.

### Q2. Development vs Distribution Certificate?

**Answer:**
- **Development**: Used to run app on your phone during debugging.
- **Distribution**: Used for App Store, TestFlight, or Enterprise distribution. Apps signed with this cannot be debugged.

### Q3. What happens when a Profile expires?

**Answer:**
- **Development**: App crashes on launch.
- **Enterprise**: App crashes on launch.
- **App Store**: Nothing. Apple re-signs the app on their server. The expiration only matters *at the moment of upload*.

### Q4. Automatic Signing?

**Answer:**
Xcode manages the creation of Certificates and Profiles for you. It simplifies the process but can cause "Revocation" headaches if multiple team members hit "Reset" buttons.
**Recommendation**: Use **Fastlane Match** to share one set of keys/profiles via Git.
