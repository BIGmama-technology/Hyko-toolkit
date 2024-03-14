.PHONY: setup lint format

setup:
	./scripts/setup.sh

lint:
	ruff check .

format:
	ruff format .
