# Strava Mobile Interview Preparation

> **Target:** iOS & Android Software Engineers (Activity Recording & Sensor Teams)  
> **Tech Stack:** Kotlin, Swift, CoreLocation, Google Location Services, Bluetooth LE, SQLite / Room, Custom Vector Map Rendering

---

## 📌 Company Overview
- **Type**: Global Social Fitness & Activity Tracking Platform
- **Focus**: Background GPS activity tracking, BLE sensor data streams (heart rate monitors, power meters), interactive route maps, segments and leaderboards.
- **Scale**: Over 120 million athletes recording billions of miles of runs, rides, and hikes.

---

## 🧠 Interview Process
1. **Round 1**: Recruiter Screen (Past mobile tracking and sensor integration experience).
2. **Round 2**: Technical Phone Screen (Swift/Kotlin concurrency, memory, location APIs).
3. **Round 3**: Data Structures & Problem Solving (Coordinate geometry, spatial indexing, polyline compression).
4. **Round 4**: Mobile System Design (Design Strava Background Activity Recording & Live Segment Matcher).
5. **Round 5**: Cultural Interview (Passion for fitness tech, product craft, community focus).

---

## 📝 Mobile Coding Questions
- [ ] **GPS Polyline Simplification (Ramer-Douglas-Peucker):** Implement an algorithm to simplify a path of 10,000 GPS coordinate points into a lightweight polyline with minimal geometric distortion.
- [ ] **Live Segment Matching:** Given a moving athlete's coordinate stream, determine whether they have entered, completed, or deviated from a predefined geographic segment.
- [ ] **Bluetooth LE Heart Rate Packet Parser:** Parse raw byte arrays from a standard Bluetooth GATT Heart Rate Service into integer BPM values.

---

## 🎨 Mobile System Design: Background Activity Recording Engine
- **Battery Optimization:** Managing persistent location updates (`CLLocationManager` / `FusedLocationProviderClient`) in the background without battery depletion or OS watchdog termination.
- **Sensor Fusion & BLE Reconnection:** Auto-reconnecting to external heart rate straps and bike sensors during intermittent Bluetooth drops.
- **Offline Map Tile Caching:** Downloading vector map tiles for remote mountainous areas with zero cell connectivity.

---

## 📚 Resources
- [Strava Engineering Blog](https://medium.com/strava-engineering)
- [Strava Careers](https://boards.greenhouse.io/strava)
