.PHONY: check test lint format-check clean

check: test lint format-check

test:
	uv run pytest

lint:
	uv run ruff check .

format-check:
	uv run ruff format --check .

clean:
	rm -rf .pytest_cache .ruff_cache .venv build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
