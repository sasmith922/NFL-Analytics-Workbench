from __future__ import annotations

import logging

from pipeline.ingestion import IngestionData

LOGGER = logging.getLogger(__name__)


class IngestionVerifyStage:
    """Verify loaded records exist after ingestion."""

    def __init__(self, database_url: str) -> None:
        self._database_url = database_url

    def run(self, data: IngestionData) -> None:
        try:
            import psycopg
        except ImportError as exc:  # pragma: no cover - runtime dependency
            raise RuntimeError("psycopg is required for pipeline verification") from exc

        team_keys = [team.abbreviation for team in data.teams]
        player_keys = [player.external_id for player in data.players]
        season_keys = [season.year for season in data.seasons]

        with psycopg.connect(self._database_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM teams WHERE abbreviation = ANY(%s)", (team_keys,))
                teams_found = int(cursor.fetchone()[0])
                cursor.execute("SELECT COUNT(*) FROM players WHERE external_id = ANY(%s)", (player_keys,))
                players_found = int(cursor.fetchone()[0])
                cursor.execute("SELECT COUNT(*) FROM seasons WHERE year = ANY(%s)", (season_keys,))
                seasons_found = int(cursor.fetchone()[0])

        if teams_found != len(team_keys):
            raise RuntimeError(
                f"Team verification failed: expected {len(team_keys)} found {teams_found}"
            )
        if players_found != len(player_keys):
            raise RuntimeError(
                f"Player verification failed: expected {len(player_keys)} found {players_found}"
            )
        if seasons_found != len(season_keys):
            raise RuntimeError(
                f"Season verification failed: expected {len(season_keys)} found {seasons_found}"
            )

        LOGGER.info(
            "Verification complete",
            extra={
                "teams_verified": teams_found,
                "players_verified": players_found,
                "seasons_verified": seasons_found,
            },
        )
