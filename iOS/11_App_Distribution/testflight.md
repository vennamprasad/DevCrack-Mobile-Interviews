# ✈️ TestFlight
> **Targeted for iOS Developers**
> **Note:** Beta Testing, Groups, and Compliance.

![TestFlight](https://img.shields.io/badge/Distribution-TestFlight-blue?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Internal vs External](#1-internal-vs-external)
- [2. Beta Review](#2-beta-review)
- [3. Feedback](#3-feedback)

---

### Q1. Internal vs External Testers?

**Answer:**
- **Internal**: Members of your App Store Connect team (Admin, Dev, Marketing).
    - **No Review Needed**: Updates appear immediately.
    - Limit: 100 users.
- **External**: Public users inviting via Email or Public Link.
    - **Review Required**: First build of a version (1.0) needs Apple Review. Subsequent builds (1.0 build 2) are usually instant.
    - Limit: 10,000 users.

### Q2. How long do builds last?

**Answer:**
TestFlight builds expire **90 days** after upload.

### Q3. Export Compliance?

**Answer:**
Every upload asks: "Does your app use encryption?".
Since almost all apps use HTTPS (Encryption), the answer is Yes.
**Fix**: Add `ITSAppUsesNonExemptEncryption` = `NO` to Info.plist if you only use standard HTTPS, to skip the popup dialog.

### Q4. Phased Release?

**Answer:**
Not available for TestFlight (everyone gets update).
Available for **App Store** (release to 1%, 2%, 5%... over 7 days).
