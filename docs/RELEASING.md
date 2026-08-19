# Releasing GuessNova

This is the concise release reference. The canonical detailed checklist is [`release.md`](release.md).

1. Ensure the exact release commit passes CI, Security checks, and CodeQL; queued/pending/older-head results are not a pass.
2. Require package build/install/smoke verification on Ubuntu, Windows, and macOS, including `python -m guessnova --help`, stable Textual workspace import, shipped challenge-app import, `guessnova doctor --help`, `guessnova-doctor --help`, and Doctor version output.
3. Update `CHANGELOG.md`, `CITATION.cff`, `pyproject.toml`, `src/guessnova/__init__.py`, `ROADMAP.md`, and `what_changed.md` in a synchronized release preparation.
4. Run lint, format, strict mypy, tests, compile, release-metadata verification, offline documentation-link verification, smoke, entry-point/both-Textual-import checks, dependency audit, build, and Twine checks.
5. Verify `python scripts/check_docs_links.py` succeeds on the exact release checkout; the checker validates repository-local Markdown/image targets without depending on external network availability.
6. Verify committed schema-1 fixtures migrate to schema 2, future schemas are rejected, and no schema 3 is introduced without a real compatibility boundary.
7. Verify bounded state/backup reads, backup-v2 integrity/schema provenance, single-read validation, legacy backup-v1 compatibility, and `MAX_EXPORT_BYTES > MAX_STATE_BYTES`.
8. Verify `guessnova doctor --verify-backup` proves current importability and rejects both tampered and checksum-valid-but-unnormalizable payloads without writing state.
9. Verify Doctor report version `1`, `state`/`backup`/`error` kinds, stable exit codes, explicit `--data-dir`, and backup-before-write repair on isolated legacy state.
10. Verify JSON repair requires `--yes` and produces one machine-readable document.
11. Verify the Textual workspace starts on Play and exercise Profiles, History, Leaderboard, Settings, and read-only Recovery through keyboard-only flows.
12. Verify v1.5 Challenge Setup: Classic/Timed/Streak/Daily selection, shared difficulty choices, non-Daily integer seed, Daily ISO date, mode-aware field disabling, target-free identity, and Reverse exclusion from numeric setup.
13. Verify invalid challenge seed/date input leaves the active target/attempt state intact and focuses the relevant field.
14. Verify configured seeded/Daily reset reconstructs the same deterministic challenge and returns focus to Guess.
15. Verify profile-switch unfinished-round isolation, exact-name recoverable deletion, history/leaderboard filtering, settings persistence, high contrast, and read-only backup verification.
16. Complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md) on the exact signed-off release candidate; v1.5 evidence includes Challenge Setup plus all six panes.
17. Verify English and Hindi presentation, including Challenge Setup and a TUI relaunch after changing profile locale.
18. Create immutable semantic tag `v1.5.0` only for project version `1.5.0` after all required automated and manual gates pass.
19. Push the tag; the release workflow independently reruns strict quality, documentation-link, and cross-platform release gates before creating artifacts.
20. Verify installation from the built wheel in a clean Python 3.13 environment and confirm `guessnova`, `guessnova-tui`, `guessnova-doctor`, `guessnova doctor` routing, stable workspace import, and shipped challenge-app import are present.
21. Add real screenshots/demo media only when captured from the exact signed-off build according to [`media/README.md`](media/README.md).

v1.5 does **not** change these compatibility identifiers:

```text
state schema = 2
backup wrapper = 2
legacy backup wrapper = 1
replay = 1
Doctor report = 1
```

Challenge configuration is in-memory application/presentation state and is not a reason to create a new persistence format.

Do not publish secrets, local state files, recoverable profile data, pre-repair backups, challenge/status captures containing private local data, Doctor/TUI recovery captures containing private profile names or paths, developer `.env` files, or private user data in release artifacts.

Backup SHA-256 is integrity/change detection, not authentication or proof of origin. Artifact signing remains gated until a real registry publishing workflow exists.
