PHONY: test, format, import-sort


test:
	python -m unittest

format:
	poetry run ruff check

import-sort:
	poetry run isort .
