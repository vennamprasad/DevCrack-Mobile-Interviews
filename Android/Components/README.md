# 🧩 Android Fundamentals & Core Components

> **Master the fundamental building blocks of the Android OS: Activities, Services, Broadcast Receivers, and Content Providers.**

![Android](https://img.shields.io/badge/Android-Components-3DDC84?style=for-the-badge&logo=android)
![Lifecycle](https://img.shields.io/badge/Lifecycle-Core_OS-blue?style=for-the-badge)
![IPC](https://img.shields.io/badge/IPC-Binder_&_Intents-orange?style=for-the-badge)

---

## 📖 Chapter Index

- **[Android Components Deep Dive](./components.md)**
  - **1. Activities & Lifecycle:** State transitions (`onCreate`, `onStart`, `onResume`, `onPause`, `onStop`, `onDestroy`, `onRestart`), process death (`onSaveInstanceState`, `ViewModelProvider`), configuration changes, launch modes (`standard`, `singleTop`, `singleTask`, `singleInstance`), and back stack tasks.
  - **2. Services:** Foreground services (notification requirements, Android 14 type declaration), Background services, Bound services (`IBinder`, `ServiceConnection`), and migration to `WorkManager`.
  - **3. Broadcast Receivers:** Static (manifest) vs dynamic (context-registered) receivers, ordered broadcasts, local broadcasts, security restrictions (Android 8+ background broadcast limits, `RECEIVER_EXPORTED` / `RECEIVER_NOT_EXPORTED` in Android 13+).
  - **4. Content Providers:** Abstracting data sharing across processes, `UriMatcher`, `ContentResolver`, `ContentObserver`, permissions, and SQLite integration.
  - **5. Inter-Component Communication:** Explicit vs Implicit Intents, PendingIntents (mutability flags `FLAG_IMMUTABLE`), AIDL (Android Interface Definition Language), and Messenger IPC.

---

## 💡 Quick Architectural Rule of Thumb

| Component | Primary Purpose | Lifecycle Tied To | Best Modern Alternative (if applicable) |
| :--- | :--- | :--- | :--- |
| **Activity** | UI Window & User Interaction | User focus / Task backstack | Single-Activity Architecture + Compose Navigation |
| **Foreground Service** | Immediate user-perceived task (playback, navigation) | User notification | `WorkManager` (with Foreground Info) |
| **Background Work** | Deferred, guaranteed work (uploads, sync) | OS Battery & Constraints | `WorkManager` (Periodic / OneTimeWorkRequest) |
| **Broadcast Receiver** | React to system/app events | Execution window (brief, < 10s) | Local Flow / Event bus for in-app events |
| **Content Provider** | Inter-process data sharing | Calling app process lifecycle | Standard REST API / Room DB for internal app data |
