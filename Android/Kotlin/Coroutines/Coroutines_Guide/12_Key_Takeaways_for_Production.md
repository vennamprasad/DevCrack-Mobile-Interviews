## **Key Takeaways for Production**

1. **Always use lifecycle-aware scopes** (`viewModelScope`, `lifecycleScope`)
2. **Use `async` for parallel independent tasks**, sequential for dependent ones
3. **Handle errors with try-catch or CoroutineExceptionHandler**
4. **Use `Mutex` or `AtomicInteger` for thread safety**
5. **Implement retry logic for network calls**
6. **Coordinate network + DB for offline-first apps**
7. **Respect cancellation with `ensureActive()` or `yield()`**
8. **Test with TestDispatcher and `runTest`**
9. **Batch operations and limit concurrency for performance**
10. **Never block Dispatchers.Main - use withContext(Dispatchers.IO)**
