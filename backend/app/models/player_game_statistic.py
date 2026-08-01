from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampedModel


class PlayerGameStatistic(Base, TimestampedModel):
    """Player-level game statistics for historical analysis."""

    __tablename__ = "player_game_statistics"
    __table_args__ = (
        UniqueConstraint(
            "game_id", "player_id", "team_id", name="uq_player_game_statistics_game_player_team"
        ),
        CheckConstraint("passing_attempts >= 0", name="player_stats_passing_attempts_non_negative"),
        CheckConstraint("rushing_attempts >= 0", name="player_stats_rushing_attempts_non_negative"),
        CheckConstraint("receptions >= 0", name="player_stats_receptions_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=False, index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False, index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)
    opponent_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False, index=True)

    passing_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passing_completions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passing_yards: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passing_touchdowns: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    interceptions_thrown: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    rushing_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rushing_yards: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rushing_touchdowns: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    targets: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    receptions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    receiving_yards: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    receiving_touchdowns: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    sacks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tackles: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    game: Mapped["Game"] = relationship(back_populates="player_statistics")
    player: Mapped["Player"] = relationship(back_populates="game_statistics")
    team: Mapped["Team"] = relationship(
        back_populates="player_game_statistics", foreign_keys=[team_id]
    )
    opponent_team: Mapped["Team"] = relationship(
        back_populates="opponent_player_game_statistics", foreign_keys=[opponent_team_id]
    )

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.player import Player
    from app.models.team import Team
