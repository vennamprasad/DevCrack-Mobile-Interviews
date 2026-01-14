# 📺 AdTech & Media Playback for Mobile Engineers
> **Target Audience:** Staff Engineers at Streaming (Netflix/Spotify) or AdTech companies.
> **Focus:** Video standards, Player internals (ExoPlayer/AVPlayer), and Ad Monetization.

![Streaming](https://img.shields.io/badge/Tech-Streaming_&_Ads-red?style=for-the-badge&logo=youtube&logoColor=white)

---

## 📖 Table of Contents
- [1. AdTech Standards (VAST vs VPAID)](#1-adtech-standards-vast-vs-vpaid)
- [2. Monetization: Waterfall vs Header Bidding](#2-monetization-waterfall-vs-header-bidding)
- [3. Media Playback Internals](#3-media-playback-internals)
- [4. DRM (Digital Rights Management)](#4-drm-digital-rights-management)
- [5. Real-World Scenarios](#5-real-world-scenarios)

---

## 1. AdTech Standards (VAST vs VPAID)

How do mobile apps know *which* ad to play and *how* to track it?

| Standard | Full Form | Description | Mobile Support |
| :--- | :--- | :--- | :--- |
| **VAST** | Video Ad Serving Template | **XML Response**. Tells the player: "Play video X at URL Y". Simple, robust. | ✅ Excellent (Preferred) |
| **VPAID** | Video Player-Ad Interface Definition | **Executable Code (JS/HTML5)**. Allows interactivity (e.g., "Click to play game"). | ⚠️ Risky (Performance heavy, security risks) |
| **OMID** | Open Measurement Interface Definition | **Viewability**. 3rd party verification (IAS/Moat) to prove ad was actually seen by user. | ✅ Mandatory for premium inventory |

### Example VAST XML (Simplified)
```xml
<VAST version="3.0">
  <Ad>
    <InLine>
      <Creatives>
        <Creative>
          <Linear>
            <Duration>00:00:15</Duration>
            <MediaFiles>
              <MediaFile type="video/mp4">https://cdn.ads.com/video.mp4</MediaFile>
            </MediaFiles>
          </Linear>
        </Creative>
      </Creatives>
    </InLine>
  </Ad>
</VAST>
```

---

## 2. Monetization: Waterfall vs Header Bidding

### A. The Waterfall (Traditional)
1.  App asks Ad Network A (High CPM).
2.  If A has no ad (No Fill) -> Ask Network B.
3.  If B has no ad -> Ask Network C.
*   **Problem:** High latency (wait for timeouts). Lower revenue (C might have paid more than B, but B was asked first).

### B. Header Bidding / Unified Auction (Modern)
1.  App asks Networks A, B, and C **simultaneously** (Pre-bidding).
2.  All return their bids.
3.  App picks the highest bidder.
*   **Result:** Higher revenue, potentially higher CPU usage (parallel requests).

---

## 3. Media Playback Internals

### HLS (Apple) vs DASH (Google)
Both use **Adaptive Bitrate Streaming (ABR)**. They split video into small chunks (segments) of 2-6 seconds.

*   **Manifest File (.m3u8 / .mpd)**: Index file describing available qualities (360p, 720p, 1080p).
*   **ABR Logic**: Player checks bandwidth every few seconds.
    *   *High Bandwidth*: Download 1080p chunk.
    *   *Bandwidth Drop*: Switch next chunk to 480p.

### Android: ExoPlayer (Media3)
*   **Thread Model**:
    *   `App Thread`: UI events.
    *   `Playback Thread`: Decoding & Rendering (Critical 100ms deadlines).
*   **LoadControl**: Decides buffering strategy (Start playback when 2ms buffered, rebuffer if <500ms).

### iOS: AVPlayer
*   **KVO (Key Value Observing)**: Heavily relies on KVO to track `status`, `timeControlStatus`.
*   **AVAssetResourceLoader**: Intercepting requests (custom caching or DRM).

---

## 4. DRM (Digital Rights Management)

Preventing piracy. The video is encrypted (AES-128). The player needs a **License Key** to decrypt frames.

*   **Google (Android)**: Widevine Modular.
*   **Apple (iOS)**: FairPlay Streaming.

**The Flow:**
1.  App downloads Manifest.
2.  Manifest says: `Content-Protection: Widevine`.
3.  Player sends "License Request" blob to Backend DRM Server.
4.  Server checks auth -> Returns "License Key".
5.  Player decrypts video frames in secure hardware (TEE).

---

## 5. Real-World Scenarios

### Q1: User complains ads are causing the main video to crash/freeze. How do you debug?
**Answer:**
*   **Root Cause**: Often VPAID ads running heavy JS on the main thread or unoptimized WebViews.
*   **Fix**:
    1.  Force **VAST-only** tags where possible (remove interactivity).
    2.  Implement a strict **Timeout** (e.g., 5s). If Ad doesn't start, kill it and fallback to content.
    3.  Check if Ad Player and Content Player are fighting for decoder resources (release one before starting other).

### Q2: Audio and Video are out of sync (AV Desync).
**Answer:**
*   **Timestamps**: Check Presentation Time Stamps (PTS) in the container (MP4/TS).
*   **Drift**: Does it happen over time? (Sample rate mismatch: 44.1kHz vs 48kHz).
*   **Bluetooth**: Latency compensation failure on BT headphones.

### Q3: How do you reduce "Re-buffering" events?
**Answer:**
*   **Start-up Customization**: Increase initial buffer constraint (start only after 5s buffered instead of 2s) -> Slower start, but smoother playback.
*   **CDN Switching**: Logic to detect slow CDN segment download and switch to backup CDN mid-stream.
*   **Ladder Optimization**: Don't offer 4K bitrate to a user on a 3G network (remove top tier from manifest).
