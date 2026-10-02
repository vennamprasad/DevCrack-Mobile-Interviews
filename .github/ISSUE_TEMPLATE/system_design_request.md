---
name: 📐 Mobile System Design Blueprint Request
about: Request an end-to-end architectural breakdown and Mermaid sequence/component diagram for a mobile application.
title: "[SYS-DESIGN]: Design <Application / Feature Name>"
labels: ["system-design", "architecture", "request"]
assignees: []
---

### 📱 Target Application / Feature
(e.g., "Design an Offline-First Ride-Hailing Driver App", "Design a Live Cricket Scorecard with SSE/WebSockets", "Design TikTok Video Feed with Prefetching")

### 🎯 Key Requirements & Scope
- **Functional Requirements:**
  1. (e.g. Drivers receive ride requests within 500ms)
  2. (e.g. Real-time GPS location streaming with battery optimization)
- **Non-Functional Requirements:**
  1. Offline resilience in network tunnels / poor connectivity
  2. Sub-100ms UI responsiveness
  3. Minimum battery drain and data usage

### 🧱 Architectural Highlights You Would Like Covered
- [ ] Network Protocol (gRPC / WebSockets / SSE / HTTP/3)
- [ ] Local Persistence & Sync (Room / SQLite / SwiftData / Realm / CRDTs)
- [ ] Background Processing (WorkManager / BGTaskScheduler)
- [ ] Component & Sequence Diagrams (Mermaid.js)
- [ ] State Management & UI Layer (Compose / SwiftUI)

### 🏢 Companies That Ask This Design Problem
(e.g., Uber, Grab, Swiggy, Netflix, Instagram)
