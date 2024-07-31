run:
	python -m aboutlife

run-daemon:
	python -m aboutlife --daemon

run-overlay:
	python -m aboutlife --overlay

run-sticky:
	python -m aboutlife --sticky

format:
	ruff format .

test:
	python -m unittest discover tests/overlay

webext:
	cd aboutlife-webext; zip -r ../extension-$(shell date +%s).zip *.js *.html icons manifest.json 
