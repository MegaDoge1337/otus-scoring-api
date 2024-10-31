PHONY: unit-test, func-test, lint, format import-sort


unit-test:
	python -m unittest ./test/unit/test.py

func-test:
	python -m unittest ./test/functional/test.py

format:
	poetry run black .

lint:
	poetry run ruff check

import-sort:
	poetry run isort .
