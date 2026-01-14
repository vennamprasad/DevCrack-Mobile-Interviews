# 🎨 Android UX (User Experience) Interview Guide
> **Targeted for Senior Android Developer / Product Engineer Roles**
> **Note:** UX is not just design; it's about flow, feedback, and accessibility.

![UX](https://img.shields.io/badge/Topic-UX_Design-FF61F6?style=for-the-badge&logo=materialdesign&logoColor=white)
![Accessibility](https://img.shields.io/badge/Focus-Accessibility-blue?style=for-the-badge)
![Material](https://img.shields.io/badge/Design-Material_3-7F52FF?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Material Design (M2 vs M3)](#-1-material-design)
- [2. Accessibility (a11y)](#-2-accessibility)
- [3. Navigation Patterns](#-3-navigation)
- [4. Dark Mode & Theming](#-4-theming)
- [5. Feedback & Micro-interactions](#-5-feedback)

---

## ✅ Overview

**User Experience (UX)** in Android is driven by Google's **Material Design** guidelines. It focuses on clean layouts, intuitive navigation, and responsive interactions.

---

## 🧩 Interview Questions (Q&A)

### 1. Material Design

#### Material 2 vs Material 3 (You)?
*   **Material 2:** Shadow-heavy, geometric, standard colors.
*   **Material 3 (Material You):** Dynamic Color (extracts colors from user wallpaper), flat, large rounded corners, pill-shaped buttons. Personalized to the user.

### 2. Accessibility (a11y)

#### Why is it important?
Allows users with disabilities (vision, hearing, motor) to use your app. Correct implementation improves SEO/Search ranking too.

#### Key Implementations?
1.  **`contentDescription`:** For ImageViews/Icons. "Submit Button" instead of "arrow_right.png".
2.  **Touch Targets:** Minimum **48x48dp** for clickable elements.
3.  **Color Contrast:** Text vs Background ratio (4.5:1 for normal text).
4.  **TalkBack:** Test your app with screen reader enabled.

### 3. Navigation

#### Patterns?
*   **Bottom Navigation:** Top-level destinations (3-5 items).
*   **Navigation Drawer:** Many top-level destinations (>5) or secondary features.
*   **Tabs:** Information of the same hierarchy.
*   **Back Stack:** System Back button must logically return to previous state.

### 4. Theming

#### Handling Dark Mode?
*   **Force Dark:** `android:forceDarkAllowed="true"` (Quick fix, not recommended).
*   **Custom Implementation:**
    *   `values-night` resource folder.
    *   Use Theme Attributes (`?attr/colorSurface`) instead of hardcoded colors (`#FFFFFF`).
    *   Check `Configuration.UI_MODE_NIGHT_MASK`.

### 5. Feedback

#### Micro-interactions?
Subtle animations or haptics that acknowledge user action.
*   **Ripple Effect:** Standard click feedback.
*   **Haptic Feedback:** `view.performHapticFeedback()`.
*   **Snackbar/Toast:** transient messages. Use Snackbar for actionable messages (e.g., "Deleted. Undo?").

---
