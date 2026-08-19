# Contributing to GuessNova

Thank you for helping improve GuessNova. Keep contributions focused, tested, accessible, privacy-preserving, and easy to review.

## Development setup

```bash
git clone https://github.com/sanskarIN/guessnova.git
cd guessnova
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
pytest
ruff check .
python scripts/smoke_test.py
```

## Contribution rules

- Keep game/domain logic independent of Rich/Textual presentation code.
- Add or update tests for behavior changes and regression fixes.
- Preserve deterministic behavior for seeded and daily challenges.
- Preserve keyboard-only operation and avoid color-only meaning.
- Never commit secrets, private production endpoints, real user data, or generated credentials.
- Update documentation and `CHANGELOG.md` for user-visible changes.
- Prefer small Conventional Commits such as `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `perf:`, `build:`, `ci:`, and `chore:`.

## Pull requests

Use the pull-request template, explain the user problem, list verification performed, and keep unrelated cleanup out of feature/fix PRs. Security vulnerabilities should follow `SECURITY.md` rather than a public issue.

## Contact

- Business: `sanskarin@outlook.in`
- Business: `sanskarin.business@gmail.com`
- Support: `supportramsandesh@gmail.com`
- GitHub: https://github.com/sanskarIN
- Buy Me a Coffee: https://buymeacoffee.com/sanskarIN

**Made by the Sanskar**
