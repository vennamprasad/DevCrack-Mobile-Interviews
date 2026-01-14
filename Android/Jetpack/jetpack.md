# 🚀 Jetpack Architecture Components
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** A suite of libraries to help developers follow best practices and reduce boilerplate code.

![Jetpack](https://img.shields.io/badge/Android-Jetpack-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Clean-blue?style=for-the-badge)
![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white)

---

## 📖 Table of Contents
- [1. Core Components (ViewModel, LiveData)](#-core-components)
- [2. Navigation & Lifecycle](#-navigation--lifecycle)
- [3. Data & Paging](#-data--paging)
- [4. WorkManager](#-background-work)
- [5. Architecture & Best Practices](#-architecture)

---

## ✅ Overview

**Android Jetpack** is a set of components, tools, and guidance to make great Android apps. It unbundles libraries from the Android OS, allowing for more frequent updates.

**Main Categories:**
1.  **Architecture:** ViewModel, LiveData, Room, WorkManager, Navigation.
2.  **UI:** Compose, Fragment, Layout, Palette.
3.  **Behavior:** Permissions, Notifications, Sharing, Slices.
4.  **Foundation:** AppCompat, Android KTX, Multidex, Test.

---

## 🧩 Interview Questions (Q&A)

### 1. ViewModel vs SavedInstanceState?
*   **ViewModel:** Handles configuration changes (screen rotation). Cleared when the Activity is finished or Fragment is detached permanently. Designed for large data.
*   **SavedInstanceState:** Handles System-initiated process death. Designed for small data (serialized). Used via `SavedStateHandle` in ViewModel.

### 2. LiveData Characteristics
*   **Lifecycle-Aware:** Only updates active observers (STARTED or RESUMED).
*   **No Memory Leaks:** Observers are automatically removed when lifecycle is DESTROYED.
*   **Data Holder:** Holds data that can be observed.

### 3. LiveData vs StateFlow (Flow)?
*   **LiveData:** Java-friendly, tied to Android Lifecycle, value is nullable (optional). Runs on Main Thread by default.
*   **StateFlow:** Pure Kotlin (Flow), requires a Coroutine Scope (`lifecycleScope`), always has an initial value, distinct until changed by default. preferred for clean architecture (Domain layer shouldn't know Android classes).

### 4. WorkManager Use Cases?
Used for **deferrable** and **guaranteed** background work.
*   **Immediate:** Sending a message locally.
*   **Long Running:** Uploading a large video.
*   **Deferrable:** Syncing logs to server once a day.
**Not** for immediate UI work (use Coroutines) or exact timing (use AlarmManager).

### 5. Navigation Component Benefits?
*   **Visual Graph:** See all flows in one place.
*   **Safe Args:** Type-safe argument passing (Removes Bundle key errors).
*   **Deep Linking:** Centralized handling of deep links.
*   **Fragment Transactions:** Handles `FragmentTransaction` boilerplate automatically options.

### 6. Paging 3 Library?
Helps load data in pages.
*   **PagingSource:** Defines how to retrieve a chunk of data (API/DB).
*   **RemoteMediator:** coordinates loading from DB (cache) and Network (source of truth).
*   **PagingData:** Container for paginated data.

### 7. What is lifecycle-aware?
A component (like `LocationManager`) that automatically adjusts its behavior based on the lifecycle state of its parent (Activity/Fragment).
*   `@OnLifecycleEvent(ON_START)` -> Start listening.
*   `@OnLifecycleEvent(ON_STOP)` -> Stop listening.

### 8. Room Database Optimization?
*   **@Transaction:** Ensures multiple operations happen atomically.
*   **Indexes:** Speed up queries on specific columns.
*   **TypeConverters:** Store complex objects (Date, List) as primitives.
*   **Pre-populated DB:** Ship app with existing data.

---

