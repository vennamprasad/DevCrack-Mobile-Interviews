# Duolingo Mobile Interview Preparation

> **Target:** Android & iOS Mobile Engineers  
> **Tech Stack:** Kotlin, Jetpack Compose, Swift, SwiftUI, Python backend, Custom Sound & Animation Engines, Offline-first synchronization

---

## 📌 Company Overview
- **Type**: Global EdTech & Gamification Leader
- **Focus**: Gamified micro-learning, complex interactive animations, offline lesson execution, sound synthesis, A/B testing infrastructure.
- **Scale**: Over 100 million monthly active users completing billions of language, math, and music exercises.

---

## 🧠 Interview Process
1. **Round 1**: Recruiter Screen (Resume walkthrough, mobile project scope, technical passions).
2. **Round 2**: Technical Phone Screen (Algorithms & core mobile principles: lifecycle, memory, collections).
3. **Round 3**: Data Structures & Algorithmic Problem Solving (Trees, graph traversal, string edits, dynamic programming).
4. **Round 4**: Mobile System Design (Design Duolingo Offline Lesson Engine & Streak Synchronizer).
5. **Round 5**: Cultural Interview (Continuous learning, A/B testing mindset, user empathy).

---

## 📝 Mobile Coding Questions
- [ ] **Levenshtein Distance for Speech/Typing Validation:** Given a target sentence and a user's typed speech input, compute the minimum edit distance to identify typos vs grammar errors.
- [ ] **Skill Tree Dependency Traversal:** Model a language curriculum as a Directed Acyclic Graph (DAG) and return the next unlocked nodes when a lesson is mastered.
- [ ] **Streak Calculator with Timezone Shifts:** Compute consecutive day streaks given a list of timestamps, correctly handling daylight savings and international timezone changes.

---

## 🎨 Mobile System Design: Design Duolingo Offline Lesson Engine
- **Asset Pre-fetching & Caching:** Downloading audio pronunciations, SVG vector illustrations, and lesson JSON manifests ahead of time on WiFi.
- **Offline Session Execution:** Running complex interactive lessons (matching pairs, speech recognition, fill-in-the-blanks) completely offline.
- **Conflict Resolution & Sync:** Syncing completed XP, gems, and daily streaks back to the server with idempotency keys upon network reconnection.
- **Animation Performance:** Rendering character animations (Duo the Owl) using Lottie / Rive / Canvas without causing jank or battery drain.

---

## 💡 Behavioral & Product Mindset
- Duolingo runs hundreds of concurrent A/B tests. How do you architect mobile code so experimental feature flags do not pollute clean architecture?
- Describe how you optimize mobile app startup time and binary APK/IPA size for users on budget devices in emerging markets.

---

## 📚 Resources
- [Duolingo Careers](https://careers.duolingo.com/)
- [Duolingo Engineering Blog](https://blog.duolingo.com/engineering/)
