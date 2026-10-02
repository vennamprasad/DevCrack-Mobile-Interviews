# 💊 RxJava & Reactive Extensions for Android

> **Complete guide to Reactive Programming in Android using RxJava 2/3: Observables, Flowables, Backpressure, Operators, Schedulers, and migration to Kotlin Flow.**

![RxJava](https://img.shields.io/badge/Reactive-RxJava_2_%2F_3-B7178C?style=for-the-badge&logo=reactivex)
![Android](https://img.shields.io/badge/Platform-RxAndroid-3DDC84?style=for-the-badge&logo=android)
![Threading](https://img.shields.io/badge/Threading-Schedulers-blue?style=for-the-badge)

---

## 📖 Chapter Index

- **[RxJava Interview Guide](./rx.md)**
  - **1. Core Concepts:** Reactive streams specification, Observer pattern, Push vs Pull streams, Cold vs Hot observables, and `CompositeDisposable` lifecycle management.
  - **2. Observables vs Flowables:** `Observable`, `Flowable` (backpressure strategies: `DROP`, `LATEST`, `BUFFER`, `ERROR`), `Single`, `Maybe`, and `Completable`.
  - **3. Operators:** Transforming (`map`, `flatMap`, `concatMap`, `switchMap`), Filtering (`filter`, `distinctUntilChanged`, `debounce`), and Combining (`zip`, `combineLatest`, `merge`).
  - **4. Schedulers & Threading:** `subscribeOn` (where upstream work runs, evaluated once) vs `observeOn` (where downstream observers receive events, switchable anytime), `Schedulers.io()`, `Schedulers.computation()`, and `AndroidSchedulers.mainThread()`.
  - **5. Subjects & Relays:** `PublishSubject`, `BehaviorSubject`, `ReplaySubject`, `AsyncSubject`, and RxRelay for non-terminal error-safe event buses.
  - **6. Error Handling:** `onErrorReturn`, `onErrorResumeNext`, `retry`, and exponential backoff retry.

---

## 🔄 RxJava to Kotlin Flow Translation Guide

| RxJava Construct | Kotlin Flow Equivalent | Notes |
| :--- | :--- | :--- |
| `Observable<T>` | `Flow<T>` | Flow is cold by default and integrates natively with coroutine cancellation. |
| `Single<T>` | `suspend fun (): T` | Direct coroutine suspend function replaces Single cleanly without reactive overhead. |
| `Completable` | `suspend fun (): Unit` | Suspend function returning Unit. |
| `BehaviorSubject<T>` | `MutableStateFlow<T>` | Thread-safe, conflated, state-holding observable. |
| `PublishSubject<T>` | `MutableSharedFlow<T>` | Broadcast event bus without conflation or initial value. |
| `subscribeOn(Schedulers.io())` | `flowOn(Dispatchers.IO)` | Modifies the CoroutineContext of upstream flow producers. |
| `observeOn(AndroidSchedulers.mainThread())` | `flow.collect { }` in `Main` | Flow operators run in the collector's scope unless shifted with `flowOn`. |
| `CompositeDisposable.clear()` | Scope cancellation | `viewModelScope.cancel()` automatically cancels all active collection jobs. |
