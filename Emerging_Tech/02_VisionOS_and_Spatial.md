# 🥽 VisionOS & Spatial Computing
> **Focus:** Spatial Design, Windows/Volumes/Spaces, and Interaction Models.

![VisionPro](https://img.shields.io/badge/Platform-visionOS-purple?style=for-the-badge)
![Spatial](https://img.shields.io/badge/Paradigm-Spatial-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Core Concepts (Windows, Volumes, Spaces)](#1-core-concepts)
- [2. Input Model (Eyes + Hands)](#2-input-model-eyes--hands)
- [3. SwiftUI for visionOS](#3-swiftui-for-visionos)
- [4. Porting iOS Apps](#4-porting-ios-apps)

---

## 1. Core Concepts

### Windows
*   Traditional 2D planes floating in 3D space.
*   Built with standard SwiftUI.
*   Users can resize and move them.

### Volumes
*   3D bounded boxes containing 3D content (`RealityView`).
*   Example: A 3D chess board or a floating globe.
*   Visible from all angles (Shared Space).

### Spaces
*   **Shared Space:** Default. Apps coexist (Like desktop windows).
*   **Full Space:** App takes over the entire world (VR mode). Can be Fully Immersive (hide room) or Mixed Reality (Passthrough).

---

## 2. Input Model (Eyes + Hands)

*   **Look and Pinch:** The primary interaction.
    1.  **Look:** Eye tracking acts as the "Hover" state.
    2.  **Pinch:** Finger tap acts as the "Click".
*   **Direct Touch:** Reaching out and touching a virtual object.
*   **System Gesture:** Pinching fingers while looking at the "Home View" button.

### Design Guideline:
**"Comfortable interactive elements should be at least 60pt (eyes represent a larger pointer than fingers)."**

---

## 3. SwiftUI for visionOS

SwiftUI is the native language of visionOS.

```swift
import SwiftUI
import RealityKit

struct ContentView: View {
    var body: some View {
        VStack {
            Text("Hello Spatial World")
                .font(.extraLargeTitle)
                .glassBackgroundEffect() // The signature material
            
            Model3D(named: "Robot") // Easy 3D loading
        }
    }
}
```

### RealityKit
*   Used for rendering complex 3D content, physics, and lighting.
*   `RealityView` creates a bridge between SwiftUI and RealityKit entities.

---

## 4. Porting iOS Apps

### Q. How do I bring my existing iOS app to Vision Pro?
**Answer:**
1.  **Compatible Apps (iPad Mode):** Default. Run unmodified as a 2D window.
2.  **Designed for iPad:** Update the target SDK to visionOS. Refine layouts. Add ornaments (sidebars/toolbars that float outside the window).
3.  **Fully Native:** Rebuild using spatial features (Volumes/ImmersiveSpace).

### Q. Key Design Changes?
*   **No Dark/Light Mode:** visionOS adapts to the room's lighting. Use system semantic colors/materials (`.glass`).
*   **Hover Effects:** Essential for feedback since there is no mouse cursor.
*   **Typography:** Use bolder weights for legibility against dynamic backgrounds.
