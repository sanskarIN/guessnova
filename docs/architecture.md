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
- `tui_workspace.py` — Textual-independent workspace helpers plus validated v1.5 challenge configuration/parsing/reconstruction.
- `tui.py` — stable v1.4 Textual six-pane workspace and event/focus orchestration over existing application/local-adapter boundaries.
- `tui_challenge.py` — localized target-free presentation of validated or already-created numeric challenges.
- `tui_challenge_widgets.py` — v1.5 mode/difficulty/seed/date controls and mode-aware field state.
- `tui_challenge_app.py` — additive v1.5 integration over `tui.GuessNovaApp`; this is the shipped `guessnova-tui` application.
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

                          tui_challenge_app.py
                                  |
               +------------------+------------------+
               |                                     |
            tui.py                           tui_challenge_widgets.py
               |                                     |
       +-------+--------+                     tui_challenge.py
       |                |                            |
tui_workspace.py   GameService                ChallengeConfiguration
       |                |                            |
 storage/history/   game/domain        tui_workspace.parse/build helpers
 leaderboard/settings
```

This keeps seeded gameplay deterministic and directly testable while allowing maintenance/recovery tooling and richer interactive presentation without duplicating game rules or state semantics.

The additive v1.5 decision is recorded in `docs/adr/0005-additive-textual-challenge-layer.md`.

## Stable Textual workspace boundary

GuessNova v1.4 established six panes:

- Play;
- Profiles;
- History;
- Leaderboard;
- Settings;
- Recovery.

`src/guessnova/tui.py` remains the stable owner of those workspace concerns:

- widget composition for the six panes;
- focus movement and pane shortcuts;
- core numeric guess/hint submission;
- profile lifecycle orchestration;
- history/leaderboard filtering and table refresh;
- settings save/apply behavior;
- active-profile transition isolation;
- high-contrast screen class;
- displaying read-only diagnostics and backup-preflight results.

The TUI does not create a second state store. Profile/history/leaderboard/settings changes continue through `Storage`, completed games continue through `GameService`, diagnostics continue through `diagnose`, and backup verification continues through `inspect_backup`.

## v1.5 challenge configuration boundary

`src/guessnova/tui_workspace.py` still has no Textual import. For challenge setup it now owns:

- immutable `ChallengeConfiguration`;
- `parse_workspace_challenge(...)`;
- `build_workspace_game(...)`.

The parser accepts presentation-friendly strings and validates mode/difficulty/seed/date before game construction.

Rules enforced by the configuration boundary:

- Reverse is not an ordinary numeric challenge;
- difficulty must come from the shared `DIFFICULTIES` registry;
- Daily requires a resolved date and derives its seed from that date;
- Daily cannot carry a manual seed;
- non-Daily challenges cannot carry a Daily date;
- seed text, when supplied, must parse as a whole number.

A blank Daily date is resolved at challenge-start time to the local current date. Tests inject `today` when validating this parser behavior so they do not depend on the test runner's wall clock.

## Challenge presentation boundary

`src/guessnova/tui_challenge.py` transforms challenge metadata into localized status text.

It is deliberately target-free. A status can identify:

- mode;
- difficulty;
- deterministic seed;
- resolved Daily date;
- unseeded/random challenge state.

It must not read/display a hidden target merely to identify the active challenge.

For an already-created Daily `GuessGame` whose source date is unavailable to the presentation layer, the app may identify the existing deterministic seed. A Daily challenge created through v1.5 setup retains its resolved date in `ChallengeConfiguration` and can show the date instead.

## Challenge widget boundary

`src/guessnova/tui_challenge_widgets.py` owns the Textual form only:

- mode selector;
- difficulty selector;
- optional seed input;
- Daily date input;
- Start Challenge action;
- help/status regions;
- seed/date enablement based on selected mode.

The widget layer does not persist results, mutate profiles, update history/leaderboards, or implement target selection.

Daily disables seed and enables date. Classic/Timed/Streak enable seed and disable date. Reverse is not offered by the numeric selector.

## Challenge integration transaction

`src/guessnova/tui_challenge_app.py` subclasses the stable workspace. It is the installed `guessnova-tui` target.

A challenge start is treated as an application-state transaction:

1. read mode/difficulty/seed/date controls;
2. parse/validate the configuration;
3. construct the replacement game;
4. only after success, assign the new configuration/game;
5. reset result-save/feedback/guess UI state;
6. normalize accepted seed/date fields;
7. update range/attempt presentation;
8. show target-free challenge identity;
9. focus Guess.

If parsing/construction fails, the current `GuessGame` object and its attempts remain active. The error is displayed and focus moves to the relevant seed/date field.

This avoids partially applying invalid configuration.

## Configured reset boundary

Once a challenge has been successfully configured, the validated `ChallengeConfiguration` is the reset source.

- Seeded Classic/Timed/Streak reconstruct from mode/difficulty/seed.
- Daily reconstructs from mode/difficulty/resolved date.
- Unseeded challenges still use normal random game construction.

The configuration contains no target value; deterministic target reproduction comes from the existing seeded/Daily engine behavior.

`Ctrl+R` remains a global reset. Plain `R` remains owned by focused `GuessInput`, so challenge/profile/search/path text fields continue to receive normal letters.

## Active-profile/game ownership boundary

An in-progress `GuessGame` belongs to the current active profile for persistence purposes. When the workspace changes the active profile by use/create/restore or by deleting the active profile, the unfinished round is reset before further play.

This prevents a user from making guesses under one profile and then accidentally recording the completed round under another profile.

For a v1.5 configured challenge, the validated configuration can remain active while attempt state is reset. Future persistence still occurs only after a new completion under the newly active profile.

Profile rename does not require a reset because identity continuity is preserved by `Storage.rename_profile(...)` together with matching leaderboard updates.

## TUI Recovery boundary

The Recovery pane is intentionally read-only:

- `diagnose(storage)` reports local state health/counts;
- `inspect_backup(path)` verifies a selected backup without importing it.

The pane does not call `repair(...)` and does not write a verified backup into application state. Repair remains explicit through Doctor so confirmation and backup-before-write guarantees remain centralized.

## TUI localization boundary

The Textual workspace selects its display locale when mounted. Activating a profile with a different saved locale updates the settings value and runtime preferences, but the current mounted presentation does not partially relabel itself. Full locale presentation changes occur on the next TUI launch.

This avoids a mixed-language UI where dynamically refreshed text changes language while already-created tab/button labels do not.

v1.5 challenge-facing copy is part of the same English/Hindi catalogs. Catalog-completeness tests still require every shipped Hindi key to cover the English key set.

Stable mode/difficulty/schema/backup/replay/Doctor identifiers remain untranslated machine values.

## TUI accessibility boundary

The workspace adds global Ctrl shortcuts for panes and quit/reset while leaving plain `Q`/`R` scoped to `GuessInput`.

v1.5 preserves the fast gameplay focus path:

- app launch explicitly focuses Guess;
- forward Tab remains Guess → Submit → Range Hint;
- challenge controls are reachable with backward focus navigation;
- successful challenge start returns to Guess;
- invalid seed/date focuses the relevant field.

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

v1.5 challenge form/configuration state is not added to `state.json`. It is active in-memory application state and does not justify schema 3.

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

GuessNova v1.5 expands the Textual presentation/application layer without creating schema 3, backup wrapper 3, replay 2, or Doctor report 2.

## Security/privacy boundaries

GuessNova has no runtime authentication, remote API, telemetry, payment, cloud sync, or required network permissions. Untrusted values are bounded, parsed, and normalized before use. Replay and backup integrity mechanisms detect corruption/change but are not encryption, authentication, origin proof, or digital signatures.

Challenge setup accepts only known numeric modes/difficulties, whole-number seeds, and ISO Daily dates before replacing a round. Challenge status deliberately excludes the hidden target.

See `docs/tui_workspace.md`, `docs/tui_challenges.md`, `docs/doctor.md`, `docs/adr/0001-modular-monolith.md`, `docs/adr/0002-versioned-json-storage.md`, `docs/adr/0004-separate-backup-and-state-versions.md`, and `docs/adr/0005-additive-textual-challenge-layer.md` for the detailed decisions and operating contracts.
