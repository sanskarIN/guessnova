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
   python scripts/smoke_test.py
   pip-audit
   python -m build
   python -m twine check dist/*
   ```

4. Review CI, Security checks, and CodeQL results for the exact release commit.
5. Require the CI platform-package matrix to complete on Ubuntu, Windows, and macOS. Each platform must build, validate, install the wheel, start the CLI, and pass the smoke test.
6. Verify CLI help, seeded play, daily play, explicit hints, reverse mode, settings, advanced history filters/grouping, profile create/use/rename/delete/restore, import/export, and Textual startup.
7. Complete a copy of `docs/accessibility_evidence_template.md` against the exact release candidate. Do not infer manual accessibility results from automated tests.
8. Verify both shipped locales (`en`, `hi`) and confirm no visible catalog key or broken placeholder reaches the user.
9. Update version metadata, `CHANGELOG.md`, `ROADMAP.md`, and `what_changed.md`.
10. Create a semantic tag such as `v1.1.0` only after required checks pass.
11. The release workflow independently verifies that the tag version equals `project.version`, then reruns lint, format, strict mypy, tests, compile, smoke, and dependency audit before it can build artifacts.
12. After verification succeeds, the workflow builds the source distribution and wheel, validates them with Twine, and attaches them to generated GitHub release notes.
13. Verify the published artifacts contain the expected package code and no local state, caches, credentials, or secrets.
14. If screenshots/demo media are published, capture them from this exact signed-off tag/commit and record provenance according to `docs/media/README.md`. Never use mock or reconstructed release media.

## Version/tag invariant

A release tag must be `v` followed by the exact `project.version` in `pyproject.toml`. For example, project version `1.1.0` must be released from tag `v1.1.0`. A mismatch intentionally fails the release workflow before artifacts are published.

## Reproducibility

Use the tagged commit as the sole release source. Do not build a release from a dirty local working tree or upload hand-modified artifacts. The GitHub workflow rebuilds distributions from checkout so artifacts are traceable to the tag.

Cross-platform CI verifies packaging behavior on the three supported desktop OS families, but the generated GitHub release artifacts still come from the release workflow's clean checkout. Platform checks validate portability; they do not create three different product versions.

## Accessibility evidence

A release candidate is not considered manually signed off until the evidence checklist has been completed on the candidate commit. Any release-blocking accessibility issue should receive a reproducible issue/test where practical before tagging.

## Release media

Real terminal screenshots and demo recordings are manual release artifacts, not generated placeholders. Store them under `docs/media/` only after capture from the signed-off build. Include the exact tag/commit in the filename or companion metadata.

## Rollback

Do not rewrite or move published tags. If a release has a defect, prepare a new patch version with a regression test, update the changelog, rerun the complete quality suite, and publish a new immutable tag.

## Secrets

GuessNova itself requires no secrets. If package-registry publishing is added later, use GitHub environment protection, trusted publishing where available, and repository/environment secrets; never place publishing tokens in source files, workflow YAML, `.env.example`, documentation, fixtures, or generated release archives.
