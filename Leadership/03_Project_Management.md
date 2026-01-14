# 🗓 Project Management & Agile Interview Guide
> **Targeted for Team Leads / Engineering Managers**
> **Focus:** Delivering value, Agile Methodologies, Estimation, Stakeholder Management.

![Agile](https://img.shields.io/badge/Methodology-Agile-green?style=for-the-badge)
![Scrum](https://img.shields.io/badge/Process-Scrum-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Methodologies (Agile/Scrum/Kanban)](#1-methodologies)
- [2. Estimation & Planning](#2-estimation--planning)
- [3. Stakeholder Management](#3-stakeholder-management)
- [4. Real-World Scenarios](#4-real-world-scenarios)

---

## 1. Methodologies

### Q1. Scrum vs Kanban - When to use which?
**Answer:**
- **Scrum:**
    - **Structure:** Defined Sprints (2 weeks), Rituals (Standup, Retro).
    - **Best For:** Product development with predictable roadmap. Teams that need rhythm.
- **Kanban:**
    - **Structure:** Continuous flow, WIP (Work In Progress) limits.
    - **Best For:** Support/Maintenance teams, DevOps, or highly reactive environments where priorities change daily.

### Q2. What is the difference between "Definition of Ready" (DoR) and "Definition of Done" (DoD)?
**Answer:**
- **DoR (Input):** Criteria for a story to enter the sprint. (e.g., UI Mockups ready, Acceptance Criteria defined, Dependencies identified).
- **DoD (Output):** Criteria for a story to be marked complete. (e.g., Code reviewed, Unit Tests passed, Passed QA, Feature Flagged).

---

## 2. Estimation & Planning

### Q3. Why do we estimate in Story Points?
**Answer:**
- **Abstraction:** Points measure **Complexity**, **Risk**, and **Effort**, not just *Time*.
- **Relativity:** A "5" is harder than a "3". It avoids the trap of "You said 4 hours, why did it take 6?".
- **Velocity:** Helped calculate team capacity over time, accounting for holidays/sickness implicitly.

### Q4. How do you handle a project that is falling behind schedule?
**Answer:**
*The Project Management Triangle: Scope, Time, Resources.*
1.  **Cut Scope:** Remove "Nice-to-haves". (Most common/effective).
2.  **Extend Time:** Push the deadline.
3.  **Add Resources:** (Brooks's Law: Adding manpower to a late project makes it later). Be careful.
4.  **Communicate:** The worst thing is to surprise stakeholders at the last minute. Raise the red flag early.

---

## 3. Stakeholder Management

### Q5. How do you say "No" to a stakeholder?
**Answer:**
*Don't just say No; say "Yes, but..." or "Not now".*
- **"Yes, but..."**: "We can do that, but it will push back Feature Y by 1 week." (Trade-off).
- **"Not now"**: "This is a great idea. Let's add it to the backlog for next quarter when we prioritize roadmap."
- **Data-Driven:** "Our current velocity is X, we cannot physically fit this in."

---

## 4. Real-World Scenarios

### Q6. Scenario: Your roadmap is completely blocked by another team.
**Answer:**
1.  **Escalate:** If peer-to-peer talk fails, escalate to EMs/Directors to align priorities.
2.  **Decouple:** Can we mock the dependency? Can we build a temporary interface?
3.  **Swarm:** Can we lend an engineer to *their* team to help build the blocker? (Inner Sourcing).

### Q7. Scenario: Sprint Carry-over is consistently high (50%).
**Answer:**
*The team is over-committing.*
- **Action:** Reduce planned capacity. Use "Yesterday's Weather" (Average of last 3 sprints velocity) to plan.
- **Investigate:** Are stories too big? -> Split them. Are interruptions high? -> Assign a "Goalie" for support.

### Q8. Scenario: Managing technical vs product backlog.
**Answer:**
*The constant battle.*
- **Strategy:** Allocate % capacity (e.g., 80% Feature, 20% Tech).
- **Pitching Tech Debt:** Translate debt into business terms. "Refactoring this module will reduce bug rate by 50% and speed up new feature dev by 2x."
