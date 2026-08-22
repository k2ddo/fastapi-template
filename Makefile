.PHONY: check format lint migrate run test

run:
	uv run fastapi dev main.py

migrate:
	uv run alembic upgrade head

format:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run pyright

test:
	uv run pytest

check: lint test
