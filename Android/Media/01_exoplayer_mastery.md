# 🎬 ExoPlayer Mastery: 50+ Interview Questions
> **Target Audience:** Senior/Staff Android Engineers specializing in Media/Streaming.
> **Scope:** Architecture, Caching, DRM, Customization, and Real-World Debugging.

![ExoPlayer](https://img.shields.io/badge/Android-Media3_ExoPlayer-green?style=for-the-badge&logo=android&logoColor=black)

---

## 📖 Table of Contents
- [Level 1: The Basics (1-10)](#level-1-the-basics)
- [Level 2: Architecture & Internals (11-20)](#level-2-architecture--internals)
- [Level 3: Buffering & Caching (21-30)](#level-3-buffering--caching)
- [Level 4: DRM & Security (31-40)](#level-4-drm--security)
- [Level 5: Customization & Advanced (41-50)](#level-5-customization--advanced)
- [Level 6: Real-World Scenarios (51+)](#level-6-real-world-scenarios)

---

## Level 1: The Basics

### Q1. What is the difference between MediaPlayer and ExoPlayer?
**Answer:**
*   **Customization:** MediaPlayer is a black box. ExoPlayer is extensible (custom Renderers, LoadControl).
*   **Streaming:** ExoPlayer supports DASH, HLS, SmoothStreaming explicitly. MediaPlayer is limited.
*   **Updates:** ExoPlayer is a library (updated via Gradle). MediaPlayer is part of the OS (tied to Android version updates).
*   **DRM:** ExoPlayer has first-class support for Widevine DRM.

### Q2. How do you set up a basic ExoPlayer instance?
**Answer:**
```kotlin
val player = ExoPlayer.Builder(context).build()
player.setMediaItem(MediaItem.fromUri("https://.../video.mp4"))
player.prepare()
player.play()
```

### Q3. What is a `MediaItem`?
**Answer:**
It represents a piece of media to be played. It holds the URI, metadata (title, artist), DRM configuration, and clipping configuration (start/end points).

### Q4. What is the lifecycle of ExoPlayer?
**Answer:**
It must be managed with the Activity/Fragment lifecycle:
*   `initializePlayer()` in `onStart()` (API > 23) or `onResume()` (API <= 23).
*   `releasePlayer()` in `onStop()` (API > 23) or `onPause()` (API <= 23).
*   *Reason*: To release hardware decoders for other apps.

### Q5. What are the 4 main states of `Player.STATE`?
**Answer:**
1.  `STATE_IDLE`: Initial state, nothing loaded.
2.  `STATE_BUFFERING`: Loading data, not ready to play.
3.  `STATE_READY`: Enough data buffered, can play immediately.
4.  `STATE_ENDED`: Playback finished.

### Q6. How do you handle screen rotation during playback?
**Answer:**
To avoid restarting the video (and re-buffering):
1.  **ConfigChanges**: Add `configChanges="orientation|screenSize"` in Manifest (Prevents Activity recreation).
2.  **Separate UI**: Keep the Player instance in a `ViewModel` or `Service` (if playing background audio).

### Q7. Can ExoPlayer play Audio only?
**Answer:**
Yes. It handles audio (MP3, AAC) exactly like video. You just don't attach a `PlayerView`.

### Q8. What is `StyledPlayerView` vs `PlayerView`?
**Answer:**
`StyledPlayerView` (deprecated in Media3, now just `PlayerView` with updated UI) provides modern UI controls (scrubbing, subtitles, settings) out of the box.

### Q9. How do you detect when playback error occurs?
**Answer:**
Add a `Player.Listener`:
```kotlin
player.addListener(object : Player.Listener {
    override fun onPlayerError(error: PlaybackException) {
        // Handle error
    }
})
```

### Q10. What is `playWhenReady`?
**Answer:**
A dictionary boolean. `true` means "User wants to play". Playback only starts if state is `READY` AND `playWhenReady` is `true`.

---

## Level 2: Architecture & Internals

### Q11. Explain the ExoPlayer Threading Model.
**Answer:**
*   **App Thread**: Where you call `player.prepare()`. Usually Main Thread.
*   **Playback Thread**: Internal background thread. Runs the `ExoPlayerImplInternal` loop. Handles downloading, decoding, and rendering. **Critical** (blocking this causes ANRs or stutter).

### Q12. What are the 3 main components injected into ExoPlayer?
**Answer:**
1.  **Renderers**: Draw video to Surface, play audio to Track (e.g., `MediaCodecVideoRenderer`).
2.  **TrackSelector**: Selects which track (Video/Audio/Text) to use based on constraints.
3.  **LoadControl**: Decides *when* to start buffering and *how much* to buffer.

### Q13. What is a `DataSource`?
**Answer:**
Abstracts reading data from a URI.
*   `DefaultHttpDataSource`: Reads from Network (HTTP).
*   `FileDataSource`: Reads from Local Storage.
*   `AssetDataSource`: Reads from APK assets.

### Q14. What is a `MediaSource`?
**Answer:**
Defines *structure* of media.
*   `ProgressiveMediaSource`: Generic files (MP4, MP3).
*   `HlsMediaSource`: HLS streams (.m3u8).
*   `DashMediaSource`: DASH streams (.mpd).
*   `ConcatenatingMediaSource`: Plays multiple sources sequentially (Playlist).

### Q15. How does `TrackSelection` work for Adaptive Streaming?
**Answer:**
`DefaultTrackSelector` picks the "Best" video track supported by the device and network.
*   **AdaptiveTrackSelection**: Monitors bandwidth. If throughput drops, it switches to a lower bitrate track automatically.

### Q16. What is `BandwidthMeter`?
**Answer:**
Estimates the user's available network speed. Used by `AdaptiveTrackSelection` to decide whether to fetch 1080p or 480p chunks.

### Q17. Explain `LoadControl` buffering policies.
**Answer:**
Default values:
*   **Min Buffer**: 50,000ms (50s)
*   **Max Buffer**: 50,000ms
*   **Buffer For Playback**: 2,500ms (Start playing after 2.5s loaded)
*   **Rebuffer**: 5,000ms (If stalled, wait for 5s of data before resuming)

### Q18. What is `RenderersFactory`?
**Answer:**
A factory creating array of Renderers. You can subclass this to inject a **Custom Renderer** (e.g., an FFmpeg audio decoder extension).

### Q19. How does `ConcatenatingMediaSource` handle seamless loops?
**Answer:**
It prepares the *next* video while the *current* video is playing. When current ends, the renderer instantly switches buffers to the next source, achieving gapless playback.

### Q20. What is the structure of HLS in ExoPlayer?
**Answer:**
*   **Master Playlist**: List of variants (Quality levels).
*   **Media Playlist**: List of segments (.ts files).
*   ExoPlayer downloads segments -> Extracts samples -> Feeds to Decoder.

---

## Level 3: Buffering & Caching

### Q21. How do you implement Offline Playback (Download)?
**Answer:**
Use `DownloadManager`.
1.  Define `DownloadRequest` with URI.
2.  `DownloadService` runs in background to fetch chunks.
3.  Store data in `Cache`.
4.  For playback, use `CacheDataSource` which checks disk before network.

### Q22. What is `CacheDataSource`?
**Answer:**
A wrapper around `UpstreamDataSource`.
*   **Read**: Checks `SimpleCache`. If hit -> Return File. If miss -> Call Network -> Write to Cache -> Return Data.

### Q23. How do you pre-cache the first 10 seconds of a video in a Feed (TikTok style)?
**Answer:**
Use `Preloading`.
Create a `CacheDataSource` and call `dataSource.open(DataSpec(uri, 0, 10MB))`.
Do this for the *next* few items in the feed list.

### Q24. How to clear the Cache?
**Answer:**
Call `SimpleCache.release()`. Or use an `Evictor` (e.g., `LeastRecentlyUsedCacheEvictor(100MB)`) to automatically delete old files when full.

### Q25. Can you use OkHttp with ExoPlayer?
**Answer:**
Yes. Use `OkHttpDataSource.Factory`.
**Benefit**: You get HTTP/2 support, Connection Pooling, and can share the same `OkHttpClient` as your API calls (Retrofit).

### Q26. How do you reduce start-up latency (Time To First Frame)?
**Answer:**
1.  **Reduce BufferForPlayback**: Set `LoadControl` to 1000ms or 500ms (Aggressive).
2.  **Pre-warm Decoder**: Initialize the player instance early.
3.  **Use UDP/QUIC**: Via Cronet extension.

### Q27. What is the difference between `CacheEvictor` and `CacheSpan`?
**Answer:**
*   **CacheSpan**: A contiguous block of cached bytes for a specific file.
*   **Evictor**: The logic deciding *which* Span to delete when disk is full (LRU usually).

### Q28. How to handle "Seek" efficiently?
**Answer:**
Video frames are I-frames (Keyframes) and P-frames (Diffs).
*   **Exact Seek**: Decodes from previous I-frame to exact time (Slow).
*   **Closest Sync**: Jumps to nearest I-frame (Fast). ExoPlayer uses `SeekParameters.CLOSEST_SYNC` by default.

### Q29. Why does existing buffer get discarded when switching qualities?
**Answer:**
If switching from 480p to 1080p, the codecs might need re-initialization (if resolution changes). Also, preserving buffer continuity across different resolutions is complex.

### Q30. What happens if I set `MaxBuffer` too high?
**Answer:**
`OutOfMemoryError`. Video buffers are stored in memory (Allocations). Storing 5 minutes of 4K Video in RAM will crash the app.

---

## Level 4: DRM & Security

### Q31. Which DRM schemes does ExoPlayer support?
**Answer:**
*   **Widevine** (Android primary)
*   **PlayReady** (TVs)
*   **ClearKey** (No security, mostly for testing)

### Q32. How do you configure a DRM protected MediaItem?
**Answer:**
```kotlin
val drmConfig = MediaItem.DrmConfiguration.Builder(C.WIDEVINE_UUID)
    .setLicenseUri("https://license.server/...")
    .build()
val item = MediaItem.Builder().setUri(uri).setDrmConfiguration(drmConfig).build()
```

### Q33. What is an Offline License?
**Answer:**
Allows playing DRM content without internet (Airplane mode).
*   **Process**: Request `OfflineLicenseHelper.downloadLicense()`. Store the `keySetId` securely.
*   **Playback**: Create player with `setDrmKeySetId(cachedKeySetId)`.

### Q34. Can you take screenshots of DRM content?
**Answer:**
**No**. The Surface is "Secure". The hardware composer blacks out the legacy screenshot API. `SurfaceView.setSecure(true)` prevents it.

### Q35. What is `L3` vs `L1` Security Level?
**Answer:**
*   **L1**: Cryptography and Decoding happen in Trusted Execution Environment (Hardware). High security. Required for HD/4K by Netflix etc.
*   **L3**: Cryptography in Software. Easier to crack. Often restricted to SD (480p) streams.

### Q36. How to handle DRM Error `CryptoException`?
**Answer:**
Usually means the device was rotated/changed output, or keys expired.
Retry playback implies re-requesting keys.
If error persists, fallback to SD content.

### Q37. What is Key Rotation?
**Answer:**
Changing decryption keys periodically *during* the stream (e.g., live sports). ExoPlayer listens for `onKeysExpired` events and fetches new keys automatically.

### Q38. How to prevent proxy sniffing of Video content?
**Answer:**
*   **SSL Pinning**: On the License Server URL.
*   **Token Authentication**: Signed URLs for the video segments (CDN tokens).

### Q39. What is `MediaDrmCallback`?
**Answer:**
The interface responsible for making the network POST request to the License Server. You implement this to add custom Headers (Authorization Tokens).

### Q40. Why does DRM playback fail on Emulators?
**Answer:**
Emulators often lack the Hardware Trusted Execution Environment (TEE) required for Widevine L1. They serve L3 at best, or fail completely.

---

## Level 5: Customization & Advanced

### Q41. How to create a Custom UI?
**Answer:**
Don't use `PlayerView`'s default controls.
1.  Create a standard Layout (`RelativeLayout` with Play/Pause standard ImageViews).
2.  Bind clicks to `player.play()`, `player.pause()`.
3.  Observe `player.addListener()` to update UI state (show buffering spinner).

### Q42. How to integrate Ads (IMA)?
**Answer:**
Use the `exo-player-ima` extension.
Wrap your `MediaSource` in an `AdsMediaSource`. It handles pausing content, playing VAST/VPAID ad, and resuming content.

### Q43. What is `Tunneling` mode?
**Answer:**
Syncs audio and video directly in the hardware layer (Audio DSP and Video Decoder), bypassing the Android Framework / Dalvik VM.
**Pros**: Saves battery, better AV sync on TVs.
**Cons**: Complex to support on all devices.

### Q44. How to support FLAC or FFmpeg codecs?
**Answer:**
Depend on `extension-ffmpeg` or `extension-flac`.
You must initialize `DefaultRenderersFactory` passing `EXTENSION_RENDERER_MODE_ON`.

### Q45. How to synchronize lyrics with audio?
**Answer:**
*   **Side-loaded**: Add a subtitle track (`MediaItem.Subtitle`).
*   **Event Handling**: Listen to `onCues(List<Cue>)`.
*   **Custom**: If JSON lyrics, parse loop and match `player.currentPosition` with timestamps.

### Q46. Implementing "Picture in Picture" (PiP)?
**Answer:**
1.  Check `packageManager.hasSystemFeature(FEATURE_PICTURE_IN_PICTURE)`.
2.  Call `enterPictureInPictureMode()` in Activity.
3.  **Critical**: In `onUserLeaveHint()`, do NOT pause the player if entering PiP.

### Q47. How to play 360-degree VR Video?
**Answer:**
Use `SphericalGLSurfaceView`. ExoPlayer supports VR projection formats (Equirectangular).

### Q48. What is `DownloadService` foreground requirement?
**Answer:**
Downloads must run in a Foreground Service (Notification required) so the OS doesn't kill the process in doze mode.

### Q49. How to get metadata (ID3 tags) from stream?
**Answer:**
`player.addListener( object: Player.Listener { onMetadata(metadata: Metadata) } )`.
Useful for HLS streams carrying "Program Date Time" or custom ad markers.

### Q50. How to handle Audio Focus (e.g., Phone Call comes in)?
**Answer:**
ExoPlayer handles it automatically if you set:
```kotlin
val attr = AudioAttributes.Builder()
    .setUsage(C.USAGE_MEDIA)
    .setContentType(C.CONTENT_TYPE_MOVIE)
    .build()
player.setAudioAttributes(attr, true) // handleAudioFocus = true
```

---

## Level 6: Real-World Scenarios

### Q51. Video plays fine, but Audio is missing on some devices.
**Debug:** Codec issue. The audio might be AC3/EAC3 (Dolby) which the device doesn't hardware decode.
**Fix:** Include the FFmpeg software decoder extension.

### Q52. "IllegalStateException: Player is accessed on the wrong thread".
**Debug:** You called `player.play()` from a background thread.
**Fix:** Wrap call in `Handler(Looper.getMainLooper()).post { ... }`.

### Q53. App crashes with OOM (Out Of Memory) when scrolling a Feed of videos.
**Debug:** You are creating a `new ExoPlayer()` for every Release row. Each player allocates buffers.
**Fix:**
1.  **Recycling**: Only keep 1 or 2 Player instances globally. Attach/Detach them to Views as user scrolls (`PlayerView.setPlayer(null)`).
2.  **Release**: Call `player.release()` instantly when holder is recycled.

### Q54. HLS Stream stalls repeatedly at 99%.
**Debug:** A discontinuity in the HLS segments (Sequence number mismatch) or CDN failure for the specific segment.
**Fix:** Check `onPlayerError`. If behind live window, call `player.seekToDefaultPosition()`.

### Q55. User hears audio glitch when looping a short video.
**Debug:** `GAPLESS` support depends on device decoder.
**Fix:** Use `Transcoding` to combine loop iterations into one longer file, or use `ConcatenatingMediaSource` with the same file added multiple times.
