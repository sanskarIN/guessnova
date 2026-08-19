# Changelog

All notable GuessNova changes are recorded here. The project follows Semantic Versioning where practical.

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
- Defensive state/profile/settings/history normalization for untrusted or corrupted imported data.
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
