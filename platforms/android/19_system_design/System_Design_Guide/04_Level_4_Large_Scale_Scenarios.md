## Level 4: Large Scale Scenarios

### Q6. Design "Instagram Stories" (Heavy Media, Transient).

**Challenges**: Pre-loading, Sequential playback, Bandwidth limits.
**Design**:

1.  **Pre-fetching**: While watching Story A, download Story B (1st chunk).
2.  **Cache Eviction**: Aggressive. Stories expire in 24h. Delete immediately.
3.  **Upload**: Background Service. Resumable Uploads (Chunked).

### Q7. How to handle 10,000 updates per second (Stock Ticker)?

**Answer**:

- ** throttling/Debouncing**: Don't render every tick. Frame-limit updates to 30fps.
- **Diffing**: Only re-bind changed fields (DiffUtil).
- **Binary Protocol**: Use Protobuf or binary WS frames instead of JSON.
