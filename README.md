# NFL Analytics Workbench

Production-quality sports analytics platform foundation focused on maintainability, modularity, and long-term scalability.

## Foundation Status

This repository is currently configured for **development foundation only**:

- Architectural boundaries and module scaffolds are in place
- Docker Compose runs PostgreSQL + backend + frontend locally
- Environment variable management is defined through `.env` and typed settings
- Linting, formatting, testing, and pre-commit tooling are configured
- Placeholder modules exist for backend, frontend, pipeline, and database subsystems

No product features are implemented yet.

## Repository Structure

- `backend/` - FastAPI backend scaffold (clean architecture boundaries)
- `frontend/` - React + TypeScript + Vite UI scaffold
- `pipeline/` - staged ingestion pipeline scaffold (extract/validate/transform/load/verify)
- `database/` - PostgreSQL initialization and schema lifecycle placeholders
- `docker/` - local container orchestration
- `docs/` - architecture and engineering documentation
- `scripts/` - automation script placeholders

## Quick Start

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Start local stack:

```bash
docker compose -f docker/docker-compose.yml up --build
```

3. Verify services:

- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost:5173`
- PostgreSQL: `localhost:5432`

4. Stop stack:

```bash
docker compose -f docker/docker-compose.yml down --volumes
```

## Local Development Commands

```bash
make backend-install
make backend-lint
make backend-test
make frontend-install
make frontend-lint
make frontend-format-check
make frontend-test
make pipeline-test
make pre-commit-install
```
