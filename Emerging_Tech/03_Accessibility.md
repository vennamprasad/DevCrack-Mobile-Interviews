# ♿ Mobile Accessibility (A11y)
> **Focus:** WCAG, VoiceOver/TalkBack, Dynamic Type, and Legal Compliance.

![A11y](https://img.shields.io/badge/Topic-Accessibility-yellow?style=for-the-badge)
![Impact](https://img.shields.io/badge/Impact-Inclusive-green?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Why Accessibility Matters](#1-why-accessibility-matters)
- [2. Screen Readers (TalkBack / VoiceOver)](#2-screen-readers)
- [3. Android Implementation](#3-android-implementation)
- [4. iOS Implementation](#4-ios-implementation)
- [5. Testing A11y](#5-testing-a11y)

---

## 1. Why Accessibility Matters

1.  **Inclusivity:** 15% of the world has some disability.
2.  **Legal:** ADA (USA), EAA (Europe) require digital accessibility. Lawsuits (e.g., Domino's) are common.
3.  **SEO & Quality:** A11y improves code structure and often helps automation testing.

---

## 2. Screen Readers

They linearize the UI, reading elements top-to-bottom, left-to-right.
*   **Android:** TalkBack
*   **iOS:** VoiceOver

**Key Concepts:**
*   **Content Description / Label:** What is this element? (e.g., "Submit Button").
*   **Role / Trait:** What does it do? (e.g., "Button", "Heading").
*   **State:** e.g., "Selected", "Disabled".
*   **Focus Order:** The sequence of navigation.

---

## 3. Android Implementation

### Labels
```xml
<!-- XML -->
<ImageButton
    android:contentDescription="@string/play_video_description" />

<!-- Compose -->
Icon(
    imageVector = Icons.Default.Play,
    contentDescription = stringResource(R.string.play_video)
)
```

### Decorating (Decorative Images)
If an image adds no info (e.g., a background pattern), hide it from TalkBack.
```kotlin
// Compose
Image(..., contentDescription = null) // null hides it
```

### Touch Targets
Minimum **48dp x 48dp**.
(Even if the icon is 24dp, add padding/hit test area).

---

## 4. iOS Implementation

### Labels & Hints
```swift
Button(action: {}) {
    Image(systemName: "plus")
}
.accessibilityLabel("Add Item")
.accessibilityHint("Creates a new task in your list")
```

### Traits
```swift
Text("Total Balance")
    .accessibilityAddTraits(.isHeader) // Helps navigation
```

### Dynamic Type (Text Scaling)
Users can set text size to 200%.
*   **Don't** hardcode heights (`frame(height: 50)`).
*   **Use** fluid layouts (`VStack`, `ScrollView`) that can expand.
*   **Use** Scaled Metrics: `@ScaledMetric var size: CGFloat = 20`.

---

## 5. Testing A11y

### Tools
1.  **Accessibility Scanner (Android):** Overlay tool that suggests fixes (Contrast, touch targets).
2.  **Accessibility Inspector (iOS):** Debugger in Xcode to check labels and traits.
3.  **Manual Test:** Turn on VoiceOver/TalkBack and try to use your app with your eyes closed (Screen Curtain).

### Common Interview Q:
**"How do you handle a custom graph view for accessibility?"**
**Answer:**
Since it's a canvas, it has no native semantic nodes.
1.  Expose data as a "List" representation.
2.  Or use `AccessibilityNodeProvider` (Android) / `UIAccessibilityContainer` (iOS) to manually draw "virtual" accessibility frames over the graph bars so screen readers can focus them.
