from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampedModel


class Player(Base, TimestampedModel):
    """Represents an NFL player."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True, index=True
    )
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    position: Mapped[str | None] = mapped_column(String(8), nullable=True, index=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    game_statistics: Mapped[list[PlayerGameStatistic]] = relationship(back_populates="player")


if TYPE_CHECKING:
    from app.models.player_game_statistic import PlayerGameStatistic
