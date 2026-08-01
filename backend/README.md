# Backend

FastAPI service scaffold aligned with clean architecture boundaries.

## Structure

- `app/api` - HTTP routes and API composition
- `app/services` - business logic layer (placeholders)
- `app/repositories` - data access layer (placeholders)
- `app/models` - persistence models (placeholders)
- `app/schemas` - request/response schemas (placeholders)
- `app/core` - shared settings and logging configuration
- `app/ml` - machine learning integration boundary (placeholder)
- `tests` - backend unit tests

## Local commands

```bash
python -m pip install -e .[dev]
ruff check .
ruff format --check .
mypy app
pytest
```
