# CitiusTech Mobile Interview Preparation

> **Target:** Senior & Mid-Level Android & iOS Engineers (Digital Health Practice)  
> **Specializations:** Digital Healthcare Solutions, FHIR / HL7 Data Integration, HIPAA Security Compliance, Medical IoT

---

## 📌 Company Overview
- **Type**: Global Healthcare Technology & Digital Solutions Specialist
- **Scale**: Over 8,500 healthcare IT and mobile specialists serving global medical device makers, hospital systems, life sciences enterprises, and health insurance leaders.
- **Focus**: Patient companion apps, remote patient monitoring, telemedicine video consultation, electronic health record (EHR) integrations.

---

## 🧠 Interview Process
1. **Round 1**: Technical Screening (Core mobile fundamentals, security, and RESTful API integration).
2. **Round 2**: Technical Round 2 (MVVM, offline database caching, biometric security, thread safety).
3. **Round 3**: Healthcare System Design (Designing a Remote Patient Monitoring App with BLE Blood Pressure / Glucose Monitor).
4. **Round 4**: Managerial & Behavioral Round (Handling sensitive data, enterprise client communications).

---

## 📝 Common Technical Questions
- [ ] **HIPAA Mobile Security Standards:** Implementing Encrypted Room/CoreData (SQLCipher), data-at-rest encryption, TLS 1.3 in-transit encryption, and automatic user session timeouts after 5 minutes of inactivity.
- [ ] **FHIR / HL7 Data Standards:** How to parse and represent HL7 FHIR (Fast Healthcare Interoperability Resources) JSON models (e.g. Patient, Observation, DiagnosticReport) in clean Kotlin/Swift data classes.
- [ ] **BLE Medical Device Communication:** Handling continuous real-time Bluetooth LE telemetry from pulse oximeters and blood pressure monitors with auto-retry and data packet validation.
- [ ] **Telemedicine WebRTC Video Integration:** Managing audio focus, camera switches, picture-in-picture (PiP) mode, and network degradation during patient-doctor video consultations.

---

## 🎨 System Design: Remote Patient Vital Monitoring App
- **Real-Time Vital Stream Buffer:** Ingesting Bluetooth telemetry packets, verifying checksums, and buffering data locally when offline.
- **Critical Alert Dispatching:** Generating high-priority local notifications and emergency alerts when vital signs cross critical medical thresholds.
- **EHR Cloud Synchronization:** Batch syncing encrypted health records with hospital FHIR endpoints when connected to secure Wi-Fi.

---

## 📚 Resources
- [CitiusTech Careers](https://www.citiustech.com/careers)
- [HL7 FHIR Mobile Guidelines](https://www.hl7.org/fhir/)
