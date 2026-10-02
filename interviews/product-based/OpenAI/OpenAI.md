# OpenAI Mobile Interview Preparation

> **Target:** iOS & Android Software Engineers (ChatGPT Mobile Team)  
> **Tech Stack:** Swift, SwiftUI, Kotlin, Jetpack Compose, WebSockets, WebRTC, C++ Core, CoreML / ONNX

---

## 📌 Company Overview
- **Type**: Global AI Frontier Product Company
- **Focus**: High-concurrency AI applications, real-time multimodal voice streaming, low-latency token rendering, on-device Whisper & local intelligence.
- **Scale**: Hundreds of millions of weekly active mobile users across ChatGPT iOS and Android apps.

---

## 🧠 Interview Process
1. **Round 1**: Recruiter Screen & Technical Fit (Past mobile architecture projects, concurrency, AI interest).
2. **Round 2**: Live Coding / Data Structures (String parsing, token trees, LRU caching, sliding window).
3. **Round 3**: Mobile System Design (Design ChatGPT Mobile Client with real-time streaming, voice mode, and offline draft queue).
4. **Round 4**: Deep-Dive Architecture & Concurrency (WebSockets, backpressure, markdown rendering performance, battery impact).
5. **Round 5**: Hiring Manager & Cross-Functional (Product trade-offs, rapid prototyping, AI ethics).

---

## 📝 Mobile Coding & Algorithmic Questions
- [ ] **Streaming Markdown Token Parser:** Implement a tokenizer that receives fragmented chunks of Markdown text and updates an AST without re-parsing the entire conversation history.
- [ ] **Chat History LRU / Disk Cache:** Implement a thread-safe two-tier cache (Memory + Disk) that evicts oldest conversation threads when memory reaches 50MB.
- [ ] **Debounced Audio Buffer Chunking:** Implement an audio recording buffer that emits 200ms audio chunks to a WebSocket while tracking silence detection.

---

## 🎨 Mobile System Design: Design ChatGPT Mobile App
- **Real-Time Token Streaming:** Server-Sent Events (SSE) vs WebSockets for token delivery. Handling network dropouts and resuming stream offsets.
- **Chat List Performance:** Rendering 10,000+ messages without frame drops using `LazyColumn` (Compose) or `LazyVStack` (SwiftUI).
- **Voice Mode Latency:** Low-latency WebRTC full-duplex audio streaming, local voice activity detection (VAD), and acoustic echo cancellation.
- **Offline Drafts & Sync:** Local storage with Room/SwiftData, optimistic UI updates, and conflict resolution when offline messages are submitted.

---

## 💡 Behavioral & Engineering Values
- How do you balance shipping cutting-edge experimental features rapidly with rock-solid production stability?
- Describe a time when a third-party API or SDK had unpredictable latency or downtime, and how you architected client-side resiliency.

---

## 📚 Resources
- [OpenAI Careers](https://openai.com/careers)
- [ChatGPT Mobile App Architecture Insights](https://openai.com/blog)
