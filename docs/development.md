# Development

Use Python 3.13+ and install the development extras:

```bash
python -m pip install -e '.[dev]'
```

## Quality loop

```bash
pytest
ruff check .
python scripts/smoke_test.py
```

Before a release also build the package and run dependency/security checks configured in GitHub Actions.

## Engineering rules

- Keep `engine.py` and domain rules independent of terminal rendering and filesystem I/O.
- Use deterministic seeds or injected clocks in automated tests.
- Preserve save/replay compatibility unless a documented migration/version change is provided.
- Keep filesystem writes atomic and local by default.
- Prefer clear typed dataclasses and small focused functions.
- Add regression tests for confirmed bugs.
- Do not commit credentials, private endpoints, real player data, local state, caches, virtual environments, or build outputs.
- Keep changes accessible in keyboard-only flows and avoid relying only on color for status.

## Commit style

Prefer focused Conventional Commits such as `feat: add ...`, `fix: handle ...`, `test: cover ...`, `docs: document ...`, `refactor: simplify ...`, `perf: optimize ...`, `build: configure ...`, `ci: verify ...`, and `chore: maintain ...`.

The requested local Git identity email is `sanskarin@outlook.in`.
