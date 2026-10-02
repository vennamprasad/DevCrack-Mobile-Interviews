# Tata Elxsi Mobile Interview Preparation

> **Target:** Senior & Mid-Level Android & Embedded Mobile Engineers  
> **Specializations:** Android Automotive OS (AAOS), Connected Vehicle Telemetry, Healthcare Companion Apps, IoT Bluetooth (BLE)

---

## 📌 Company Overview
- **Type**: Premier Design & Technology Services Consultancy (Tata Group)
- **Focus**: Automotive infotainment, digital cockpits, Android Automotive OS (AAOS), medical device companion apps, smart consumer appliances.
- **Client Base**: Global automotive OEMs, tier-1 suppliers, and medical technology enterprises.

---

## 🧠 Interview Process
1. **Round 1**: Technical Screening (Android OS internals, IPC Binder, Services, Bluetooth BLE).
2. **Round 2**: Deep-Dive Technical Round (Android Automotive OS architecture, HAL, CarService, multi-threading).
3. **Round 3**: System Design Round (Design In-Vehicle Connected Telemetry App or Medical Monitor Companion App).
4. **Round 4**: Client Delivery & Managerial Round (Agile methodologies, client stakeholder management).

---

## 📝 Common Technical Questions
- [ ] **Android Binder IPC & AIDL:** Explain how Inter-Process Communication (IPC) operates in Android and how AIDL contracts interface between system services and apps.
- [ ] **Android Automotive OS (AAOS):** How does `CarPropertyManager` interface with the Vehicle HAL (VHAL) to read vehicle telemetry (speed, gear, battery level)?
- [ ] **Bluetooth Low Energy (BLE) State Machine:** Write a robust BLE connection manager that handles scanning, peripheral discovery, characteristic subscription, and auto-reconnection on disconnect.
- [ ] **Android Services:** Difference between Foreground Service, Background Service, and Bound Service. Android 14/15 restrictions on foreground service types.

---

## 🎨 Mobile System Design: Connected Vehicle Telemetry Dashboard
- **Vehicle Data Stream Ingestion:** Ingesting high-frequency CAN bus data via VHAL and rendering speedometer / battery gauges at 60 FPS without CPU throttling.
- **Driver Distraction Guidelines (DDG):** Designing compliant Android Automotive UIs that adhere to NHTSA driver distraction rules (restricted taps, voice-first interactions).
- **Offline Telemetry Sync:** Buffering diagnostic trouble codes (DTCs) in local SQLite/Room when driving through remote areas with zero cell connectivity.

---

## 📚 Resources
- [Tata Elxsi Careers](https://www.tataelxsi.com/careers)
- [Android Automotive OS Official Documentation](https://source.android.com/devices/automotive)
