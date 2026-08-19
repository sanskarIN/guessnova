# Troubleshooting

## `guessnova`, `guessnova-tui`, or `guessnova-doctor` is not found

Activate the project virtual environment and reinstall:

```bash
python -m pip install -e .
```

Verify the installed routes:

```bash
python -m guessnova --help
guessnova doctor --help
guessnova-doctor --help
```

`guessnova doctor` is the recommended diagnostics route. `guessnova-doctor` remains the standalone compatibility entry point.

## Python version error

GuessNova requires Python 3.13+. Check:

```bash
python --version
```

## Local data appears corrupted, oversized, or old

GuessNova stores versioned JSON under its application-data directory. Inspect it without modifying state:

```bash
guessnova doctor
guessnova doctor --json
```

For a specific directory without changing `GUESSNOVA_HOME`:

```bash
guessnova doctor --data-dir ./suspect-data
guessnova doctor --json --data-dir ./suspect-data
```

A schema-0/schema-1 file may simply need supported forward migration to schema 2. Doctor reports this as attention rather than silently claiming the old file is already current.

State reads are byte bounded. An oversized file is rejected before normal JSON processing and is not repairable automatically.

For readable, supported state that needs explicit normalization:

```bash
guessnova doctor --repair
```

Repair asks for confirmation and creates an integrity-protected pre-repair backup before writing normalized state. Use `--backup-dir PATH` to choose the backup location. Unreadable JSON, non-object state, oversized state, unsupported future schemas, and other unnormalizable state are not silently overwritten.

Always preserve the original state/backup while investigating a problem. Use a temporary `GUESSNOVA_HOME` or explicit `--data-dir` when reproducing recovery steps.

## Validate a backup before importing it

Use the read-only preflight first:

```bash
guessnova doctor --verify-backup ./guessnova-backup.json
guessnova doctor --json --verify-backup ./guessnova-backup.json
```

A valid preflight means the supported wrapper passed validation and the embedded payload can pass current state normalization. It does **not** prove who created the file.

Backup verification reports whether the source is a legacy wrapper, whether wrapper-v2 integrity is present, source/normalized schema versions, whether normalization would change the payload, and normalized state counts. It does not write application state.

## Import is rejected

Current backups use wrapper version 2, which includes the embedded payload schema and SHA-256 integrity metadata. GuessNova also accepts legacy wrapper-version-1 backups when their embedded state schema is supported.

Import or Doctor preflight is intentionally rejected for cases such as:

- wrong `guessnova-export` marker;
- invalid/future wrapper version;
- future state schema;
- wrapper/payload schema mismatch;
- missing/invalid integrity metadata in wrapper v2;
- changed payload whose SHA-256 digest no longer matches;
- invalid JSON/non-object payload;
- oversized backup file;
- checksum-valid payload that cannot pass current state normalization.

Do not edit the digest to force an import. If a backup was intentionally changed, create a fresh valid backup from supported state instead.

## Backup preflight reports `normalization_changed=true`

This can be expected for a supported legacy state schema or a payload containing values that current normalization safely canonicalizes. The report also provides `schema_version` and `normalized_schema_version`.

Preflight does not rewrite the backup or state. If the file is deliberately being restored, normal import/save will persist current normalized state.

## Replay code is rejected

Replay codes are checksum protected. A changed/truncated code is intentionally rejected. Generate a new code from a completed saved challenge.

## Doctor exits with status 1

Exit status `1` means an interactive repair was cancelled. No repair write is performed.

## Doctor exits with status 2

Exit status `2` means Doctor found state requiring attention or encountered a handled validation/filesystem error. Review the reported issues. A supported schema migration/normalization requirement can often be handled with `--repair`; unreadable/oversized/future-schema state should be preserved and restored/replaced from a known backup rather than force-written.

## Doctor JSON is used by a script

Use:

```bash
guessnova doctor --json
```

The current machine contract has `report_version: 1` and document kinds `state`, `backup`, or `error`.

For unattended repair, `--json --repair` requires `--yes`:

```bash
guessnova doctor --json --repair --yes --backup-dir ./repair-backups
```

This rule prevents an interactive prompt from corrupting machine-readable stdout. Exit codes are stable: `0` success/healthy/valid, `1` cancelled repair, `2` attention/error.

## Doctor backup verification cannot be combined with another option

`--verify-backup` is a separate read-only mode and cannot be combined with `--repair`, `--yes`, `--backup-dir`, or `--data-dir`. Run backup preflight and state diagnosis/repair as separate commands.

## Terminal styling is difficult to read

Try a terminal with modern Unicode/ANSI support and use profile settings/high-contrast theme where available. Core CLI and Doctor commands remain keyboard-driven and do not require mouse input. `--plain` is available for reduced terminal styling.

For unresolved problems, see `SUPPORT.md` and [`doctor.md`](doctor.md). Include OS, Python version, GuessNova version/commit, command, Doctor report version, and non-sensitive error output. Do not attach personal state/backup files publicly unless you have reviewed and intentionally removed private data.
