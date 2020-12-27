.PHONY: clean clean-test clean-pyc clean-build docs help test
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@echo "\033[0;1mCommands\033[0m"
	@grep -E '^[.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[34;1m%-30s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc clean-test ## clean everything except for site

clean-build: ## remove build artifacts
	rm -fr dist/

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

clean-site:
	rm -fr site/

lint: ## check style with pylint
	poetry run pylint logdir tests

test: ## run tests
	poetry run pytest

docs: clean-site ## generate HTML documentation, including API docs
	poetry run mkdocs build
	$(BROWSER) site/index.html

servedocs: ## compile the docs watching for changes
	poetry run mkdocs serve

release: ## package and upload a release
	poetry publish --build

dist: clean ## builds source and wheel package
	poetry build
	ls -l dist

install: clean ## install to the active Python's site-packages
	pip install .
