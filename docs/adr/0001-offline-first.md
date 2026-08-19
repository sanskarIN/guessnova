# ADR 0001: Offline-First Local Data

**Status:** Accepted

## Context

GuessNova does not need remote infrastructure to provide its core experience. Accounts and cloud state would add privacy, maintenance, reliability, and security costs.

## Decision

The Python edition stores profiles, settings, statistics, achievements, XP, and leaderboards locally. Gameplay has no mandatory network dependency and no telemetry.

## Consequences

Users control their data and can play offline. Cross-device sync is not automatic. Portable JSON export/import is provided instead.
