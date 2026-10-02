# 🤖 On-Device ML for Mobile Engineers
> **Focus:** CoreML, TensorFlow Lite, MediaPipe, and Performance.

![AI](https://img.shields.io/badge/Tech-AI%2FML-purple?style=for-the-badge)
![Mobile](https://img.shields.io/badge/Platform-iOS%2FAndroid-blue?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Why On-Device?](#1-why-on-device)
- [2. iOS: CoreML & CreateML](#2-ios-coreml--createml)
- [3. Android: TensorFlow Lite & MediaPipe](#3-android-tensorflow-lite--mediapipe)
- [4. Performance Considerations](#4-performance-considerations)
- [5. Real-World Interview Questions](#5-real-world-interview-questions)

---

## 1. Why On-Device?

Cloud AI is powerful (GPT-4), but On-Device AI is essential for:
1.  **Privacy:** Data (photos/health) never leaves the device.
2.  **Latency:** Real-time feedback (e.g., AR face filters, Camera focus). No network round-trip.
3.  **Offline Capability:** Works without internet.
4.  **Cost:** Reducing server inference costs.

---

## 2. iOS: CoreML & CreateML

### CoreML
Apple's framework to integrate ML models.
*   **Format:** `.mlmodel`
*   **Hardware Acceleration:** Automatically uses Neural Engine (ANE), GPU, or CPU.
*   **Vision Framework:** Used for Image Analysis (Face detection, Text recognition/OCR) integrated with CoreML.

### CreateML
*   Drag-and-drop tool to *train* custom models on Mac.
*   Easy for: Image Classification, Sound Classification, Tabular Data.

---

## 3. Android: TensorFlow Lite & MediaPipe

### TensorFlow Lite (TFLite)
Google's lightweight solution for mobile.
*   **Format:** `.tflite`
*   **Integration:**
    1.  Add library.
    2.  Load model (`Interpreter`).
    3.  Run inference on input ByteBuffer.

### MediaPipe
Google's high-level framework for multimodal pipelines.
*   **Use Cases:** Hand tracking, Pose detection, Face Mesh.
*   **Cross-platform:** Works on Android, iOS, Web.

---

## 4. Performance Considerations

### Quantization (Shrinking the Model)
*   Converting 32-bit floats to 8-bit integers.
*   **Benefit:** Reduces model size (4x smaller) and speeds up inference.
*   **Trade-off:** Slight loss in accuracy.

### Hardware Delegation
*   **GPU Delegate:** For parallel processing (Images).
*   **NPU (Neural Processing Unit):** Highly efficient for matrix math.
*   **NNAPI (Android):** Layer to access hardware acceleration.

---

## 5. Real-World Interview Questions

### Q1. How would you implement an offline document scanner?
**Answer:**
*   Use native vision frameworks (Vision/VisionKit on iOS, ML Kit on Android).
*   **Steps:** Edge detection -> Perspective Correction (homography) -> OCR (Text Recognition).
*   **Privacy:** Ensure all processing happens locally.

### Q2. The ML model is freezing the UI. How do you fix it?
**Answer:**
*   **Threading:** Inference is CPU/GPU intensive. Run it on a background thread (Coroutines/DispatchQueue).
*   **Sampling:** Do not run inference on *every* camera frame (30fps). Throttle to 5-10fps if acceptable.
*   **Resolution:** Resize input images to the model's expected size (e.g., 224x224) efficiently *before* passing to the model.

### Q3. How do you update the model without an app update?
**Answer:**
*   **Remote Config/Download:** Host the model (`.tflite`/`.mlmodel`) on a CDN.
*   On app launch, check version hash.
*   Download new model in background.
*   Hot-swap the interpreter reference.
