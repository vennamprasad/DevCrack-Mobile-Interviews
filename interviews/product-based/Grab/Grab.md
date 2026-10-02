# Grab Mobile Interview Preparation

> **Target:** Android & iOS Mobile Engineers (Transport, Deliveries & Financial Services)  
> **Tech Stack:** Kotlin, Swift, Jetpack Compose, SwiftUI, RIBs Architecture, Mapbox / Google Maps SDK, Geofencing, WebSocket tracking

---

## 📌 Company Overview
- **Type**: Southeast Asia's Leading Superapp
- **Focus**: Ride-hailing, food delivery, logistics, digital payments, driver-partner location telemetry.
- **Scale**: Serving millions of daily bookings across Singapore, Indonesia, Malaysia, Philippines, Thailand, and Vietnam.

---

## 🧠 Interview Process
1. **Round 1**: Recruiter Screen (Past mobile experience, handling high-scale concurrent systems).
2. **Round 2**: Technical Phone Screen (Algorithms, collection complexity, mobile networking).
3. **Round 3**: Data Structures & Coding (Graphs, shortest path algorithms, intervals, spatial coordinates).
4. **Round 4**: Mobile System Design (Design Grab Real-Time Driver Tracking & Ride Booking).
5. **Round 5**: Values & Cross-Functional Collaboration (Operating in emerging markets, multi-lingual apps).

---

## 📝 Mobile Coding Questions
- [ ] **GPS Kalman Filter / Coordinate Smoothing:** Implement an algorithm that filters noisy GPS readings and smoothly interpolates a vehicle's position along a road polyline.
- [ ] **Geohash Proximity Query:** Given a set of driver coordinates, encode them into Geohashes and find all drivers within a 2km bounding box.
- [ ] **Multi-Stop Route Optimizer:** Calculate the optimal visiting order for a courier delivering 4 orders to minimize total travel time.

---

## 🎨 Mobile System Design: Design Grab Live Driver Location Tracking
- **Battery-Efficient Location Polling:** Balancing GPS accuracy (`ACCESS_FINE_LOCATION`) with battery drain using accelerometer motion triggers.
- **WebSocket / MQTT Telemetry Pipeline:** Streaming lightweight Protobuf location payloads over shaky 3G/4G cellular networks.
- **Real-Time Map Marker Animation:** Smoothly animating driver car icons on the map between sparse coordinate updates using bearing interpolation.
- **Offline Fare Estimate Caching:** Caching route topologies and fare matrix tables for offline reference during network dead zones.

---

## 💡 Behavioral & Engineering Mindset
- How do you design mobile applications for tier-2/tier-3 cities with weak cellular connectivity and budget Android hardware?
- Describe a situation where your app had to handle sudden surges in network traffic (e.g., peak rush hour bookings).

---

## 📚 Resources
- [Grab Careers](https://grab.careers/)
- [Grab Tech Blog](https://engineering.grab.com/)
