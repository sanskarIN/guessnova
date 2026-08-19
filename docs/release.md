# Release Process

## Release checklist

1. Start from a clean checkout of the target commit.
2. Use Python 3.13+ and install `.[dev]`.
3. Run `pytest`, `ruff check .`, the smoke test, and the package build.
4. Review dependency/security workflow results and CodeQL findings.
5. Verify CLI help, deterministic seeded play, reverse mode, import/export, and Textual startup.
6. Update version metadata, `CHANGELOG.md`, `ROADMAP.md`, and `what_changed.md`.
7. Create a semantic tag such as `v1.0.0` only after required checks pass.
8. Let the release workflow create reproducible source/wheel artifacts and GitHub release notes.
9. Verify the published artifacts contain the expected package code and no local data/secrets.

## Rollback

Do not rewrite published tags. If a release has a defect, prepare a new patch version with a regression test and document the fix in the changelog.

## Secrets

GuessNova itself requires no secrets. If package publishing is added later, use GitHub environment protection and repository secrets; never place publishing tokens in source files, workflow YAML, `.env.example`, or documentation.
