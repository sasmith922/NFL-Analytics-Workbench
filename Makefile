.PHONY: backend-install backend-lint backend-test frontend-install frontend-lint frontend-test up down

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

frontend-test:
	cd frontend && npm run test

up:
	docker compose -f docker/docker-compose.yml up --build

down:
	docker compose -f docker/docker-compose.yml down --volumes
