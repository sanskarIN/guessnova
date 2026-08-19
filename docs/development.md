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
python scripts/verify_release_metadata.py
python scripts/smoke_test.py
```

Before a release also build and validate the package:

```bash
python -m pip install build twine pip-audit
python -m build
python -m twine check dist/*
pip-audit
```

Verify built entry points where practical:

```bash
python -m guessnova --help
guessnova-doctor --help
```

## Engineering rules

- Keep `engine.py` and domain rules independent of terminal rendering, diagnostics, backup envelopes, and filesystem I/O.
- Use deterministic seeds, explicit targets, dates, committed migration fixtures, or injected clocks in automated tests.
- Keep state-schema, backup-wrapper, and replay versions as separate compatibility domains.
- Introduce a new state schema only for a real canonical format boundary and add representative fixtures from the prior supported schema.
- Preserve older supported backup wrappers explicitly rather than guessing unknown versions.
- Treat imported/local JSON as untrusted and normalize it through storage/profile boundaries.
- Treat backup SHA-256 as integrity detection, not authentication/signing/encryption.
- Keep filesystem writes atomic and local by default.
- A repair operation must create a readable backup before a normalization write and must refuse data it cannot safely decode/normalize.
- Keep `guessnova-doctor --json` stable as one machine-readable JSON document.
- Prefer clear typed dataclasses and small focused functions.
- Keep strict mypy clean; avoid broad ignores that hide real type errors.
- Add regression tests for confirmed bugs.
- Do not commit credentials, private endpoints, real player data, local state, exports, repair backups, caches, virtual environments, or build outputs.
- Keep changes accessible in keyboard-only flows and avoid relying only on color for status.
- Preserve `--plain` and `--compact` output paths when adding presentation features.
- Add new UI colors through semantic theme roles rather than hard-coded meaning-bearing colors.

## State migration workflow

When a state schema changes:

1. document the concrete compatibility boundary;
2. increment `SCHEMA_VERSION`;
3. add a deterministic migration step from the immediately previous supported schema;
4. add committed old-schema fixtures under `tests/fixtures/state/`;
5. prove important data survives migration;
6. keep future-schema rejection;
7. update canonical/concise data docs, changelog, roadmap, release docs, and `what_changed.md`.

Do not bump the backup wrapper merely because the state schema changed. `EXPORT_VERSION` changes only when the backup envelope itself changes.

## Backup and doctor workflow

Changes in `storage.py`, `import_export.py`, `diagnostics.py`, or `doctor_cli.py` are related reliability boundaries. Review them together for:

- legacy compatibility;
- future-version rejection;
- wrapper/payload schema agreement;
- integrity validation;
- atomic writes;
- backup-before-repair ordering;
- safe failure without destructive overwrite;
- script-safe JSON behavior;
- privacy-safe support output.

## Repository workflow

CI, CodeQL, and Security checks run for pull requests. Superseded runs are cancelled so the newest commit is the verification target. The package matrix builds/installs on Ubuntu, Windows, and macOS and verifies both game and doctor entry points. Repository-level branch protection, labels, Discussions, milestones, and release guidance are documented in [`github_repository.md`](github_repository.md).

## Commit style

Prefer focused Conventional Commits such as `feat: add ...`, `fix: handle ...`, `test: cover ...`, `docs: document ...`, `refactor: simplify ...`, `perf: optimize ...`, `build: configure ...`, `ci: verify ...`, and `chore: maintain ...`.

The requested local Git identity email is `sanskarin@outlook.in`.
