# 📡 Offline-First Apps
> **Targeted for Senior iOS Developers**
> **Note:** Sync Strategies, Conflict Resolution.

![Offline](https://img.shields.io/badge/Design-Offline_First-green?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Architecture](#1-architecture)
- [2. Synchronization](#2-synchronization)
- [3. Conflict Resolution](#3-conflict-resolution)

---

### Q1. What is Offline-First?

**Answer:**
The app works 100% without network.
UI reads from **Local Database** (Single Source of Truth), never directly from Network.
Network updates the Local Database in the background.

### Q2. Sync Strategies?

**Answer:**
1.  **Poll**: Fetch changes every X minutes. (Battery heavy).
2.  **Push**: Server sends Silent Push Notification to trigger sync. (Efficient).
3.  **Delta Sync**: Client sends "Last Sync Timestamp". Server returns only changes since then.

### Q3. Conflict Resolution?

**Answer:**
User A edits Note offline. User B edits Note online. User A goes online.
- **Last Write Wins**: Server timestamp decides. (Simple, data loss risk).
- **Manual Merge**: Ask user to choose.
- **CRDTs (Conflict-free Replicated Data Types)**: Mathematical structures that ensure mathematical consistency without conflicts.

### Q4. Optimistic UI?

**Answer:**
Update the UI immediately when user performs an action (e.g., "Keep"), assuming it will succeed.
If the API fails later, rollback the UI state and show error.
**Crucial for perceived performance.**
