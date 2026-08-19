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
python -m guessnova --help
python -m guessnova doctor --help
python -m guessnova.doctor_cli --help
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
```

`make check` runs the same core quality sequence plus entry-point verification on systems with Make available.

## Contribution rules

- Keep game/domain logic independent of Rich/Textual presentation, diagnostics, backup wrappers, command dispatch, and filesystem I/O.
- Keep `entrypoint.py` limited to routing; do not duplicate gameplay or Doctor business logic there.
- Keep reusable Textual workspace data/configuration behavior in `tui_workspace.py` when it does not require widget/focus knowledge.
- Keep `tui.py` focused on composition, focus, event handling, and presentation orchestration over existing application/local-adapter APIs.
- Add or update focused tests for behavior changes and regression fixes.
- Preserve deterministic behavior for seeded and daily challenges.
- Use temporary storage and deterministic targets/seeds/clocks in tests; never touch a contributor's real GuessNova state.
- Preserve keyboard-only operation and avoid color-only meaning.
- Keep destructive local-data operations confirmed and recoverable where practical.
- TUI profile deletion must retain exact-name confirmation and recoverable trash semantics unless an intentional safer design replaces it.
- Changing active TUI profile ownership must not allow a partially played round to be persisted under a different profile.
- TUI global bindings must not steal normal character input from profile/search/path fields; retain globally reliable Ctrl alternatives when single-letter shortcuts exist.
- Keep TUI Recovery read-only unless a separately reviewed design proves explicit confirmation and pre-repair backup guarantees.
- Keep one mounted TUI linguistically consistent; do not partially relabel only some widgets after a locale change.
- Keep state, replay, backup, and Doctor-report compatibility explicit. Do not invent a schema migration unless a concrete state-format boundary exists.
- When introducing a real schema migration, commit representative fixtures for the previous supported schema and test forward migration/future-schema rejection.
- Keep backup-wrapper versioning independent from state-schema versioning and Doctor-report versioning.
- Backup integrity changes must retain clear boundaries: unkeyed SHA-256 is corruption/change detection, not encryption, authentication, signing, or origin proof.
- Bound application-controlled/user-selected JSON file reads before decoding/parsing where practical.
- Maintain `MAX_EXPORT_BYTES > MAX_STATE_BYTES` so every accepted repairable state can fit inside its mandatory pre-repair backup.
- Backup preflight must validate current state normalization/importability before reporting a file as valid.
- A repair path must never rewrite unreadable/non-object/oversized/future-schema/unsupported state and must preserve the original payload in a recoverable backup before a required normalization write.
- Doctor `--json` is a scripting contract: keep it as one valid versioned JSON document on normal, attention, backup, repair, and expected-error paths.
- `--json --repair` must remain noninteractive unless `--yes` is explicitly supplied.
- Keep Doctor exit semantics stable unless an intentional compatibility change is documented, versioned, and tested.
- New user-facing presentation strings should use the offline message catalog where appropriate. Stable Doctor JSON keys/report kinds are machine identifiers and should remain untranslated.
- When adding/changing a catalog key, update every shipped locale and keep named placeholders compatible.
- Do not translate stable command names, environment variables, schema keys, replay fields, backup markers, diagnostic JSON keys, mode/difficulty IDs, or achievement IDs without a compatibility design.
- Never commit secrets, private production endpoints, real user data, local profile backups, repair backups, private Doctor reports, generated credentials, or release captures containing private terminal data.
- Update documentation, `CHANGELOG.md`, and `what_changed.md` for user-visible/release-relevant changes.
- Prefer small Conventional Commits such as `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `perf:`, `build:`, `ci:`, and `chore:`.

## Migration fixtures

Migration fixtures live under `tests/fixtures/state/`. Keep them minimal but realistic. A fixture should represent a previously supported on-disk state, not a synthetic future schema. New migrations must demonstrate:

- the old fixture loads;
- data intended to survive is preserved;
- new canonical fields are populated safely;
- the result reports the current schema;
- future schemas remain rejected.

Do not add schema-3 fixtures until schema 3 exists for a concrete compatibility reason.

## Backup changes

Changes to `import_export.py` or `backup_inspection.py` should consider the full boundary together. Add tests for:

- bounded single-read input;
- integrity metadata;
- schema provenance;
- legacy compatibility;
- future-version rejection;
- current state normalization/importability;
- checksum-valid but unimportable payload rejection;
- atomic export output;
- read-only backup preflight.

## Doctor/diagnostics changes

Changes to `diagnostics.py`, `doctor_cli.py`, `doctor_protocol.py`, `entrypoint.py`, or `storage.py` should cover relevant behavior across both:

```bash
guessnova doctor
guessnova-doctor
```

Review:

- explicit `--data-dir` isolation;
- Doctor report version/kinds;
- stable exit codes;
- `--version` consistency;
- JSON single-document behavior;
- backup verification option conflicts;
- bounded state reads/writes;
- repair backup readability;
- backup-before-write ordering;
- safe refusal paths;
- support-output privacy.

## Textual workspace changes

Use `Storage(tmp_path)` and deterministic/injected `GuessGame(...)` instances with Textual's `run_test()` pilot. Reusable non-widget behavior belongs in helper tests when practical.

When changing a pane, review relevant items:

- initial and post-action focus;
- Ctrl+number pane shortcuts;
- Tab/Shift+Tab navigation;
- normal text entry for `q`/`r` characters;
- completed-round exactly-once persistence;
- active-profile round isolation;
- recoverable deletion confirmation;
- history/leaderboard filter correctness;
- settings persistence and immediate-vs-next-launch behavior;
- high-contrast focus visibility;
- English/Hindi catalog completeness;
- read-only Recovery guarantees;
- temporary/private test state only.

Keep the focused pilot suites separated by concern rather than growing one giant scenario.

## Accessibility changes

Keep `docs/accessibility.md` current. Release-candidate changes affecting interaction, layout, contrast, localization, destructive actions, workspace focus, or Recovery behavior should also update the manual evidence checklist when needed. Automated pilot tests supplement rather than replace manual terminal review.

## Pull requests

Use the pull-request template, explain the user/developer problem, list verification performed, and keep unrelated cleanup out of feature/fix PRs. Security vulnerabilities should follow `SECURITY.md` rather than a public issue.

Before requesting review, verify that the PR's **current head**—not an earlier superseded commit—has the intended CI, CodeQL, and Security-check status. Queued/pending status is not a successful conclusion.

## Contact

- Business: `sanskarin@outlook.in`
- Business: `sanskarin.business@gmail.com`
- Support: `supportramsandesh@gmail.com`
- GitHub: https://github.com/sanskarIN
- Buy Me a Coffee: https://buymeacoffee.com/sanskarIN

**Made by the Sanskar**
