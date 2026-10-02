# Endava Mobile Interview Preparation

> **Target:** Senior & Mid-Level Android & iOS Engineers (Payments & FinTech Practice)  
> **Specializations:** Digital Wallets, Payment Gateways, PCI-DSS Security Compliance, Reactive UI

---

## 📌 Company Overview
- **Type**: Global Digital Acceleration & Agile IT Consulting Leader
- **Scale**: Over 11,000 employees globally, heavily focused on European, UK, and US enterprises in Banking, Capital Markets, Insurance, and Healthcare.
- **Engineering Values**: Distributed Agile development, clean code standards, automated testing, high engineering rigor.

---

## 🧠 Interview Process
1. **Round 1**: Technical Phone Interview (Language internals, design patterns, reactive programming).
2. **Round 2**: Live Hands-On Coding (Implementing a clean, testable feature with network mocks and unit tests).
3. **Round 3**: Architecture & System Design (Designing a high-security Digital Wallet with offline QR payments).
4. **Round 4**: Client Delivery & Culture Interview (Agile sprint ceremonies, communicating technical trade-offs to clients).

---

## 📝 Common Technical Questions
- [ ] **Mobile Security & PCI-DSS:** Implementing SSL/TLS certificate pinning with backup pins, detecting rooted/jailbroken devices, and preventing screenshot capture in sensitive payment screens (`FLAG_SECURE`).
- [ ] **Reactive Concurrency (Flow vs Combine vs RxJava):** Comparing backpressure handling, cold vs hot streams, and transformation operators (`flatMapLatest` vs `switchMap`).
- [ ] **Decoupled Navigation Architecture:** Designing a Coordinator pattern or Jetpack Navigation Compose graph with type-safe arguments.
- [ ] **Clean Architecture Dependency Flow:** Explaining why the Domain layer must be pure Kotlin/Swift with zero framework dependencies.

---

## 🎨 System Design: Contactless QR Digital Payment Wallet
- **Dynamic QR Code Generation:** Offline generation of encrypted time-based payment tokens for merchant POS terminal scanning.
- **Biometric Authorization Flow:** Secure cryptographic signing of transaction hashes using hardware-backed Secure Enclave / Android StrongBox.
- **Audit Logging & Telemetry:** Encrypting and batch-uploading sensitive financial audit events without blocking main UI threads.

---

## 📚 Resources
- [Endava Careers](https://www.endava.com/careers)
- [Endava Engineering Insights](https://www.endava.com/insights)
