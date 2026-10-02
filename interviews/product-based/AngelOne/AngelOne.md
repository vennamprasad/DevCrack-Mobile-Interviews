# Angel One Mobile Interview Preparation

> **Target:** Senior & Mid-Level Android & iOS Engineers (Trading & Market Data Practice)  
> **Tech Stack:** Kotlin, Jetpack Compose, Swift, SwiftUI, WebSockets, High-Frequency Financial Charts, SmartAPI

---

## 📌 Company Overview
- **Type**: Leading Indian FinTech & Stock Broking Giant
- **Focus**: High-speed retail stock trading, F&O derivatives, real-time tick-by-tick market depth, custom technical indicators, biometric account security.
- **Scale**: Over 20 million registered trading clients executing millions of trades during Indian market hours (09:15 - 15:30 IST).

---

## 🧠 Interview Process
1. **Round 1**: Technical Screening (Core mobile fundamentals, concurrency, memory profiling).
2. **Round 2**: Live Machine Coding / Data Structures (High-frequency data streams, buffering, sliding window max/min).
3. **Round 3**: Mobile System Design (Design Angel One Real-Time Market Watch & Order Placement Engine).
4. **Round 4**: Techno-Managerial Round (Production trade-offs, handling market opening bell volatility).

---

## 📝 Mobile Coding Questions
- [ ] **Market Ticker Throttling Buffer:** Given a WebSocket emitting 500 stock price updates per second, design a sampling buffer that updates UI labels at 60 FPS without dropping the latest LTP (Last Traded Price).
- [ ] **Moving Average (SMA/EMA) Calculator:** Compute the 20-day Simple Moving Average (SMA) over a streaming list of historical candle closes in $O(1)$ amortized time.
- [ ] **Order Book Depth Visualizer:** Render a real-time Bid/Ask ladder (Market Depth 5) with color-coded horizontal bars proportional to trade volume.

---

## 🎨 Mobile System Design: Angel One Real-Time Trading App
- **WebSocket Binary Packet Parsing:** Parsing compact binary Protobuf / FlatBuffers market packets directly on background IO threads.
- **Real-Time Interactive Charts:** Drawing candlestick charts, MACD, and RSI indicators on a hardware-accelerated Canvas with pinch-zoom timeframes (1m, 5m, 1D).
- **Two-Factor Authentication (TOTP / Biometrics):** Secure login flow with MPIN, biometric auth, and automatic token expiry according to SEBI regulations.

---

## 📚 Resources
- [Angel One Careers](https://www.angelone.in/careers)
- [Angel One Engineering](https://www.angelone.in/smartapi)
