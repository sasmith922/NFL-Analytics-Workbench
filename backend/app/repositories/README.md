# Repositories

Repository layer contracts for data access.

## MVP repository interfaces

- `SeasonRepositoryInterface`
- `TeamRepositoryInterface`
- `PlayerRepositoryInterface`
- `GameRepositoryInterface`
- `PlayerGameStatisticRepositoryInterface`
- `TeamGameStatisticRepositoryInterface`

These interfaces define backend-facing query contracts while keeping concrete database implementations replaceable.
