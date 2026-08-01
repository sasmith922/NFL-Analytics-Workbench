.PHONY: backend-install backend-lint backend-test frontend-install frontend-lint frontend-format-check frontend-test pipeline-test pre-commit-install up down

backend-install:
	cd backend && python -m pip install -e .[dev]

backend-lint:
	cd backend && ruff check . && ruff format --check . && mypy app

backend-test:
	cd backend && pytest

frontend-install:
	cd frontend && npm install

frontend-lint:
	cd frontend && npm run lint

frontend-format-check:
	cd frontend && npm run format:check

frontend-test:
	cd frontend && npm run test

pipeline-test:
	PYTHONPATH=. python -m pytest pipeline/tests

pre-commit-install:
	python -m pip install pre-commit && pre-commit install

up:
	docker compose -f docker/docker-compose.yml up --build

down:
	docker compose -f docker/docker-compose.yml down --volumes
