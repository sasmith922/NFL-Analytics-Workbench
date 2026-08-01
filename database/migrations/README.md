# migrations

Alembic migration assets for PostgreSQL schema evolution.

For backend schema changes, run Alembic from the `backend/` directory:

```bash
alembic upgrade head
```

Initial MVP migration:

- `backend/alembic/versions/20260801_0001_create_mvp_schema.py`
