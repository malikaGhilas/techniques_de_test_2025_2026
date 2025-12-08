.PHONY: test unit_test perf_test coverage lint doc

test:
	python -m pytest TP/tests/

unit_test:
	python -m pytest TP/tests/ -m "not slow"

perf_test:
	python -m pytest TP/tests/ -m slow
coverage:
	python -m coverage run -m pytest TP/tests/
	python -m coverage report
	python -m coverage html

lint:
	python -m ruff check TP/triangulator/ TP/tests/

doc:
	python -m pdoc --output-dir docs TP.triangulator