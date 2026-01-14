# 👨‍💼 Engineering Management Interview Guide
> **Targeted for Engineering Manager (EM) & Staff/Principal Roles**
> **Focus:** People Management, 1:1s, Performance Reviews, Conflict Resolution.

![Leadership](https://img.shields.io/badge/Skill-Leadership-blue?style=for-the-badge)
![Management](https://img.shields.io/badge/Focus-People%20Management-green?style=for-the-badge)

---

## 📖 Table of Contents
- [1. The Role of an EM](#1-the-role-of-an-em)
- [2. One-on-Ones (1:1s)](#2-one-on-ones-11s)
- [3. Performance Management](#3-performance-management)
- [4. Handling Underperformance (PIP)](#4-handling-underperformance-pip)
- [5. Conflict Resolution](#5-conflict-resolution)
- [6. Real-World Scenarios](#6-real-world-scenarios)

---

## 1. The Role of an EM

### Q1. How do you define the role of an Engineering Manager?
**Answer:**
An EM's primary goal is to **build high-performing teams** and **enable them to deliver value**.
- **People:** Career growth, hiring, retention, morale.
- **Process:** Unblocking the team, refining agile processes, removing friction.
- **Technical:** Assessing feasibility, guiding architecture (not coding daily), managing tech debt.
- **Product:** Aligning technical output with business goals.

### Q2. Transitioning from IC (Individual Contributor) to Manager?
**Answer:**
- **Shift in Focus:** From "I wrote this code" to "My team delivered this features".
- **Success Metric:** Team output > Individual output.
- **Challenges:** Letting go of coding, trusting the team, dealing with ambiguity.
- **Why:** Desire to have a multiplier effect on the organization.

---

## 2. One-on-Ones (1:1s)

### Q3. How do you structure your 1:1s?
**Answer:**
- **Frequency:** Weekly or Bi-weekly (30-45 mins).
- **Ownership:** The report owns the agenda.
- **Structure:**
    1.  **Wellness Check:** How are you feeling doing? (Burnout check).
    2.  **Unblocking:** Any immediate blockers?
    3.  **Wins/Feedback:** Recent accomplishments or course corrections.
    4.  **Career Development:** (Once a month) Progress towards promotion/goals.
- **Anti-Pattern:** Treating it as a status update meeeting.

### Q4. A high-performer tells you they are bored. What do you do?
**Answer:**
1.  **Acknowledge:** Validate their feelings.
2.  **Explore:** Identify interests (Mentoring? Architecture? New Tech? Public Speaking?).
3.  **Action:** Delegate "Stretch Goals" or complex problems from your plate.
4.  **Growth:** Discuss promotion path or lateral moves to other teams if beneficial for them.

---

## 3. Performance Management

### Q5. How do you handle promotions?
**Answer:**
- **Evidence-Based:** Collect "Promo Pack" (Design docs, Code reviews, Impact metrics).
- **Gap Analysis:** Compare current performance vs Next Level expectations.
- **Sponsorship:** Advocate for them in calibration meetings with other managers.
- **No Surprises:** The promotion conversation should be the confirmation of a long process, not a surprise event.

### Q6. How do you deliver critical feedback?
**Answer:**
- **Timely:** Do not save it for the performance review. Give it immediately (within 24-48 hrs).
- **Specific:** Cite specific examples (behavior), not character traits.
- **Format (SBI):**
    - **Situation:** "In yesterday's outage meeting..."
    - **Behavior:** "You interrupted the junior engineer three times..."
    - **Impact:** "This discouraged them from sharing their root cause analysis."
- **Action:** Ask them for their perspective and agree on a different approach next time.

---

## 4. Handling Underperformance (PIP)

### Q7. How do you manage an underperforming engineer?
**Answer:**
1.  **Diagnosis:** Is it Skill (Training needed)? Will (Motivation/Burnout)? or Environment (Unclear goals)?
2.  **Clear Expectation:** explicitly state where they are missing the mark.
3.  **Support Plan:** Pair programming, mentorship, smaller tasks to build momentum.
4.  **Review:** Set a timeline (e.g., 4 weeks) to re-evaluate.

### Q8. Walk me through a PIP (Performance Improvement Plan).
**Answer:**
*A PIP is the last resort when coaching fails.*
1.  **Document:** Formal document outlining specific deficiencies.
2.  **SMART Goals:** Specific, Measurable, Achievable, Relevant, Time-bound goals they must hit to pass.
3.  **Check-ins:** Weekly check-ins to track progress.
4.  **Outcome:** If goals are met -> PIP ends (successful). If not -> Termination.
*Crucial: Treat it with empathy, but firmness.*

---

## 5. Conflict Resolution

### Q9. Two senior engineers disagree on an architectural decision. How do you resolve it?
**Answer:**
1.  **Mediated Discussion:** Get them in a room/call.
2.  **Disagree and Commit:** If no consensus, someone (Lead/Architect/EM) must decide to move forward.
3.  **Criteria-based:**
    - "What is the cost of reversing this decision?" (Type 1 vs Type 2 decision).
    - "Which aligns better with our long-term goals (Scalability/Speed)?"
4.  **Outcome:** Document the decision (ADR - Architecture Decision Record) and reason.

### Q10. A Product Manager keeps adding scope creep. The team is burning out.
**Answer:**
1.  **Shield the Team:** "No new requests in the current sprint."
2.  **Data:** Show the PM the "Iron Triangle" (Scope, Time, Quality/Resources). "If you add X, we must drop Y or delay the release."
3.  **Process:** Enforce a "Feature Freeze" or strict Change Request process.
4.  **Relationship:** Build trust so the PM understands you are protecting delivery quality, not just saying "No".

---

## 6. Real-World Scenarios

### Q11. Scenario: You just joined a new team as an EM. What do you do in the first 30 days?
**Answer:**
- **Listen & Learn:** Don't make changes yet.
- **1:1s:** Meet everyone. Ask: "What is working well?", "What is broken?", "If you were me, what would you fix?"
- **Meet Stakeholders:** PM, Design, Other EMs.
- **Quick Wins:** Identify small friction points (e.g., "Too many meetings") and fix them to build trust.

### Q12. Scenario: An engineer is "Toxic High Performer" (Brilliant Jerk).
**Answer:**
*Zero tolerance policy.*
- **Impact:** They destroy the team's psychological safety, costing more than they produce.
- **Action:**
    1.  Give Feedback: "Your code is great, but your behavior in code reviews is unacceptable."
    2.  Set Boundaries: "Collaboration is a job requirement."
    3.  Exit: If behavior doesn't change, they must go. "We value culture over code."

### Q13. Scenario: The team missed a critical deadline.
**Answer:**
- **Own it:** Take responsibility to upper management. "The team missed it" -> "We missed it."
- **Retrospective:** Run a blameless post-mortem. Why? (Bad estimation? Unforeseen complexity? Scope creep?).
- **Communication:** Inform stakeholders early (as soon as you know), not at the deadline.
- **Fix:** Adjust process to prevent recurrence (e.g., add buffer to estimates).

### Q14. Scenario: How do you measure your team's success?
**Answer:**
- **DORA Metrics:** Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR (Mean Time to Recovery).
- **Business Impact:** Did we move the needle on user retention/revenue?
- **Team Health:** Retention rate, eNPS (Employee Net Promoter Score).

### Q15. Scenario: Layoffs. You have to let go of 2 people.
**Answer:**
*The hardest part of the job.*
1.  **Criteria:** Objective selection (Role redundancy, Performance, Tenure - depending on legal/company policy).
2.  **The Meeting:** Be direct, compassionate, and brief. Do not promise things you can't deliver. "Today is your last day."
3.  **The Survivors:** Address the remaining team immediately. Be honest (within legal limits). Reassure them about the future focus.
