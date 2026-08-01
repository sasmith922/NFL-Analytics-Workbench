from __future__ import annotations

import logging
from typing import Any

from pipeline.ingestion import RawIngestionData

LOGGER = logging.getLogger(__name__)


def _frame_to_records(frame: Any) -> list[dict[str, Any]]:
    records = frame.to_dict("records")
    if not isinstance(records, list):
        raise TypeError("Expected nflverse dataframe conversion to produce a list of records")
    return [record for record in records if isinstance(record, dict)]


class NflverseExtractStage:
    """Extract teams, players, and seasons from nflverse datasets."""

    def __init__(self) -> None:
        try:
            import nfl_data_py as nfl  # type: ignore[import-not-found]
        except ImportError as exc:  # pragma: no cover - import path depends on runtime env
            raise RuntimeError(
                "nfl_data_py is required for pipeline extraction. Install it before running the job."
            ) from exc
        self._nfl = nfl

    def run(self, seasons: list[int]) -> RawIngestionData:
        LOGGER.info("Extracting nflverse teams, players, and seasons", extra={"seasons": seasons})

        teams_frame = self._nfl.import_team_desc()
        players_frame = self._nfl.import_ids()
        schedules_frame = self._nfl.import_schedules(seasons)

        teams = _frame_to_records(teams_frame)
        players = _frame_to_records(players_frame)
        schedules = _frame_to_records(schedules_frame)

        season_rows = [{"season": schedule["season"]} for schedule in schedules if "season" in schedule]

        LOGGER.info(
            "Extraction complete",
            extra={
                "teams_extracted": len(teams),
                "players_extracted": len(players),
                "season_rows_extracted": len(season_rows),
            },
        )
        return RawIngestionData(teams=teams, players=players, seasons=season_rows)
