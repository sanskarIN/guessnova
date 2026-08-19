.PHONY: install test lint smoke check build

install:
	python -m pip install -e '.[dev]'

test:
	pytest

lint:
	ruff check .

smoke:
	python scripts/smoke_test.py

check: test lint smoke

build:
	python -m build
