# Architecture

## System Boundaries

The project is divided into four independent systems:

1. **pipeline/** - data ingestion and transformation only
2. **database/** - PostgreSQL schema and lifecycle assets
3. **backend/** - API and business logic boundary
4. **frontend/** - presentation and user interaction boundary

## Responsibility Rules

- Frontend never accesses external data providers directly
- Backend never performs ingestion or scraping
- Pipeline never contains application feature logic
- Database is the single source of truth for application data

## Backend Structure

`backend/app` is organized into:

- `api` (routing)
- `services` (business logic)
- `repositories` (data access)
- `models` (persistence models)
- `schemas` (request/response contracts)
- `core` (cross-cutting config such as settings and logging)
- `ml` (machine-learning integration boundary)

## Frontend Structure

`frontend/src` is organized into:

- `components`, `pages`, `hooks`, `api`, `charts`, `tables`, `types`, `utils`

## Pipeline Structure

Pipeline stages are isolated into:

- `extract`, `validate`, `transform`, `load`, `verify`

Each stage is intended to be independently testable and replaceable.
