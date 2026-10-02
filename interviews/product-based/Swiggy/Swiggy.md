# Swiggy Mobile Interview Preparation

> **Target:** SDE-1, SDE-2 & Senior Mobile Engineers (Consumer, Delivery & Instamart)  
> **Tech Stack:** Kotlin, Jetpack Compose, Swift, SwiftUI, Multi-Module Clean Architecture, Live Activities, Google Maps SDK, WebSockets

---

## 📌 Company Overview
- **Type**: Premier Indian Food Delivery & Quick-Commerce (Instamart) Platform
- **Focus**: Real-time order tracking, sub-10 minute Instamart deliveries, live driver location smoothing, multi-restaurant cart builder, iOS Live Activities / Dynamic Island.
- **Scale**: Serving millions of daily hungry consumers across 500+ Indian cities.

---

## 🧠 Interview Process
1. **Round 1**: Machine Coding / Practical UI Round (90 Mins): Build a functional food menu with accordion categories, floating cart pill, and local state management.
2. **Round 2**: Data Structures & Problem Solving (60 Mins): Arrays, sliding window, topological sort, string parsing.
3. **Round 3**: Mobile System Design (60 Mins): Design Swiggy Real-Time Order Tracking & Live Map Routing.
4. **Round 4**: Techno-Managerial Round: Handling production incidents, trade-offs between battery drain and GPS accuracy.

---

## 📝 Mobile Coding Questions
- [ ] **Sticky Floating Cart Indicator:** Build a restaurant menu list with sticky category headers and a floating cart summary button that animates in/out based on scroll velocity.
- [ ] **Driver Coordinate Interpolation:** Given GPS coordinate breadcrumbs received every 5 seconds over a WebSocket, calculate bearing and interpolate vehicle movement along the road at 60 FPS.
- [ ] **Multi-Store Delivery Sorter:** Group items in a combined grocery + food order into distinct delivery batches based on store proximity and prep time.

---

## 🎨 Mobile System Design: Live Order Tracking & Dynamic Island
- **Live Location Telemetry:** Streaming delivery partner coordinates via WebSockets / MQTT with graceful HTTP polling fallback.
- **iOS Live Activities & Android Ongoing Notifications:** Updating lock screen widgets in real time as order state transitions (`Order Placed -> Kitchen Preparing -> Out for Delivery -> Delivered`).
- **Resilient Offline Cart Storage:** Storing uncommitted restaurant meals and grocery items locally in Room/CoreData, handling item price changes when the user returns online.

---

## 📚 Resources
- [Swiggy Bytes Tech Blog](https://bytes.swiggy.com/)
- [Swiggy Careers](https://careers.swiggy.com/)
