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

## Persistence / backup / diagnostics

- [ ] A real schema change includes migration fixtures for the previous supported schema.
- [ ] Future state schemas are still rejected rather than downgraded.
- [ ] Backup-wrapper versioning remains independent from state-schema versioning.
- [ ] Backup integrity/schema-provenance behavior has focused regression coverage when changed.
- [ ] Legacy supported backups remain readable or the compatibility break is explicitly documented and versioned.
- [ ] Repair paths preserve the original payload before writing and refuse state they cannot safely normalize.
- [ ] `guessnova-doctor --json` remains one valid JSON document on changed normal/error/repair paths.

## Privacy / compatibility / accessibility

- [ ] No telemetry, cloud sync, account requirement, or unexpected runtime network behavior was added.
- [ ] Persistence changes are backward-compatible or include a documented real migration.
- [ ] New local-data deletion behavior is confirmed/recoverable where practical.
- [ ] New presentation messages are represented in every shipped locale where applicable.
- [ ] Stable serialized/command/backup/diagnostic identifiers were not translated accidentally.
- [ ] Essential UI information does not rely on color alone.
- [ ] Keyboard focus/bindings remain usable for changed interactive flows.
- [ ] Tests use temporary/deterministic state instead of real user data.
- [ ] Fixtures, exports, repair backups, logs, and screenshots contain no real private user data.

## Release impact

- [ ] `CHANGELOG.md` updated when user-visible behavior changed.
- [ ] `what_changed.md` updated when release/continuation state changed.
- [ ] Package/runtime/citation/changelog versions are synchronized for a release change.
- [ ] Built-wheel entry-point changes are covered by the cross-platform package matrix.
- [ ] Manual accessibility/media evidence requirements were considered for UI changes.
