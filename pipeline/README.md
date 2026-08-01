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
