.PHONY: install test lint format type compile metadata smoke entrypoints check build

install:
	python -m pip install -e '.[dev]'

test:
	pytest

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

smoke:
	python scripts/smoke_test.py

entrypoints:
	python -m guessnova --help
	python -m guessnova doctor --help
	python -m guessnova.doctor_cli --help

check: lint format type test compile metadata smoke entrypoints

build:
	python -m build
