# 🏆 Idiomatic Python DSA & Coding Interview Cheatsheet

> **The ultimate cheat sheet for acing Data Structures & Algorithms coding interviews in Python. Master the standard library modules that save 10+ lines of code per problem.**

---

## ⚡ 1. Standard Library Superpowers at a Glance

| Task / Data Structure | Idiomatic Python Tool | Time Complexity |
|:---|:---|:---|
| **Queue / Double-Ended Queue** | `collections.deque` | $O(1)$ append / pop on both ends |
| **Min Heap / Priority Queue** | `heapq.heappush`, `heapq.heappop` | $O(\log N)$ push / pop, $O(N)$ heapify |
| **Max Heap** | Store negative values `(-val, val)` | $O(\log N)$ |
| **Frequency Counting** | `collections.Counter` | $O(N)$ count, $O(K \log N)$ `most_common(k)` |
| **Auto-Initializing Maps** | `collections.defaultdict(list)` | $O(1)$ lookup / insert |
| **Binary Search (Sorted Array)** | `bisect.bisect_left`, `bisect.bisect_right`| $O(\log N)$ search |
| **Memoization / Caching** | `@functools.lru_cache(None)` | $O(1)$ cache hit |

---

## 🛠️ 2. Essential Code Snippets for Top Interview Patterns

### 1. BFS & Sliding Window with `collections.deque`
```python
from collections import deque

# BFS Traversal
queue = deque([(root, 0)])  # (node, depth)
while queue:
    curr, depth = queue.popleft()  # O(1) pop from front!
    for neighbor in curr.children:
        queue.append((neighbor, depth + 1))
```

### 2. Top-K Elements / Dijkstra with `heapq`
```python
import heapq

# 1. K Largest Elements
nums = [3, 2, 1, 5, 6, 4]
k = 2
k_largest = heapq.nlargest(k, nums)  # [6, 5]

# 2. Min-Heap Priority Queue for Dijkstra
heap = [(0, start_node)]  # (cost, node)
while heap:
    cost, u = heapq.heappop(heap)
    # Process edges...
    heapq.heappush(heap, (cost + weight, v))
```

### 3. Binary Search with `bisect`
```python
import bisect

arr = [1, 3, 3, 3, 7, 9]

# Find first position >= 3
idx = bisect.bisect_left(arr, 3)   # Index: 1

# Find first position > 3
idx = bisect.bisect_right(arr, 3)  # Index: 4
```

### 4. Dynamic Programming with `@lru_cache`
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
```

### 5. Custom Sorting with `key` & Lambda / `functools.cmp_to_key`
```python
# Sort tuples by second element ascending, then first descending
points = [(1, 2), (3, 2), (2, 1), (4, 3)]
points.sort(key=lambda p: (p[1], -p[0]))
# Result: [(2, 1), (3, 2), (1, 2), (4, 3)]
```

---

## 🎯 3. Complexity Quick Reference

* **List append:** $O(1)$ amortized
* **List pop(0):** ❌ $O(N)$ — Always use `deque.popleft()` ($O(1)$)
* **Dict / Set lookup:** $O(1)$ average
* **String concatenation in loop:** ❌ $O(N^2)$ — Use `''.join(list_of_strings)` ($O(N)$)
* **Sorting (`list.sort()` / `sorted()`):** $O(N \log N)$ (Timsort)
