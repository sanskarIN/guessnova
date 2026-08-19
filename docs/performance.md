# Performance

GuessNova's runtime hot path is intentionally small: integer comparisons, deterministic random selection, and bounded local JSON updates. There is no gameplay, Doctor, or backup-verification network I/O.

## Runtime performance budgets

- CLI help and command dispatch should feel immediate on supported systems.
- The top-level dispatcher should only inspect enough arguments to decide whether to route `doctor`; it must not duplicate game initialization or state loading.
- A guess should perform no network requests and only constant-time domain work aside from small local persistence on completion.
- Reverse mode uses binary search and therefore needs logarithmic guesses for a valid range.
- Leaderboard/history/profile trash remain bounded locally.
- Persistence uses one local state file written atomically; no background polling is used.
- Doctor state diagnosis uses one bounded state read plus normalization.
- Backup validation/inspection uses one bounded source read; it must not validate one copy and re-read a second copy merely for metadata.
- Backup preflight may normalize the complete bounded state in memory because its purpose is to prove current importability before restore.

## Explicit data-size limits

Current code defines separate byte budgets:

- `MAX_STATE_BYTES` — local state input and normalized state output ceiling.
- `MAX_EXPORT_BYTES` — backup-wrapper input/output ceiling.

Readers request at most the configured ceiling plus one byte. The extra byte is only used to identify oversized input before decoding/parsing the complete file.

`MAX_EXPORT_BYTES` must remain larger than `MAX_STATE_BYTES` because a repairable state may need to be wrapped with backup metadata before a normalization write.

These limits are resource-safety boundaries, not targets for normal file size. Typical GuessNova state should remain far below them because history/profile trash and other retained collections are bounded.

## Measurement

Optimize only after a measured regression. Useful checks include Python timing/profiling around:

- startup/dispatcher routing;
- state normalization;
- bounded state serialization;
- backup canonical digest generation;
- backup preflight normalization;
- unusually large but valid profile/history/leaderboard fixtures.

Avoid caching that adds invalidation complexity or bypasses current validation without a demonstrated benefit.

## Memory/data growth

Keep persisted collections bounded where practical and avoid retaining duplicate replay/game objects in memory. Backup and state validation necessarily hold bounded JSON bytes plus decoded objects temporarily; their hard byte ceilings prevent unbounded input growth.

If future features materially increase valid state size, first measure representative files and review both state and backup capacity invariants. Do not raise limits blindly or introduce a database merely to avoid understanding local growth.
