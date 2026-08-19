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
guessnova-doctor --help
```

## Installed entry points

A normal installation provides:

```text
guessnova          Rich command-line game and local data commands
guessnova-tui      Textual app-like terminal interface
guessnova-doctor   local state diagnostics and safe normalization repair
```

## Local doctor

Inspect state without modifying it:

```bash
guessnova-doctor
guessnova-doctor --json
```

Repairable migration/normalization changes can be applied only after confirmation. GuessNova creates a pre-repair backup first:

```bash
guessnova-doctor --repair
guessnova-doctor --repair --yes --backup-dir ./repair-backups
```

Do not run `--repair` merely because a state file is old; a normal GuessNova load/save also performs supported forward migration. The doctor is mainly for visibility, scripting, and explicit normalization/repair workflows.

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
python scripts/verify_release_metadata.py
python scripts/smoke_test.py
```

## Optional environment variables

- `GUESSNOVA_HOME` — override the local application-data directory.
- `GUESSNOVA_SEED` — default deterministic seed for CLI challenges.

GuessNova does not require API keys, accounts, telemetry credentials, or runtime network access.
