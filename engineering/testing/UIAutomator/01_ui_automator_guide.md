# 🤖 UI Automator
> **Targeted for Android QA & Developers**
> **Note:** Cross-app functional UI testing.

![UI Automator](https://img.shields.io/badge/Testing-UI_Automator-blue?style=for-the-badge&logo=android&logoColor=white)

---

## 📖 Table of Contents
- [1. Overview](#overview)
- [2. Espresso vs UI Automator](#espresso-vs-ui-automator)
- [3. Key Classes](#key-classes)
- [4. Finder & Selectors](#selectors)

---

### Q1. What is UI Automator?

**Answer:**
UI Automator is a testing framework provided by Google that lets you verify the state of your app and interact with the **entire device**. Unlike Espresso, it can interact with **system apps** (Settings, Notification Shade) and **other installed apps**.

### Q2. Espresso vs UI Automator?

**Answer:**
| Feature | Espresso | UI Automator |
| :--- | :--- | :--- |
| **Scope** | Single App (White-box) | System-wide / Cross-App (Black-box) |
| **Speed** | Very Fast (Synchronized) | Slower |
| **Access** | Access to app internal code | Only what's visible on screen |
| **Use Case** | Unit/Integration UI Tests | Functional/System Tests |

### Q3. How do you identify elements?

**Answer:**
UI Automator uses **`UiSelector`** to query the hierarchy.
Common selectors:
- `text("Home")`
- `resourceId("com.example:id/btn_submit")`
- `className("android.widget.Button")`
- `description("Content Description")`

### Q4. Example Test Code?

**Answer:**
```java
// 1. Get device instance
UiDevice device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation());

// 2. Press Home button
device.pressHome();

// 3. Find an App icon by text and click
UiObject allAppsButton = device.findObject(new UiSelector().description("Apps"));
allAppsButton.click();

// 4. Scroll to find Settings
UiScrollable appViews = new UiScrollable(new UiSelector().scrollable(true));
appViews.scrollIntoView(new UiSelector().text("Settings"));
```

### Q5. How to handle dynamic elements?

**Answer:**
Since UI Automator does not automatically sync with the UI (unlike Espresso), you often need to use `wait` functions.
```java
// Wait up to 5 seconds for the object to appear
device.wait(Until.findObject(By.text("Welcome")), 5000);
```

### Q6. Can it run on CI/CD?
**Answer:**
Yes, it runs via `adb shell am instrument` just like other instrumentation tests. It is commonly used in device farms (like Firebase Test Lab) to ensure the app interacts correctly with system permissions dialogs or share sheets.
