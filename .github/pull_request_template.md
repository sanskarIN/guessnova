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
- [ ] `python -m guessnova --help`
- [ ] `python -m guessnova doctor --help`
- [ ] `python -m guessnova.doctor_cli --help`

## Persistence / backup / Doctor

- [ ] A real state-schema change includes migration fixtures for the previous supported schema; no future schema was invented just to satisfy a roadmap item.
- [ ] Future state schemas are still rejected rather than downgraded.
- [ ] State input/output size bounds remain enforced before unsafe processing/final persistence when relevant.
- [ ] Backup-wrapper versioning remains independent from state-schema, replay, and Doctor-report versioning.
- [ ] Backup reads/metadata use one bounded validated source when relevant.
- [ ] Backup integrity/schema-provenance behavior has focused regression coverage when changed.
- [ ] Legacy supported backups remain readable or the compatibility break is explicitly documented and versioned.
- [ ] Backup preflight proves current state normalization/importability before reporting a backup as valid.
- [ ] `MAX_EXPORT_BYTES > MAX_STATE_BYTES` remains true.
- [ ] Repair paths preserve the original payload before a required write and refuse state they cannot safely normalize.
- [ ] `guessnova doctor` and `guessnova-doctor` remain behaviorally aligned.
- [ ] Doctor JSON remains one valid versioned document on changed state/backup/error/repair paths.
- [ ] JSON repair remains noninteractive unless `--yes` is explicit.
- [ ] Doctor report-version and exit-code semantics remain compatible or the change is explicitly versioned/documented.

## Privacy / compatibility / accessibility

- [ ] No telemetry, cloud sync, account requirement, or unexpected runtime network behavior was added.
- [ ] Persistence changes are backward-compatible or include a documented real migration.
- [ ] New local-data deletion behavior is confirmed/recoverable where practical.
- [ ] New presentation messages are represented in every shipped locale where applicable.
- [ ] Stable serialized/command/backup/Doctor identifiers were not translated accidentally.
- [ ] Essential UI information does not rely on color alone.
- [ ] Keyboard focus/bindings remain usable for changed interactive flows.
- [ ] Tests use temporary/deterministic state instead of real user data.
- [ ] Fixtures, exports, repair backups, Doctor reports, logs, and screenshots contain no real private user data.
- [ ] Integrity checks are not described as encryption, authentication, signing, or origin proof.

## Release impact

- [ ] `CHANGELOG.md` updated when user-visible behavior changed.
- [ ] `what_changed.md` updated when release/continuation state changed.
- [ ] Package/runtime/citation/changelog versions are synchronized for a release change.
- [ ] Built-wheel entry-point changes are covered by the cross-platform package matrix.
- [ ] Exact current-head CI/CodeQL/Security status was checked; queued/pending/older-head results were not recorded as passes.
- [ ] Manual accessibility/media evidence requirements were considered for UI changes.
