# 🖼 LRU Cache (Least Recently Used)
> **Use Case:** Image Caching (Glide/Picasso), Network Caching.
> **Core Data Structure:** HashMap + Doubly Linked List.

![Cache](https://img.shields.io/badge/Topic-Caching-blue?style=for-the-badge)
![DS](https://img.shields.io/badge/DS-LinkedList-green?style=for-the-badge)

---

## 📖 Table of Contents
- [1. The Problem](#1-the-problem)
- [2. Visualizing LRU Cache](#2-visualizing-lru-cache)
- [3. Implementation (Kotlin/Swift)](#3-implementation)
- [4. Real-World Mobile Example](#4-real-world-mobile-example)

---

## 1. The Problem

We have strict memory limits on mobile (e.g., 200MB heap).
If we load 1000 images, the app crashes (`OutOfMemoryError`).
We need a cache that holds the **Most Recently Used** items and evicts the **Least Recently Used** when full.

---

## 2. Visualizing LRU Cache

We use a **HashMap** for O(1) lookup.
We use a **Doubly Linked List** to track order.
- **Head:** Most Recently Used.
- **Tail:** Least Recently Used (Candidate for eviction).

```mermaid
graph LR
    subgraph HashMap
    Key1[Key: "profile.png"] --> Node1
    Key2[Key: "banner.jpg"] --> Node2
    Key3[Key: "icon.svg"] --> Node3
    end

    subgraph "Doubly Linked List (Order)"
    direction LR
    Node1[Head: profile.png] <--> Node2[banner.jpg] <--> Node3[Tail: icon.svg]
    end

    style Node1 fill:#d4f1f9,stroke:#333
    style Node3 fill:#ffcccc,stroke:#333,stroke-dasharray: 5 5
```

**Operations:**
1.  **Get(Key):** If exists, move that Node to **Head**.
2.  **Put(Key, Value):**
    *   If new, add to **Head**.
    *   If full, remove **Tail**, then add to **Head**.

---

## 3. Implementation

### Kotlin (Using `LinkedHashMap`)
Java/Kotlin's `LinkedHashMap` has a hidden constructor `accessOrder = true` that turns it into an LRU.

```kotlin
class ImageCache(private val capacity: Int) {
    // accessOrder = true enables LRU mode (Move accessed items to end)
    private val cache = object : LinkedHashMap<String, Bitmap>(0, 0.75f, true) {
        override fun removeEldestEntry(eldest: MutableMap.MutableEntry<String, Bitmap>?): Boolean {
            return size > capacity // Evict if size exceeds capacity
        }
    }

    fun get(url: String): Bitmap? = cache[url]
    
    fun put(url: String, bitmap: Bitmap) {
        cache[url] = bitmap
    }
}
```

### Custom Implementation (The "Interview" Way)
Sometimes they ask you to build it from scratch without `LinkedHashMap`.

```kotlin
class Node(var key: Int, var value: Int) {
    var prev: Node? = null
    var next: Node? = null
}

class LRUCache(val capacity: Int) {
    val map = HashMap<Int, Node>()
    val head = Node(0, 0) // Dummy Head
    val tail = Node(0, 0) // Dummy Tail

    init {
        head.next = tail
        tail.prev = head
    }
    
    // O(1)
    fun get(key: Int): Int {
        if (!map.containsKey(key)) return -1
        val node = map[key]!!
        remove(node) // Unlink
        insert(node) // Move to front
        return node.value
    }
    
    // O(1)
    fun put(key: Int, value: Int) {
        if (map.containsKey(key)) remove(map[key]!!)
        if (map.size == capacity) remove(tail.prev!!) // Evict LRU
        
        insert(Node(key, value))
    }
    
    private fun remove(node: Node) {
        map.remove(node.key)
        node.prev?.next = node.next
        node.next?.prev = node.prev
    }
    
    private fun insert(node: Node) {
        map[node.key] = node
        val headNext = head.next
        head.next = node
        node.prev = head
        node.next = headNext
        headNext?.prev = node
    }
}
```

---

## 4. Real-World Mobile Example

**Scenario:** You are building an Instagram Clone feeds.
1.  User scrolls down. Images download and go into Cache.
2.  User scrolls back up. Images shouldn't reload.
3.  **Low Memory Warning:** Android OS sends `onTrimMemory(TRIM_MEMORY_RUNNING_CRITICAL)`.
    *   **Action:** You call `cache.evictAll()` or reduce size by half immediately.
