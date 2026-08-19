# GuessNova

<p align="center">
  <img src="assets/guessnova-logo.svg" alt="GuessNova logo" width="150" />
</p>

<p align="center"><strong>A production-quality, privacy-first number guessing game for the terminal.</strong></p>

<p align="center">
  <a href="https://github.com/sanskarIN/guessnova/actions/workflows/ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/sanskarIN/guessnova/ci.yml?branch=main&label=CI"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://www.python.org/"><img alt="Python 3.13+" src="https://img.shields.io/badge/python-3.13%2B-3776AB.svg"></a>
  <a href="https://buymeacoffee.com/sanskarIN"><img alt="Buy Me a Coffee" src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20GuessNova-FFDD00?logo=buymeacoffee&logoColor=000000"></a>
</p>

> **Made by the Sanskar**

GuessNova turns the familiar number-guessing game into a polished local experience with multiple modes, deterministic challenges, replay codes, profiles, achievements, XP, statistics, a local leaderboard, export/import, smart hints, and both Rich CLI and Textual TUI interfaces.

## Highlights

- **Classic** — focused number guessing with difficulty-based ranges and attempt budgets.
- **Timed** — solve before the difficulty-specific timer expires.
- **Streak** — play streak-tagged rounds and build persistent profile streaks.
- **Reverse** — think of a number and let GuessNova find it with binary search.
- **Daily Challenge** — date-seeded, reproducible challenge shared by everyone using the same version.
- **Smart hints** — temperature, direction, and parity clues without revealing the answer.
- **Profiles** — local-only stats, streaks, XP, settings, and achievements.
- **Replay codes** — checksum-protected portable summaries for replayable seeded challenges.
- **Local leaderboard** — ranked winning results stored on your device.
- **Import/export** — human-readable JSON backups with schema validation.
- **Deterministic test mode** — use `--seed` or `GUESSNOVA_SEED` for reproducibility.
- **Accessible terminal UX** — keyboard-first operation, reduced-noise CLI, high-contrast-ready settings, no mandatory animation or audio.
- **Privacy-first** — no accounts, ads, analytics, telemetry, or network calls in the application.

## Requirements

- Python **3.13+**
- Windows 10/11, macOS, or modern Linux
- A terminal capable of Unicode and ANSI color for the best experience

## Install

### From source

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
```

macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Play

```bash
guessnova play
guessnova play --difficulty hard
guessnova play --mode timed --difficulty expert
guessnova play --mode daily
guessnova play --mode daily --day 2026-08-19
guessnova reverse
guessnova stats
guessnova leaderboard
guessnova-tui
```

For a fully deterministic run:

```bash
guessnova play --seed 20260819 --no-save
```

or:

```bash
GUESSNOVA_SEED=20260819 guessnova play --no-save
```

## Data and privacy

GuessNova stores data only in a local application-data directory. Set `GUESSNOVA_HOME` to choose a custom location. See [PRIVACY.md](PRIVACY.md) and [docs/DATA_FORMAT.md](docs/DATA_FORMAT.md).

Back up local data:

```bash
guessnova export ./guessnova-backup.json
guessnova import ./guessnova-backup.json
```

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
python scripts/smoke_test.py
```

The repository uses CI for Python 3.13 tests, linting, package build validation, and security-oriented dependency review.

## Project documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Game modes](docs/GAME_MODES.md)
- [Data format](docs/DATA_FORMAT.md)
- [Accessibility](docs/ACCESSIBILITY.md)
- [Testing](docs/TESTING.md)
- [Release process](docs/RELEASING.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Security](SECURITY.md)
- [Support](SUPPORT.md)

## Contributing

Issues and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) first.

## Contact

- Business: **sanskarin@outlook.in**
- Business: **sanskarin.business@gmail.com**
- Support: **supportramsandesh@gmail.com**
- GitHub: **https://github.com/sanskarIN**

## Support the project

<a href="https://buymeacoffee.com/sanskarIN"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-@sanskarIN-FFDD00?logo=buymeacoffee&logoColor=000000" alt="Buy Me a Coffee @sanskarIN"></a>

Your support helps fund maintenance, documentation, accessibility improvements, and future open-source projects.

## License

GuessNova is open source under the [MIT License](LICENSE).
