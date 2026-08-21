.PHONY: install test browser lint format type compile metadata web-package smoke entrypoints check build

install:
	python -m pip install -e '.[dev]'

test:
	pytest

browser:
	node --test tests/web/*.mjs
	node --check src/guessnova/web/app.js
	node --check src/guessnova/web/browser-state.mjs
	node --check src/guessnova/web/game-engine.mjs
	node --check src/guessnova/web/sw.js

lint:
	ruff check .

format:
	ruff format --check .

type:
	mypy src/guessnova

compile:
	python -m compileall -q src tests scripts

metadata:
	python scripts/verify_release_metadata.py

web-package:
	python scripts/verify_web_package.py

smoke:
	python scripts/smoke_test.py

entrypoints:
	python -m guessnova --help
	python -m guessnova doctor --help
	python -m guessnova.doctor_cli --help
	python -c "from guessnova.tui import GuessNovaApp; print(GuessNovaApp.TITLE)"
	python -c "from guessnova.tui_challenge_app import GuessNovaApp; print(GuessNovaApp.TITLE)"
	guessnova web --help
	guessnova-web --help

check: lint format type test browser compile metadata web-package smoke entrypoints

build:
	python -m build
