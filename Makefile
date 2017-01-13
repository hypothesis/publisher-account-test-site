FLASK_PORT=5050

.PHONY: run
run:
	export FLASK_APP=app.py; \
	export FLASK_DEBUG=1; \
	flask run --port $(FLASK_PORT)

.PHONY: lint
lint:
	flake8
