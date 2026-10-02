# 🏎️ Performance Tuning
> **Targeted for Senior iOS Developers**
> **Note:** Rendering, Battery, and Network.

![Tuning](https://img.shields.io/badge/Performance-Tuning-green?style=for-the-badge&logo=apple&logoColor=white)

---

## 📖 Table of Contents
- [1. High Refresh Rate (ProMotion)](#1-promotion)
- [2. View Optimizations](#2-view-optimizations)
- [3. Battery Life](#3-battery-life)

---

### Q1. Optimizing for 120Hz (ProMotion)?

**Answer:**
You have 8ms per frame (instead of 16ms).
- **Main Thread**: Keep it nearly idle. Any blocking work causes dropped frames (stutter).
- **Commit Transactions**: Group layout changes.

### Q2. Drawing Optimizations?

**Answer:**
- **Opaque**: Set `.isOpaque = true`. System ignores layers behind it (no blending).
- **Corner Radius**: High cost (off-screen render). Use `UIBezierPath` clipping or a pre-rounded image if performance suffers.
- **Shadows**: Always provide a `shadowPath`. Without it, Core Animation renders the view content to determine shadow shape (expensive).

### Q3. Reducing Battery Drain?

**Answer:**
- **Network**: Batch requests. Use gzip. Avoid frequent "polling".
- **Location**: Use "Significant Change" location service instead of GPS when backgrounded.
- **Timers**: Avoid high-frequency timers.

### Q4. MetricKit?

**Answer:**
Framework to receive on-device power and performance metrics collected by the OS.
You receive a daily report containing Launch Time, Hang Rate, Memory usage, and Energy drain (averaged across your user base).
