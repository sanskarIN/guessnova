# Architecture

GuessNova is a local-first Python modular monolith. It deliberately avoids network services and database complexity that do not benefit a terminal number-guessing game.

## Major modules

- `domain.py` — shared enums and dataclasses for difficulties, feedback, summaries, and player statistics.
- `engine.py` — deterministic core guessing engine and reverse binary-search guesser with no UI dependency.
- `rng.py`, `daily.py`, `hints.py` — deterministic randomness, daily challenge selection, and smart hint rules.
- `achievements.py` — XP, streak, and milestone progression.
- `profile.py`, `settings.py`, `themes.py` — local player identity/preferences and presentation choices.
- `storage.py` — versioned local state, schema migration, normalization, and atomic file replacement.
- `leaderboard.py` — validated local winning-result ranking data.
- `import_export.py` — independent backup-wrapper versioning, payload-schema provenance, SHA-256 integrity validation, atomic export, and legacy backup import compatibility.
- `diagnostics.py` — read-only local state inspection plus backup-before-write normalization repair.
- `replay.py` — portable replay-code encoding/validation with replay-version integrity rules separate from state/backup versioning.
- `service.py` — application orchestration connecting game summaries to profile and leaderboard persistence.
- `cli.py`, `tui.py` — Rich CLI and Textual gameplay/presentation layers.
- `doctor_cli.py` — dedicated local diagnostics/repair entry point with human-readable, compact, and JSON output.
- `security.py` — bounded integer, profile-name sanitization, and permitted-path helpers.

## Dependency direction

Core gameplay does not depend on Rich, Textual, filesystem storage, backup wrappers, or diagnostics. Presentation and diagnostic commands may import application/local-adapter modules. Persistence receives serializable domain/profile data. This keeps seeded gameplay deterministic and directly testable while allowing additional frontends and maintenance tools without duplicating game rules.

```text
Rich CLI   Textual TUI   Doctor CLI
    \          |          /
       application/local orchestration
          /               \
    game domain        local adapters
                       /    |      \
                  storage backup diagnostics
```

## Persistence model

`Storage` writes one normalized versioned `state.json` in the platform-specific application-data directory. Schema 2 makes `deleted_profiles` a canonical top-level container. Schema 0 and schema 1 migrate forward deterministically; future schemas are rejected rather than silently downgraded.

Writes use a temporary file in the destination directory, flush and `fsync`, then atomic replacement where supported.

## Backup boundary

Backup format versioning is intentionally independent from state schema versioning. Backup wrapper v2 records the embedded payload schema and a canonical SHA-256 payload digest. Import validates wrapper version, payload schema, wrapper/payload schema agreement, integrity metadata, and payload type before current storage performs any migration/normalization.

Legacy GuessNova backup wrapper v1 is retained as an explicit compatibility path. See `docs/adr/0004-separate-backup-and-state-versions.md`.

## Diagnostics and repair boundary

`diagnostics.py` inspects the on-disk JSON without mutating it. It reports migration/normalization requirements and aggregate local-state counts. Repair is intentionally conservative:

1. unreadable/non-object/unsupported state is refused;
2. repairable state is normalized in memory;
3. the original payload is exported to an integrity-protected backup;
4. only then is normalized state written through `Storage`.

The doctor command never uploads state or requires network access.

## Security/privacy boundaries

GuessNova has no runtime authentication, remote API, telemetry, payment, cloud sync, or required network permissions. Untrusted values are parsed/validated before use. Replay and backup integrity mechanisms detect corruption but are not encryption, authentication, or digital signatures.

See `docs/adr/0001-modular-monolith.md`, `docs/adr/0002-versioned-json-storage.md`, and `docs/adr/0004-separate-backup-and-state-versions.md` for recorded decisions.
