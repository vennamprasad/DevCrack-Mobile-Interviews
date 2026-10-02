# 🦄 Kotlin Multiplatform (KMP / KMM)

> **Sharing business logic, networking, and UI across Android, iOS, Desktop, and Web using Kotlin Multiplatform and Compose Multiplatform.**

![KMP](https://img.shields.io/badge/Tech-Kotlin_Multiplatform-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)
![Compose](https://img.shields.io/badge/UI-Compose_Multiplatform-3DDC84?style=for-the-badge)

---

## 📖 Available Guide

- **[Kotlin Multiplatform (KMP/KMM) Guide](./kmm.md)**
  - **Section 1: Core Concepts:** `expect` / `actual` declarations, SourceSets (`commonMain`, `androidMain`, `iosMain`), Kotlin/Native compiler.
  - **Section 2: Memory & Concurrency:** The new Kotlin/Native memory manager (relaxed threading, no freeze requirement), Coroutines and Flow across Swift/Objective-C boundaries.
  - **Section 3: Ecosystem:** Ktor Client, SQLDelight / Room Multiplatform, KotlinX Serialization, Koin KMP.
  - **Section 4: UI Sharing:** Compose Multiplatform on iOS (Skiko rendering, UIKit interop).
  - **Section 5: Real-World Scenarios:** CocoaPods vs Swift Package Manager (SPM) distribution (`XCFramework`), iOS crash symbolication.
