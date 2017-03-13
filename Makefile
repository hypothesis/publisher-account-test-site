FLASK_PORT=5050

ifndef FLASK_HOST
FLASK_HOST = 127.0.0.1
endif

.PHONY: run
run:
	./app.py

.PHONY: lint
lint:
	flake8
