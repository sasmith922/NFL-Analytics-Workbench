# Database

## Local PostgreSQL

Local development uses PostgreSQL 16 through Docker Compose.

- Service name: `postgres`
- Host from containers: `postgres`
- Host from machine: `localhost`
- Port: `5432`

Default credentials are defined in `.env.example` and can be overridden in `.env`.

## Initialization

Startup initialization scripts are loaded from:

- `database/init`

Current initialization enables `uuid-ossp` extension.

## Schema Lifecycle

- `database/migrations` stores schema migration files
- `database/schema_docs` stores schema design references
- `database/seed_data` stores optional bootstrap fixtures

No production schema has been implemented yet.
