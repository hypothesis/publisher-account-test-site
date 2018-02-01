FLASK_PORT=5050

ifndef FLASK_HOST
FLASK_HOST = 127.0.0.1
endif

.PHONY: run
run:
	export FLASK_APP=app.py; \
	export FLASK_DEBUG=1; \
	flask run --port $(FLASK_PORT) --host $(FLASK_HOST)

.PHONY: lint
lint:
	flake8

.PHONY: docker
docker:
	git archive HEAD | docker build -t hypothesis-publisher-site -

