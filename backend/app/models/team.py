from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampedModel


class Team(Base, TimestampedModel):
    """Represents an NFL franchise."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    abbreviation: Mapped[str] = mapped_column(String(3), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    city: Mapped[str] = mapped_column(String(64), nullable=False)
    conference: Mapped[str | None] = mapped_column(String(8), nullable=True)
    division: Mapped[str | None] = mapped_column(String(16), nullable=True)

    home_games: Mapped[list[Game]] = relationship(
        back_populates="home_team", foreign_keys="Game.home_team_id"
    )
    away_games: Mapped[list[Game]] = relationship(
        back_populates="away_team", foreign_keys="Game.away_team_id"
    )
    team_game_statistics: Mapped[list[TeamGameStatistic]] = relationship(back_populates="team")
    player_game_statistics: Mapped[list[PlayerGameStatistic]] = relationship(
        back_populates="team", foreign_keys="PlayerGameStatistic.team_id"
    )
    opponent_player_game_statistics: Mapped[list[PlayerGameStatistic]] = relationship(
        back_populates="opponent_team", foreign_keys="PlayerGameStatistic.opponent_team_id"
    )


if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.player_game_statistic import PlayerGameStatistic
    from app.models.team_game_statistic import TeamGameStatistic
