# Architecture

GuessNova is a local-first Python modular monolith. It deliberately avoids network services and database complexity that do not benefit a terminal number-guessing game.

## Major modules

- `domain.py` — shared enums and dataclasses for difficulties, feedback, summaries, and player statistics.
- `engine.py` — deterministic core guessing engine and reverse binary-search guesser with no UI dependency.
- `rng.py`, `daily.py`, `hints.py` — deterministic randomness, daily challenge selection, and smart hint rules.
- `achievements.py` — XP, streak, and milestone progression.
- `profile.py`, `settings.py`, `themes.py` — local player identity/preferences and presentation choices.
- `storage.py` — versioned local state, migration, and atomic file replacement.
- `leaderboard.py`, `import_export.py`, `replay.py` — portable data/replay and local ranking adapters.
- `service.py` — application orchestration connecting game summaries to profile and leaderboard persistence.
- `cli.py`, `tui.py` — Rich CLI and Textual UI presentation layers.
- `security.py` — bounded integer, profile-name sanitization, and permitted-path helpers.

## Dependency direction

Core gameplay does not depend on Rich or Textual. Presentation may import application/domain modules, and persistence receives serializable domain/profile data. This separation keeps seeded gameplay deterministic and testable while allowing additional frontends without duplicating business rules.

## Persistence model

`Storage` writes a single versioned `state.json` in the platform-specific application-data directory. Writes use a temporary file plus `fsync` and atomic replacement. Migration rejects saves from unsupported future schemas instead of silently overwriting them.

## Security/privacy boundaries

GuessNova has no runtime authentication, remote API, telemetry, payment, or required network permissions. Untrusted values are parsed/validated before use; replay codes include integrity checking; exports have an explicit format/version marker.

See `docs/adr/0001-modular-monolith.md` and `docs/adr/0002-versioned-json-storage.md` for recorded decisions.
