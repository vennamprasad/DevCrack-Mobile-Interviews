# 🔄 iOS App Lifecycle
> **Targeted for iOS Developers**
> **Note:** App States, AppDelegate vs SceneDelegate.

![Lifecycle](https://img.shields.io/badge/iOS-Lifecycle-green?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. App States](#1-app-states)
- [2. The Delegates](#2-appdelegate-vs-scenedelegate)
- [3. Main Run Loop](#3-main-run-loop)

---

### Q1. What are the 5 executions states of an iOS App?

**Answer:**
1.  **Not Running**: Terminated or not launched.
2.  **Inactive**: Foreground but not receiving events (e.g., call incoming, Notification Center pulled down).
3.  **Active**: Foreground and receiving events (Normal usage).
4.  **Background**: Executing code but not visible (e.g., Music playing, finishing a download).
5.  **Suspended**: In background, essentially frozen (Memory held, no CPU).

### Q2. AppDelegate vs SceneDelegate?

**Answer:**
Introduced in iOS 13 (iPad Multitasking).
- **AppDelegate**: Handles Process-level events (App Launch, Push Notification registration, Memory Warnings). "The App".
- **SceneDelegate**: Handles UI Lifecycle events (Screen entering foreground/background). "The Window".
*One App can have multiple Scenes (Windows) on iPad.*

### Q3. Key Lifecycle Methods?

**Answer:**
**SceneDelegate:**
- `sceneDidDisconnect`: Release resources.
- `sceneDidBecomeActive`: Restart paused tasks (e.g., timers).
- `sceneWillResignActive`: Pause tasks (game loop), save data.
- `sceneWillEnterForeground`: Undo background changes.
- `sceneDidEnterBackground`: Release shared resources, save state.

### Q4. What is the Main Run Loop?

**Answer:**
An event processing loop (`NSRunLoop.main`) that keeps the app alive.
It waits for input (Touches, Network) -> Wakes up -> Processes Event -> Updates UI -> Sleeps.
**Crucial**: Never perform long-running tasks on the Main Run Loop, or it cannot process Touch events (App Freeze).
