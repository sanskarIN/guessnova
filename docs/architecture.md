# Architecture

GuessNova is a local-first Python modular monolith. It deliberately avoids network services and database complexity that do not benefit a terminal number-guessing game.

## Major modules

- `domain.py` — shared enums and dataclasses for difficulties, feedback, summaries, and player statistics.
- `engine.py` — deterministic core guessing engine and reverse binary-search guesser with no UI dependency.
- `rng.py`, `daily.py`, `hints.py` — deterministic randomness, daily challenge selection, and smart hint rules.
- `achievements.py` — XP, streak, and milestone progression.
- `profile.py`, `settings.py`, `themes.py` — local player identity/preferences and presentation choices.
- `storage.py` — versioned local state, schema migration, normalization, bounded reads/writes, and atomic file replacement.
- `leaderboard.py` — validated local winning-result ranking data.
- `import_export.py` — independent backup-wrapper versioning, bounded single-read validation, payload-schema provenance, SHA-256 integrity validation, atomic export, and legacy backup compatibility.
- `backup_inspection.py` — read-only backup preflight that proves current state normalization/importability and reports normalized structural metadata.
- `diagnostics.py` — read-only local state inspection plus backup-before-write normalization repair using the same bounded state reader as normal storage.
- `doctor_protocol.py` — stable Doctor machine report version and exit-code constants.
- `replay.py` — portable replay-code encoding/validation with replay-version integrity rules separate from state/backup/Doctor versioning.
- `service.py` — application orchestration connecting game summaries to profile and leaderboard persistence.
- `cli.py` — established Rich gameplay/profile/history/settings/data CLI.
- `doctor_cli.py` — reusable local diagnostics, backup verification, and repair command implementation.
- `entrypoint.py` — compatibility-preserving top-level dispatcher that routes `doctor` to Doctor and all existing game commands to `cli.py`.
- `tui_workspace.py` — Textual-independent workspace helpers for challenge construction, local snapshots, profile statistics, history/leaderboard selection, and settings persistence.
- `tui.py` — Textual six-pane workspace and event/focus orchestration over existing application/local-adapter boundaries.
- `security.py` — bounded integer, profile-name sanitization, and permitted-path helpers.

## Dependency direction

Core gameplay does not depend on Rich, Textual, filesystem storage, backup wrappers, diagnostics, or the dispatcher. The dispatcher does not implement game or recovery business logic; it only selects the established command family.

The Textual workspace deliberately keeps reusable data/query/configuration logic outside widget code:

```text
                         entrypoint.py
                        /             \
                    cli.py        doctor_cli.py
                      |             /       \
                      |      diagnostics   backup_inspection
                      |          |              |
                   service     storage      import_export
                      |          \             /
                      +------ game/domain -----+

                             tui.py
                               |
                    +----------+-----------+
                    |                      |
             tui_workspace.py          GameService
              /   |    |   \              |
        storage history leaderboard    game/domain
```

This keeps seeded gameplay deterministic and directly testable while allowing maintenance/recovery tooling and richer interactive presentation without duplicating game rules or state semantics.

## Textual workspace boundary

GuessNova 1.4 expands `guessnova-tui` into six panes:

- Play;
- Profiles;
- History;
- Leaderboard;
- Settings;
- Recovery.

`src/guessnova/tui_workspace.py` has no Textual import. It provides reusable helpers for:

- deterministic seeded/non-reverse challenge construction;
- daily challenge construction from an ISO date;
- workspace snapshots;
- derived profile statistics;
- newest-first history selection;
- ranked leaderboard filtering;
- validated settings persistence.

`src/guessnova/tui.py` owns presentation concerns:

- widget composition;
- focus movement;
- keyboard shortcuts;
- user-entered filter/form values;
- data-table refresh;
- active-profile transition orchestration;
- high-contrast screen class;
- displaying diagnostics and backup-preflight results.

The TUI does not create a second state store. Profile/history/leaderboard/settings changes continue through `Storage`, completed games continue through `GameService`, diagnostics continue through `diagnose`, and backup verification continues through `inspect_backup`.

## Active-profile/game ownership boundary

An in-progress `GuessGame` belongs to the current active profile for persistence purposes. When the workspace changes the active profile by use/create/restore or by deleting the active profile, the unfinished round is reset before further play.

This prevents a user from making guesses under one profile and then accidentally recording the completed round under another profile.

Profile rename does not require a reset because identity continuity is preserved by `Storage.rename_profile(...)` together with matching leaderboard updates.

## TUI Recovery boundary

The Recovery pane is intentionally read-only:

- `diagnose(storage)` reports local state health/counts;
- `inspect_backup(path)` verifies a selected backup without importing it.

The pane does not call `repair(...)` and does not write a verified backup into application state. Repair remains explicit through Doctor so confirmation and backup-before-write guarantees remain centralized.

## TUI localization boundary

The Textual workspace selects its display locale when mounted. Activating a profile with a different saved locale updates the settings value and runtime preferences, but the current mounted presentation does not partially relabel itself. Full locale presentation changes occur on the next TUI launch.

This avoids a mixed-language UI where dynamically refreshed text changes language while already-created tab/button labels do not.

Stable mode/difficulty/schema/backup/replay/Doctor identifiers remain untranslated machine values.

## TUI accessibility boundary

The workspace adds global Ctrl shortcuts for panes and quit/reset while leaving plain `Q`/`R` as non-priority bindings. Text-editing widgets can therefore consume ordinary characters instead of losing them to application shortcuts.

High-contrast preference is represented by a screen CSS class with stronger borders and focus outlines. Switches use `animate=False`. Reduced-motion remains a saved presentation preference and no fake delays/decorative workspace animation are introduced.

## Command-dispatch boundary

The installed `guessnova` script and `python -m guessnova` both call `entrypoint.main`.

The dispatcher recognizes `doctor` after supported leading presentation flags and delegates the remaining arguments to the same Doctor implementation used by `guessnova-doctor`. Existing non-Doctor arguments are delegated unchanged to the established Rich game CLI.

This design preserves the standalone Doctor compatibility surface while making recovery discoverable as:

```bash
guessnova doctor
```

Root help appends a Doctor discovery hint instead of maintaining a second duplicate copy of the large game parser tree.

## Persistence model

`Storage` writes one normalized versioned `state.json` in the platform-specific application-data directory. Schema 2 makes `deleted_profiles` a canonical top-level container. Schema 0 and schema 1 migrate forward deterministically; future schemas are rejected rather than silently downgraded.

State input is bounded by `MAX_STATE_BYTES`: the reader consumes at most the limit plus one byte before UTF-8/JSON decoding. State output is normalized/serialized and size checked before the temporary-file/`fsync`/atomic-replacement sequence.

## Backup boundary

Backup format versioning is intentionally independent from state schema versioning. Backup wrapper v2 records the embedded payload schema and a canonical SHA-256 payload digest.

`load_validated_export(...)` performs one bounded read and returns `ValidatedExport`, carrying the validated wrapper/payload metadata from that same read. Import and backup inspection share this boundary instead of re-reading the file independently.

Legacy GuessNova backup wrapper v1 is retained as an explicit compatibility path. See `docs/adr/0004-separate-backup-and-state-versions.md`.

`MAX_EXPORT_BYTES` is larger than `MAX_STATE_BYTES` so any state accepted for repair can fit within the mandatory backup envelope.

## Backup-inspection boundary

`backup_inspection.py` is read-only. It first validates the envelope and then runs the embedded state through current `normalize_state(...)` in memory.

A wrapper can therefore pass its checksum but still fail preflight if the payload cannot be imported by current state rules. Valid reports use normalized structural counts and expose source/normalized schema metadata without printing the state payload.

## Diagnostics and repair boundary

`diagnostics.py` uses the same bounded `read_state_payload(...)` function as normal storage. It reports migration/normalization requirements and aggregate local-state counts.

Repair is intentionally conservative:

1. missing state is a no-op;
2. unreadable/non-object/oversized/future-schema/unnormalizable state is refused;
3. repairable state is re-read through the bounded reader and normalized in memory;
4. if no write is required, repair returns without creating a redundant backup;
5. if a write is required, the original payload is exported to an integrity-protected backup;
6. only after that backup succeeds is normalized state written through `Storage`.

Doctor never uploads state or requires network access.

## Doctor protocol boundary

Doctor JSON output is a separately versioned machine contract. Current `DOCTOR_REPORT_VERSION` is `1`.

Kinds:

- `state`
- `backup`
- `error`

Stable exit codes:

- `0` — success/healthy state/valid backup/successful or no-op repair;
- `1` — interactive repair cancelled;
- `2` — attention/validation/handled error.

A future incompatible JSON contract must increment this report version instead of silently changing existing field meaning.

## Compatibility domains

Current independent compatibility identifiers remain:

- state schema: `2`;
- backup wrapper: `2` plus legacy `1` support;
- replay format: `1`;
- Doctor report: `1`.

GuessNova 1.4 expands the presentation/application layer without creating schema 3, backup wrapper 3, replay 2, or Doctor report 2.

## Security/privacy boundaries

GuessNova has no runtime authentication, remote API, telemetry, payment, cloud sync, or required network permissions. Untrusted values are bounded, parsed, and normalized before use. Replay and backup integrity mechanisms detect corruption/change but are not encryption, authentication, origin proof, or digital signatures.

See `docs/tui_workspace.md`, `docs/doctor.md`, `docs/adr/0001-modular-monolith.md`, `docs/adr/0002-versioned-json-storage.md`, and `docs/adr/0004-separate-backup-and-state-versions.md` for the detailed decisions and operating contracts.
