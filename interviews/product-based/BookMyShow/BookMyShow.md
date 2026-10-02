# BookMyShow Mobile Interview Preparation

> **Target:** SDE-1, SDE-2 & Senior Mobile Engineers (Android & iOS)  
> **Tech Stack:** Kotlin, Jetpack Compose, Swift, SwiftUI, Interactive Canvas, High-Concurrency Seat Locking

---

## 📌 Company Overview
- **Type**: India's Premier Entertainment & Ticketing Giant
- **Focus**: High-concurrency movie and concert ticket booking, interactive cinema seat layout rendering, timed checkout reservations, digital QR ticket passes.
- **Scale**: Managing massive flash ticket sales (Coldplay, IPL, World Cup, blockbuster movie releases) with millions of concurrent app users.

---

## 🧠 Interview Process
1. **Round 1**: Machine Coding / UI Engineering Round (90 Mins): Build an interactive movie auditorium seating chart with zoom/pan, seat selection, and price tier calculations.
2. **Round 2**: Data Structures & Problem Solving (60 Mins): Bitmaps, matrices, intervals, priority queues.
3. **Round 3**: Mobile System Design (60 Mins): Design BookMyShow High-Concurrency Seat Locking & Checkout Engine.
4. **Round 4**: Hiring Manager & Architecture Review.

---

## 📝 Mobile Coding Questions
- [ ] **Auditorium Seat Layout Matrix (Canvas):** Render an interactive $50 \times 50$ seat grid on an Android/iOS Canvas that supports pinch-to-zoom, pan, and tap detection with single-frame response.
- [ ] **Seat Allocation Algorithm:** Given a cinema row with occupied and vacant seats, find $K$ contiguous available seats closest to the screen center.
- [ ] **8-Minute Reservation Lock Timer:** Implement a resilient countdown timer that synchronizes with the server lock expiration timestamp even if the user backgrounds the app or changes device system clock.

---

## 🎨 Mobile System Design: Seat Reservation & Flash Booking
- **Interactive Seating Grid Performance:** Using custom Canvas vector drawing instead of nested views/composables to render thousands of seats without memory bottlenecks.
- **Optimistic Concurrency & Lock Expiry:** Handling seat collision state (when two users attempt to lock the same seat simultaneously) with instant UI feedback.
- **Offline Apple Wallet / Google Wallet Passes:** Generating and saving digital barcode / QR passes to native device wallets for gate entry without cell reception.

---

## 📚 Resources
- [BookMyShow Careers](https://in.bookmyshow.com/careers)
- [BookMyShow Tech Insights](https://medium.com/bookmyshow)
