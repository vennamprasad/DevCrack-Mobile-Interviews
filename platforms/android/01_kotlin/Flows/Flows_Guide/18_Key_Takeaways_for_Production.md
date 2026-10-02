## **Key Takeaways for Production**

1. **Use StateFlow for UI state**, SharedFlow for events
2. **Debounce user input** to avoid excessive API calls
3. **Implement offline-first** with cache + network patterns
4. **Handle errors gracefully** with `catch` and `retry`
5. **Convert callbacks to flows** using `callbackFlow`
6. **Test flows** with Turbine or manual collection
7. **Use `flatMapLatest`** for cancellable operations (like search)
8. **Combine flows** when multiple data sources needed
9. **Use `stateIn`** to convert cold flows to hot StateFlows
10. **Always cleanup** in `awaitClose` when using `callbackFlow`
