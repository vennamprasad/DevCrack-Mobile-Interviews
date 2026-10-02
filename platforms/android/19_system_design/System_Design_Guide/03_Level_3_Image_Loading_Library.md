## Level 3: Image Loading Library

### Q5. Design "Glide" or "Picasso" from scratch.

**Requirements**: Async loading, Caching (Memory/Disk), Recycling.
**Components**:

1.  **Request Manager**: Handles lifecycle (Pause requests when Activity stops).
2.  **Engine**:
    - `MemoryCache` (LRU Cache): Check first.
    - `DiskCache` (DiskLruCache): Check second.
    - `NetworkFetcher`: Download Stream.
3.  **Decoder**: Stream -> Bitmap. Downsampling (Resize 4K image to ImageView size).
4.  **Transformation**: Crop, RoundedCorners.
5.  **Target**: Render to ImageView.

**Critical optimization**:

- **InBitmap**: Re-use bitmap memory.
- **Pause on Scroll**: Don't load while flinging list.
