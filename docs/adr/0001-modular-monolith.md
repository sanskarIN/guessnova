# ADR 0001 — Modular monolith with UI-independent domain logic

- Status: Accepted
- Date: 2026-08-19

## Context

GuessNova needs both Rich CLI and Textual TUI interfaces while keeping gameplay deterministic, testable, offline, and easy for contributors to understand.

## Decision

Use one Python package with small modules. Keep domain models, RNG, hints, and game engines independent from Rich/Textual and persistence. Coordinate persistence through application/service modules instead of embedding storage operations in the engine.

## Consequences

- Core behavior can be tested without terminal automation.
- CLI/TUI can evolve independently and a future frontend can reuse rules.
- Deployment stays simple: one local package, no service boundary or remote dependency.
- Contributors must avoid importing presentation code into domain modules.
