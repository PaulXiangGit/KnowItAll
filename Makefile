COMPOSE ?= docker-compose -f compose.yaml
PYTHON ?= python3.12
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python

.PHONY: install dev test lint typecheck check infra-up infra-down

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install -e '.[dev]'

dev:
	$(VENV_PYTHON) -m uvicorn knowitall.api.main:app --reload --host 127.0.0.1 --port 8000

test:
	$(VENV_PYTHON) -m pytest

lint:
	$(VENV_PYTHON) -m ruff check .

typecheck:
	$(VENV_PYTHON) -m mypy

check: lint typecheck test

infra-up:
	$(COMPOSE) up -d postgres redis minio

infra-down:
	$(COMPOSE) down
