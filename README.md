# NFL Analytics Workbench

## Overview

NFL Analytics Workbench is a production-quality sports analytics platform focused on historical NFL data exploration, visualization, and predictive modeling.

The goal is not to build another statistics website, but to create an analytics environment similar to Tableau or Jupyter Notebook that is tailored specifically for football.

The platform emphasizes:

- Interactive data exploration
- Advanced visualizations
- Predictive modeling
- Fantasy football analytics
- Reproducible analysis
- Long-term extensibility

Future versions will support additional sports while sharing the same underlying architecture.

---

## Project Goals

- Modular architecture
- Clean separation of concerns
- Production-quality code
- Strong typing
- Reusable components
- Reproducible analytics
- Scalable infrastructure

---

## High-Level Architecture

Data Pipeline
        ↓
 PostgreSQL Database
        ↓
 FastAPI Backend
        ↓
 React Frontend

Each layer has a single responsibility.

---

## Repository Structure

backend/

frontend/

pipeline/

database/

docs/

docker/

scripts/

---

## Technology Stack

Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Polars
- Pandas
- scikit-learn

Frontend

- React
- TypeScript
- Vite
- TailwindCSS
- TanStack Query
- TanStack Table
- Plotly

Database

- PostgreSQL

Infrastructure

- Docker
- GitHub Actions

---

## Documentation

See the `/docs` directory for project architecture, coding standards, and development guidelines.