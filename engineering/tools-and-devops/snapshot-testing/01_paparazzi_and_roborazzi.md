# 📸 Headless Snapshot Testing: Paparazzi, Roborazzi & Point-Free

> **Fast, deterministic visual regression testing: Rendering Jetpack Compose and SwiftUI on the host JVM/CLI without booting emulators or simulators.**

---

## 📌 Executive Summary

Traditional UI screenshot testing on mobile was historically abandoned by many teams because:
1. Booting an Android Emulator or iOS Simulator in a GitHub Actions Linux runner takes **3 to 7 minutes**.
2. Rendering 200 screens across multiple screen sizes took **over 30 minutes in CI**.
3. Slight GPU rendering differences between a developer's M3 MacBook and a CI cloud runner caused **false-positive pixel mismatch failures**.

The modern mobile snapshot ecosystem has solved this via **Headless JVM Rendering**:
- **Paparazzi** (Cash App) and **Roborazzi** render Android Jetpack Compose and XML layouts **directly on the host JVM** in milliseconds without an emulator.
- **Point-Free SnapshotTesting** provides native SwiftUI and UIKit visual regression checking for iOS.

---

## 🏗️ How Paparazzi Works: JVM LayoutLib Architecture

```
Traditional Emulator Snapshotting:
[ Test Runner ] ──> [ Boot Android OS (Linux Kernel + ART) ] ──> [ GPU Rasterizer ] ──> [ Screenshot ]
⏱️ Time: ~45 seconds per screen test.

Paparazzi Headless JVM Architecture:
[ Compose Code ] ──> [ Android Studio LayoutLib (Pure Java/Kotlin) ] ──> [ Software Canvas ] ──> [ PNG File ]
⏱️ Time: ~35 milliseconds per screen test!
```

By decoupling UI rendering from the Android OS runtime and routing rendering through `LayoutLib` (the internal rendering engine that powers Android Studio's design preview), Paparazzi runs **thousands of visual tests in seconds**.

---

## 💻 Writing a Production Snapshot Test (Kotlin / Compose)

```kotlin
// CheckoutButtonTest.kt
class CheckoutButtonTest {

    @get:Rule
    val paparazzi = Paparazzi(
        deviceConfig = DeviceConfig.PIXEL_6.copy(
            nightMode = NightMode.NOTNIGHT,
            fontScale = 1.0f
        ),
        theme = "android:Theme.Material.Light.NoActionBar"
    )

    @Test
    fun snapCheckoutButton_DefaultState() {
        paparazzi.snapshot {
            MyDesignSystemTheme {
                PrimaryButton(
                    text = "Pay $49.99",
                    isLoading = false,
                    enabled = true,
                    onClick = {}
                )
            }
        }
    }

    @Test
    fun snapCheckoutButton_LoadingState() {
        paparazzi.snapshot {
            MyDesignSystemTheme {
                PrimaryButton(
                    text = "Pay $49.99",
                    isLoading = true,
                    enabled = false,
                    onClick = {}
                )
            }
        }
    }

    @Test
    fun snapCheckoutButton_Accessibility_LargeFont() {
        // Test WCAG Accessibility 200% font scaling
        paparazzi.unsafeUpdateConfig(
            deviceConfig = DeviceConfig.PIXEL_6.copy(fontScale = 2.0f)
        )
        paparazzi.snapshot {
            MyDesignSystemTheme {
                PrimaryButton(
                    text = "Pay $49.99 with Apple Pay",
                    isLoading = false,
                    enabled = true,
                    onClick = {}
                )
            }
        }
    }
}
```

---

## 🍎 iOS: Point-Free Snapshot Testing (SwiftUI)

```swift
import XCTest
import SnapshotTesting
import SwiftUI
@testable import MyApp

final class PrimaryButtonTests: XCTestCase {
    func testPrimaryButton_LightMode() {
        let view = PrimaryButton(title: "Complete Order", state: .normal)
        let hostingController = UIHostingController(rootView: view)
        
        // Assert visual snapshot matches golden image
        assertSnapshot(of: hostingController, as: .image(on: .iPhone13Pro))
    }

    func testPrimaryButton_DarkMode() {
        let view = PrimaryButton(title: "Complete Order", state: .normal)
            .preferredColorScheme(.dark)
        let hostingController = UIHostingController(rootView: view)
        
        assertSnapshot(of: hostingController, as: .image(on: .iPhone13Pro))
    }
}
```

---

## 🔄 The CI/CD Golden Image Workflow

```
 Developer Laptop                   Pull Request (CI)                  Golden Storage (Git LFS)
[ Edit UI Component ] ──> [ Record Golden Images ] ───────────> [ Commit PNGs to Git LFS ]
                          (./gradlew recordPaparazziDebug)                  │
                                                                           ▼
[ Push Pull Request ] ─────────────────────────────────────────> [ CI Verification Task ]
                                                                 (./gradlew verifyPaparazziDebug)
                                                                           │
                                                     ┌─────────────────────┴─────────────────────┐
                                                     ▼                                           ▼
                                             [ 0 Pixel Diff ]                          [ Pixel Mismatch! ]
                                             ✅ PR Check Passes                        ❌ PR Fails; Bot posts
                                                                                          visual diff overlay!
```

---

## 🎯 Staff / Lead Interview Questions & Scenarios

### Q1: "How do you handle OS font rendering and anti-aliasing discrepancies between macOS developer laptops and Ubuntu Linux CI runners?"
* **Answer**:
  - The exact same text string can render with minor sub-pixel anti-aliasing variations when rendered by FreeType on Linux vs. CoreText on macOS, causing `verify` tasks to fail in CI even when the design is unchanged.
  - **Solutions**:
    1. **Strict Docker Containerization**: Run `./gradlew recordPaparazziDebug` inside a standardized Docker container (e.g., Ubuntu Temurin JDK) locally and in CI so the rendering host environment is identical.
    2. **Configurable Tolerance Threshold**: Configure a pixel tolerance threshold (e.g., allow up to 0.1% pixel difference to account for sub-pixel anti-aliasing while catching layout shifts).
    3. **Commit Golden Files via CI Bot**: Have developers push UI changes, and let a dedicated CI action generate and commit the golden images using the canonical Linux environment.

### Q2: "Why should snapshot tests be prioritized over full end-to-end emulator tests for Design Systems?"
* **Answer**:
  - Design systems require testing dozens of component permutations: **5 states** (default, pressed, focused, disabled, loading) × **2 themes** (light/dark) × **3 font scales** (100%, 150%, 200%) × **2 directions** (LTR, RTL).
  - That produces **60 permutations for a single button**.
  - Running 60 emulator tests takes 10+ minutes. Running 60 Paparazzi headless JVM tests takes **under 2 seconds**.
