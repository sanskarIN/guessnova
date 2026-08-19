# Development

Use Python 3.13+ and install the development extras:

```bash
python -m pip install -e '.[dev]'
```

## Quality loop

Run the same core checks enforced by CI before opening a pull request:

```bash
ruff check .
ruff format --check .
mypy src/guessnova
pytest --cov=guessnova --cov-report=term-missing
python -m compileall -q src tests scripts
python scripts/smoke_test.py
```

Before a release also build and validate the package:

```bash
python -m pip install build twine pip-audit
python -m build
python -m twine check dist/*
pip-audit
```

## Engineering rules

- Keep `engine.py` and domain rules independent of terminal rendering and filesystem I/O.
- Use deterministic seeds, explicit targets, dates, or injected clocks in automated tests.
- Preserve save/replay compatibility unless a documented migration/version change is provided.
- Treat imported/local JSON as untrusted and normalize it through the storage/profile boundaries.
- Keep filesystem writes atomic and local by default.
- Prefer clear typed dataclasses and small focused functions.
- Keep strict mypy clean; avoid broad ignores that hide real type errors.
- Add regression tests for confirmed bugs.
- Do not commit credentials, private endpoints, real player data, local state, caches, virtual environments, or build outputs.
- Keep changes accessible in keyboard-only flows and avoid relying only on color for status.
- Preserve `--plain` and `--compact` output paths when adding presentation features.
- Add new UI colors through semantic theme roles rather than hard-coded meaning-bearing colors.

## Repository workflow

CI, CodeQL, and Security checks run for pull requests. Superseded runs are cancelled so the newest commit is the verification target. Repository-level branch protection, labels, Discussions, milestones, and release guidance are documented in [`github_repository.md`](github_repository.md).

## Commit style

Prefer focused Conventional Commits such as `feat: add ...`, `fix: handle ...`, `test: cover ...`, `docs: document ...`, `refactor: simplify ...`, `perf: optimize ...`, `build: configure ...`, `ci: verify ...`, and `chore: maintain ...`.

The requested local Git identity email is `sanskarin@outlook.in`.
