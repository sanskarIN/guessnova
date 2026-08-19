# Changelog

All notable GuessNova changes are recorded here. The project follows Semantic Versioning where practical.

## [1.5.0] - 2026-08-19

### Added

- Validated Challenge Setup controls inside the shipped Textual Play experience.
- Play-side Classic, Timed, Streak, and Daily challenge selection while keeping Reverse on its dedicated interaction path.
- Difficulty selection sourced from the shared `DIFFICULTIES` registry rather than duplicated TUI rules.
- Optional deterministic integer seeds for Classic/Timed/Streak challenges.
- Daily `YYYY-MM-DD` configuration with blank-date resolution to the local current date.
- Immutable `ChallengeConfiguration` plus Textual-independent `parse_workspace_challenge(...)` validation/reconstruction helpers.
- Localized target-free challenge identity presentation for active/configured games.
- Mode-aware challenge fields: seed is disabled for Daily, while date is disabled for Classic/Timed/Streak.
- Additive `tui_challenge_app.py` integration over the stable v1.4 six-pane workspace.
- Focused challenge configuration, presentation, widget, integration, validation-preservation, reset, initial-status, localization, and keyboard regression suites.
- Dedicated `docs/tui_challenges.md` guide and a repository definition-of-done audit.
- Built-wheel import verification for both the stable workspace and the shipped challenge-enabled Textual app on Linux, Windows, and macOS package matrices.

### Changed

- `guessnova-tui` now routes through the challenge-enabled application layer while retaining all v1.4 workspace panes and local persistence/service boundaries.
- `build_workspace_game(...)` now delegates through the validated challenge configuration parser/model before constructing the game.
- Play keeps the numeric guess field as initial focus even though challenge controls are mounted before it in document order.
- Forward Tab from Guess continues to reach Submit then Range Hint; backward keyboard navigation reaches challenge setup.
- Successful challenge start normalizes seed/date fields, clears prior round UI state, updates range/attempts, reports target-free challenge identity, and returns focus to Guess.
- Configured seeded/Daily reset reconstructs from validated configuration instead of relying on ad-hoc widget state.
- Smoke testing now exercises challenge parsing, deterministic reconstruction, and localized challenge presentation.
- Canonical/concise Textual documentation now describes v1.5 challenge setup in addition to the v1.4 workspace.

### Accessibility, privacy, and reliability

- Invalid seed or Daily-date input is rejected before the active `GuessGame` is replaced, preserving target, attempts, and result-save state.
- Challenge validation errors are visible text and focus the relevant input.
- Seed/date inputs remain ordinary text fields; plain `Q/R` continue to belong only to the numeric `GuessInput` rather than becoming application-global shortcuts.
- Irrelevant challenge inputs are disabled according to selected mode so the form does not imply unsupported configuration.
- Active challenge status contains mode/difficulty/seed/date identity only and never deliberately exposes the hidden target.
- English and Hindi catalogs include every new challenge-facing message, with catalog-completeness coverage retained.
- Challenge configuration remains in-memory application/presentation state and does not create a new persistence schema or remote service.

### Compatibility

- Local state schema remains `2`; v1.5 does not introduce schema 3.
- Backup wrapper remains version `2` and legacy wrapper-v1 support is retained.
- Replay format remains version `1`.
- Doctor machine report protocol remains version `1`.
- Existing Rich CLI, `guessnova doctor`, standalone `guessnova-doctor`, and v1.4 workspace behavior remain supported.

## [1.4.0] - 2026-08-19

### Added

- Full six-pane Textual workspace: Play, Profiles, History, Leaderboard, Settings, and read-only Recovery.
- Direct keyboard pane navigation with `Ctrl+1` through `Ctrl+6`, plus global `Ctrl+R` reset and `Ctrl+Q` quit.
- Dedicated Play `GuessInput` bindings that retain plain `R` reset and `Q` quit without making those letters global to workspace text fields.
- TUI profile summary and unlocked-achievement visibility.
- TUI profile use/create/rename/recoverable-delete/restore flows using the existing `Storage` lifecycle APIs.
- Exact selected-name confirmation before a profile can be moved to recoverable trash from the TUI.
- TUI History table with result, mode, difficulty, search, since-date, and until-date filters.
- TUI Leaderboard table with mode, difficulty, and case-insensitive player filters.
- TUI Settings pane for theme, locale, reduced motion, high contrast, sound preference, and automatic smart hints.
- Immediate Textual high-contrast border/focus treatment plus non-animated Switch controls.
- Read-only TUI state diagnostics and read-only backup verification using the same v1.3 diagnostics/preflight boundaries as Doctor.
- `tui_workspace.py` as a Textual-independent helper layer for workspace snapshots, profile summaries, deterministic challenge construction, history selection, leaderboard filtering, and validated settings persistence.
- Focused Textual pilot suites for workspace navigation, profile lifecycle, history, leaderboard, settings, Recovery, round isolation, locale consistency, and high contrast.
- Built-wheel Textual workspace import verification on Ubuntu, Windows, and macOS package matrices.
- Canonical and concise Textual workspace documentation plus an expanded six-pane manual accessibility evidence checklist.

### Changed

- Package/runtime/citation version advanced to `1.4.0`.
- `guessnova-tui` now opens a full local workspace while preserving Play as the initial pane and the numeric guess field as initial focus.
- Plain `Q` and `R` are owned only by the focused numeric Play input; profile/search/player/path fields receive those characters normally, while global `Ctrl+Q`/`Ctrl+R` remain available everywhere.
- Active-profile changes reset any unfinished TUI round so a partially played game cannot later be persisted under another profile.
- TUI profile activation loads the selected profile's settings without partially changing the mounted UI language.
- Locale changes are persisted immediately but full mounted Textual presentation changes take effect on the next launch for language consistency.
- Completed TUI games refresh profile, history, leaderboard, and Recovery views from the shared local state.
- Smoke testing now exercises reusable workspace snapshots, deterministic challenge construction, history/leaderboard selection, and settings persistence.
- Normal CI and tagged-release package matrices explicitly import the Textual workspace from the built wheel.

### Accessibility, privacy, and reliability

- High-contrast TUI mode strengthens structural borders and focus visibility without making color the only status signal.
- Workspace text inputs retain ordinary character entry because single-letter reset/quit bindings are scoped to the Play guess widget instead of the application.
- TUI profile deletion remains recoverable and requires explicit typed-name confirmation.
- TUI Recovery intentionally exposes no repair/write button; repair remains centralized in Doctor with confirmation and backup-before-write guarantees.
- Backup verification in the TUI is read-only and does not import or rewrite selected state.
- All new normal workspace labels/status copy is represented in both shipped English and Hindi catalogs, with catalog-completeness tests retained.
- The workspace remains local-only and adds no accounts, telemetry, cloud sync, remote leaderboard, or runtime network dependency.

### Compatibility

- Local state schema remains `2`; v1.4 does not introduce schema 3.
- Backup wrapper remains version `2` and legacy wrapper-v1 support is retained.
- Replay format remains version `1`.
- Doctor machine report protocol remains version `1`.
- Existing CLI and standalone `guessnova-doctor` entry points remain supported.

## [1.3.0] - 2026-08-19

### Added

- `guessnova doctor` as the primary diagnostics/recovery route while preserving the standalone `guessnova-doctor` entry point.
- Read-only backup verification with structural metadata, legacy-wrapper visibility, current normalization preview, and proof that the payload can actually be imported by current state normalization.
- Explicit `--data-dir` targeting for diagnostics without modifying `GUESSNOVA_HOME`.
- Stable Doctor JSON protocol version `1` with `state`, `backup`, and `error` document kinds.
- Stable Doctor exit semantics: `0` success/healthy/valid, `1` cancelled repair, and `2` attention/validation failure.
- Doctor `--version` output aligned to the package runtime version.
- Bounded local-state reads and writes via `MAX_STATE_BYTES`.
- Single-read, bounded backup validation metadata via `ValidatedExport`.
- Canonical and concise Doctor documentation.
- End-to-end smoke coverage for the primary doctor route, backup verification, legacy repair backup inspection, and current-schema normalization.

### Changed

- Package/runtime/citation version advanced to `1.3.0`.
- Installed `guessnova` now routes through a compatibility-preserving top-level dispatcher while existing gameplay commands remain handled by the established Rich CLI.
- `python -m guessnova` uses the same dispatcher as the installed `guessnova` executable.
- Backup verification now validates both the envelope and the embedded state payload's ability to pass current normalization before reporting it as valid.
- Backup/state file readers consume only the configured maximum plus one byte before oversized input is rejected.
- Backup maximum size increased above the accepted state maximum so every accepted repairable state can fit inside its mandatory pre-repair backup envelope.
- `make check`, normal CI, and tagged-release package matrices verify both Doctor entry paths.

### Security, privacy, and reliability

- Backup inspection no longer validates one read and reports metadata from a second read, removing that time-of-check/time-of-use inconsistency.
- State diagnostics and repair now reuse the same bounded state reader as normal storage.
- Checksum-valid but structurally unimportable backups are rejected by Doctor before an import is attempted.
- Repair continues to create a successful backup before any required normalization write.
- Doctor remains local-only and does not upload reports, state, or backup content.
- Backup SHA-256 continues to be described as integrity detection, not authentication, signing, encryption, or proof of origin.

### Compatibility

- Local state schema remains `2`; v1.3 does not invent schema 3.
- Backup wrapper remains version `2` and legacy wrapper-v1 import/inspection support is retained.
- Replay version remains `1`; gameplay and replay semantics are unchanged.
- The standalone `guessnova-doctor` command remains supported alongside `guessnova doctor`.

## [1.2.0] - 2026-08-19

### Added

- Formal schema-2 local-state migration with committed schema-1 fixtures covering legacy state with and without recoverable profile trash.
- Version-2 backup wrapper with independent backup-format versioning, SHA-256 payload integrity metadata, and explicit source-schema provenance.
- Backward-compatible import support for legacy GuessNova version-1 backup wrappers.
- `guessnova-doctor` local diagnostic command with human-readable, compact, and machine-readable JSON output.
- Local diagnostic reporting for source/current schema, profile/history/leaderboard/trash counts, active profile, normalization changes, and repairable issues.
- Safe doctor repair flow that creates an integrity-protected pre-repair backup before writing normalized state.
- Regression coverage for migration fixtures, legacy backups, backup tampering, schema metadata mismatches, diagnostics, repair confirmation, and JSON-mode repair output.

### Changed

- Local state schema advanced from version `1` to version `2`; schema 2 formally makes `deleted_profiles` a canonical top-level state container.
- Package/runtime/citation version advanced to `1.2.0`.
- Backup format version is now independent from local state schema version so future state migrations do not automatically invalidate older backup wrappers.
- Backup exports record the payload's actual schema version rather than always reporting the running application's schema.

### Security, privacy, and reliability

- Backup v2 payloads are checked with constant-time SHA-256 digest comparison before import.
- Backup wrapper schema metadata must match the embedded payload schema metadata.
- Future backup-format and future state-schema versions are rejected explicitly.
- Diagnostics and repair remain fully local; no account, telemetry, analytics, cloud sync, or network service is introduced.
- Repair refuses unreadable/non-object state rather than overwriting data it cannot safely normalize.

### Compatibility

- Schema-0 and schema-1 state migrate forward to schema 2.
- GuessNova <=1.1 version-1 backup wrappers remain importable and are migrated only when persisted through current storage.
- Replay version remains unchanged; v1.2 does not change guessing rules or replay compatibility.

## [1.1.0] - 2026-08-19

### Added

- Safe profile-management commands for listing, creating, activating, renaming, deleting, viewing trash, and restoring local profiles.
- Recoverable profile trash with bounded retention and restoration of the deleted profile's local leaderboard entries.
- Richer history filtering by result, free-text match, date range, and grouping by day, mode, difficulty, or result.
- Positive-limit validation for history and leaderboard CLI queries.
- Hindi (`hi`) as a second complete shipped message catalog while English remains the default/fallback locale.
- Catalog-completeness validation so shipped locales can be checked against the English key set.
- Textual pilot coverage for focus order, input submission, range hints, reset behavior, and persisted winning results.
- TUI result persistence through the same application service used by the CLI.
- Deterministic initial TUI input focus and priority reset/quit keyboard bindings.
- Release-candidate accessibility evidence template covering keyboard, plain/compact output, TUI, scaling, and localization checks.
- Verified release-media workflow that forbids fabricated screenshots and requires exact commit/tag provenance.
- Windows, macOS, and Linux package/build/install/CLI/smoke verification in CI.

### Changed

- Package and runtime version advanced to `1.1.0`.
- History query logic moved into reusable domain helpers rather than living only in CLI rendering code.
- Profile rename now updates matching local leaderboard player names.
- Profile deletion removes associated local leaderboard entries while retaining them inside recoverable trash for undo.
- TUI now loads the active profile locale and records completed rounds exactly once.

### Compatibility

- Existing schema-1 save files remain readable; recoverable profile trash is an additive optional top-level field.
- Existing profiles without Hindi/localization-specific settings continue to default to English.
- Stable mode/difficulty/replay/save identifiers remain English machine identifiers and are not translated.

## [1.0.0] - 2026-08-19

### Added

- Rich CLI and Textual TUI entry points for Python 3.13+.
- Classic, timed, streak-tagged, reverse, and deterministic daily challenge modes.
- Easy, normal, hard, and expert difficulty presets.
- Deterministic seeds, smart temperature/direction/parity hints, and replay codes with integrity checks.
- Explicit narrowed-range hints with optional XP penalties.
- Local profiles with XP, win rate, average guesses, streaks, achievements, settings, and bounded session history.
- First-run onboarding that explains controls, local-data behavior, and settings without requiring an account.
- English-first externalized message catalog plus persisted locale setting for future offline translations.
- `history`, `settings`, and `about` CLI commands.
- `--plain` and `--compact` terminal modes plus per-round smart-hint overrides.
- Saved semantic terminal themes and a high-contrast palette applied to Rich CLI output.
- Adaptive Textual card layout and an explicit range-hint action.
- Local leaderboard plus validated JSON export/import.
- Atomic local state persistence and schema migration baseline.
- Defensive state/profile/settings/history/leaderboard normalization for untrusted or corrupted imported data.
- Privacy/security helpers and local-only defaults.
- Automated tests, smoke checks, replay fuzz-style coverage, strict formatting/type/lint gates, repository quality automation, documentation, and release engineering baseline.
- Dependency/secret auditing, CodeQL, Dependabot, quality-gated tagged release automation, and repository operations guidance.
- Editable SVG logo/banner branding and visible `Made by the Sanskar` credit.

### Security and privacy

- No runtime accounts, analytics, telemetry, advertising, or required network access.
- Input sanitization, replay integrity verification, bounded values, path containment helpers, future-schema rejection, and normalized imported state.
- Replay decoding validates encoded length, Base64/envelope integrity, field allowlists, numeric bounds, range/attempt consistency, finite timing values, and portable seed bounds before constructing a summary.
- Local history is capped so malformed or unusually long imports cannot cause unbounded retained history.
- Tagged releases cannot publish artifacts until lint, formatting, strict typing, tests, compile, smoke, dependency audit, and version/tag matching succeed.

### Compatibility

- Existing schema-1 profiles without `history`, `locale`, or `onboarding_complete` fields continue to load with safe defaults.
- Existing version-1 replay codes without explicit-hint metadata continue to load through default summary fields.
- Stable serialized identifiers remain untranslated so future display locales do not invalidate saves, exports, achievements, or replay codes.
