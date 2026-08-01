from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampedModel


class TeamGameStatistic(Base, TimestampedModel):
    """Aggregated team-level statistics for one game."""

    __tablename__ = "team_game_statistics"
    __table_args__ = (
        UniqueConstraint("game_id", "team_id", name="uq_team_game_statistics_game_team"),
        CheckConstraint("points >= 0", name="team_stats_points_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=False, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)

    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    first_downs: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_yards: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passing_yards: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rushing_yards: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    turnovers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalties: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    penalty_yards: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    time_of_possession_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    game: Mapped["Game"] = relationship(back_populates="team_statistics")
    team: Mapped["Team"] = relationship(back_populates="team_game_statistics")

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.team import Team
