.PHONY: default
default: help

.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make dev               Run the app in the development server"
	@echo "make lint              Run the code linter(s) and print any warnings"

.PHONY: dev
dev: python
	tox -q -e py36-dev

.PHONY: devdata
devdata: python
	@tox -q -e py36-dev -- python bin/devdata.py

.PHONY: lint
lint: python
	tox -q -e py36-lint

.PHONY: python
python:
	@./bin/install-python
