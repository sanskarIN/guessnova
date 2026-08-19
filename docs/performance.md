# Performance

GuessNova's runtime hot path is intentionally small: integer comparisons, deterministic random selection, and bounded local JSON updates. There is no gameplay network I/O.

## v1 performance budgets

- CLI help and command dispatch should feel immediate on supported systems.
- A guess should perform no network requests and only constant-time domain work.
- Reverse mode uses binary search and therefore needs logarithmic guesses for a valid range.
- Leaderboard storage is capped/sorted locally and should stay small.
- Persistence is a single local state file written atomically; no background polling is used.

## Measurement

Optimize only after a measured regression. Useful checks include Python timing/profiling around startup, serialization, and unusually large local leaderboard/profile fixtures. Avoid caching that adds invalidation complexity without a demonstrated benefit.

## Memory/data growth

Keep persisted lists bounded where practical and avoid retaining duplicate replay/game objects in memory. If future history features materially increase state size, add explicit limits/migrations and benchmarks before introducing a database.
