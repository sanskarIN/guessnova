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

**GuessNova** is a production-minded, privacy-first number guessing game for Python terminals. It turns a familiar game into a polished local product with multiple modes, deterministic friend/daily challenges, replay codes, smart and explicit hints, recoverable profiles, rich session history, achievements, XP, statistics, a leaderboard, backup/restore, bilingual presentation, first-run onboarding, semantic themes, and both Rich CLI and Textual TUI interfaces.

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
- **Import/export** — human-readable JSON backups with format/schema validation and state normalization.
- **Deterministic test mode** — use `--seed` or `GUESSNOVA_SEED` for reproducibility.
- **Accessible terminal modes** — `--plain` disables color and `--compact` prefers concise text over panels/tables.
- **Keyboard-first TUI** — predictable focus order, Enter submission, range-hint control, reliable reset/quit bindings, and persisted completed rounds.
- **Themes and contrast** — saved semantic Rich themes plus a dedicated high-contrast palette.
- **English + Hindi** — complete offline `en` and `hi` message catalogs with English fallback and per-profile locale settings.
- **Privacy-first** — no accounts, ads, analytics, telemetry, or application network calls.

## Supported platforms

- Windows 10/11
- Current macOS releases with Python 3.13+
- Modern Linux distributions with Python 3.13+

A Unicode/ANSI-capable terminal provides the richest presentation, but `--plain` remains available for reduced formatting. CI builds, validates, installs, launches, and smoke-tests the package on Windows, macOS, and Linux runners.

## Tech stack

- **Python 3.13+** for domain/application code.
- **Rich** for accessible terminal presentation.
- **Textual** for the app-like TUI and deterministic pilot testing.
- **JSON** for versioned local persistence, exports, and replay payloads.
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

### Backup and TUI

```bash
guessnova export ./guessnova-backup.json
guessnova import ./guessnova-backup.json
guessnova-tui
```

For deterministic non-daily play you may also set:

```bash
GUESSNOVA_SEED=20260819 guessnova play --no-save
```

## Data, privacy, and security

GuessNova stores data only in a local application-data directory; set `GUESSNOVA_HOME` to choose a custom location. Saves use versioned JSON and atomic replacement. Export/import state is normalized before persistence, recoverable profile trash is bounded, and replay text is length-bounded, checksum checked, field-allowlisted, and range validated before use. The runtime needs no account, API key, telemetry endpoint, or network connection.

Read [`PRIVACY.md`](PRIVACY.md), [`SECURITY.md`](SECURITY.md), and [`docs/data_format.md`](docs/data_format.md).

## Development and testing

```bash
python -m pip install -e '.[dev]'
ruff check .
ruff format --check .
mypy src/guessnova
pytest --cov=guessnova --cov-report=term-missing
python -m compileall -q src tests scripts
python scripts/smoke_test.py
python -m build
```

The repository CI runs linting, formatting, strict typing, tests, Textual pilot coverage, coverage reporting, bytecode compilation, smoke testing, cross-platform package build/install/Twine validation, dependency auditing, secret-material checks, and CodeQL analysis. Replay/import boundaries also have deterministic malformed-input/fuzz-style regression coverage. See [`docs/development.md`](docs/development.md) and [`docs/testing.md`](docs/testing.md).

## Architecture

GuessNova is a modular monolith with UI-independent game rules:

```text
Rich CLI / Textual TUI
          |
  application service
     /          \
 domain       local adapters
(engine)   (storage/replay/export)
```

The core engine has no Rich/Textual or filesystem dependency, making seeded gameplay deterministic and directly testable. Presentation messages resolve through offline English/Hindi catalogs while serialized identifiers remain stable. See [`docs/architecture.md`](docs/architecture.md), [`docs/localization.md`](docs/localization.md), and [`docs/adr/`](docs/adr/).

## Build and release

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Semantic tags are handled by a quality-gated GitHub release workflow. The tag must match the package version, and release artifacts are blocked until the full verification suite succeeds. Release candidates additionally require documented manual accessibility evidence. Real screenshot/demo media must be captured from the exact signed-off build rather than fabricated by automation.

See [`docs/release.md`](docs/release.md), [`docs/accessibility_evidence_template.md`](docs/accessibility_evidence_template.md), [`docs/media/README.md`](docs/media/README.md), and [`CHANGELOG.md`](CHANGELOG.md).

## Documentation

- [Setup](docs/setup.md)
- [Development](docs/development.md)
- [Architecture](docs/architecture.md)
- [Game modes](docs/game_modes.md)
- [Data format](docs/data_format.md)
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
