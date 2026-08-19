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
guessnova-tui
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
guessnova-tui
guessnova doctor --help
guessnova-doctor --help
```

## Installed entry points

A normal installation provides:

```text
guessnova          primary CLI dispatcher for gameplay/data commands and `doctor`
guessnova-tui      six-pane Textual workspace with v1.5 Play challenge setup
guessnova-doctor   standalone Doctor compatibility entry point
```

`python -m guessnova` uses the same top-level dispatcher as the installed `guessnova` script.

## Textual workspace

Launch:

```bash
guessnova-tui
```

GuessNova starts on Play with the numeric guess input focused. Workspace panes:

```text
Ctrl+1  Play
Ctrl+2  Profiles
Ctrl+3  History
Ctrl+4  Leaderboard
Ctrl+5  Settings
Ctrl+6  Recovery
Ctrl+R  New round
Ctrl+Q  Quit
```

The workspace provides:

- normal Textual gameplay/hints/result persistence;
- v1.5 Challenge Setup for Classic, Timed, Streak, and Daily numeric challenges;
- difficulty selection from the same registry used by the engine;
- optional deterministic integer seed for Classic/Timed/Streak;
- Daily `YYYY-MM-DD` selection, with blank date resolving to the local current date when started;
- target-free active challenge identity;
- local profile create/use/rename/recoverable-delete/restore;
- active-profile statistics and achievements;
- bounded history filtering;
- local leaderboard filtering;
- local profile settings;
- high-contrast TUI focus/border behavior;
- read-only state diagnostics;
- read-only backup verification.

Reverse mode has a different interaction model and remains available through:

```bash
guessnova reverse
```

### Challenge Setup behavior

For Classic, Timed, and Streak, the optional seed field is active and the Daily date field is disabled. For Daily, the seed field is disabled and the date field is active.

Example deterministic challenge configuration:

```text
Mode: timed
Difficulty: hard
Seed: 20260819
```

Example Daily configuration:

```text
Mode: daily
Difficulty: normal
Date: 2026-08-19
```

Press **Start Challenge** after choosing the configuration. A valid challenge replaces the current round, updates the range/attempt display, shows its identity without exposing the hidden target, and returns focus to Guess.

Invalid seed/date text is rejected before the current round is replaced. Existing target and attempt state remain active, and focus moves to the field that needs correction.

For a configured seeded or Daily challenge, `Ctrl+R` reconstructs that deterministic challenge. Plain `R` and `Q` remain commands only while the numeric Guess field is focused; ordinary text inputs receive those letters normally.

Changing the active profile resets an unfinished round. This prevents a partially played game from being saved under a different profile.

A locale change is persisted immediately but full TUI relabeling happens on the next launch. This keeps one running interface linguistically consistent.

Recovery repair is intentionally not available as a TUI button. Use Doctor for an explicit repair workflow:

```bash
guessnova doctor --repair
```

See [`tui_workspace.md`](tui_workspace.md) for complete workspace behavior and [`tui_challenges.md`](tui_challenges.md) for challenge semantics.

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

The same backup-preflight logic is available read-only from the TUI Recovery pane.

Repairable migration/normalization changes can be applied only after confirmation. GuessNova creates a pre-repair backup before a required rewrite:

```bash
guessnova doctor --repair
guessnova doctor --repair --yes --backup-dir ./repair-backups
```

Do not run `--repair` merely because a state file is old; a normal GuessNova load/save also performs supported forward migration. Doctor is mainly for visibility, scripting, backup preflight, support diagnosis, and explicit normalization/repair workflows.

Doctor refuses oversized, undecodable, non-object, future-schema, or otherwise unnormalizable state. `--json --repair` requires `--yes` so machine output cannot be mixed with an interactive prompt.

See [`doctor.md`](doctor.md) for the full recovery contract.

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
python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
python -c "from guessnova.tui_challenge_app import GuessNovaApp; print(GuessNovaApp.TITLE)"
```

## Optional environment variables

- `GUESSNOVA_HOME` — override the default local application-data directory for normal commands and TUI state.
- `GUESSNOVA_SEED` — default deterministic seed for CLI challenges.

Doctor `--data-dir PATH` can inspect a specific GuessNova data directory without modifying `GUESSNOVA_HOME`.

GuessNova does not require API keys, accounts, telemetry credentials, or runtime network access.
