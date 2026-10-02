# ⚛️ React Native Interview Questions & Answers
> **Targeted for Senior Android Developer / Team Lead Roles**

![React Native](https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Expeirence](https://img.shields.io/badge/Senior_Level-Expert-red?style=for-the-badge)
![Interview](https://img.shields.io/badge/Interview-Ready-green?style=for-the-badge)

---

## 📖 Table of Contents

- [Section 1: Core Fundamentals & Architecture](#-section-1--core-fundamentals--architecture)
- [Section 2: State Management](#-section-2--state-management)
- [Section 3: Performance Optimization](#-section-3--performance-optimization)
- [Section 4: Navigation & Animations](#-section-4--navigation--animations)
- [Section 5: Native Integration](#-section-5--native-integration-critical-for-android-leads)
- [Section 6: Testing & Security](#-section-6--testing--security)
- [Section 7: System Design & Trade-offs](#-section-7--system-design--trade-offs)

---

## ✅ Section 1 — Core Fundamentals & Architecture

### 1. Architecture & The Bridge

#### **Q: Explain the thread model in the "Old" Architecture.**
React Native (Legacy) runs on 3 main threads:
1.  **Main Thread (UI Thread):** Standard Android/iOS main thread. Handles UI rendering and user gestures.
2.  **JavaScript Thread:** Runs the JS Bundle (logic, React diffing, API calls).
3.  **Shadow Thread (Background):** Calculates layout using **Yoga** (Flexbox engine).
> **The Bridge:** An asynchronous, serialized message queue (JSON) that allows these threads to communicate. It is the main bottleneck (slow, distinct memory spaces).

#### **Q: What is the "New Architecture" (Fabric & TurboModules)?**
Solves the "Bridge" bottleneck. Key components:
- **JSI (JavaScript Interface):** Allows JS to hold direct references to C++ Host Objects. No JSON serialization needed. Synchronous communication.
- **Fabric (New Renderer):** Uses JSI to allow React to communicate directly with the Shadow Tree and UI Native components. Enables synchronous UI updates (solving the "white flash" on scroll).
- **TurboModules:** Lazy-loaded native modules. Instead of loading *all* native modules at startup (slowing launch), they are loaded only when needed via JSI.
- **Codegen:** Automates type safety (TypeScript/Flow -> C++) between JS and Native.

#### **Q: What is Hermes?**
An open-source JS engine optimized for React Native.
- **AOT (Ahead-of-Time) Compilation:** Compiles JS to Bytecode at build time (unlike V8's JIT).
- **Benefits:** Faster startup, smaller APK size, lower memory usage.

### 2. React Fundamentals

#### **Q: Virtual DOM vs Real DOM in RN context**
React Native uses the same Virtual DOM concept as Web. React Reconciler diffs the tree.
- Instead of rendering HTML `<div>`, it maps to **Native UI Components** (`ViewGroup` on Android, `UIView` on iOS).

#### **Q: Lifecycle: Class vs Functional Components**
Modern RN is all **Hooks** (Functional).
- `componentDidMount` -> `useEffect(() => {}, [])`
- `componentDidUpdate` -> `useEffect(() => {}, [dependency])`
- `componentWillUnmount` -> `useEffect(() => { return () => cleanup }, [])`

[⬆️ Back to Top](#-table-of-contents)

---

## ✅ Section 2 — State Management

### 3. Managing State

#### **Q: Context API vs Redux vs Zustand**
- **Context API:** Built-in. Good for global static data (Theme, Auth User). *Pitfall:* Updates trigger re-render of *all* consumers. Not optimized for high-frequency updates.
- **Redux (Toolkit):** Industry standard. STRICT unidirectional data flow. Good for debugging (Time travel), middleware, and large teams. Heavy boilerplate (reduced by Toolkit).
- **Zustand:** "Modern simplified Redux". Minimal boilerplate, hooks-based, no provider wrapper needed. Very fast and popular recently.

#### **Q: What is "Prop Drilling" and how to avoid it?**
Passing data through many layers of components that don't need it.
- **Fix:** Use Composition (pass components as children), Context, or a Global State Manager.

---

## ✅ Section 3 — Performance Optimization

### 4. Rendering & Lists

#### **Q: FlatList vs ScrollView**
- **ScrollView:** Renders *all* children at once. Performance disaster for large lists.
- **FlatList:** Virtualized. Only renders items in the viewport (plus window size). Recycles views.

#### **Q: How do you optimize a choppy FlatList?**
1.  `getItemLayout`: Skip layout calculation (if fixed height).
2.  `windowSize`: Reduce rendering window.
3.  `removeClippedSubviews={true}`: Free memory of off-screen views.
4.  **FlashList (by Shopify):** Use this instead of FlatList. It uses "Cell Recycling" (like Android `RecyclerView`) instead of destroying/recreating views, offering 5x performance.

#### **Q: useMemo vs useCallback**
- **useMemo:** Caches a *calculated value*. Prevents expensive recalculation on every render.
- **useCallback:** Caches a *function definition*. Prevents the function reference from changing, so child components wrapped in `React.memo` don't needlessly re-render.

#### **Q: What is "InteractionManager"?**
Delays execution of a task until interactions (animations/transitions) are finished.
- *Use Case:* Perform heavy calculation only after the navigation push animation completes to avoid dropping frames during the transition.

[⬆️ Back to Top](#-table-of-contents)

---

## ✅ Section 4 — Navigation & Animations

### 5. Navigation

#### **Q: React Navigation vs Native Navigation (Wix)**
- **React Navigation:** JS-based. Most popular. Highly customizable. Uses standard Native components (`UINavigationController` / `Fragment`) under the hood in newer versions (Native Stack), but logic is in JS.
- **React Native Navigation (Wix):** Truly native navigation. Each screen is a native Activity/ViewController. Better performance for complex transitions, but harder to integrate with JS state libraries.

### 6. Animations

#### **Q: Animated API vs React Native Reanimated**
- **Animated API:** Built-in. Good for simple things. Can use `useNativeDriver: true` to offload to UI thread, but limited (cannot animate layout properties like height/width easily on UI thread).
- **Reanimated (v2/v3):** The standard for complex animations. Runs generic JS logic on the **UI Thread** (via JSI/Worklets). Eliminates bridge delays. 60 FPS guaranteed even if JS thread is blocked.

[⬆️ Back to Top](#-table-of-contents)

---

## ✅ Section 5 — Native Integration (Critical for Android Leads)

### 7. Native Modules

#### **Q: How do you access a native Android API not available in RN?**
Write a **Native Module**.
1.  Create a Java/Kotlin class extending `ReactContextBaseJavaModule`.
2.  Annotate methods with `@ReactMethod`.
3.  Register module in a `ReactPackage`.
4.  Add package to `MainApplication` (or Autolinking will handle it).
5.  Access in JS via `NativeModules.MyModule`.

#### **Q: How does New Architecture change Native Modules?**
It introduces **TurboModules**.
- Requires pure C++ implementation (mostly) or JSI bindings.
- Methods are synchronous.
- Code is type-safe via **Codegen** specs (Native <-> JS interface defined in TypeScript).

### 8. Deployment & Tooling

#### **Q: What is CodePush?**
A cloud service (Microsoft App Center) that enables OTA (Over-The-Air) updates.
- Allows updating the JS Bundle and Assets *without* a Store release.
- *Limitation:* Cannot update Native Code (Java/Swift/Gradle changes).

#### **Q: How do you debug React Native?**
- **Flipper:** (Being deprecated, but still used) Network logs, Layout Inspector DB.
- **Chrome DevTools:** Console logs (if not using Hermes).
- **React DevTools:** Inspect Component hierarchy/props.
- **Performance Monitor:** FPS overlay.

[⬆️ Back to Top](#-table-of-contents)

---

## ✅ Section 6 — Testing & Security

### 9. Testing

#### **Q: How do you split testing in RN?**
- **Static Analysis:** ESLint, Prettier, TypeScript (compile time checks).
- **Unit Testing:** Jest. Test logic, hooks, and snapshots of components.
- **Integration Testing:** `react-native-testing-library`. Tests user interactions ("press button", "see text") on a simulated component tree.
- **E2E Testing:** Detox (Grey box) or Appium (Black box). Runs on real emulator. Detox is preferred for RN as it synchronizes with the app lifecycle (avoids `sleep()` flakes).

### 10. Security

#### **Q: Secure Storage options?**
- Avoid `AsyncStorage` for secrets (it's essentially unencrypted XML/SQLite).
- Use `react-native-encrypted-storage` or `react-native-keychain` (wraps Android Keystore / iOS Keychain).

---

## ✅ Section 7 — System Design & Trade-offs

### 11. Trade-offs

#### **Q: React Native vs Native Android vs Flutter?**
- **Native:** Best performance, latest OS features day 1, hard to maintain 2 codebases.
- **React Native:** "Write Once", uses Native UI widgets (looks native), huge web ecosystem (npm). *Cons:* Bridge bottleneck (solved by new arch), fragile upgrades.
- **Flutter:** Best consistency (Skia), great tooling. *Cons:* Non-native UI widgets (uncanny valley), Dart is less popular than JS/TS.

#### **Q: How to structure a scalable RN app?**
- **Atomic Design:** atoms, molecules, organisms.
- **Feature-based:** `src/features/auth`, `src/features/feed`.
- **Separation:** Logic (Hooks) separate from UI (Views). `useAuth()` hook handles logic, `LoginView` just renders.

[⬆️ Back to Top](#-table-of-contents)
