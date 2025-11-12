.PHONY: style linting test lock sync export

export PYTHONPATH = .
sources := src tests

style:
	uv run ruff format $(sources)
	uv run ruff check --select I --fix $(sources)

linting:
	uv run ruff check $(sources)

test:
	uv run pytest tests/

lock:
	uv lock

sync:
	uv sync --dev

export:
	uv export --no-dev --format requirements-txt --output-file requirements.txt
