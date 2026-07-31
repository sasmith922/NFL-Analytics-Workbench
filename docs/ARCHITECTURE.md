# Architecture

## Philosophy

Every part of the system should have one responsibility.

The application is divided into four independent systems.

- Data Pipeline
- Database
- Backend API
- Frontend

These systems communicate through well-defined interfaces.

---

## Design Principles

- Clean Architecture
- Separation of concerns
- Dependency inversion
- Modular design
- Extensibility
- Testability

---

## Responsibilities

### Pipeline

Responsible for collecting, validating, transforming, and loading data.

Never contains application logic.

---

### Database

Single source of truth.

Stores all historical and derived data.

---

### Backend

Responsible for business logic.

Never scrapes data.

Never performs frontend rendering.

---

### Frontend

Responsible only for user interaction.

Never performs statistical calculations.

Never accesses raw data sources directly.

---

## Future Expansion

The architecture should support additional sports without requiring major refactoring.

NFL-specific logic should remain isolated where appropriate.