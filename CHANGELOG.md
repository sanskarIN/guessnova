# Changelog

All notable GuessNova changes are recorded here. The project follows Semantic Versioning where practical.

## [1.0.0] - 2026-08-19

### Added

- Rich CLI and Textual TUI entry points for Python 3.13+.
- Classic, timed, streak-tagged, reverse, and deterministic daily challenge modes.
- Easy, normal, hard, and expert difficulty presets.
- Deterministic seeds, smart temperature/direction/parity hints, and replay codes with integrity checks.
- Explicit narrowed-range hints with optional XP penalties.
- Local profiles with XP, win rate, average guesses, streaks, achievements, settings, and bounded session history.
- `history`, `settings`, and `about` CLI commands.
- `--plain` and `--compact` terminal modes plus per-round smart-hint overrides.
- Local leaderboard plus validated JSON export/import.
- Atomic local state persistence and schema migration baseline.
- Defensive state/profile/settings/history normalization for untrusted or corrupted imported data.
- Privacy/security helpers and local-only defaults.
- Automated tests, smoke checks, strict formatting/type/lint gates, repository quality automation, documentation, and release engineering baseline.
- Dependency/secret auditing, CodeQL, Dependabot, tagged release automation, and repository operations guidance.
- Editable SVG logo/banner branding and visible `Made by the Sanskar` credit.

### Security and privacy

- No runtime accounts, analytics, telemetry, advertising, or required network access.
- Input sanitization, replay integrity verification, bounded values, path containment helpers, future-schema rejection, and normalized imported state.
- Local history is capped so malformed or unusually long imports cannot cause unbounded retained history.

### Compatibility

- Existing schema-1 profiles without a `history` field continue to load.
- Existing version-1 replay codes without explicit-hint metadata continue to load through default summary fields.
