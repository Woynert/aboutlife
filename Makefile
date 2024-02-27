run:
	python -m aboutlife

run-overlay:
	python -m aboutlife --overlay

run-sticky:
	python -m aboutlife --sticky

format:
	ruff format .

test:
	python -m unittest discover tests/overlay
