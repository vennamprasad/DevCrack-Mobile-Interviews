# 🕵️ Charles Proxy Debugging
> **Targeted for Mobile Developers**
> **Note:** Inspecting, throttling, and mocking network traffic.

![Charles](https://img.shields.io/badge/Tool-Charles_Proxy-6a329f?style=for-the-badge)

---

## 📖 Table of Contents
- [1. Setup & SSL Proxying](#setup--ssl-proxying)
- [2. Breakpoints & Mocking](#breakpoints--mocking)
- [3. Network Throttling](#network-throttling)
- [4. Alternatives](#alternatives)

---

### Q1. What is Charles Proxy?

**Answer:**
Charles is a web debugging proxy that sits between your mobile device and the internet. It enables you to:
- **Inspect** HTTP/HTTPS traffic (headers, JSON bodies).
- **Edit** requests/responses on the fly.
- **Throttle** network speeds (simulate 3G, Edge).
- **Mock** API errors or data.

### Q2. How to setup SSL Proxying?

**Answer:**
By default, HTTPS traffic is encrypted. To read it:
1.  **PC/Mac**: Help > SSL Proxying > Install Charles Root Certificate.
2.  **Mobile**:
    - Set PC's IP as Proxy in Wifi Settings (Port 8888).
    - Browse to `chls.pro/ssl`.
    - Download and install the certificate.
    - **iOS**: Enable "Full Trust" for the root certificate in Settings.
    - **Android (Nougat+)**: Add a `network_security_config.xml` to your app allowing user certificates in debug builds.

### Q3. How to Mock a 500 Error?

**Answer:**
Use the **Rewrite** or **Breakpoints** feature:
- **Breakpoint**: Right-click a request endpoint -> Enable Breakpoints. When the request triggers, Charles pauses execution. You can edit the Response code to `500` and Body to `{"error": "Crash"}` then Execute.
- **Map Local**: Map a remote URL (e.g., `/api/user`) to a local JSON file on your computer.

### Q4. Simulating Slow Network?

**Answer:**
**Proxy > Throttle Settings**.
Allows simulating:
- 3G / 4G speeds.
- High Latency.
- Packet Loss.
Crucial for testing loading states, timeouts, and retry logic.