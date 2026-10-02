# Flipkart Mobile Interview Preparation

> **Target:** SDE-1, SDE-2 & Senior Mobile Engineers (Android & iOS)  
> **Tech Stack:** Kotlin, Jetpack Compose, Swift, SwiftUI, Multi-Module Clean Architecture, Custom Image Cache, Server-Driven UI

---

## 📌 Company Overview
- **Type**: Premier Indian E-Commerce Giant (Walmart-backed)
- **Focus**: High-concurrency shopping, Big Billion Days flash sales, Server-Driven UI (SDUI), low-bandwidth network resiliency across Tier-2/3/4 Indian cities.
- **Scale**: Hundreds of millions of registered users, peak concurrency exceeding 100,000+ orders per minute during Big Billion Days.

---

## 🧠 Interview Process
1. **Round 1**: Machine Coding / Practical Assignment (90–120 Mins): Build a functional Android/iOS feature (e.g., Infinite Product Grid with offline Room/CoreData caching, search filtering, and unit tests).
2. **Round 2**: Data Structures & Algorithmic Problem Solving (60 Mins): Array manipulation, intervals, Trie autocomplete, Dynamic Programming.
3. **Round 3**: Mobile System Design (LLD & HLD - 60 Mins): Design Flipkart Flash Sale Checkout or Product Details Page (PDP) with SDUI.
4. **Round 4**: Hiring Manager & Cultural Fit: Extreme ownership, customer first, handling Big Billion Day production crunches.

---

## 📝 Mobile Coding & Algorithmic Questions
- [ ] **Autocomplete Search Trie:** Build an autocomplete engine with debounced keystrokes that searches through 50,000 product keywords and returns top 5 results ranked by popularity.
- [ ] **Flash Sale Countdown Synchronizer:** Implement a timer that synchronizes local device countdown clocks with Flipkart server NTP timestamps, preventing client-side clock tampering.
- [ ] **Cart Promotion Engine:** Given a list of items and conflicting coupon rules (e.g., "Flat 20% off" vs "Buy 2 Get 1 Free"), calculate the combination that yields maximum savings for the user.

---

## 🎨 Mobile System Design: Design Flipkart Product Details Page (PDP)
- **Server-Driven UI (SDUI):** Dynamically rendering review sections, EMI calculators, delivery pin code checkers, and image carousels based on JSON layout payloads.
- **Image Pre-Fetching & Caching:** Custom multi-tier image caching (Memory + Disk LRU) with progressive JPEG loading to save bandwidth on 2G/3G networks.
- **High-Concurrency Flash Sale Cart Lock:** Reserving inventory in local state for 10 minutes while handling network retry backoff without double-charging the user.
- **App Size Optimization:** Dynamic feature delivery, ProGuard/R8 byte-code shrinking, and WebP asset compression to keep base APK under 25MB.

---

## 💡 Behavioral & Core Values
- How do you design mobile applications that function reliably on budget Android devices (2GB RAM, Android Go) prevalent across Tier-3 Indian cities?
- Describe how you prepare a mobile application for catastrophic traffic spikes during festival sales.

---

## 📚 Resources
- [Flipkart Careers](https://www.flipkartcareers.com/)
- [Flipkart Tech Blog](https://tech.flipkart.com/)
