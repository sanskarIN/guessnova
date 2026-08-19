# Contributing to GuessNova

Thank you for helping improve GuessNova. Keep contributions focused, tested, accessible, privacy-preserving, deterministic where required, and easy to review.

## Development setup

```bash
git clone https://github.com/sanskarIN/guessnova.git
cd guessnova
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

## Required local quality loop

```bash
ruff check .
ruff format --check .
mypy src/guessnova
pytest
python -m compileall -q src tests scripts
python scripts/verify_release_metadata.py
python scripts/smoke_test.py
```

`make check` runs the same core quality sequence on systems with Make available.

## Contribution rules

- Keep game/domain logic independent of Rich/Textual presentation, diagnostics, backup wrappers, and filesystem I/O.
- Add or update focused tests for behavior changes and regression fixes.
- Preserve deterministic behavior for seeded and daily challenges.
- Use temporary storage and deterministic targets/seeds/clocks in tests; never touch a contributor's real GuessNova state.
- Preserve keyboard-only operation and avoid color-only meaning.
- Keep destructive local-data operations confirmed and recoverable where practical.
- Keep state, replay, and backup compatibility explicit. Do not invent a schema migration unless a concrete state-format boundary exists.
- When introducing a real schema migration, commit representative fixtures for the previous supported schema and test forward migration/future-schema rejection.
- Keep backup-wrapper versioning independent from state-schema versioning. Do not reuse one version integer for both compatibility domains.
- Backup integrity changes must retain clear boundaries: unkeyed SHA-256 is corruption/tamper detection, not encryption, authentication, or a signature.
- A repair path must never rewrite unreadable/non-object/unsupported state and must preserve the original payload in a recoverable backup before a normalization write.
- `guessnova-doctor --json` is a scripting contract: keep it as one valid JSON document on normal, attention, repair, and expected-error paths.
- New user-facing presentation strings should use the offline message catalog where appropriate. Stable diagnostic JSON keys are machine identifiers and should remain untranslated.
- When adding/changing a catalog key, update every shipped locale and keep named placeholders compatible.
- Do not translate stable command names, environment variables, schema keys, replay fields, backup markers, diagnostic JSON keys, mode/difficulty IDs, or achievement IDs without a compatibility design.
- Never commit secrets, private production endpoints, real user data, local profile backups, repair backups, generated credentials, or release captures containing private terminal data.
- Update documentation, `CHANGELOG.md`, and `what_changed.md` for user-visible/release-relevant changes.
- Prefer small Conventional Commits such as `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `perf:`, `build:`, `ci:`, and `chore:`.

## Migration fixtures

Migration fixtures live under `tests/fixtures/state/`. Keep them minimal but realistic. A fixture should represent a previously supported on-disk state, not a synthetic future schema. New migrations must demonstrate:

- the old fixture loads;
- data intended to survive is preserved;
- new canonical fields are populated safely;
- the result reports the current schema;
- future schemas remain rejected.

## Backup and diagnostics changes

Changes to `import_export.py`, `diagnostics.py`, `doctor_cli.py`, or `storage.py` should consider the full boundary together. Add tests for integrity metadata, schema provenance, legacy compatibility, atomic writes, repair backup readability, and JSON-mode CLI behavior when relevant.

## Textual changes

For TUI behavior, prefer dependency-injected `Storage(tmp_path)` and deterministic `GuessGame(...)` instances with Textual's `run_test()` pilot. Cover focus order, keyboard bindings, submission, and persistence when those areas change.

## Accessibility changes

Keep `docs/accessibility.md` current. Release-candidate changes affecting interaction, layout, contrast, localization, or destructive actions should also update the manual evidence checklist when needed. Automated pilot tests supplement rather than replace manual terminal review.

## Pull requests

Use the pull-request template, explain the user/developer problem, list verification performed, and keep unrelated cleanup out of feature/fix PRs. Security vulnerabilities should follow `SECURITY.md` rather than a public issue.

Before requesting review, verify that the PR's current head—not an earlier superseded commit—has the intended CI, CodeQL, and Security-check status.

## Contact

- Business: `sanskarin@outlook.in`
- Business: `sanskarin.business@gmail.com`
- Support: `supportramsandesh@gmail.com`
- GitHub: https://github.com/sanskarIN
- Buy Me a Coffee: https://buymeacoffee.com/sanskarIN

**Made by the Sanskar**
