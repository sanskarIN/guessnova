# Architecture

Canonical detailed architecture: [`architecture.md`](architecture.md).

GuessNova uses a layered, offline-first Python modular monolith. It deliberately avoids a network service or database layer that does not benefit a local terminal number-guessing game.

## Domain

`domain.py`, `engine.py`, `hints.py`, `rng.py`, and `daily.py` contain deterministic game behavior. They have no dependency on Rich, Textual, filesystem paths, or console input.

## Application services

`service.py` coordinates completed games with profile statistics, achievements, history, and leaderboard persistence.

## Persistence and recovery

`storage.py`, `profile.py`, `settings.py`, `leaderboard.py`, and `import_export.py` own local data structures, schema versioning, migration, bounded I/O, backup validation, and atomic writes.

`backup_inspection.py` is read-only backup preflight. `diagnostics.py` owns local state inspection and safe backup-before-write repair. `doctor_protocol.py` owns the separately versioned machine-report/exit-code contract.

## Interfaces

`cli.py` is the Rich gameplay/data CLI. `doctor_cli.py` is the diagnostics/recovery command. `entrypoint.py` routes `guessnova doctor` while preserving existing game commands.

The Textual interface is intentionally split:

- `tui.py` — stable six-pane v1.4 workspace and core event/focus orchestration;
- `tui_workspace.py` — Textual-independent workspace queries plus validated challenge configuration/parsing;
- `tui_challenge.py` — localized target-free challenge presentation;
- `tui_challenge_widgets.py` — v1.5 challenge controls and mode-aware field state;
- `tui_challenge_app.py` — additive v1.5 integration over the stable workspace and the shipped `guessnova-tui` app.

See [`adr/0005-additive-textual-challenge-layer.md`](adr/0005-additive-textual-challenge-layer.md).

## Dependency direction

```text
Rich CLI / Doctor / Textual presentation
              |
       application helpers/services
              |
        domain + local adapters
```

The domain never imports terminal UI modules.

The v1.5 challenge widgets do not duplicate game rules or persistence. They pass presentation-friendly values through `parse_workspace_challenge(...)`; completed games still persist through `GameService` and existing `Storage` boundaries.

## Challenge configuration transaction

A configured TUI round is installed only after mode/difficulty/seed/date parsing and replacement-game construction succeed. Invalid configuration leaves the active round intact.

Seeded Classic/Timed/Streak and resolved-date Daily configurations can reconstruct deterministic resets. Reverse remains on its dedicated interaction path.

Challenge configuration is in-memory application state, not a new save format.

## State and compatibility

The canonical state schema is `2`. Schema 0/1 migrate forward and future schemas are rejected. Independent compatibility identifiers remain:

```text
state schema = 2
backup wrapper = 2
legacy backup wrapper = 1
replay format = 1
Doctor report = 1
```

v1.5 does not change these formats.

## Determinism

Normal play uses system randomness. Tests and reproducible challenges can inject a seed. Daily challenges derive a stable integer seed from an ISO date and a versioned namespace. Tests use explicit targets/seeds/dates rather than relying on live wall-clock challenge targets.

## Privacy boundary

No runtime account, analytics, telemetry, cloud sync, remote leaderboard, or application network service is required. Challenge configuration and recovery operations remain local.
