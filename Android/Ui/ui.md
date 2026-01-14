# 🖼️ Android UI Interview Questions and Answers
> **Targeted for Junior - Mid Android Developer Roles**
> **Topic:** Building pixel-perfect, responsive UIs.

![UI](https://img.shields.io/badge/Topic-User_Interface-3DDC84?style=for-the-badge&logo=android&logoColor=white)
![Layouts](https://img.shields.io/badge/Focus-Layouts-orange?style=for-the-badge)
![Views](https://img.shields.io/badge/Type-Views-blue?style=for-the-badge)

---

## General UI Questions

### **Q1: What is the difference between `View` and `ViewGroup` in Android?**
**A:** `View` is the base class for all UI components (e.g., Button, TextView). `ViewGroup` is a subclass of `View` that can contain multiple child views (e.g., LinearLayout, RelativeLayout).

### **Q2: How do you support multiple screen sizes and resolutions in Android?**
**A:**
- Use flexible layouts (ConstraintLayout, LinearLayout, etc.).
- Provide alternative resources (layouts, drawables) in resource folders like `layout-sw600dp`, `drawable-hdpi`, etc.
- Use `dp` and `sp` units instead of `px`.
- Test on multiple devices and use the Android emulator's device profiles.

### **Q3: What is the purpose of `ConstraintLayout`?**
**A:** `ConstraintLayout` allows you to create complex layouts with a flat view hierarchy, improving performance and flexibility.

### **Q4: How do you create custom views in Android?**
**A:** Extend the `View` class and override methods like `onDraw()`, `onMeasure()`, and handle custom attributes in the constructor.

### **Q5: How can you optimize UI performance in Android?**
**A:**
- Minimize view hierarchy depth.
- Use RecyclerView for lists.
- Avoid overdraw.
- Use hardware acceleration.
- Load images efficiently (e.g., Glide, Picasso).

---

## Supporting Multiple Devices with a Single Codebase

### **Q6: How do you support multiple mobile devices with a single codebase in Android?**
**A:**
- Use responsive layouts and resource qualifiers (`layout`, `layout-land`, `layout-sw600dp`, etc.).
- Use fragments for modular UI.
- Avoid hardcoding dimensions; use `dp` and `sp`.
- Use vector drawables for scalable images.
- Test on different screen sizes and densities.

### **Q7: What are resource qualifiers and how do they help?**
**A:** Resource qualifiers (e.g., `-land`, `-sw600dp`, `-hdpi`) allow you to provide alternative resources for different device configurations, enabling UI adaptation without changing code.

### **Q8: How do you handle orientation changes in Android UI?**
**A:**
- Use resource folders (`layout-land`, `layout-port`).
- Save UI state in `onSaveInstanceState()`.
- Use ViewModel for data persistence.

### **Q9: What is the role of themes and styles in Android UI?**
**A:** Themes and styles help maintain consistent look and feel, enable easy customization, and support dark/light modes.

### **Q10: How do you implement dark mode in Android?**
**A:**
- Define night resources (`values-night`).
- Use theme attributes (`?attr/colorPrimary`).
- Detect and respond to UI mode changes.