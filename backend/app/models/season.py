from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampedModel


class Season(Base, TimestampedModel):
    """Represents an NFL season for grouping schedules and statistics."""

    __tablename__ = "seasons"
    __table_args__ = (
        CheckConstraint("year >= 1920", name="season_year_min_1920"),
        CheckConstraint("year <= 2100", name="season_year_max_2100"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(SmallInteger, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, default="Regular Season")

    games: Mapped[list[Game]] = relationship(back_populates="season")


if TYPE_CHECKING:
    from app.models.game import Game
