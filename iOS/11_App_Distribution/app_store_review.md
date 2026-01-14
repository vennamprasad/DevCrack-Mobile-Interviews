# 📝 App Store Review
> **Targeted for iOS Developers**
> **Note:** Guidelines, Rejections, and Metadata.

![Review](https://img.shields.io/badge/Distribution-App_Store-blue?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Common Rejections](#1-common-rejections)
- [2. Guidelines](#2-guidelines)
- [3. Expedited Review](#3-expedited-review)

---

### Q1. Top reasons for Rejection?

**Answer:**
1.  **Crashes**: App crashes on launch (reviewers test on iPad even if iPhone only!).
2.  **Incomplete Info**: Missing demo account credentials.
3.  **Guideline 2.1 (Performance)**: Placeholder content ("Lorem Ipsum").
4.  **Guideline 3.1.1 (Payments)**: Trying to unlock features without using In-App Purchase (IAP).
5.  **Privacy Policy**: Missing or invalid URL.

### Q2. App Tracking Transparency (ATT)?

**Answer:**
If you collect IDFA (Identifier for Advertisers) or share data with 3rd parties (Facebook SDK, Analytics), you **must** show the ATT prompt (`requestTrackingAuthorization`).
Failing to do so (or tracking before asking) causes rejection.

### Q3. Can I ask for an Expedited Review?

**Answer:**
Yes, but sparingly.
**Valid reasons**: Critical Bug Fix (fixing a crash for users), Sensitive Timing Event.
**Invalid reasoning**: "I forgot to submit yesterday."

### Q4. Developer Response?

**Answer:**
If rejected, you can communicate with the reviewer in Resolution Center. Often, clarifications ("This feature is hidden here...") can resolve the rejection without a new binary upload.
