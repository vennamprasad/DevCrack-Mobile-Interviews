# 💊 RxJava Interview Guide
> **Targeted for Senior Android Developer / Team Lead Roles**
> **Note:** While Flow is preferred for Kotlin projects, Legacy Codebases still heavily rely on RxJava2/3. Use this guide to master Reactive Programming.

![RxJava](https://img.shields.io/badge/RxJava-B7178C?style=for-the-badge&logo=reactivex&logoColor=white)
![Reactive](https://img.shields.io/badge/Pattern-Reactive-blue?style=for-the-badge)
![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)

---

## 📖 Table of Contents
- [1. Core Concepts](#-1-what-is-rxjava)
- [2. Observables & Flowables](#-5-what-is-the-difference-between-observable-and-flowable)
- [3. Operators (Map vs FlatMap)](#-11-what-is-the-difference-between-map-and-flatmap)
- [4. Schedulers & Threading](#-16-what-is-the-difference-between-observeon-and-subscribeon)
- [5. Subjects](#-12-what-is-a-subject-in-rxjava)
- [6. Error Handling](#-15-how-do-you-handle-errors-in-rxjava)

---

## ✅ Overview

**RxJava** (Reactive Extensions for Java) is a library for composing asynchronous and event-based programs by using observable sequences. It extends the Observer pattern to support sequences of data and events.

*   **RxAndroid:** Adds Android-specific bindings (e.g., `AndroidSchedulers.mainThread()`).
*   **RxKotlin:** Adds Kotlin extension functions for more idiomatic usage.
*   **RxJava 3:** The current standard version.

---

## 🧩 Interview Questions (Q&A)

### 1. Fundamental Types
*   **`Observable`**: A stream of data that emits 0 to n items and then completes or errors. No backpressure.
*   **`Flowable`**: Same as Observable but involves **Backpressure** support (for massive amounts of data).
*   **`Single`**: Emits exactly one item or an error (e.g., Network Call).
*   **`Maybe`**: Emits one item, no item, or an error (e.g., Database Query usually optional).
*   **`Completable`**: Emits no items, just success or error (e.g., Delete operation).

### 2. Backpressure
**Backpressure** occurs when the publisher emits items faster than the consumer can process them. `Flowable` handles this using strategies:
*   `BUFFER`: Buffers items in memory (can cause OOM).
*   `DROP`: Drops most recent items if downstream busy.
*   `LATEST`: Keeps only the latest item.

### 3. `map` vs `flatMap` vs `concatMap`
*   **`map`**: Transforms item T -> U. (One-to-One).
*   **`flatMap`**: Transforms T -> Observable<U>. Returns a merged stream. Emitted items can be interleaved (Order NOT guaranteed).
*   **`concatMap`**: Same as `flatMap` but waits for the previous Observable to finish before starting the next. (Order IS guaranteed).
*   **`switchMap`**: Unsubscribes from the previous Observable when a new item arrives. Great for Search bars (ignore old query if user types new one).

### 4. Schedulers (`subscribeOn` vs `observeOn`)
*   **`subscribeOn()`**: Affects the thread where the upstream source works (Network request). Can only be called once.
*   **`observeOn()`**: Affects the thread where downstream operators/subscribers work (UI updates). Can be called multiple times to switch threads mid-stream.

```kotlin
api.getUser()
    .subscribeOn(Schedulers.io()) // Fetch on IO
    .map { user -> user.copy(name = "Prefix " + user.name) } // Compute on IO
    .observeOn(AndroidSchedulers.mainThread()) // Switch to Main
    .subscribe { showOnUi(it) } // Run on Main
```

### 5. Types of Subjects
Subjects act as both Observer and Observable.
*   **`PublishSubject`**: Emits only subsequent items to subscribers. (Hot).
*   **`BehaviorSubject`**: Emits the most recent item (and subsequent) to new subscribers. Great for State.
*   **`ReplaySubject`**: Replays all previous items to new subscribers.
*   **`AsyncSubject`**: Emits only the LAST item after onComplete.

### 6. Cold vs Hot Observables?
*   **Cold**: Starts emitting items only when subscribed to. Each subscriber gets its own stream (e.g., Database Query, Network Call).
*   **Hot**: Emits items regardless of subscribers. Subscribers share the stream (e.g., Timer, UI Events, Subject).

### 7. How to avoid Memory Leaks?
Using `CompositeDisposable`.
```kotlin
val disposables = CompositeDisposable()

fun onStart() {
    disposables.add(
        observable.subscribe()
    )
}

fun onDestroy() {
    disposables.clear() // Unsubscribes everything
}
```

---
