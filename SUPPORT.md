# Support

For help using GuessNova, open a GitHub issue when the question and diagnostic information can be discussed publicly.

Before reporting a local-state problem, run the recommended read-only Doctor route:

```bash
guessnova doctor
guessnova doctor --json
```

For a specific local data directory:

```bash
guessnova doctor --json --data-dir ./data
```

The standalone compatibility route remains available:

```bash
guessnova-doctor --json
```

Doctor is local-only and can identify schema migration/normalization requirements without changing state. If a supported repair is appropriate, `guessnova doctor --repair` creates a pre-repair backup before writing normalized state.

Before reporting a backup problem, preflight it without importing:

```bash
guessnova doctor --json --verify-backup ./guessnova-backup.json
```

Backup preflight validates supported wrapper/integrity/schema rules and current state normalizability. A structurally valid result is not proof of who created the backup.

## What to include in a public issue

Prefer non-sensitive details:

- operating system;
- Python version;
- GuessNova version/commit;
- command that failed;
- exit code;
- Doctor `report_version`;
- Doctor result `kind`;
- concise error/issue message;
- healthy/attention/unreadable status where relevant;
- source/current schema numbers when relevant;
- backup wrapper/source/normalized schema versions when relevant;
- whether the issue reproduces with an isolated `--data-dir`.

Review diagnostic JSON before sharing it. Doctor output can contain an active local profile name, selected local paths, and aggregate counts. Do **not** publicly upload `state.json`, exported backups, pre-repair backups, private Doctor reports, replay codes containing personally meaningful data, credentials, private terminal history, or other files you have not reviewed.

## Doctor exit codes

- `0` — success / healthy state / valid backup / successful or no-op repair.
- `1` — interactive repair cancelled.
- `2` — attention required or handled validation/filesystem error.

For scripted repair, `--json --repair` requires `--yes` so stdout remains one machine-readable JSON document.

## Private support

For support that should not be public, contact `supportramsandesh@gmail.com`.

Business contact:

- `sanskarin@outlook.in`
- `sanskarin.business@gmail.com`

Project home: `https://github.com/sanskarIN/guessnova`

Support development: `https://buymeacoffee.com/sanskarIN`

Full recovery guide: `docs/doctor.md`

**Made by the Sanskar**
