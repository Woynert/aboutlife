run:
	python -m aboutlife

run-overlay:
	python -m aboutlife --overlay

format:
	ruff format .

test:
	python -m unittest discover tests/overlay
