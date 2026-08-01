# Pipeline

Data ingestion pipeline scaffold with independently testable stages.

## Stages

- `extract` - source data acquisition adapters
- `validate` - schema and quality checks
- `transform` - normalization and derived metrics
- `load` - persistence into PostgreSQL
- `verify` - post-load integrity validation

## Supporting modules

- `jobs` - orchestration entry points
- `config` - pipeline configuration
- `tests` - stage unit tests

## Initial ingestion job

`pipeline/jobs/initial_ingestion.py` implements the first end-to-end ingestion workflow for:

- teams
- players
- seasons

Pipeline flow:

1. Extract from nflverse (`nfl_data_py`)
2. Validate required fields and year ranges
3. Transform into typed records
4. Load into PostgreSQL using idempotent upserts
5. Verify inserted rows exist
