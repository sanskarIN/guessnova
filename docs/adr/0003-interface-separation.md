# ADR 0003: Separate Domain from Terminal Interfaces

**Status:** Accepted

## Decision

Game rules live outside Rich and Textual code. CLI and TUI are adapters over the same engine.

## Consequences

The project can add future interfaces without rewriting gameplay rules, while engine tests remain fast and independent of terminal rendering.
