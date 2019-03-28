.PHONY: default
default: help

.PHONY: help
help:
	@echo "make help              Show this help message"
	@echo "make dev               Run the app in the development server"
	@echo "make lint              Run the code linter(s) and print any warnings"

.PHONY: dev
dev:
	tox -q -e py27-dev

.PHONY: lint
lint:
	tox -q -e py27-lint
