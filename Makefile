PHONY: test, lint, format import-sort


test:
	python -m unittest

format:
	poetry run black .

lint:
	poetry run ruff check

import-sort:
	poetry run isort .
