## What changed

Describe the focused change.

## Why

Explain the user/developer problem being solved.

## Validation

- [ ] `ruff check .`
- [ ] `ruff format --check .`
- [ ] `mypy src/guessnova`
- [ ] `pytest`
- [ ] `python -m compileall -q src tests scripts`
- [ ] `python scripts/verify_release_metadata.py`
- [ ] `python scripts/smoke_test.py`

## Privacy / compatibility / accessibility

- [ ] No telemetry or unexpected runtime network behavior was added.
- [ ] Persistence changes are backward-compatible or include a documented real migration.
- [ ] New local-data deletion behavior is confirmed/recoverable where practical.
- [ ] New presentation messages are represented in every shipped locale where applicable.
- [ ] Stable serialized/command identifiers were not translated accidentally.
- [ ] Essential UI information does not rely on color alone.
- [ ] Keyboard focus/bindings remain usable for changed interactive flows.
- [ ] Tests use temporary/deterministic state instead of real user data.

## Release impact

- [ ] `CHANGELOG.md` updated when user-visible behavior changed.
- [ ] `what_changed.md` updated when release/continuation state changed.
- [ ] Manual accessibility/media evidence requirements were considered for UI changes.
