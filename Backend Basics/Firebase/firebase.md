# 🔥 Firebase Real-time & Backend
> **Targeted for Mobile Developers**
> **Note:** Serverless backend, Real-time Database, and Authentication.

![Firebase](https://img.shields.io/badge/Backend-Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

---

## 📖 Table of Contents
- [1. Realtime DB vs Firestore](#1-realtime-db-vs-firestore)
- [2. Firebase Auth](#2-firebase-authentication)
- [3. Cloud Functions](#3-cloud-functions)
- [4. Remote Config & Crashlytics](#4-extra-tools)

---

### 1. Realtime DB vs Firestore
Both are NoSQL databases.

| Feature | Realtime Database | Cloud Firestore |
| :--- | :--- | :--- |
| **Data Model** | Huge JSON tree | Collections and Documents |
| **Queries** | Limited sorting/filtering | Advanced querying (compound) |
| **Scalability** | Harder to scale (sharding) | Auto-scaling |
| **Offline** | Supported | Supported (better conflict resolution) |
| **Pricing** | Bandwidth + Storage | Reads/Writes + Storage |

**Use Case:**
- **Realtime DB**: Simple syncing, presence systems (online/offline).
- **Firestore**: Main backend DB, complex data structures.

### 2. Firebase Authentication
Supports Email/Pass, Phone, Google, Facebook, Apple, etc.
- **JWT**: Uses JSON Web Tokens for identity.
- **Integration**:
```kotlin
val auth = FirebaseAuth.getInstance()
auth.signInWithEmailAndPassword(email, pass)
    .addOnCompleteListener { task ->
        if (task.isSuccessful) {
            val user = auth.currentUser
        }
    }
```

### 3. Cloud Functions
Serverless backend logic. Runs Node.js, Python, or Go code in response to events (DB write, Auth create, HTTP request).
- **Triggers**:
    - `onCall`: Directly callable from client SDK.
    - `onRequest`: Standard HTTP endpoint.
    - `onCreate`/`onUpdate`: Database triggers.

### 4. Extra Tools
- **Remote Config**: Change app behavior/appearance without update (A/B testing).
- **Crashlytics**: Real-time crash reporting.
- **FCM (Cloud Messaging)**: Push notifications.

 ---

## Interview Questions

### Q1. How does Firebase handle offline data?
**Answer:**
Firebase SDKs persist data to disk. When the app is offline, writes are queued locally. When connectivity returns, the client syncs with the server. Firestore handles conflict resolution (last-write-wins usually).

### Q2. Is Firebase secure?
**Answer:**
Yes, if **Security Rules** are configured correctly. By default, it might be open.
- **Firestore Rules**:
```javascript
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### Q3. How do you optimize Firestore costs?
**Answer:**
Since Firestore charges by **Reads/Writes**:
1.  Don't fetch unnecessary data.
2.  Use **Pagination** (cursors).
3.  Denormalize data if needed to avoid multiple reads.
4.  Cache data locally.

### Q4. What is the difference between FCM Data Messages and Notification Messages?
**Answer:**
- **Notification Message**: Handled by system tray automatically when app is in background. High level.
- **Data Message**: Handled by client app (`onMessageReceived`) always. Gives full control to the app even in background (though constrained by battery optimizations).
