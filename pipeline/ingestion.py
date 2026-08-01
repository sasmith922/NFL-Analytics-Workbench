from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Protocol


@dataclass(frozen=True)
class TeamRecord:
    abbreviation: str
    name: str
    city: str
    conference: str | None = None
    division: str | None = None


@dataclass(frozen=True)
class PlayerRecord:
    external_id: str
    first_name: str
    last_name: str
    display_name: str
    position: str | None = None
    birth_date: date | None = None


@dataclass(frozen=True)
class SeasonRecord:
    year: int
    name: str = "Regular Season"


@dataclass(frozen=True)
class RawIngestionData:
    teams: list[dict[str, Any]]
    players: list[dict[str, Any]]
    seasons: list[dict[str, Any]]


@dataclass(frozen=True)
class IngestionData:
    teams: list[TeamRecord]
    players: list[PlayerRecord]
    seasons: list[SeasonRecord]


@dataclass(frozen=True)
class IngestionCounts:
    teams: int
    players: int
    seasons: int


@dataclass(frozen=True)
class IngestionJobResult:
    extracted: IngestionCounts
    loaded: IngestionCounts


class ExtractStage(Protocol):
    def run(self, seasons: list[int]) -> RawIngestionData: ...


class ValidateStage(Protocol):
    def run(self, raw: RawIngestionData) -> RawIngestionData: ...


class TransformStage(Protocol):
    def run(self, raw: RawIngestionData) -> IngestionData: ...


class LoadStage(Protocol):
    def run(self, data: IngestionData) -> IngestionCounts: ...


class VerifyStage(Protocol):
    def run(self, data: IngestionData) -> None: ...
