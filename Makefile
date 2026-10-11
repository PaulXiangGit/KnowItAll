COMPOSE ?= $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose -f compose.yaml"; else echo "docker-compose -f compose.yaml"; fi)
PYTHON ?= python3.12
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python

.PHONY: install dev up down status logs test lint typecheck check infra-pull infra-up infra-down

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install -e '.[dev]'

dev:
	$(VENV_PYTHON) -m uvicorn knowitall.api.main:app --reload --host 127.0.0.1 --port 8000

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

status:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f api

test:
	$(VENV_PYTHON) -m pytest

lint:
	$(VENV_PYTHON) -m ruff check .

typecheck:
	$(VENV_PYTHON) -m mypy

check: lint typecheck test

infra-pull:
	$(COMPOSE) pull postgres redis

infra-up:
	$(COMPOSE) up -d postgres redis

infra-down:
	$(COMPOSE) down
