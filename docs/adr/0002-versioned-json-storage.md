# ADR 0002 — Versioned JSON with atomic replacement

- Status: Accepted
- Date: 2026-08-19

## Context

GuessNova needs portable local profiles, settings, achievements, and a small leaderboard without requiring a database or network service.

## Decision

Store one versioned JSON state document in the application-data directory. Persist changes through a temporary file, flush/fsync, and atomic replacement. Migrate known older schemas in memory and reject unsupported newer schemas.

## Consequences

- Users can inspect, back up, and export data easily.
- No database dependency or migration toolchain is required at the current scale.
- Atomic replacement protects against many partial-write failures.
- Schema versioning must be updated deliberately for incompatible future changes.
- If future query/history scale justifies SQLite, it should be introduced behind the storage boundary with explicit migration tests.
