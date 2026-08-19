# Changelog

All notable GuessNova changes are recorded here. The project follows Semantic Versioning where practical.

## [1.0.0] - 2026-08-19

### Added

- Rich CLI and Textual TUI entry points for Python 3.13+.
- Classic, timed, streak-tagged, reverse, and deterministic daily challenge modes.
- Easy, normal, hard, and expert difficulty presets.
- Deterministic seeds, smart temperature/direction/parity hints, and replay codes with integrity checks.
- Local profiles with XP, win rate, streaks, achievements, and settings.
- Local leaderboard plus validated JSON export/import.
- Atomic local state persistence and schema migration baseline.
- Privacy/security helpers and local-only defaults.
- Automated tests, repository quality automation, documentation, and release engineering baseline.
- Editable SVG branding and visible `Made by the Sanskar` credit.

### Security and privacy

- No runtime accounts, analytics, telemetry, advertising, or required network access.
- Input sanitization, replay integrity verification, bounded values, and path containment helpers.
