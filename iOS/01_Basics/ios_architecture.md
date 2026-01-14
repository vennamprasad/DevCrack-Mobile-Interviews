# 🏛️ iOS System Architecture
> **Targeted for iOS Developers**
> **Note:** The 4 Layers of iOS.

![Architecture](https://img.shields.io/badge/iOS-System-blue?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. Core OS Layer](#1-core-os-layer)
- [2. Core Services Layer](#2-core-services-layer)
- [3. Media Layer](#3-media-layer)
- [4. Cocoa Touch Layer](#4-cocoa-touch-layer)

---

### Q1. What are the 4 abstraction layers of iOS?

**Answer:**
1.  **Core OS**: (Bottom) Kernel, File System, Networking, Security, Power Management. Close to hardware.
2.  **Core Services**: Data management (Core Data), Location, GCD, Foundation framework.
3.  **Media**: Graphics, Audio, Video (Core Graphics, Core Animation, AVFoundation).
4.  **Cocoa Touch**: (Top) UI, Touch input, Push Notifications, Multitasking (UIKit, SwiftUI).

### Q2. What is the Foundation Framework?

**Answer:**
Part of **Core Services**. It provides base classes and data types for primitive objects (Strings, Arrays, Dictionaries), Networking (URLSession), and File Management (FileManager). It creates the primitives that UIKit/SwiftUI build upon.

### Q3. What is the Sandbox?

**Answer:**
A security mechanism at the **Kernel level**.
- Every app has its own isolated directory.
- An app **cannot** access files from another app (unless explicitly shared via Extensions or App Groups).
- Contains: `Bundle` (Read-only), `Documents`, `Library`, `tmp`.

### Q4. What is a Bundle?

**Answer:**
A directory that groups the executable code and related resources (images, sounds, nib files) together in one place. The main bundle is where the app code lives.
