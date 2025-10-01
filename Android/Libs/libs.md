

### Retrofit — https://square.github.io/retrofit/
A type-safe HTTP client for Android and Java that maps REST APIs to interfaces and supports converters (Gson/Moshi).  
Built on OkHttp; simplifies request/response handling, async calls, and error parsing.
Interview Q: How do you handle different response types and implement custom converters or interceptors in Retrofit?

---

### OkHttp — https://square.github.io/okhttp/
A fast, efficient HTTP & HTTP/2 client providing connection pooling, interceptors, and caching.  
Often used as the network layer underlying Retrofit; great for low-level request customization and mocking.
Interview Q: Explain how interceptors differ from network interceptors and when to use each.

---

### Glide — https://bumptech.github.io/glide/
An image loading and caching library focused on smooth scrolling and resource efficiency.  
Supports GIFs, thumbnails, transformations, and integrates with lifecycle to manage requests.
Interview Q: How do you implement custom transformations and handle large image memory usage with Glide?

---

### Coil — https://coil-kt.github.io/coil/
An image loading library for Kotlin backed by Kotlin Coroutines and modern APIs; lightweight and lifecycle-aware.  
Optimized for Kotlin-first projects and Compose support; easy custom image loaders and decoders.
Interview Q: How does Coil differ from Glide/Picasso, and how do you create a custom ImageLoader?

---

### Picasso — https://square.github.io/picasso/
A simple image downloading and caching library with a fluent API for loading images into views.  
Easy setup for basic image needs; handles image transformation, placeholders, and memory caching.
Interview Q: How do you handle complex transformations and cancel in-flight requests in Picasso?

---

### Dagger / Hilt — https://dagger.dev/  /  https://dagger.dev/hilt/
Dagger: a compile-time dependency injection framework for Java/Kotlin; Hilt: opinionated DI built on Dagger for Android.  
Provides scoped components, reduces boilerplate, and improves testability when used correctly.
Interview Q: Compare Hilt and manual Dagger setup; how do you scope dependencies to Activity or ViewModel lifecycles?

---

### Koin — https://insert-koin.io/
A lightweight, Kotlin-first dependency injection library using DSL modules and runtime injection.  
Simpler to set up than Dagger for small-to-medium projects; good developer ergonomics and easy testing.
Interview Q: How do you declare modules and handle different environments (debug/release) in Koin?

---

### Kotlinx.coroutines — https://github.com/Kotlin/kotlinx.coroutines
Official Kotlin coroutines library for structured concurrency, dispatchers, and async primitives.  
Enables easier async code, cancellation, and integration with lifecycle and Flow for reactive streams.
Interview Q: Explain structured concurrency, cancellation, and Dispatcher choices for IO vs Main workloads.

---

### Room — https://developer.android.com/jetpack/androidx/releases/room
An SQLite object-mapping library that provides compile-time checked SQL queries and LiveData/Flow support.  
Manages migrations, type converters, and simplifies local persistence with DAO interfaces.
Interview Q: How do you handle migrations, multithreading, and observe changes via Flow or LiveData in Room?

---

### Moshi / Gson — https://github.com/square/moshi  /  https://github.com/google/gson
JSON libraries for Kotlin/Java; Moshi has Kotlin adapters and better null-safety, Gson is widely used and flexible.  
Both provide converters for Retrofit; choose Moshi for Kotlin data classes and strict parsing.
Interview Q: How do you write custom adapters/serializers and handle polymorphic JSON with Moshi/Gson?

---

### Timber — https://github.com/JakeWharton/timber
A lightweight logging utility that wraps Android Log with tree-based configuration and easier disabling in prod.  
Supports custom trees for crash reporting and structured logs without log tag boilerplate.
Interview Q: How do you implement a custom Timber Tree for remote crash logging and avoid performance overhead in release builds?

---

### LeakCanary — https://square.github.io/leakcanary/
A memory leak detection library that automatically detects retained objects and provides leak traces.  
Integrates into debug builds to help identify Activity/Fragment/context leaks early in development.
Interview Q: How do you interpret a LeakCanary leak trace and fix common causes of Android memory leaks?

---

### Lottie — https://airbnb.io/lottie/
A library to render After Effects animations as vector graphics natively on Android.  
Reduces APK size vs frame animations and supports runtime animation control and composition.
Interview Q: How do you optimize Lottie animations for performance and control animation progress programmatically?

---

### Mockito / MockK — https://site.mockito.org/  /  https://mockk.io/
Popular testing libraries for creating mocks and stubs; MockK is Kotlin-first and supports coroutines and object mocking.  
Used in unit tests to isolate dependencies and verify interactions with concise syntax.
Interview Q: How do you mock final classes, suspend functions, and verify coroutine behavior with Mockito vs MockK?

---

### Espresso — https://developer.android.com/training/testing/espresso
UI testing framework for Android that synchronizes with the UI thread and provides view matchers and actions.  
Ideal for end-to-end interaction tests; integrates with Test Orchestrator and UI Automator when needed.
Interview Q: How do you write reliable Espresso tests for RecyclerView and handle asynchronous network calls during UI tests?


### ExoPlayer — https://exoplayer.dev/
A highly customizable media playback library for Android supporting DASH/HLS/SmoothStreaming, DRM (Widevine), adaptive bitrate, audio focus, and efficient buffering/caching. Extensible renderers and track selection for advanced media apps.  
Interview Q: How do you implement adaptive streaming, DRM playback, and custom renderers or caching strategies with ExoPlayer?

---

### Ktor — https://ktor.io/
A Kotlin-native asynchronous HTTP client and server framework built on coroutines; supports multiple engines (CIO, OkHttp), websockets, plugins, and multiplatform targets. Good for building lightweight backend services or HTTP clients in Kotlin Multiplatform projects.  
Interview Q: How do you configure different engines, implement websockets, and share client/server code across platforms with Ktor?

---

### kotlinx.serialization — https://github.com/Kotlin/kotlinx.serialization
A Kotlin-first multiplatform serialization library with JSON, ProtoBuf, CBOR formats; supports generated serializers, polymorphism, and custom serializers for complex types. Integrates well with coroutines and multiplatform codebases for efficient parsing/encoding.  
Interview Q: How do you write custom and polymorphic serializers, handle versioned payloads, and integrate serialization with networking layers?

---

### SQLDelight — https://github.com/cashapp/sqldelight
A library that generates typesafe Kotlin APIs from SQL schema and queries, enabling compile-time checked SQL and multiplatform database access. Supports coroutines/Flow, migrations, and native/ad-hoc drivers for Android, iOS, and JVM.  
Interview Q: How do you model relationships and transactions in SQLDelight, manage migrations, and stream query results via Flow?

---

### WorkManager — https://developer.android.com/topic/libraries/architecture/workmanager
Jetpack library for deferrable, guaranteed background work with constraint-based scheduling, one-off/periodic tasks, and chaining/unique work policies. Handles retries, backoff, and integrates with foreground services when needed for long-running tasks.  
Interview Q: How do you schedule unique or periodic work, handle constraints and retries, and test WorkManager jobs reliably?

---

### Accompanist — https://google.github.io/accompanist/
A collection of Jetpack Compose libraries providing utilities not yet in Compose core (insets, pager, navigation animations, Coil/Image support, system UI helpers). Accelerates Compose development with battle-tested, Compose-first utilities.  
Interview Q: When should you use Accompanist components vs Compose core, and how do you implement paged content, insets handling, or animated navigation transitions?

