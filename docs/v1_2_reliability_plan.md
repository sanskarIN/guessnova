# GuessNova v1.2 Reliability Plan

This phase is limited to reliability, portability, migration safety, backup integrity, diagnostics, and release evidence. It does not change the core guessing rules or add network/account requirements.

## Goals

- Formalize schema version 2 around recoverable profile trash and migration fixtures.
- Preserve schema-1 saves through deterministic forward migration.
- Strengthen backup files with an explicit wrapper version and SHA-256 payload integrity metadata while retaining legacy export compatibility.
- Add a local diagnostics command that validates normalized state and reports schema/profile/history/leaderboard/trash health without sending data anywhere.
- Expand migration/import/export tests and smoke coverage.
- Keep release metadata, docs, CI, and package manifests synchronized.

## Compatibility rules

- Existing schema-0 and schema-1 saves must remain loadable.
- Existing version-1 GuessNova export wrappers must remain importable.
- Future save/export versions must be rejected safely.
- Stable replay codes and gameplay semantics remain unchanged.
- No telemetry, cloud sync, account system, or runtime network call may be introduced.
