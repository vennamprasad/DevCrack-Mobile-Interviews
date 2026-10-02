# Ather Energy Mobile Interview Preparation

> **Target:** Senior & Mid-Level Android & iOS Engineers (Connected Vehicle Team)  
> **Tech Stack:** Kotlin, Swift, Jetpack Compose, SwiftUI, Bluetooth Low Energy (BLE), MQTT, Mapbox Navigation, Vehicle Telemetry

---

## 📌 Company Overview
- **Type**: Premier Indian Smart Electric Vehicle (EV) Pioneer
- **Focus**: Connected smart electric scooter companion app, Bluetooth auto-unlock, remote charging telemetry, live Ather Grid fast-charging route navigation, ride statistics.
- **Hardware Integration**: Communicating directly with the vehicle's Android-based dashboard and cloud telematics over BLE and 4G eSIM.

---

## 🧠 Interview Process
1. **Round 1**: Technical Phone Screen (Bluetooth LE lifecycle, async threading, background location).
2. **Round 2**: Live Machine Coding (BLE connection state machine, packet serialization, coordinate parsing).
3. **Round 3**: Mobile System Design (Design Ather Companion App with Live Battery Telemetry & Push-to-Scooter Navigation).
4. **Round 4**: Cultural & Embedded IoT Mindset.

---

## 📝 Mobile Coding Questions
- [ ] **Bluetooth LE Auto-Connect State Machine:** Implement a resilient BLE service that discovers the scooter peripheral within 5 meters, pairs securely, and auto-reconnects on signal loss.
- [ ] **State-of-Charge (SoC) Range Estimator:** Given current battery percentage, rider mode (Eco, Ride, Warp), and route elevation profile, compute projected vehicle range.
- [ ] **Push-to-Scooter Coordinate Encoder:** Format a multi-stop GPX route into compact byte packets transmitted to the vehicle dashboard over Bluetooth GATT.

---

## 🎨 Mobile System Design: Ather Companion App
- **Live Battery & Charging Notification:** Updating charging progress and remaining time to full charge via background push notifications and live lock-screen widgets.
- **Trip History & Ride Analytics:** Visualizing top speed, average efficiency (Wh/km), and regenerative braking recovery on interactive graph charts.
- **Theft & Tow Alerts:** Instantly notifying the rider with high-priority notifications when unauthorized scooter motion or geofence exit is detected.

---

## 📚 Resources
- [Ather Energy Careers](https://www.atherenergy.com/careers)
- [Ather Tech Insights](https://blog.atherenergy.com/)
