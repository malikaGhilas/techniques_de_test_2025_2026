.PHONY: test unit_test perf_test coverage lint doc

ROOT_DIR := ..

test:
	python -m pytest tests/ --tb=short

unit_test:
	python -m pytest tests/ -m "not performance" --tb=short

perf_test:
	python -m pytest tests/ -m performance --tb=short

coverage:
	python -m coverage run -m pytest tests/ --tb=short
	python -m coverage report

lint:
	python -m ruff check . --config=$(ROOT_DIR)/pyproject.toml

doc:
	python -m pdoc --html --output-dir docs triangulator