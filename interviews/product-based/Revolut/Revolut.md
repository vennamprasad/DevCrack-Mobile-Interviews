# Revolut Mobile Interview Preparation

> **Target:** Senior & Mid-Level Android & iOS Engineers (FinTech & Core Banking Team)  
> **Tech Stack:** Kotlin, Jetpack Compose, Swift, SwiftUI, Multi-Module Clean Architecture, Strict Biometrics, Reactive Streams

---

## 📌 Company Overview
- **Type**: Global FinTech Super-App & Digital Bank
- **Focus**: Multi-currency accounts, real-time stock/crypto trading, international money transfers, debit card controls, ultra-strict mobile security.
- **Scale**: Over 45 million retail customers globally conducting hundreds of millions of transactions monthly.

---

## 🧠 Interview Process
1. **Round 1**: Technical Screening / Take-Home Assignment (Building a production-ready currency converter or stock ticker app with unit tests).
2. **Round 2**: Assignment Deep Dive & Code Review (Defending architecture decisions, thread safety, testing edge cases).
3. **Round 3**: Data Structures & Problem Solving (Concurrency, sliding window, financial decimal precision math, caching).
4. **Round 4**: Mobile System Design (Design Revolut Real-Time Stock Trading & Multi-Currency Wallet).
5. **Round 5**: Engineering Leadership & Fit (Speed of execution, handling high pressure, production ownership).

---

## 📝 Mobile Coding Questions
- [ ] **Financial Precision Math:** Implement an arithmetic calculator for currency exchange that avoids floating-point rounding errors (e.g., using `BigDecimal` or custom integer cent representation).
- [ ] **Real-Time Crypto Ticker Buffer:** Given an asynchronous stream of 100 price updates per second, buffer and emit the latest prices at 60 FPS to prevent UI thread flooding.
- [ ] **Transaction History Search & Grouping:** Group a list of 5,000 transactions by month and category, calculating running balances in $O(N)$ time.

---

## 🎨 Mobile System Design: Design Revolut Real-Time Trading App
- **High-Security Client Hardening:** Biometric authentication (FaceID / Android BiometricPrompt), Keychain/EncryptedSharedPreferences for tokens, root/jailbreak detection, and SSL pinning.
- **Real-Time Interactive Financial Charts:** Rendering candlestick and line charts smoothly at 120 FPS using custom canvas drawing.
- **Offline Card Freeze / Security Action Queue:** Storing emergency security actions offline and retrying with exponential backoff.
- **Multi-Module Clean Architecture:** Structuring 50+ feature modules with strict dependency inversion to optimize build times and team autonomy.

---

## 💡 Behavioral & Culture
- Revolut places immense emphasis on rapid execution and delivery ownership. How do you maintain 99.9% crash-free stability under fast deployment cycles?
- How do you handle code reviews when strict security guidelines conflict with product feature delivery timelines?

---

## 📚 Resources
- [Revolut Careers](https://www.revolut.com/careers/)
- [Revolut Tech Insights](https://medium.com/revolut)
