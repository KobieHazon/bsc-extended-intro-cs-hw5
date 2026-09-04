.PHONY: check test lint format-check privacy-check clean

check: test lint format-check privacy-check

test:
	uv run pytest

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

privacy-check:
	uv run python scripts/check_repository.py

clean:
	rm -rf .pytest_cache .ruff_cache .venv build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
