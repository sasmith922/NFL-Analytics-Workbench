from __future__ import annotations

import logging
from datetime import date
from typing import Any

from pipeline.ingestion import IngestionData, PlayerRecord, RawIngestionData, SeasonRecord, TeamRecord

LOGGER = logging.getLogger(__name__)


def _clean_optional(value: Any) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip()
    return cleaned if cleaned else None


def _parse_birth_date(value: Any) -> date | None:
    parsed = _clean_optional(value)
    if parsed is None:
        return None
    try:
        return date.fromisoformat(parsed)
    except ValueError:
        return None


class IngestionTransformStage:
    """Normalize validated raw records to strongly typed ingestion records."""

    def run(self, raw: RawIngestionData) -> IngestionData:
        teams_by_abbreviation: dict[str, TeamRecord] = {}
        for source_team in raw.teams:
            abbreviation = str(
                source_team.get("team_abbr") or source_team.get("abbreviation") or ""
            ).strip()
            if not abbreviation:
                continue
            city = str(source_team.get("team_name") or source_team.get("city") or "").strip()
            nickname = str(source_team.get("team_nick") or source_team.get("name") or "").strip()
            if not city or not nickname:
                continue
            teams_by_abbreviation[abbreviation] = TeamRecord(
                abbreviation=abbreviation,
                city=city,
                name=nickname,
                conference=_clean_optional(source_team.get("team_conf") or source_team.get("conference")),
                division=_clean_optional(
                    source_team.get("team_division") or source_team.get("division")
                ),
            )

        players_by_external_id: dict[str, PlayerRecord] = {}
        for source_player in raw.players:
            external_id = _clean_optional(
                source_player.get("gsis_id")
                or source_player.get("pfr_id")
                or source_player.get("espn_id")
                or source_player.get("external_id")
            )
            if external_id is None:
                continue
            display_name = _clean_optional(source_player.get("name") or source_player.get("display_name"))
            first_name = _clean_optional(source_player.get("first_name"))
            last_name = _clean_optional(source_player.get("last_name"))
            if display_name is None:
                continue
            if first_name is None and last_name is None:
                parts = display_name.split(" ", maxsplit=1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) > 1 else parts[0]
            players_by_external_id[external_id] = PlayerRecord(
                external_id=external_id,
                first_name=first_name or "",
                last_name=last_name or "",
                display_name=display_name,
                position=_clean_optional(source_player.get("position")),
                birth_date=_parse_birth_date(source_player.get("birth_date")),
            )

        seasons: set[int] = set()
        for source_season in raw.seasons:
            season_year = source_season.get("season") or source_season.get("year")
            if season_year is None:
                continue
            try:
                parsed_year = int(season_year)
            except (TypeError, ValueError):
                continue
            if 1920 <= parsed_year <= 2100:
                seasons.add(parsed_year)

        transformed = IngestionData(
            teams=list(teams_by_abbreviation.values()),
            players=list(players_by_external_id.values()),
            seasons=[SeasonRecord(year=year) for year in sorted(seasons)],
        )
        LOGGER.info(
            "Transformation complete",
            extra={
                "teams_transformed": len(transformed.teams),
                "players_transformed": len(transformed.players),
                "seasons_transformed": len(transformed.seasons),
            },
        )
        return transformed
