# 📚 Popular Android Third-Party Libraries

> **Essential open-source networking, image loading, dependency injection, and utility libraries standard across Android production codebases.**

![Libraries](https://img.shields.io/badge/Android-Libraries-orange?style=for-the-badge&logo=android)
![OpenSource](https://img.shields.io/badge/Ecosystem-Open_Source-blue?style=for-the-badge)

---

## 📖 Chapter Index

- **[Android Libraries Interview Guide](./01_android_libraries_guide.md)**
  - **Networking:**
    - **[Retrofit](https://square.github.io/retrofit/):** REST client interface mapping, OkHttp converters (Moshi/Gson/KotlinX Serialization), custom CallAdapters.
    - **[OkHttp](https://square.github.io/okhttp/):** HTTP/2 client, connection pooling, cache control headers, app vs network interceptors, certificate pinning.
  - **Image Loading:**
    - **[Coil](https://coil-kt.github.io/coil/):** Modern Kotlin-first image loader built natively for Coroutines and Jetpack Compose.
    - **[Glide](https://bumptech.github.io/glide/):** High-performance image loading with bitmap recycling and memory disk caching.
  - **JSON Serialization:**
    - **KotlinX Serialization:** Reflection-free compiler plugin serialization.
    - **Moshi:** Modern JVM JSON library with codegen and streaming support.
  - **Logging & Debugging:**
    - **Timber:** Extensible logging utility preventing debug logs leaking to release builds.
    - **LeakCanary:** Automatic memory leak detection in debug builds.
    - **Flipper / Chucker:** On-device and desktop network inspection tools.

---

## 💡 Library Selection Decision Matrix

| Task | Recommended Modern Choice | Legacy / Alternative | Trade-off |
| :--- | :--- | :--- | :--- |
| **Networking** | Retrofit + OkHttp | Ktor Client | Ktor is multiplatform (KMP), while Retrofit is Android/JVM optimized. |
| **JSON Parsing** | KotlinX Serialization | Moshi / Gson | KotlinX Serialization requires zero reflection and supports KMP. Gson is slow and lacks null-safety. |
| **Image Loading** | Coil | Glide / Picasso | Coil is 100% Kotlin & Compose native, lightweight (~2k methods), and uses OkHttp directly. |
| **Memory Leaks** | LeakCanary | Android Studio Profiler | LeakCanary runs automatically during QA/debug; profilers require manual heap dump analysis. |
