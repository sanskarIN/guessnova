# Performance

GuessNova's runtime hot path is intentionally small: integer comparisons, deterministic random selection, bounded local JSON updates, and lightweight Textual presentation state. There is no gameplay, Challenge Setup, Doctor, or backup-verification network I/O.

## Runtime performance budgets

- CLI help and command dispatch should feel immediate on supported systems.
- The top-level dispatcher should only inspect enough arguments to decide whether to route `doctor`; it must not duplicate game initialization or state loading.
- A guess should perform no network requests and only constant-time domain work aside from small local persistence on completion.
- Reverse mode uses binary search and therefore needs logarithmic guesses for a valid range.
- Challenge mode/difficulty/seed/date validation is constant-size form parsing and must not scan persisted history/leaderboard data.
- Starting a configured challenge should construct one replacement `GuessGame` only after validation succeeds.
- Configured reset should reconstruct one game from the stored validated configuration; it must not search history or reread state merely to reproduce a seeded/Daily target.
- Target-free challenge status should format only small mode/difficulty/seed/date metadata and must not trigger persistence or network work.
- Mode-aware seed/date enablement is local widget state only.
- Leaderboard/history/profile trash remain bounded locally.
- TUI History/Leaderboard presentation is bounded rather than rendering unbounded persisted collections.
- Persistence uses one local state file written atomically; no background polling is used.
- Doctor state diagnosis uses one bounded state read plus normalization.
- Backup validation/inspection uses one bounded source read; it must not validate one copy and re-read a second copy merely for metadata.
- Backup preflight may normalize the complete bounded state in memory because its purpose is to prove current importability before restore.

## v1.5 Challenge Setup

Challenge Setup intentionally does not introduce:

- a database query layer;
- a cache;
- a background worker;
- a network request;
- persisted form state;
- repeated state-file reads on selector changes.

The reusable configuration model validates a handful of scalar values and constructs a game through the existing engine/Daily helpers.

A deterministic reset reuses the validated configuration metadata rather than recalculating identity from mutable widget text or querying saved sessions. This keeps reset work comparable to constructing a normal seeded game.

Invalid configuration is rejected before the current game is replaced. Besides correctness, this avoids constructing/persisting compensating state after a partially applied form update.

## Explicit data-size limits

Current code defines separate byte budgets:

- `MAX_STATE_BYTES` — local state input and normalized state output ceiling.
- `MAX_EXPORT_BYTES` — backup-wrapper input/output ceiling.

Readers request at most the configured ceiling plus one byte. The extra byte is only used to identify oversized input before decoding/parsing the complete file.

`MAX_EXPORT_BYTES` must remain larger than `MAX_STATE_BYTES` because a repairable state may need to be wrapped with backup metadata before a normalization write.

These limits are resource-safety boundaries, not targets for normal file size. Typical GuessNova state should remain far below them because history/profile trash and other retained collections are bounded.

v1.5 challenge form/configuration state is not serialized into `state.json`, so it does not increase the persistent-state size budget.

## Measurement

Optimize only after a measured regression. Useful checks include Python timing/profiling around:

- startup/dispatcher routing;
- Textual startup/mount time;
- configured challenge start/reset;
- state normalization;
- bounded state serialization;
- backup canonical digest generation;
- backup preflight normalization;
- unusually large but valid profile/history/leaderboard fixtures.

Avoid caching that adds invalidation complexity or bypasses current validation without a demonstrated benefit.

## Memory/data growth

Keep persisted collections bounded where practical and avoid retaining duplicate replay/game objects in memory. The active v1.5 challenge configuration contains only small mode/difficulty/seed/date metadata; it does not retain a second hidden target or copy persisted workspace state.

Backup and state validation necessarily hold bounded JSON bytes plus decoded objects temporarily; their hard byte ceilings prevent unbounded input growth.

If future features materially increase valid state size, first measure representative files and review both state and backup capacity invariants. Do not raise limits blindly or introduce a database merely to avoid understanding local growth.
