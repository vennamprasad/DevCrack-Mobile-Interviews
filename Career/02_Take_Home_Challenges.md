# 💻 Take-Home Challenge Strategy
> **Focus:** Readme Quality, Testing, Clean Code, and Git History.

![Coding](https://img.shields.io/badge/Task-Coding%20Challenge-blue?style=for-the-badge)
![Review](https://img.shields.io/badge/Phase-Take%20Home-green?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Why Candidates Fail](#1-why-candidates-fail)
- [2. The Evaluation Rubric](#2-the-evaluation-rubric)
- [3. The README (Your Sales Pitch)](#3-the-readme-your-sales-pitch)
- [4. Technical Checklist](#4-technical-checklist)

---

## 1. Why Candidates Fail

Most candidates treat the Take-Home as a "hackathon" - they rush to make it *work*, ignoring *how* it works.
Reviewers look for **Production Readiness**, not just functionality.

**Common Rejection Reasons:**
*   **No Readme:** Reviewer doesn't know how to run it.
*   **Spaghetti Code:** Everything in `MainActivity` or massive ViewModels.
*   **No Tests:** "I didn't have time" is a red flag. Write 2-3 essential tests.
*   **Single Commit:** "Initial commit" containing all code. Shows poor development habits.
*   **Hardcoded Keys/Strings:** Lack of polish.

---

## 2. The Evaluation Rubric

What reviewers are grading you on (Score 1-5):

| Category | Criteria |
| :--- | :--- |
| **Architecture** | Separation of concerns (Clean/MVVM). Is data flow unidirectional? |
| **Code Quality** | Naming conventions, function length, error handling. |
| **Testing** | Are the critical paths covered? Are tests brittle? |
| **UX/UI** | Does it look decent? Are states handled (Loading, Error, Empty)? |
| **Git History** | Atomic commits? Descriptive messages? |

---

## 3. The README (Your Sales Pitch)

This is the **first thing** the reviewer sees. Make it impressive.

**Structure:**
1.  **Screenshots/GIFs:** Show the app running.
2.  **Architecture:** "I used MVVM/Clean because..." (Explain your decisions).
3.  **Libraries:** List libraries used and *why* (e.g., "Used Coil for image loading because it's lightweight").
4.  **Trade-offs:** "Given more time, I would handle pagination and add better error retry logic." (This saves you points!).
5.  **How to Run:** "Clone repo, add API Key in `local.properties`, build."

---

## 4. Technical Checklist

### ✅ Architecture
- [ ] Use a standard pattern (MVVM/MVI).
- [ ] Dependency Injection (Hilt/Koin for Android, Factory/Container for iOS) - Keep it simple if scope is small.

### ✅ Networking
- [ ] Handle **Loading** State (Spinner/Skeleton).
- [ ] Handle **Error** State (Snackbar/Retry Button).
- [ ] Handle **Empty** State.
- [ ] Do not expose API Keys (use BuildConfig/xcconfig).

### ✅ Code Quality
- [ ] No Magic Numbers/Strings.
- [ ] Consistent formatting (Cmd+Opt+L).
- [ ] Remove unused imports/resources.

### ✅ Testing
- [ ] Unit Test the ViewModel (Business Logic).
- [ ] Unit Test the Repository/Mapper.
- [ ] (Bonus) 1 UI Test (Espresso/XCUITest).

### ✅ Git
- [ ] At least 5-10 commits.
- [ ] Message: "feat: Implement UserList ViewModel" (Conventional Commits).
