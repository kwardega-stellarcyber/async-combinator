# Makefile for common development tasks

.PHONY: help setup configure-repo tests lint format type-check all-checks build publish clean docs

# Variables
PROJECT_DIR ?= $(CURDIR)
REPO_NAME = stellarpypi

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies
	@echo "Installing dependencies..."
	@poetry install

configure-repo: ## Configure Poetry repository (requires URL, USERNAME, PASSWORD)
	@if [ -z "$(url)" ] || [ -z "$(username)" ]; then \
		echo "Error: url, username, and password are required."; \
		echo "Usage: make configure-repo url=<repo-url> username=<username>"; \
		exit 1; \
	fi
	@echo "Configuring Poetry repository..."
	@poetry config http-basic.$(REPO_NAME) $(username)
	@echo "Poetry repository configured."

tests: ## Run tests
	@echo "Running tests..."
	@poetry run pytest


lint: ## Run linting
	@echo "Running linting..."
	@poetry run ruff check

format: ## Run formatting
	@echo "Running formatting..."
	@poetry run ruff format

type-check: ## Run type checking
	@echo "Running type checking..."
	@poetry run pyright async_combinator/ tests/

all-checks: format lint type-check tests ## Run all checks (formatting, linting, type checking, tests)
	@echo "Running all checks..."

build: ## Build distribution
	@echo "Building distribution..."
	@rm -rf dist/*
	@poetry build

docs: ## Make and host docs
	@echo "Hosting docs..."
	@poetry run pdoc async_combinator

publish: build ## Publish distribution
	@poetry publish -vvv --repository $(REPO_NAME)

clean: ## Clean up Docker containers and resources
	@echo "Cleaning up generated files..."
	@rm -rf dist **/__pycache__
