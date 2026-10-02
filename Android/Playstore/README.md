# 🛒 Google Play Store & Android App Distribution

> **Master the release lifecycle, Google Play Console, Android App Bundles (AAB), Play Feature Delivery, Android Vitals, and policy compliance.**

![PlayStore](https://img.shields.io/badge/Store-Google_Play-414141?style=for-the-badge&logo=googleplay)
![Distribution](https://img.shields.io/badge/Format-Android_App_Bundle-3DDC84?style=for-the-badge&logo=android)
![Vitals](https://img.shields.io/badge/Quality-Android_Vitals-blue?style=for-the-badge)

---

## 📖 Chapter Index

- **[Google Play Store & Console Interview Guide](./playstore.md)**
  - **1. General Play Store Questions:** Developer account setup, publishing process, APK vs AAB, Play App Signing, and version code vs version name management.
  - **2. Console-Specific Deep Dives:** Release tracks (Internal, Closed Alpha/Beta, Open Testing, Production), Staged Rollouts (incremental percentages, pausing rollouts), and In-App Updates API (Immediate vs Flexible flows).
  - **3. Advanced Scenarios & Android Vitals:** ANR rate threshold (< 0.47%), crash rate threshold (< 1.09%), frozen frames, slow rendering, target API level deprecation timelines, and Google Play Policy compliance.

---

## 🚀 Key Release & Delivery Concepts

| Concept | What It Does | Why It Matters |
| :--- | :--- | :--- |
| **Android App Bundle (.aab)** | Publishes compiled code and resources; Google Play generates split APKs tailored to user device ABI, screen density, and language. | Reduces download size by 15–35% compared to monolithic APKs. |
| **Play App Signing** | Google securely stores and manages app's upload & signing keys in Google Cloud KMS. | Protects against losing private signing keystore; enables dynamic feature delivery. |
| **Android Vitals** | System metrics tracked directly by the OS measuring stability and responsiveness. | Apps exceeding Bad Behavior Thresholds lose search rankings and explore placement in the Play Store. |
| **Staged Rollout** | Gradually release update to 5% -> 10% -> 20% -> 50% -> 100% of active users. | Catches critical production crashes before affecting the entire user base. |
