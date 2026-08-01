from __future__ import annotations

import os
from dataclasses import dataclass


def _parse_seasons(raw_value: str) -> list[int]:
    years = [int(token.strip()) for token in raw_value.split(",") if token.strip()]
    if not years:
        raise ValueError("PIPELINE_SEASONS must include at least one year")
    return sorted(set(years))


@dataclass(frozen=True)
class IngestionConfig:
    database_url: str
    seasons: list[int]
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> IngestionConfig:
        database_url = os.getenv("DATABASE_URL", "").strip()
        if not database_url:
            raise ValueError("DATABASE_URL is required for ingestion")
        seasons = _parse_seasons(os.getenv("PIPELINE_SEASONS", "2024"))
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        return cls(database_url=database_url, seasons=seasons, log_level=log_level)
