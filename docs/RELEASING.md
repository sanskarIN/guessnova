# Releasing GuessNova

This is the concise release reference. The canonical detailed checklist is [`release.md`](release.md).

1. Ensure the exact release commit passes CI, Security checks, and CodeQL.
2. Require package build/install/smoke verification on Ubuntu, Windows, and macOS.
3. Update `CHANGELOG.md`, `CITATION.cff`, `pyproject.toml`, `src/guessnova/__init__.py`, `ROADMAP.md`, and `what_changed.md`.
4. Run the complete local lint/format/mypy/test/compile/smoke/audit/build/Twine suite.
5. Complete [`accessibility_evidence_template.md`](accessibility_evidence_template.md) on the signed-off release candidate.
6. Verify English and Hindi presentation and the profile/history/TUI flows changed by v1.1.
7. Create an immutable semantic tag matching the package version exactly, for example `v1.1.0` for project version `1.1.0`.
8. Push the tag; the release workflow independently reruns release gates before creating artifacts.
9. Verify installation from the built wheel in a clean Python 3.13 environment.
10. Add real screenshots/demo media only when captured from the exact signed-off build according to [`media/README.md`](media/README.md).

Do not publish secrets, local state files, recoverable profile data, developer `.env` files, or private user data in release artifacts.
