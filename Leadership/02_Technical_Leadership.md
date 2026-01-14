# 🏗 Technical Leadership Interview Guide
> **Targeted for Staff Engineers / Tech Leads**
> **Focus:** Architecture Decisions, Technical Debt, Mentorship, Cross-Team Collaboration.

![Tech Lead](https://img.shields.io/badge/Role-Tech%20Lead-orange?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Focus-Architecture-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. The Tech Lead Role](#1-the-tech-lead-role)
- [2. Architecture & Decision Making](#2-architecture--decision-making)
- [3. Managing Technical Debt](#3-managing-technical-debt)
- [4. Mentorship & Force Multiplication](#4-mentorship--force-multiplication)
- [5. Real-World Scenarios](#5-real-world-scenarios)

---

## 1. The Tech Lead Role

### Q1. What is the difference between a Senior Engineer and a Staff/Tech Lead?
**Answer:**
- **Senior:** Solves complex problems *within* a defined scope/team. High quality execution.
- **Staff/TL:** Solves "Ambiguous" problems. Operates *across* teams.
- **Scope:** TL thinks about the entire system, not just the feature.
- **Influence:** TL influences other engineers without necessarily having managerial authority.

### Q2. How do you balance coding vs. leading?
**Answer:**
- **The Shift:** 30-50% Coding, 50-70% Review/Design/Meetings.
- **Coding:** Focus on "Critical Path" (Architecture skeleton, complex core logic) or "Janitorial Work" (Unblocking others). Avoid taking "Critical Feature Work" that blocks the release if you get pulled into meetings.
- **Leading:** RFC Reviews, Unblocking junior devs, Alignment with PM.

---

## 2. Architecture & Decision Making

### Q3. How do you choose a new technology stack? (e.g., KMP vs Flutter vs Native)
**Answer:**
*It’s not just about "Cool Factor".*
1.  **Problem Fit:** Does it solve our specific problem?
2.  **Team Capabilities:** Does the team know language X? What is the learning curve?
3.  **Hiring Market:** Can we hire devs for this stack?
4.  **Ecosystem/Maturity:** Is it production-ready? (Community support, libraries).
5.  **Long-term Maintenance:** Who will own this in 2 years?
6.  **Prototype:** Build a POC (Proof of Concept) to validate assumptions.

### Q4. What is a "One-Way Door" vs "Two-Way Door" decision?
**Answer:**
- **One-Way (Type 1):** Hard to reverse. High stakes. (e.g., Picking a database, Public API contract). **Requires slow, deep deliberation.**
- **Two-Way (Type 2):** Easy to reverse. Low stakes. (e.g., Picking a UI library for an internal tool). **Decide fast and iterate.**

### Q5. Explain the concept of RFC (Request for Comments) or Design Docs.
**Answer:**
- **Purpose:** To scale decision making and gather async feedback.
- **Structure:**
    - **Context:** Why are we doing this?
    - **Proposed Solution:** High-level design.
    - **Alternatives Considered:** Why did we reject option B?
    - **Risks/Trade-offs:** What could go wrong?
- **Outcome:** Consensus and documentation for future onboarding.

---

## 3. Managing Technical Debt

### Q6. How do you handle Tech Debt?
**Answer:**
*Tech debt is a tool, not a crime. It allows speed now for cost later.*
- **Tracking:** Create tickets for debt. Do not rely on "TODO" comments.
- **Prioritization:**
    - **Prudent Debt:** "We need to release for a conference, we will hardcode this now." -> Pay it back immediately after.
    - **Reckless Debt:** "We didn't write tests because we were lazy." -> Fix immediately.
- **Strategy:**
    - **Boy Scout Rule:** Leave the code cleaner than you found it.
    - **20% Time:** Dedicate 20% of sprint capacity to debt/refactoring.
    - **Refactoring Strategy:** Do not pause features for 6 months for a "Rewrite". Refactor gracefully in parallel (Strangler Fig Pattern).

### Q7. When should you do a Full Rewrite?
**Answer:**
*Almost Never.* (Joel Spolsky's famous advice).
- **Risks:** You throw away years of bug fixes and domain knowledge. You deliver 0 value during the rewrite.
- **Alternative:** **Incremental Refactor.** Isolate components, wrap them in interfaces, and replace them one by one.
- **Exception:** The underlying tech is deprecated/unsupported (e.g., Moving from Flash to HTML5).

---

## 4. Mentorship & Force Multiplication

### Q8. How do you mentor junior engineers?
**Answer:**
- **Socratic Method:** Ask questions ("How would you solve this?") instead of giving answers.
- **Code Reviews:** Focus on logic/design, not just syntax (use linters for syntax). Explain "Why".
- **Safety:** Allow them to make small mistakes (in dev/staging) to learn.
- **Sponsorship:** Give them visibility. "Alice did a great job on X" in the team meeting.

### Q9. How do you scale yourself?
**Answer:**
- **Delegation:** Hand off tasks you possess "Subject Matter Expertise" in, to build that expertise in others.
- **Documentation:** Write things down so you don't answer the same question 10 times.
- **Automation:** Automate CI/CD, linting, and processes.

---

## 5. Real-World Scenarios

### Q10. Scenario: The team wants to use a new shiny library, but you disagree.
**Answer:**
1.  **Investigate:** Why do they want it? (Developer Experience? Performance?).
2.  **Evaluate:** Create a decision matrix. Compare it with the standard solution.
3.  **Constraint:** "If you want to use it, you own the documentation and the migration plan."
4.  **Veto:** If it introduces significant risk (security, size, license) without value, use "Authority" sparingly to say no, but explain why.

### Q11. Scenario: You discover a critical bug in production 1 hour before a major marketing launch.
**Answer:**
1.  **Triage:** How bad is it? (Crash? Typos? Data Loss?).
2.  **Mitigate:** Can we feature-flag it off? Can we hotfix?
3.  **Decision:**
    - If "Data Loss" or "Crash": **Abort Launch.** Reputation damage > Delay.
    - If "Visual Glitch": **Proceed**, fix immediately after.
4.  **Communication:** Inform stakeholders immediately with options and recommendation.

### Q12. Scenario: Your codebase compiles too slow (10+ mins). Developers are complaining.
**Answer:**
*This is a "Developer Productivity" crisis.*
1.  **Profile:** Use build profilers (Gradle Scan, Xcode Build Timing).
2.  **Modularize:** Break monolith into modules to enable parallel builds and caching.
3.  **Hardware:** Upgrade dev machines (Cheapest fix).
4.  **Remote Cache:** Implement remote build caching.

### Q13. Scenario: Another team breaks your API contract constantly.
**Answer:**
1.  **Diplomacy:** Talk to their Tech Lead.
2.  **Contract Tests:** Implement Consumer-Driven Contracts (Pact).
3.  **CI Block:** If they break the contract, their build should fail (by running your contract tests).
4.  **Versioning:** Enforce semantic versioning.

### Q14. Scenario: Dealing with a "Hero" developer who hoards knowledge.
**Answer:**
*Bus Factor = 1 is a risk.*
- **Pairing:** Force them to pair program on their domain.
- **Documentation:** Make it a requirement for "Definition of Done".
- **Rotation:** Mandate that someone else must pick up tasks in their domain next sprint.
- **Feedback:** Explain that "being the only one who knows X" is actually a failure of leadership, not a strength.
