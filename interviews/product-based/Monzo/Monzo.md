# Monzo Mobile Interview Preparation

> **Target:** iOS & Android Software Engineers (Core Banking Team)  
> **Tech Stack:** Swift, Kotlin, Reactive UI, Clean Architecture, Event-Driven Backend, Offline Ledger

---

## 📌 Company Overview
- **Type**: UK Digital Challenger Bank & FinTech Pioneer
- **Focus**: Real-time spending notifications, collaborative budgeting, international transfers, transparent digital banking.
- **Engineering Culture**: Known for extreme transparency, modular architecture, and high code craft.

---

## 🧠 Interview Process
1. **Round 1**: Recruiter Chat & Background Alignment.
2. **Round 2**: Take-Home Mobile Coding Project (Building a clean transaction feed with offline caching, error handling, and unit tests).
3. **Round 3**: Technical Code Review & Architecture Discussion on Take-Home.
4. **Round 4**: Mobile System Design (Design Instant Transaction Push & Offline Balance Reconciliation).
5. **Round 5**: Culture & Leadership Round.

---

## 📝 Mobile Coding Questions
- [ ] **Transaction Grouping by Date & Category:** Given an asynchronous stream of transactions, group and render them with running daily balances.
- [ ] **Offline Balance Deduplication:** Merge offline pending purchases with authoritative server ledger updates without double-counting transactions.
- [ ] **Custom Search Filter with Debounce:** Implement a real-time merchant search with local disk fallback when network latency exceeds 300ms.

---

## 🎨 Mobile System Design: Instant Push Notification & Feed Update
- **Silent Push Notifications (APNs / FCM):** Awakening background app state to update local ledger balances before the user taps the notification.
- **Biometric Security & Step-Up Auth:** Implementing FaceID / Fingerprint authorization for high-risk money movements.
- **Accessibility & Design System:** Enforcing WCAG AAA compliance, Dynamic Type support, and VoiceOver/TalkBack labels.

---

## 📚 Resources
- [Monzo Careers](https://monzo.com/careers/)
- [Monzo Engineering Blog](https://monzo.com/blog/engineering/)
