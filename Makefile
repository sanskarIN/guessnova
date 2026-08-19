.PHONY: install test lint format type compile smoke check build

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

smoke:
	python scripts/smoke_test.py

check: lint format type test compile smoke

build:
	python -m build
