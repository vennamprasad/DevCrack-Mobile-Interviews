# 🚀 Android Jetpack Architecture Components

> **Master the suite of official AndroidX Jetpack libraries: ViewModel, LiveData, Navigation, Lifecycle, Paging, and WorkManager.**

![Jetpack](https://img.shields.io/badge/Android-Jetpack-3DDC84?style=for-the-badge&logo=android)
![AndroidX](https://img.shields.io/badge/Library-AndroidX-blue?style=for-the-badge)
![Lifecycle](https://img.shields.io/badge/Architecture-Lifecycle_Aware-orange?style=for-the-badge)

---

## 📖 Chapter Index

- **[Jetpack Architecture Components Guide](./01_jetpack_architecture_components.md)**
  - **1. Core Components:** `ViewModel` internals (how `ViewModelStore` survives configuration changes), `SavedStateHandle`, `LiveData` vs Kotlin `StateFlow`, active/inactive observer states.
  - **2. Navigation Component:** NavGraph, Deep linking, SafeArgs, nested graphs, Single-Activity pattern, and Compose Navigation integration.
  - **3. Data & Paging:** Room ORM architecture, database migrations, `Paging 3` architecture (`PagingSource`, `RemoteMediator`, `Pager`, `PagingData`).
  - **4. Background Work (`WorkManager`):** Guaranteed background execution, constraint checking (battery, network), `CoroutineWorker`, periodic requests, chaining tasks, and expedited jobs.
  - **5. Architecture & Best Practices:** Clean separation between UI, domain, and data layers using Jetpack libraries.

---

## 🧭 Modern Evolution of Jetpack Components

| Classic Jetpack Component | Modern Recommended Successor | Why Migrate? |
| :--- | :--- | :--- |
| `LiveData` | `StateFlow` / `SharedFlow` | Flow is Kotlin-native, multiplatform friendly, has rich operators (`map`, `filter`, `combine`), and avoids Main-thread affinity bugs. |
| XML Navigation Graph | Compose Navigation / Type-Safe Nav (Navigation 2.8+) | Direct Kotlin type-safety for destinations without XML or SafeArgs code generation plugins. |
| `AsyncTask` / `IntentService` | `WorkManager` & Coroutines | Resilient to process death, battery-aware, complies with Android 12+ background restrictions. |
| `SharedPreferences` | `DataStore` (Preferences / Proto) | Fully asynchronous (Flow-based), prevents UI jank, thread-safe, transactional consistency. |
