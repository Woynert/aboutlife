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

webext:
	zip -r extension-$(shell date +%s).zip aboutlife-webext/manifest.json aboutlife-webext/icons aboutlife-webext/*.js aboutlife-webext/*.html
