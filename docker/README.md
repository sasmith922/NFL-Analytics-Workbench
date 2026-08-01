# Docker

Container orchestration for local development.

## Services

- `postgres` - PostgreSQL 16 with initialization scripts from `database/init`
- `backend` - FastAPI service on port `8000`
- `frontend` - Vite dev server on port `5173`

## Usage

```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up --build
```

Stop and remove data volume:

```bash
docker compose -f docker/docker-compose.yml down --volumes
```
