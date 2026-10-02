# 🎬 Android Media & Audio/Video Playback

> **Staff-level guide to Android Media3, ExoPlayer, adaptive video streaming (HLS, DASH), DRM encryption, caching, and custom renderers.**

![Media3](https://img.shields.io/badge/Framework-AndroidX_Media3-3DDC84?style=for-the-badge&logo=android)
![ExoPlayer](https://img.shields.io/badge/Player-ExoPlayer-green?style=for-the-badge)
![Streaming](https://img.shields.io/badge/Protocols-HLS_%2F_DASH_%2F_SS-blue?style=for-the-badge)

---

## 📖 Chapter Index

- **[ExoPlayer Mastery: 50+ Senior Interview Questions](./01_exoplayer_mastery.md)**
  - **Level 1: The Basics (1–10):** MediaSource types (`ProgressiveMediaSource`, `HlsMediaSource`, `DashMediaSource`), PlayerView, and Media3 unification.
  - **Level 2: Architecture & Internals (11–20):** How renderers (`MediaCodecVideoRenderer`, `MediaCodecAudioRenderer`), TrackSelector, and LoadControl collaborate on playback threads.
  - **Level 3: Buffering & Caching (21–30):** `SimpleCache`, `CacheDataSourceFactory`, prefetching next video in short-form video feeds (TikTok/Reels), and eviction policies (Least-Recently-Used).
  - **Level 4: DRM & Security (31–40):** Widevine Modular DRM, license acquisition callbacks, hardware-backed security levels (L1 vs L3), and HDCP enforcement.
  - **Level 5: Customization & Advanced (41–50):** Custom audio processors, seamless looping, surface switching without decoder re-initialization, and Picture-in-Picture (PiP).
  - **Level 6: Real-World Scenarios (51+):** Preventing ANRs during player release, managing audio focus across calls, and battery drain diagnostics.

---

## 🏗️ ExoPlayer Architectural Pipeline

```
  ┌──────────────────────────────────────────────┐
  │           MediaSource (HLS / DASH)           │
  │     Extracts chunks & manifest data           │
  └──────────────────────┬───────────────────────┘
                         │
  ┌──────────────────────▼───────────────────────┐
  │                 LoadControl                   │
  │ Controls buffer size & when to fetch data    │
  └──────────────────────┬───────────────────────┘
                         │
  ┌──────────────────────▼───────────────────────┐
  │                TrackSelector                 │
  │ Selects optimal audio / video / text bitrate │
  └──────────────────────┬───────────────────────┘
                         │
  ┌──────────────────────▼───────────────────────┐
  │          Renderers (Audio / Video)           │
  │ Feeds decoded frames to Surface & AudioTrack │
  └──────────────────────────────────────────────┘
```
