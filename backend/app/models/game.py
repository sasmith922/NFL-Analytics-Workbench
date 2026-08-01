from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampedModel


class Game(Base, TimestampedModel):
    """Represents a single NFL game in a season."""

    __tablename__ = "games"
    __table_args__ = (
        CheckConstraint("week >= 1", name="game_week_min_1"),
        CheckConstraint("week <= 25", name="game_week_max_25"),
        CheckConstraint("home_team_id <> away_team_id", name="game_teams_must_differ"),
        UniqueConstraint("season_id", "week", "home_team_id", "away_team_id", name="uq_game_slot"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True, index=True
    )
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"), nullable=False, index=True)
    week: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    game_type: Mapped[str] = mapped_column(String(16), nullable=False, default="regular")
    kickoff_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    venue: Mapped[str | None] = mapped_column(String(128), nullable=True)

    season: Mapped[Season] = relationship(back_populates="games")
    home_team: Mapped[Team] = relationship(back_populates="home_games", foreign_keys=[home_team_id])
    away_team: Mapped[Team] = relationship(back_populates="away_games", foreign_keys=[away_team_id])
    team_statistics: Mapped[list[TeamGameStatistic]] = relationship(back_populates="game")
    player_statistics: Mapped[list[PlayerGameStatistic]] = relationship(back_populates="game")


if TYPE_CHECKING:
    from app.models.player_game_statistic import PlayerGameStatistic
    from app.models.season import Season
    from app.models.team import Team
    from app.models.team_game_statistic import TeamGameStatistic
