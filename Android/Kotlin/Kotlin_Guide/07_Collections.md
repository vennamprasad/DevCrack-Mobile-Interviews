## **Collections**

### Q22. What are the different collection types in Kotlin?

**Answer:**

**Immutable Collections (Read-only):**
```kotlin
// List - ordered, allows duplicates
val list = listOf(1, 2, 3, 2)
val emptyList = emptyList<Int>()

// Set - unordered, unique elements
val set = setOf(1, 2, 3, 2) // [1, 2, 3]
val emptySet = emptySet<Int>()

// Map - key-value pairs
val map = mapOf(
    "name" to "John",
    "age" to "25"
)
val emptyMap = emptyMap<String, String>()
```

**Mutable Collections:**
```kotlin
// Mutable List
val mutableList = mutableListOf(1, 2, 3)
mutableList.add(4)
mutableList.remove(2)

// Mutable Set
val mutableSet = mutableSetOf(1, 2, 3)
mutableSet.add(4)

// Mutable Map
val mutableMap = mutableMapOf("a" to 1)
mutableMap["b"] = 2
mutableMap.remove("a")
```

**Specific Implementations:**
```kotlin
// ArrayList
val arrayList = arrayListOf(1, 2, 3)

// LinkedList
val linkedList = LinkedList<Int>()

// HashSet
val hashSet = hashSetOf(1, 2, 3)

// LinkedHashSet (maintains insertion order)
val linkedHashSet = linkedSetOf(1, 2, 3)

// HashMap
val hashMap = hashMapOf("a" to 1)

// LinkedHashMap (maintains insertion order)
val linkedHashMap = linkedMapOf("a" to 1)
```

---

### Q23. What are collection operations in Kotlin?

**Answer:**

**Transformation:**
```kotlin
val numbers = listOf(1, 2, 3, 4, 5)

// map - transform elements
numbers.map { it * 2 } // [2, 4, 6, 8, 10]

// mapIndexed - with index
numbers.mapIndexed { index, value ->
    "$index: $value"
}

// flatMap - flatten nested collections
listOf(listOf(1, 2), listOf(3, 4))
    .flatMap { it } // [1, 2, 3, 4]

// flatten
listOf(listOf(1, 2), listOf(3, 4))
    .flatten() // [1, 2, 3, 4]
```

**Filtering:**
```kotlin
numbers.filter { it % 2 == 0 } // [2, 4]
numbers.filterNot { it % 2 == 0 } // [1, 3, 5]
numbers.filterIndexed { index, value -> index % 2 == 0 }

// Partition - split into two lists
val (evens, odds) = numbers.partition { it % 2 == 0 }
```

**Aggregation:**
```kotlin
numbers.sum() // 15
numbers.average() // 3.0
numbers.max() // 5
numbers.min() // 1
numbers.count() // 5
numbers.count { it % 2 == 0 } // 2

// reduce - accumulate from first element
numbers.reduce { acc, i -> acc + i } // 15

// fold - accumulate with initial value
numbers.fold(10) { acc, i -> acc + i } // 25
```

**Grouping:**
```kotlin
val words = listOf("a", "abc", "ab", "def", "abcd")

// groupBy - create map of groups
words.groupBy { it.length }
// {1=[a], 3=[abc, def], 2=[ab], 4=[abcd]}

// associateBy - create map by key
words.associateBy { it.length }
// {1=a, 3=def, 2=ab, 4=abcd}

// associate - create map with transform
words.associate { it to it.length }
// {a=1, abc=3, ab=2, def=3, abcd=4}
```

**Ordering:**
```kotlin
numbers.sorted() // [1, 2, 3, 4, 5]
numbers.sortedDescending() // [5, 4, 3, 2, 1]
words.sortedBy { it.length }
words.sortedByDescending { it.length }
```

---

### Q24. What are sequences and when to use them?

**Answer:**
Sequences are lazily evaluated collections, processing elements one by one instead of creating intermediate collections.

```kotlin
// List (eager) - creates intermediate collections
val result1 = listOf(1, 2, 3, 4, 5)
    .map { it * 2 } // Creates new list [2, 4, 6, 8, 10]
    .filter { it > 5 } // Creates new list [6, 8, 10]
    .sum() // 24

// Sequence (lazy) - no intermediate collections
val result2 = listOf(1, 2, 3, 4, 5)
    .asSequence()
    .map { it * 2 }
    .filter { it > 5 }
    .sum() // 24

// Order of operations differs
val numbers = listOf(1, 2, 3, 4, 5)

// List: map all, then filter all
numbers
    .map {
        println("map $it")
        it * 2
    }
    .filter {
        println("filter $it")
        it > 5
    }
// Output: map 1, map 2, ..., map 5, filter 2, filter 4, ..., filter 10

// Sequence: process each element completely
numbers
    .asSequence()
    .map {
        println("map $it")
        it * 2
    }
    .filter {
        println("filter $it")
        it > 5
    }
    .toList()
// Output: map 1, filter 2, map 2, filter 4, ...

// Generate infinite sequences
val infiniteNumbers = generateSequence(1) { it + 1 }
val first10 = infiniteNumbers.take(10).toList()

// When to use sequences:
// 1. Large collections
// 2. Multiple operations
// 3. Want lazy evaluation
// 4. Don't need all results immediately
```
