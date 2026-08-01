# Models

SQLAlchemy ORM models for the backend persistence layer.

## MVP entities

- `Season`
- `Team`
- `Player`
- `Game`
- `PlayerGameStatistic`
- `TeamGameStatistic`

All models inherit from a shared declarative base and include normalized foreign-key relationships for historical analytics queries.
