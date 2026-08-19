# GuessNova

<p align="center">
  <img src="assets/banner.svg" alt="GuessNova — number guessing, supernova style" width="820" />
</p>

<p align="center">
  <a href="https://github.com/sanskarIN/guessnova/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/sanskarIN/guessnova/ci.yml?branch=main&label=CI"></a>
  <a href="https://github.com/sanskarIN/guessnova/actions/workflows/codeql.yml"><img alt="CodeQL" src="https://img.shields.io/github/actions/workflow/status/sanskarIN/guessnova/codeql.yml?branch=main&label=CodeQL"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://www.python.org/"><img alt="Python 3.13+" src="https://img.shields.io/badge/python-3.13%2B-3776AB.svg"></a>
  <a href="https://buymeacoffee.com/sanskarIN"><img alt="Buy Me a Coffee" src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20GuessNova-FFDD00?logo=buymeacoffee&logoColor=000000"></a>
</p>

> **Made by the Sanskar**

**GuessNova** is a production-minded, privacy-first number guessing game for Python terminals. It turns a familiar game into a polished local product with multiple modes, deterministic friend/daily challenges, replay codes, smart and explicit hints, recoverable profiles, rich session history, achievements, XP, statistics, a leaderboard, integrity-protected backup/restore, read-only backup verification, local diagnostics/repair, bilingual presentation, first-run onboarding, semantic themes, and both Rich CLI and Textual TUI interfaces.

## Demo

Real release captures belong in `docs/media/` and must come from a signed-off build. Until then, the CLI flow looks like:

```text
GuessNova · Classic · Normal · 1–100
Guess [9 left] › 50
Too low.
Hint: warm; try higher. The target is odd.
Guess [8 left] › hint
Range hint: the target is between 62 and 82. Using it costs 10 XP from a winning reward.
```

## Features

- **Classic** — focused number guessing with difficulty-based ranges and attempt budgets.
- **Timed** — solve before the difficulty-specific timer expires.
- **Streak** — play streak-tagged rounds and build persistent profile streaks.
- **Reverse** — think of a number and let GuessNova find it with binary search.
- **Daily Challenge** — date-seeded, reproducible challenges shared by players using the same rules version.
- **Smart hints** — temperature, direction, and parity feedback after guesses.
- **Explicit range hints** — type `hint` for a narrowed range clue, with optional XP penalty via `--hint-penalty` / `--no-hint-penalty`.
- **Profiles** — local stats, average guesses, streaks, XP, settings, achievements, and bounded session history.
- **Safe profile lifecycle** — list, create, activate, rename, delete, inspect recoverable trash, and restore profiles without permanent one-command deletion.
- **Advanced history** — filter by mode, difficulty, result, date range, free-text search, and group by day/mode/difficulty/result.
- **First-run onboarding** — concise keyboard/privacy/settings guidance with no sign-in or network requirement.
- **Replay codes** — checksum-protected, strictly validated portable summaries for completed challenges.
- **Local leaderboard** — ranked winning results stored on your device; profile rename/delete/restore keeps related local data coherent.
- **Schema-2 persistence** — explicit migration from older saves with committed migration fixtures and future-schema rejection.
- **Integrity-protected backups** — backup wrapper v2 separates backup-format versioning from state schema and verifies SHA-256 payload integrity while retaining legacy backup compatibility.
- **Backup preflight** — `guessnova doctor --verify-backup PATH` validates wrapper integrity, schema metadata, and current importability without writing state.
- **Local doctor** — `guessnova doctor` inspects schema/profile/history/leaderboard/trash health and can safely normalize repairable state after creating a pre-repair backup; `guessnova-doctor` remains a compatible standalone entry point.
- **Bounded persistence I/O** — state and backup readers reject oversized input before unbounded JSON processing, and state saves are size checked before atomic replacement.
- **Scriptable diagnostics** — Doctor JSON report protocol v1 plus stable exit codes for healthy/valid, cancelled, and attention/error states.
- **Deterministic test mode** — use `--seed` or `GUESSNOVA_SEED` for reproducibility.
- **Accessible terminal modes** — `--plain` disables color and `--compact` prefers concise text over panels/tables.
- **Keyboard-first TUI** — predictable focus order, Enter submission, range-hint control, reliable reset/quit bindings, and persisted completed rounds.
- **Themes and contrast** — saved semantic Rich themes plus a dedicated high-contrast palette.
- **English + Hindi** — complete offline `en` and `hi` message catalogs with English fallback and per-profile locale settings.
- **Privacy-first** — no accounts, ads, analytics, telemetry, cloud sync, or application network calls.

## Supported platforms

- Windows 10/11
- Current macOS releases with Python 3.13+
- Modern Linux distributions with Python 3.13+

A Unicode/ANSI-capable terminal provides the richest presentation, but `--plain` remains available for reduced formatting. CI builds, validates, installs, launches the game and both doctor routes, and smoke-tests the package on Windows, macOS, and Linux runners.

## Tech stack

- **Python 3.13+** for domain/application code.
- **Rich** for accessible terminal presentation.
- **Textual** for the app-like TUI and deterministic pilot testing.
- **JSON** for versioned local persistence, backup wrappers, and replay payloads.
- **SHA-256** from Python's standard library for backup/replay integrity checks.
- **pytest / pytest-cov** for automated tests.
- **Ruff**, **mypy**, **pip-audit**, **CodeQL**, and **GitHub Actions** for repository quality and security automation.

## Quick start

```bash
git clone https://github.com/sanskarIN/guessnova.git
cd guessnova
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
guessnova play
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
guessnova play
```

See [`docs/setup.md`](docs/setup.md) for full setup details.

## Play and manage local data

```bash
guessnova play
guessnova play --difficulty hard
guessnova play --mode timed --difficulty expert
guessnova play --mode daily
guessnova play --mode daily --day 2026-08-19
guessnova play --seed 20260819 --no-save
guessnova reverse
guessnova stats
guessnova leaderboard
```

### History

```bash
guessnova history --limit 20
guessnova history --result win --difficulty hard
guessnova history --since 2026-08-01 --until 2026-08-31
guessnova history --search daily --group-by mode
guessnova --plain --compact history --group-by result
```

### Profiles and undoable deletion

```bash
guessnova profiles list
guessnova profiles create Nova
guessnova profiles use Nova
guessnova profiles rename Nova Explorer
guessnova profiles delete Explorer
guessnova profiles trash
guessnova profiles restore Explorer
```

Profile deletion normally asks you to type the profile name before moving it to recoverable local trash. `--yes` is available for intentional scripted deletion. Recoverable trash is bounded to the most recent 20 deleted profiles.

### Settings and localization

```bash
guessnova settings
guessnova settings --theme mono --reduced-motion --no-smart-hints
guessnova settings --high-contrast
guessnova settings --locale en
guessnova settings --locale hi
guessnova --plain --compact about
```

### Backup, diagnostics, and recovery

```bash
guessnova export ./guessnova-backup.json
guessnova doctor --verify-backup ./guessnova-backup.json
guessnova doctor --json --verify-backup ./guessnova-backup.json
guessnova import ./guessnova-backup.json

guessnova doctor
guessnova doctor --compact
guessnova doctor --json
guessnova doctor --data-dir ./alternate-data
guessnova doctor --repair
guessnova doctor --repair --yes --backup-dir ./guessnova-repair-backups

# Compatibility entry point
guessnova-doctor --help
```

A normal Doctor state run and `--verify-backup` are read-only. Repair requires confirmation unless `--yes` is provided, refuses unreadable/oversized/future-schema/un-normalizable state, and writes an integrity-protected backup before normalization when a rewrite is needed. `--json` emits one versioned JSON document; `--json --repair` requires `--yes` so an interactive prompt cannot corrupt machine-readable output.

Doctor exit codes are stable: `0` success/healthy/valid, `1` repair cancelled, and `2` attention or validation failure. See [`docs/doctor.md`](docs/doctor.md).

### Textual interface

```bash
guessnova-tui
```

For deterministic non-daily play you may also set:

```bash
GUESSNOVA_SEED=20260819 guessnova play --no-save
```

## Data, privacy, and security

GuessNova stores data only in a local application-data directory; set `GUESSNOVA_HOME` to choose a custom location. Saves use schema-2 normalized JSON and atomic replacement. Local state reads/writes are bounded; backup reads are separately bounded. Backup wrapper v2 records the embedded source schema and verifies a canonical SHA-256 payload digest before import. Legacy version-1 GuessNova backups remain readable when their state schema is supported. Doctor backup verification additionally proves the embedded state can pass current normalization before reporting the backup as valid. Recoverable profile trash is bounded, and replay text is length-bounded, checksum checked, field-allowlisted, and range validated before use. The runtime needs no account, API key, telemetry endpoint, cloud service, or network connection.

Read [`PRIVACY.md`](PRIVACY.md), [`SECURITY.md`](SECURITY.md), [`docs/data_format.md`](docs/data_format.md), and [`docs/doctor.md`](docs/doctor.md).

## Development and testing

```bash
python -m pip install -e '.[dev]'
ruff check .
ruff format --check .
mypy src/guessnova
pytest --cov=guessnova --cov-report=term-missing
python -m compileall -q src tests scripts
python scripts/verify_release_metadata.py
python scripts/smoke_test.py
python -m guessnova --help
python -m guessnova doctor --help
python -m build
```

The repository CI runs linting, formatting, strict typing, tests, migration fixtures, backup-integrity/importability regressions, bounded state-I/O regressions, doctor/repair protocol regressions, Textual pilot coverage, coverage reporting, bytecode compilation, release-metadata verification, smoke testing, cross-platform package build/install/Twine validation, both doctor entry-path checks, dependency auditing, secret-material checks, and CodeQL analysis. Replay/import boundaries retain deterministic malformed-input/fuzz-style regression coverage. See [`docs/development.md`](docs/development.md) and [`docs/testing.md`](docs/testing.md).

## Architecture

GuessNova is a modular monolith with UI-independent game rules:

```text
Top-level command dispatcher
        /          \
   Rich game CLI   Doctor CLI
          \        /
        application services       Textual TUI
          /            \               |
      domain        local adapters -----+
     (engine)  (storage/replay/backup/diagnostics)
```

The dispatcher only routes command families; it does not duplicate game rules or recovery logic. The core engine has no Rich/Textual or filesystem dependency, making seeded gameplay deterministic and directly testable. State migration, backup integrity, diagnostics, and repair remain local adapter/application concerns rather than game-rule concerns. Presentation messages resolve through offline English/Hindi catalogs while serialized identifiers remain stable. See [`docs/architecture.md`](docs/architecture.md), [`docs/localization.md`](docs/localization.md), and [`docs/adr/`](docs/adr/).

## Build and release

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Semantic tags are handled by a quality-gated GitHub release workflow. The tag must match the package version, and release artifacts are blocked until strict verification and Windows/macOS/Linux package checks succeed. Built wheels must expose the game CLI, the `guessnova doctor` route, and the standalone doctor compatibility entry point. Release candidates additionally require documented manual accessibility evidence. Real screenshot/demo media must be captured from the exact signed-off build rather than fabricated by automation.

See [`docs/release.md`](docs/release.md), [`docs/accessibility_evidence_template.md`](docs/accessibility_evidence_template.md), [`docs/media/README.md`](docs/media/README.md), and [`CHANGELOG.md`](CHANGELOG.md).

## Documentation

- [Setup](docs/setup.md)
- [Development](docs/development.md)
- [Architecture](docs/architecture.md)
- [Game modes](docs/game_modes.md)
- [Data format](docs/data_format.md)
- [Doctor diagnostics and recovery](docs/doctor.md)
- [v1.2 reliability plan](docs/v1_2_reliability_plan.md)
- [Localization](docs/localization.md)
- [Accessibility](docs/accessibility.md)
- [Accessibility evidence template](docs/accessibility_evidence_template.md)
- [Testing](docs/testing.md)
- [Performance](docs/performance.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Release process](docs/release.md)
- [Release media](docs/media/README.md)
- [GitHub repository operations](docs/github_repository.md)
- [Architecture decisions](docs/adr/)
- [Branding](docs/BRANDING.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Work continuity](what_changed.md)

## Contributing

Issues and pull requests are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) first. Security vulnerabilities should follow the private reporting guidance in [`SECURITY.md`](SECURITY.md) rather than being published as exploit details in a normal issue.

## License

GuessNova is open source under the [MIT License](LICENSE).

## Contact and support

- Business: **sanskarin@outlook.in**
- Business: **sanskarin.business@gmail.com**
- Support: **supportramsandesh@gmail.com**
- GitHub: **https://github.com/sanskarIN**
- Repository: **https://github.com/sanskarIN/guessnova**

## Support the project

<a href="https://buymeacoffee.com/sanskarIN"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-@sanskarIN-FFDD00?logo=buymeacoffee&logoColor=000000" alt="Buy Me a Coffee @sanskarIN"></a>

Support is optional; every GuessNova feature remains fully usable without donating.

**Made by the Sanskar**
