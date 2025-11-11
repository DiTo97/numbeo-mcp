.PHONY: style linting test lock sync export

export PYTHONPATH = .
check_dirs := src tests

style:
	uv run ruff format $(check_dirs)
	uv run ruff check --select I --fix $(check_dirs)

linting:
	uv run ruff check $(check_dirs)

test:
	uv run pytest tests/

lock:
	uv lock

sync:
	uv sync --no-dev

export:
	uv export --no-dev --format requirements-txt --output-file requirements.txt