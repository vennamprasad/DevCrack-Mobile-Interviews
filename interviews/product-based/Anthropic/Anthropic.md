# Anthropic Mobile Interview Preparation

> **Target:** iOS & Android Software Engineers (Claude Mobile Team)  
> **Tech Stack:** Swift, SwiftUI, Kotlin, Jetpack Compose, Server-Sent Events (SSE), Local Storage, Modern Concurrency

---

## 📌 Company Overview
- **Type**: Frontier AI Research & Product Safety Company
- **Focus**: Claude mobile applications, low-latency streaming inference, long-context conversation visualization, mobile AI agent execution.
- **Engineering Values**: Safety-first, high technical precision, clean architecture, minimal cognitive bloat.

---

## 🧠 Interview Process
1. **Round 1**: Recruiter Fit & Mobile Technical Background.
2. **Round 2**: Technical Screening (Swift / Kotlin language internals, async stream processing).
3. **Round 3**: Algorithmic & Systems Coding (Token stream manipulation, incremental syntax trees, cancellation).
4. **Round 4**: Mobile System Design (Design Claude Mobile Client with Real-Time SSE Token Streaming & Local Caching).
5. **Round 5**: Cultural Values & AI Safety Alignment.

---

## 📝 Mobile Coding Questions
- [ ] **Stream Cancellation & Token Debouncing:** Implement an asynchronous stream processor that gracefully handles rapid user prompt interruptions, immediately aborting pending network tokens and freeing memory.
- [ ] **Incremental Code Block Syntax Highlighter:** Highlight programming language code blocks within a live streaming LLM response without freezing the main UI thread.
- [ ] **Chat Session Paging & Local Encryption:** Design a local encrypted database schema (using SQLCipher) for storing enterprise chat histories securely on-device.

---

## 🎨 Mobile System Design: Design Claude Mobile App
- **Server-Sent Events (SSE) Client Pipeline:** Consuming HTTP chunked text streams, reconstructing fragmented UTF-8 characters, and updating UI state at 60 FPS.
- **Artifacts / Multi-Window Viewer:** Rendering complex interactive artifacts (SVGs, Markdown, Code) side-by-side on tablet/foldable form factors.
- **Zero-Latency Offline Draft State:** Persisting unsent user queries and voice notes across app backgrounding and unexpected process termination.

---

## 📚 Resources
- [Anthropic Careers](https://www.anthropic.com/careers)
- [Anthropic Engineering & Research](https://www.anthropic.com/news)
