from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import get_settings

_settings = get_settings()

engine: Engine = create_engine(
    _settings.sqlalchemy_database_url,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session and ensure proper cleanup."""

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
