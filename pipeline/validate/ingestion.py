from __future__ import annotations

import logging
from typing import Any

from pipeline.ingestion import RawIngestionData

LOGGER = logging.getLogger(__name__)


def _has_value(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


class IngestionValidateStage:
    """Validate raw records before transformation."""

    def run(self, raw: RawIngestionData) -> RawIngestionData:
        teams = [team for team in raw.teams if self._valid_team(team)]
        players = [player for player in raw.players if self._valid_player(player)]
        seasons = [season for season in raw.seasons if self._valid_season(season)]

        LOGGER.info(
            "Validation complete",
            extra={
                "teams_valid": len(teams),
                "teams_dropped": len(raw.teams) - len(teams),
                "players_valid": len(players),
                "players_dropped": len(raw.players) - len(players),
                "seasons_valid": len(seasons),
                "seasons_dropped": len(raw.seasons) - len(seasons),
            },
        )
        return RawIngestionData(teams=teams, players=players, seasons=seasons)

    def _valid_team(self, team: dict[str, Any]) -> bool:
        abbreviation = team.get("team_abbr") or team.get("abbreviation")
        name = team.get("team_nick") or team.get("name")
        city = team.get("team_name") or team.get("city")
        return _has_value(abbreviation) and _has_value(name) and _has_value(city)

    def _valid_player(self, player: dict[str, Any]) -> bool:
        external_id = player.get("gsis_id") or player.get("pfr_id") or player.get("espn_id")
        display_name = player.get("name") or player.get("display_name")
        first_name = player.get("first_name")
        last_name = player.get("last_name")
        return _has_value(external_id) and _has_value(display_name) and (
            _has_value(first_name) or _has_value(last_name)
        )

    def _valid_season(self, season: dict[str, Any]) -> bool:
        year = season.get("season") or season.get("year")
        if not _has_value(year):
            return False
        try:
            parsed = int(year)
        except (TypeError, ValueError):
            return False
        return 1920 <= parsed <= 2100
