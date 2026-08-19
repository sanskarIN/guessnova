# Release Process

## Release checklist

1. Start from a clean checkout of the intended release commit on `main`.
2. Use Python 3.13+ and install `.[dev]` plus `build`, `twine`, and `pip-audit`.
3. Run the complete local quality suite:

   ```bash
   ruff check .
   ruff format --check .
   mypy src/guessnova
   pytest --cov=guessnova --cov-report=term-missing
   python -m compileall -q src tests scripts
   python scripts/verify_release_metadata.py
   python scripts/smoke_test.py
   pip-audit
   python -m build
   python -m twine check dist/*
   ```

4. Review CI, Security checks, and CodeQL results for the exact release commit.
5. Require the CI platform-package matrix to complete on Ubuntu, Windows, and macOS. Each platform must build, validate, install the wheel, start both `python -m guessnova --help` and `guessnova-doctor --help`, and pass the smoke test.
6. Verify CLI help, seeded play, daily play, explicit hints, reverse mode, settings, advanced history filters/grouping, profile create/use/rename/delete/restore, backup export/import, and Textual startup.
7. Verify schema migration from both committed schema-1 fixtures and confirm the resulting normalized state is schema 2.
8. Verify a backup-v2 round trip, legacy wrapper-v1 import, and a deliberately modified backup failing its SHA-256 integrity check.
9. Verify `guessnova-doctor`, `guessnova-doctor --json`, and a repair flow against isolated schema-1 state. Confirm the repair backup contains the original schema-1 payload and the repaired state is schema 2.
10. Complete a copy of `docs/accessibility_evidence_template.md` against the exact release candidate. Do not infer manual accessibility results from automated tests.
11. Verify both shipped locales (`en`, `hi`) and confirm no visible catalog key or broken placeholder reaches the user.
12. Update version metadata, `CHANGELOG.md`, `ROADMAP.md`, and `what_changed.md`.
13. Create a semantic tag such as `v1.2.0` only after required checks pass.
14. The release workflow independently verifies that the tag version equals `project.version`, then reruns lint, format, strict mypy, tests, compile, release metadata, smoke, dependency audit, and the cross-platform package matrix before it can publish artifacts.
15. After verification succeeds, the workflow builds the source distribution and wheel, validates them with Twine, and attaches them to generated GitHub release notes.
16. Verify the published wheel exposes `guessnova`, `guessnova-tui`, and `guessnova-doctor` and contains no local state, caches, credentials, repair backups, or secrets.
17. If screenshots/demo media are published, capture them from this exact signed-off tag/commit and record provenance according to `docs/media/README.md`. Never use mock or reconstructed release media.

## Version/tag invariant

A release tag must be `v` followed by the exact `project.version` in `pyproject.toml`. For project version `1.2.0`, the release tag must be `v1.2.0`. A mismatch intentionally fails the release workflow before artifacts are published.

Package, runtime, citation, and changelog release metadata are also checked by `scripts/verify_release_metadata.py`.

## State/backup compatibility gate

A v1.2 release must not ship unless all of these remain true:

- schema 0 can migrate forward;
- committed schema-1 fixtures migrate to schema 2;
- future state schemas are rejected;
- backup wrapper v2 records the embedded payload schema;
- wrapper/payload schema mismatch is rejected;
- backup payload tampering is rejected by integrity validation;
- legacy backup wrapper v1 remains importable when its embedded state schema is supported;
- repair creates a backup before rewriting repairable state;
- unreadable/non-object state is not silently overwritten.

Backup SHA-256 integrity is corruption detection, not authentication, encryption, or digital signing.

## Reproducibility

Use the tagged commit as the sole release source. Do not build a release from a dirty local working tree or upload hand-modified artifacts. The GitHub workflow rebuilds distributions from checkout so artifacts are traceable to the tag.

Cross-platform CI verifies packaging behavior on the three supported desktop OS families, but the generated GitHub release artifacts still come from the release workflow's clean checkout. Platform checks validate portability; they do not create three different product versions.

## Accessibility evidence

A release candidate is not considered manually signed off until the evidence checklist has been completed on the candidate commit. Any release-blocking accessibility issue should receive a reproducible issue/test where practical before tagging.

## Release media

Real terminal screenshots and demo recordings are manual release artifacts, not generated placeholders. Store them under `docs/media/` only after capture from the signed-off build. Include the exact tag/commit in the filename or companion metadata.

## Rollback

Do not rewrite or move published tags. If a release has a defect, prepare a new patch version with a regression test, update the changelog, rerun the complete quality suite, and publish a new immutable tag.

A rollback must not rewrite a user's newer state schema with older software. If state compatibility is uncertain, preserve the state directory and use export/repair backups rather than attempting a downgrade write.

## Secrets

GuessNova itself requires no secrets. If package-registry publishing is added later, use GitHub environment protection, trusted publishing where available, and repository/environment secrets; never place publishing tokens in source files, workflow YAML, `.env.example`, documentation, fixtures, or generated release archives.
