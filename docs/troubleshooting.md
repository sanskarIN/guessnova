# Troubleshooting

## `guessnova`, `guessnova-tui`, or `guessnova-doctor` is not found

Activate the project virtual environment and reinstall:

```bash
python -m pip install -e .
```

You can also run the main game CLI with `python -m guessnova`.

## Python version error

GuessNova requires Python 3.13+. Check:

```bash
python --version
```

## Local data appears corrupted or old

GuessNova stores versioned JSON under its application-data directory. Inspect it without modifying state:

```bash
guessnova-doctor
guessnova-doctor --json
```

A schema-0/schema-1 file may simply need supported forward migration to schema 2. The doctor reports this as attention rather than silently claiming the old file is already current.

For a readable, repairable state that needs explicit normalization:

```bash
guessnova-doctor --repair
```

Repair asks for confirmation and creates an integrity-protected pre-repair backup before writing normalized state. Use `--backup-dir PATH` to choose the backup location. Unreadable JSON, non-object state, and unsupported future schemas are not silently overwritten.

Always preserve the original state/backup while investigating a problem. Set `GUESSNOVA_HOME` to a temporary directory when reproducing recovery steps.

## Import is rejected

Current backups use wrapper version 2, which includes the embedded payload schema and SHA-256 integrity metadata. GuessNova also accepts legacy wrapper-version-1 backups when their embedded state schema is supported.

Import is intentionally rejected for cases such as:

- wrong `guessnova-export` marker;
- invalid/future wrapper version;
- future state schema;
- wrapper/payload schema mismatch;
- missing/invalid integrity metadata in wrapper v2;
- changed payload whose SHA-256 digest no longer matches;
- invalid JSON/non-object payload;
- oversized backup file.

Do not edit the digest to force an import. If a backup was intentionally changed, create a fresh valid backup from supported state instead.

## Replay code is rejected

Replay codes are checksum protected. A changed/truncated code is intentionally rejected. Generate a new code from a completed saved challenge.

## Doctor exits with status 2

Exit status 2 means the doctor found state that requires attention or encountered an expected state/filesystem error. Review the reported issues. A normal schema migration/normalization requirement can often be handled with `--repair`; unreadable state should be restored/replaced from a known backup rather than force-written.

## Doctor JSON is used by a script

Use:

```bash
guessnova-doctor --json
```

The command emits one JSON document, including repair/error paths designed for scripting. Do not mix it with terminal prompts in unattended scripts; use `--repair --yes` only when the script intentionally authorizes a repair and has a suitable backup location.

## Terminal styling is difficult to read

Try a terminal with modern Unicode/ANSI support and use profile settings/high-contrast theme where available. Core CLI commands remain keyboard-driven and do not require mouse input.

For unresolved problems, see `SUPPORT.md` and include OS, Python version, GuessNova version/commit, command, and non-sensitive error output. Do not attach personal state/backup files publicly unless you have reviewed and intentionally removed private data.
