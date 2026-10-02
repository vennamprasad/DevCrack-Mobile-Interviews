# 🌊 Kotlin Asynchronous Flows & Channels

> **Mastering reactive mobile architecture: Cold Streams, StateFlow, SharedFlow, Channels, Debounce Search, Reactive Pagination, and Lifecycle Safety.**

---

## 📚 Curriculum Catalog

| Chapter | Topic & Focus |
| :--- | :--- |
| **[01. Flow Fundamentals: Cold vs Hot](./01_flow_fundamentals_cold_vs_hot.md)** | Cold streams vs Hot streams, flow builders (`flow {}`, `channelFlow`), context preservation, and `repeatOnLifecycle`. |
| **[02. StateFlow vs SharedFlow vs Channels](./02_stateflow_vs_sharedflow_vs_channel.md)** | Choosing the right reactive primitive: State observation vs event buses vs point-to-point queues. |
| **[03. Common & Advanced Operators](./03_common_and_advanced_operators.md)** | `map`, `filter`, `transform`, `flatMapConcat`, `flatMapMerge`, `flatMapLatest`, and custom intermediate operators. |
| **[04. Real-Time Search with Debouncing](./04_real_time_search_debouncing.md)** | Search input debouncing, `distinctUntilChanged`, and auto-cancelling stale queries with `flatMapLatest`. |
| **[05. Reactive Pagination](./05_reactive_pagination.md)** | Infinite scrolling with Flow, cursor-based pagination, and Android Jetpack `PagingSource` integration. |
| **[06. Offline-First Cache & Network](./06_offline_first_cache_and_network.md)** | Emitting cached database state first, refreshing from network, and streaming database updates. |
| **[07. Combining Multiple Flows](./07_combining_multiple_flows.md)** | Merging UI states with `combine`, `zip`, and `merge` across multiple independent data sources. |
| **[08. Error Handling & Retry Logic](./08_error_handling_and_retry.md)** | Exception transparency, `catch` operator, and exponential backoff retries with `retryWhen`. |
| **[09. Callback to Flow Conversions](./09_callback_to_flow_conversions.md)** | Wrapping legacy callback-based SDKs (Location, Sensor, Firebase) with `callbackFlow` and `awaitClose`. |
| **[10. Unit Testing Flows](./10_testing_flows.md)** | Using Cash App's **Turbine** library, testing `StateFlow`, asserting emissions, and virtual time execution. |
| **[11. Production Patterns & Interview Scenarios](./11_production_patterns_and_interviews.md)** | Staff-level interview questions on Kotlin Flows, common memory leak pitfalls, and thread-safety invariants. |

---

[⬅️ Back to Kotlin Master Hub](../README.md)
