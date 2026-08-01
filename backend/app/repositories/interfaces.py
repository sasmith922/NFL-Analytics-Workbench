from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.models.game import Game
from app.models.player import Player
from app.models.player_game_statistic import PlayerGameStatistic
from app.models.season import Season
from app.models.team import Team
from app.models.team_game_statistic import TeamGameStatistic


class SeasonRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, season_id: int) -> Season | None:
        """Fetch a season by its internal identifier."""

    @abstractmethod
    def get_by_year(self, year: int) -> Season | None:
        """Fetch a season by season year."""

    @abstractmethod
    def list_all(self) -> Sequence[Season]:
        """List all seasons."""


class TeamRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, team_id: int) -> Team | None:
        """Fetch a team by id."""

    @abstractmethod
    def get_by_abbreviation(self, abbreviation: str) -> Team | None:
        """Fetch a team by abbreviation."""

    @abstractmethod
    def list_all(self) -> Sequence[Team]:
        """List all teams."""


class PlayerRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, player_id: int) -> Player | None:
        """Fetch a player by id."""

    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Player | None:
        """Fetch a player by source-system external id."""

    @abstractmethod
    def list_by_team_and_season(self, team_id: int, season_id: int) -> Sequence[Player]:
        """List players who appeared for a team during a season."""


class GameRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, game_id: int) -> Game | None:
        """Fetch a game by id."""

    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Game | None:
        """Fetch a game by source-system external id."""

    @abstractmethod
    def list_by_season(self, season_id: int) -> Sequence[Game]:
        """List games for a season."""


class PlayerGameStatisticRepositoryInterface(ABC):
    @abstractmethod
    def list_for_game(self, game_id: int) -> Sequence[PlayerGameStatistic]:
        """List player stats for one game."""

    @abstractmethod
    def list_for_player(
        self, player_id: int, season_id: int | None = None
    ) -> Sequence[PlayerGameStatistic]:
        """List player stats across all games, optionally by season."""


class TeamGameStatisticRepositoryInterface(ABC):
    @abstractmethod
    def list_for_game(self, game_id: int) -> Sequence[TeamGameStatistic]:
        """List both teams' stats for one game."""

    @abstractmethod
    def list_for_team(
        self, team_id: int, season_id: int | None = None
    ) -> Sequence[TeamGameStatistic]:
        """List team stats across games, optionally by season."""
