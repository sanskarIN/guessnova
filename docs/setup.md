# Setup

## Requirements

- Python 3.13+
- Git
- Windows 10/11, current macOS, or a modern Linux distribution
- UTF-8 terminal recommended

## Windows PowerShell

```powershell
git clone https://github.com/sanskarIN/guessnova.git
cd guessnova
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
guessnova play
guessnova doctor --help
guessnova-doctor --help
```

## macOS / Linux

```bash
git clone https://github.com/sanskarIN/guessnova.git
cd guessnova
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
guessnova play
guessnova doctor --help
guessnova-doctor --help
```

## Installed entry points

A normal installation provides:

```text
guessnova          primary CLI dispatcher for gameplay/data commands and `doctor`
guessnova-tui      Textual app-like terminal interface
guessnova-doctor   standalone Doctor compatibility entry point
```

`python -m guessnova` uses the same top-level dispatcher as the installed `guessnova` script.

## Local Doctor

Recommended state inspection:

```bash
guessnova doctor
guessnova doctor --json
guessnova doctor --data-dir ./alternate-data
```

Compatibility route:

```bash
guessnova-doctor --json
```

Verify a backup before import without writing state:

```bash
guessnova doctor --verify-backup ./guessnova-backup.json
guessnova doctor --json --verify-backup ./guessnova-backup.json
```

Repairable migration/normalization changes can be applied only after confirmation. GuessNova creates a pre-repair backup before a required rewrite:

```bash
guessnova doctor --repair
guessnova doctor --repair --yes --backup-dir ./repair-backups
```

Do not run `--repair` merely because a state file is old; a normal GuessNova load/save also performs supported forward migration. Doctor is mainly for visibility, scripting, backup preflight, support diagnosis, and explicit normalization/repair workflows.

Doctor refuses oversized, undecodable, non-object, future-schema, or otherwise unnormalizable state. `--json --repair` requires `--yes` so machine output cannot be mixed with an interactive prompt.

See [`doctor.md`](doctor.md) for the full recovery contract.

## Textual interface

```bash
guessnova-tui
```

## Development dependencies

```bash
python -m pip install -e '.[dev]'
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
```

## Optional environment variables

- `GUESSNOVA_HOME` — override the default local application-data directory for normal commands.
- `GUESSNOVA_SEED` — default deterministic seed for CLI challenges.

Doctor `--data-dir PATH` can inspect a specific GuessNova data directory without modifying `GUESSNOVA_HOME`.

GuessNova does not require API keys, accounts, telemetry credentials, or runtime network access.
