# Delhivery Mobile Interview Preparation

> **Target:** SDE-1, SDE-2 & Senior Mobile Engineers (Field Operations & Logistics Apps)  
> **Tech Stack:** Kotlin, Jetpack Compose, CameraX / ML Kit Barcode Scanning, Offline-First Room DB, Location Tracking

---

## 📌 Company Overview
- **Type**: India's Largest Fully-Integrated Logistics Provider
- **Focus**: Field delivery agent mobile apps, real-time dispatching, high-speed multi-barcode camera scanning, offline proof-of-delivery (PoD) capture, optimal delivery routing.
- **Scale**: Handling over 2 billion parcels across 18,000+ Indian pin codes with tens of thousands of field riders.

---

## 🧠 Interview Process
1. **Round 1**: Technical Screening (Android fundamentals, offline caching, Camera lifecycle).
2. **Round 2**: Machine Coding & Data Structures (Local database queries, image compression, battery optimization).
3. **Round 3**: Mobile System Design (Design Field Delivery Agent App with Offline Proof-of-Delivery & GPS Breadcrumbs).
4. **Round 4**: Techno-Managerial Round (Designing for rugged devices, poor connectivity in rural areas).

---

## 📝 Mobile Coding Questions
- [ ] **High-Speed Continuous Barcode Scanner:** Using CameraX and ML Kit, implement a barcode scanner that scans and beeps on 50 packages per minute without dropping preview frames or leaking memory.
- [ ] **Optimal Delivery Route Re-ordering:** Given a delivery rider's remaining 30 stops, dynamically re-order remaining destinations based on current GPS location and delivery time windows.
- [ ] **Resilient Photo Compression & Sync:** Capture delivery proof photos, compress them to under 150KB without losing signature clarity, and queue them for background upload with exponential backoff.

---

## 🎨 Mobile System Design: Field Delivery Agent App
- **100% Offline-First Architecture:** Ensuring riders can scan, deliver, collect cash-on-delivery (CoD), and capture digital signatures in remote basements with zero cellular reception.
- **Battery-Conscious Breadcrumb Tracking:** Logging location checkpoints every 30 seconds for audit without draining the delivery agent's phone battery before their 8-hour shift ends.
- **Fraud Prevention & Geo-tagging:** Verifying that the delivery agent's GPS coordinates match the delivery address before unlocking the "Mark Delivered" action.

---

## 📚 Resources
- [Delhivery Careers](https://www.delhivery.com/careers/)
- [Delhivery Technology](https://www.delhivery.com/technology/)
