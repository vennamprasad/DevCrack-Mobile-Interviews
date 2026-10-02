# Zomato Mobile Interview Preparation

> **Target:** SDE-1, SDE-2 & Senior Mobile Engineers (Consumer Dining, Delivery & Blinkit)  
> **Tech Stack:** Kotlin, Jetpack Compose, Swift, SwiftUI, Dynamic Design System, WebSockets, Live Activities

---

## 📌 Company Overview
- **Type**: Global Food Delivery, Dining Out & Quick Commerce Giant
- **Focus**: High-conversion visual restaurant discovery, real-time live order updates, dynamic delivery pricing calculation, hyper-local search with sub-50ms latency.
- **Scale**: Operating in hundreds of cities with over 80 million active foodies.

---

## 🧠 Interview Process
1. **Round 1**: Machine Coding / Practical Assignment: Build an interactive restaurant discovery screen with debounced search, rating filter chips, and image carousels.
2. **Round 2**: Data Structures & Algorithmic Round: Heaps, two-pointers, graphs, dynamic programming.
3. **Round 3**: Mobile System Design: Design Zomato Restaurant Discovery & Menu Caching Engine.
4. **Round 4**: Cultural Values & Leadership: Speed of shipping, user delight, resilience during festival delivery peaks (New Year's Eve).

---

## 📝 Mobile Coding Questions
- [ ] **Debounced Real-Time Search Filter:** Implement a search query pipeline with a 250ms debounce window that queries local SQLite cache before hitting the backend.
- [ ] **Restaurant Distance Ranking:** Given a user's latitude and longitude and a list of 5,000 restaurants, compute Haversine distances and return the top 20 closest open restaurants using a Min-Heap.
- [ ] **Dynamic Pricing Breakdown Calculator:** Compute total order charges incorporating platform fees, delivery surcharges, surge pricing, GST, and coupon discounts.

---

## 🎨 Mobile System Design: Zomato Discovery & Menu Caching
- **Menu Hierarchy Caching:** Designing a multi-tiered cache that stores thousands of dish items, tags (Vegan, Jain, Chef's Special), and add-on variant groups with instant search indexing.
- **Image Preloading & Low Memory Optimization:** Aggressively pre-fetching dish hero banners while keeping memory usage under 80MB on mid-tier Android devices.
- **Real-Time Live Activities (iOS & Android):** Updating lock screen delivery ETA countdowns over APNs / FCM.

---

## 📚 Resources
- [Zomato Careers](https://www.zomato.com/careers)
- [Zomato Technology Blog](https://blog.zomato.com/)
