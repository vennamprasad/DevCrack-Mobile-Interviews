# Discord Mobile Interview Preparation

> **Target:** Android & iOS Mobile Engineers  
> **Tech Stack:** Kotlin, Jetpack Compose, Swift, SwiftUI, WebSockets, WebRTC, React Native migration to Native

---

## 📌 Company Overview
- **Type**: Global Communications Platform
- **Focus**: Ultra-low latency voice/video chat, massive real-time message streams, custom rich media rendering, server community moderation.
- **Architectural Shift**: Famously completed a high-profile migration on Android from React Native to native Kotlin to eliminate frame drops, slow startup times, and bridge serialization bottlenecks.

---

## 🧠 Interview Process
1. **Round 1**: Technical Phone Screen (45 Mins - Kotlin/Swift core, concurrency, network protocols).
2. **Round 2**: Live Coding Challenge (60 Mins - Complex collection manipulations, message tree traversal, custom Trie/LRU).
3. **Round 3**: Mobile System Design (60 Mins - Design Discord Real-Time Chat & Server Channels).
4. **Round 4**: Concurrency & Networking Deep Dive (WebSockets, Gateway heartbeat, message reconciliation, voice jitter buffers).
5. **Round 5**: Cultural Fit & Collaborative Values (Cross-team communication, developer advocacy).

---

## 📝 Mobile Coding & Algorithmic Questions
- [ ] **Autocomplete Mention Indexer:** Implement a Trie data structure to search user tags (`@username`) across a server with 100,000 members in under 5ms.
- [ ] **Message Reconciliation Queue:** Given an ordered stream of incoming WebSocket messages and an uncommitted local message queue, merge them without duplicating messages or dropping unsent messages.
- [ ] **Custom Rate Limiter:** Implement a client-side sliding window rate limiter that queues message sends and prevents 429 Too Many Requests errors.

---

## 🎨 Mobile System Design: Design Discord Chat & Voice Client
- **WebSocket Gateway Connection:** Maintaining a persistent bidirectional connection, handling network transitions (WiFi $\leftrightarrow$ Cellular), and resuming dropped sequence IDs with heartbeat ACKs.
- **Infinite Virtualized Message List:** Rendering messages with rich embeds, mentions, animated emojis, and inline attachments at a rock-solid 120 FPS.
- **Voice Channels (WebRTC):** Managing audio session categories (`AVAudioSession` / `AudioManager`), mute/deafen states, noise suppression, and background audio execution.
- **Local Database Caching:** Caching recent channels and messages using SQLite/Room/SwiftData for instantaneous cold start rendering.

---

## 💡 Behavioral
- Why did Discord transition its Android app from React Native back to 100% Native Kotlin, and what are the trade-offs between cross-platform frameworks and pure native code?
- Describe a challenging memory leak or main-thread hang you resolved using platform profilers.

---

## 📚 Resources
- [Discord Engineering Blog](https://discord.com/category/engineering)
- [Discord Careers](https://discord.com/careers)
