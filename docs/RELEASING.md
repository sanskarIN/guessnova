# Releasing GuessNova

This is the concise release reference. The canonical detailed checklist is [`release.md`](release.md).

1. Ensure the exact release commit passes CI, Security checks, and CodeQL; queued/pending/older-head results are not a pass.
2. Require package build/install/smoke verification on Ubuntu, Windows, and macOS, including `python -m guessnova --help`, built-wheel Textual workspace import, `guessnova doctor --help`, `guessnova-doctor --help`, and Doctor version output.
3. Update `CHANGELOG.md`, `CITATION.cff`, `pyproject.toml`, `src/guessnova/__init__.py`, `ROADMAP.md`, and `what_changed.md`.
4. Run lint, format, strict mypy, tests, compile, release-metadata verification, smoke, entry-point/workspace-import checks, dependency audit, build, and Twine checks.
5. Verify committed schema-1 fixtures migrate to schema 2, future schemas are rejected, and no schema 3 is introduced without a real compatibility boundary.
6. Verify bounded state/backup reads, backup-v2 integrity/schema provenance, single-read validation, legacy backup-v1 compatibility, and `MAX_EXPORT_BYTES > MAX_STATE_BYTES`.
7. Verify `guessnova doctor --verify-backup` proves current importability and rejects both tampered and checksum-valid-but-unnormalizable payloads without writing state.
8. Verify Doctor report version `1`, `state`/`backup`/`error` kinds, stable exit codes, explicit `--data-dir`, and backup-before-write repair on isolated legacy state.
9. Verify JSON repair requires `--yes` and produces one machine-readable document.
10. Verify the Textual workspace starts on Play and exercise Profiles, History, Leaderboard, Settings, and read-only Recovery through keyboard-only flows.
11. Verify profile-switch unfinished-round isolation, exact-name recoverable deletion, history/leaderboard filtering, settings persistence, high contrast, and read-only backup verification.
12. Complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md) on the signed-off release candidate; the v1.4 template includes all six panes.
13. Verify English and Hindi presentation, including a TUI relaunch after changing profile locale.
14. Create immutable semantic tag `v1.4.0` only for project version `1.4.0` after all required gates pass.
15. Push the tag; the release workflow independently reruns strict and cross-platform release gates before creating artifacts.
16. Verify installation from the built wheel in a clean Python 3.13 environment and confirm `guessnova`, `guessnova-tui`, `guessnova-doctor`, `guessnova doctor` routing, and Textual workspace import are present.
17. Add real screenshots/demo media only when captured from the exact signed-off build according to [`media/README.md`](media/README.md).

v1.4 does **not** change these compatibility identifiers:

```text
state schema = 2
backup wrapper = 2
legacy backup wrapper = 1
replay = 1
Doctor report = 1
```

Do not publish secrets, local state files, recoverable profile data, pre-repair backups, Doctor/TUI recovery captures containing private profile names or paths, developer `.env` files, or private user data in release artifacts.

Backup SHA-256 is integrity/change detection, not authentication or proof of origin. Artifact signing remains gated until a real registry publishing workflow exists.
