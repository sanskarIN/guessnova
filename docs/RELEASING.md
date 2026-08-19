# Releasing GuessNova

This is the concise release reference. The canonical detailed checklist is [`release.md`](release.md).

1. Ensure the exact release commit passes CI, Security checks, and CodeQL.
2. Require package build/install/smoke verification on Ubuntu, Windows, and macOS, including both the game and `guessnova-doctor` entry points.
3. Update `CHANGELOG.md`, `CITATION.cff`, `pyproject.toml`, `src/guessnova/__init__.py`, `ROADMAP.md`, and `what_changed.md`.
4. Run lint, format, strict mypy, tests, compile, release-metadata verification, smoke, dependency audit, build, and Twine checks.
5. Verify committed schema-1 fixtures migrate to schema 2 and future schemas are rejected.
6. Verify backup-v2 integrity/schema provenance, legacy backup-v1 import, and deliberate-tamper rejection.
7. Verify `guessnova-doctor --json` and backup-before-write repair on isolated legacy state.
8. Complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md) on the signed-off release candidate.
9. Verify English and Hindi presentation plus the profile/history/TUI flows retained from v1.1.
10. Create an immutable semantic tag matching the package version exactly, for example `v1.2.0` for project version `1.2.0`.
11. Push the tag; the release workflow independently reruns strict and cross-platform release gates before creating artifacts.
12. Verify installation from the built wheel in a clean Python 3.13 environment and confirm `guessnova`, `guessnova-tui`, and `guessnova-doctor` are present.
13. Add real screenshots/demo media only when captured from the exact signed-off build according to [`media/README.md`](media/README.md).

Do not publish secrets, local state files, recoverable profile data, pre-repair backups, developer `.env` files, or private user data in release artifacts.
