from __future__ import annotations

import logging
from datetime import date
from typing import Any

from pipeline.ingestion import IngestionCounts, IngestionData

LOGGER = logging.getLogger(__name__)


class PostgresLoadStage:
    """Load ingestion records into PostgreSQL with idempotent upserts."""

    def __init__(self, database_url: str) -> None:
        self._database_url = database_url

    def run(self, data: IngestionData) -> IngestionCounts:
        try:
            import psycopg
        except ImportError as exc:  # pragma: no cover - runtime dependency
            raise RuntimeError("psycopg is required for pipeline loading") from exc

        with psycopg.connect(self._database_url) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO teams (abbreviation, name, city, conference, division)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (abbreviation) DO UPDATE SET
                        name = EXCLUDED.name,
                        city = EXCLUDED.city,
                        conference = EXCLUDED.conference,
                        division = EXCLUDED.division,
                        updated_at = NOW()
                    """,
                    [
                        (
                            team.abbreviation,
                            team.name,
                            team.city,
                            team.conference,
                            team.division,
                        )
                        for team in data.teams
                    ],
                )
                cursor.executemany(
                    """
                    INSERT INTO players (external_id, first_name, last_name, display_name, position, birth_date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (external_id) DO UPDATE SET
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        display_name = EXCLUDED.display_name,
                        position = EXCLUDED.position,
                        birth_date = EXCLUDED.birth_date,
                        updated_at = NOW()
                    """,
                    [self._player_row(player) for player in data.players],
                )
                cursor.executemany(
                    """
                    INSERT INTO seasons (year, name)
                    VALUES (%s, %s)
                    ON CONFLICT (year) DO UPDATE SET
                        name = EXCLUDED.name,
                        updated_at = NOW()
                    """,
                    [(season.year, season.name) for season in data.seasons],
                )
            connection.commit()

        counts = IngestionCounts(
            teams=len(data.teams),
            players=len(data.players),
            seasons=len(data.seasons),
        )
        LOGGER.info(
            "Load complete",
            extra={
                "teams_loaded": counts.teams,
                "players_loaded": counts.players,
                "seasons_loaded": counts.seasons,
            },
        )
        return counts

    def _player_row(self, player: Any) -> tuple[str, str, str, str, str | None, date | None]:
        return (
            player.external_id,
            player.first_name or player.display_name,
            player.last_name or player.display_name,
            player.display_name,
            player.position,
            player.birth_date,
        )
