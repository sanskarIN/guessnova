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
```

## Textual interface

```bash
guessnova-tui
```

## Development dependencies

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
```

## Optional environment variables

- `GUESSNOVA_HOME` — override the local application-data directory.
- `GUESSNOVA_SEED` — default deterministic seed for CLI challenges.

GuessNova does not require API keys or secrets.
