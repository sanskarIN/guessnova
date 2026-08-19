.PHONY: install test lint format type compile metadata smoke check build

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

check: lint format type test compile metadata smoke

build:
	python -m build
