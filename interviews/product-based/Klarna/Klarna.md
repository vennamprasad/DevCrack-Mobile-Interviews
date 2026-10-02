# Klarna Mobile Interview Preparation

> **Target:** Android, iOS & React Native Engineers (Shopping & Payments App)  
> **Tech Stack:** Kotlin, Swift, React Native, Server-Driven UI (SDUI), Modern WebViews, Microfrontends

---

## 📌 Company Overview
- **Type**: Global Buy Now Pay Later (BNPL) & Shopping App
- **Focus**: Server-driven checkout flows, virtual one-time payment cards, integrated in-app web shopping browser, AI shopping recommendations.
- **Scale**: Over 150 million active shoppers and 500,000+ merchant integrations worldwide.

---

## 🧠 Interview Process
1. **Round 1**: Recruiter Introduction & Technical Overview.
2. **Round 2**: Live Mobile Coding (Clean code, collections, asynchronous state management).
3. **Round 3**: Mobile System Design (Design Klarna Server-Driven UI (SDUI) Checkout Flow).
4. **Round 4**: WebView & Native Bridge Architecture (Security, cookie injection, postMessage bridges).
5. **Round 5**: Cultural Fit & Collaboration.

---

## 📝 Mobile Coding Questions
- [ ] **SDUI Component Parser:** Parse a deeply nested JSON schema describing buttons, carousels, and input forms into native Compose / SwiftUI view hierarchies.
- [ ] **Installment Schedule Calculator:** Given an order total and payment plan (e.g. Pay in 4), generate exact payment dates and cent amounts handling uneven division.
- [ ] **Safe JS-Native Bridge Handler:** Create a bidirectional message bus between a checkout WebView and the native app that validates origins and prevents XSS token theft.

---

## 🎨 Mobile System Design: Server-Driven UI (SDUI) Engine
- **JSON Component Schema:** Versioned component contracts (`HeaderComponent`, `PaymentSelectorComponent`, `PromoBannerComponent`).
- **Dynamic Action Routing:** Handling remote click actions (`deeplink`, `open_modal`, `authorize_payment`) without requiring App Store app updates.
- **Cache Invalidation & A/B Testing:** Fast local schema caching and instant layout swaps.

---

## 📚 Resources
- [Klarna Engineering](https://engineering.klarna.com/)
- [Klarna Careers](https://www.klarna.com/careers/)
