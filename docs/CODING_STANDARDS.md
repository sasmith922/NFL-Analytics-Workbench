# Coding Standards

## General

- Prefer readability over cleverness
- Keep modules focused on one responsibility
- Avoid duplicated business logic
- Favor composition over inheritance
- Handle errors explicitly and log useful context

## Backend (Python)

- Use type hints for all public interfaces
- Keep API routes thin: validate, call service, return response
- Keep SQL/data access logic in repositories
- Run `ruff`, `mypy`, and `pytest` before merging

## Frontend (TypeScript/React)

- Keep components presentational where possible
- Put reusable behavior into hooks
- Keep backend communication inside `src/api`
- Run lint, format check, and tests before merging

## Pipeline

- Keep stages independent: extract, validate, transform, load, verify
- Keep provider-specific code behind adapters
- Ensure each stage is independently testable
