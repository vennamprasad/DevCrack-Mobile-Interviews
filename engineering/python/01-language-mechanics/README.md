# 🟢 Phase 1: Python Language Mechanics & Deep Dives

> **Master CPython's execution model, memory allocators, async event loops, and type-safe systems.**

---

## 📑 Guides in this Module

1. **[Memory Management, Cyclic GC & The GIL](./memory-gc-and-gil.md)**
   * Reference counting internals, tri-generational cycle detection, and the Global Interpreter Lock.
   * Free-threaded Python 3.13 (PEP 703) architecture.
2. **[Asyncio, Event Loops & Concurrency](./asyncio-and-concurrency.md)**
   * `async` / `await` syntax, event loops, tasks, and comparing `asyncio` vs `threading` vs `multiprocessing`.
3. **[Decorators, Generators & Context Managers](./decorators-and-generators.md)**
   * Metaprogramming with `@wraps`, memory-efficient generator streaming, and `contextlib.asynccontextmanager`.
4. **[Type Hints & Pydantic v2](./type-hints-and-pydantic.md)**
   * Strict typing with `typing`, `TypeVar`, `Generic`, and runtime validation with Pydantic v2.
