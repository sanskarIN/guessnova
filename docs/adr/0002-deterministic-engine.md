# ADR 0002: Deterministic Core Engine

**Status:** Accepted

## Context

Daily challenges, tests, reproducible bug reports, and replayable challenges require predictable behavior.

## Decision

Random target selection accepts a seed, daily challenge seeds are date-derived, and timed games accept an injected clock.

## Consequences

Core behavior is straightforward to test and reproduce without coupling tests to wall-clock delays or global randomness.
