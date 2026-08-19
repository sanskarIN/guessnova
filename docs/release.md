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

4. Review CI, Security checks, and CodeQL results for the release commit.
5. Verify CLI help, seeded play, daily play, explicit hints, reverse mode, settings, history, import/export, and Textual startup on representative supported platforms.
6. Update version metadata, `CHANGELOG.md`, `ROADMAP.md`, and `what_changed.md`.
7. Create a semantic tag such as `v1.0.0` only after required checks pass.
8. The release workflow independently verifies that the tag version equals `project.version`, then reruns lint, format, strict mypy, tests, compile, smoke, and dependency audit before it can build artifacts.
9. After verification succeeds, the workflow builds the source distribution and wheel, validates them with Twine, and attaches them to generated GitHub release notes.
10. Verify the published artifacts contain the expected package code and no local state, caches, credentials, or secrets.

## Version/tag invariant

A release tag must be `v` followed by the exact `project.version` in `pyproject.toml`. For example, project version `1.0.0` must be released from tag `v1.0.0`. A mismatch intentionally fails the release workflow before artifacts are published.

## Reproducibility

Use the tagged commit as the sole release source. Do not build a release from a dirty local working tree or upload hand-modified artifacts. The GitHub workflow rebuilds distributions from checkout so artifacts are traceable to the tag.

## Rollback

Do not rewrite or move published tags. If a release has a defect, prepare a new patch version with a regression test, update the changelog, rerun the complete quality suite, and publish a new immutable tag.

## Secrets

GuessNova itself requires no secrets. If package-registry publishing is added later, use GitHub environment protection, trusted publishing where available, and repository/environment secrets; never place publishing tokens in source files, workflow YAML, `.env.example`, documentation, fixtures, or generated release archives.
