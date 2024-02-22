run:
	python -m aboutlife.main

format:
	ruff format .

test:
	python -m unittest discover tests/overlay
