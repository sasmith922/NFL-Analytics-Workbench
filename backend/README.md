# Backend

FastAPI service scaffold aligned with clean architecture boundaries.

## Structure

- `app/api` - HTTP routes and API composition
- `app/services` - business logic layer (placeholders)
- `app/repositories` - data access layer (placeholders)
- `app/models` - SQLAlchemy persistence models
- `app/schemas` - request/response schemas (placeholders)
- `app/core` - shared settings, logging, and database session configuration
- `app/ml` - machine learning integration boundary (placeholder)
- `tests` - backend unit tests

## Database migrations

Alembic migrations are managed inside `backend/alembic`.

```bash
alembic upgrade head
```

## Local commands

```bash
python -m pip install -e .[dev]
ruff check .
ruff format --check .
mypy app
pytest
```
