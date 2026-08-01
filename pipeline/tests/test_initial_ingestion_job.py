from __future__ import annotations

from dataclasses import dataclass

from pipeline.config.ingestion import IngestionConfig
from pipeline.ingestion import IngestionCounts, IngestionData, RawIngestionData, SeasonRecord, TeamRecord
from pipeline.jobs.initial_ingestion import run_initial_ingestion_job
from pipeline.transform.ingestion import IngestionTransformStage
from pipeline.validate.ingestion import IngestionValidateStage


def test_validate_stage_drops_invalid_records() -> None:
    stage = IngestionValidateStage()
    raw = RawIngestionData(
        teams=[{"team_abbr": "BUF", "team_name": "Buffalo", "team_nick": "Bills"}, {"team_name": "Bad"}],
        players=[{"gsis_id": "00-001", "name": "Jane Doe", "first_name": "Jane"}, {"name": "No Id"}],
        seasons=[{"season": 2024}, {"season": 3024}],
    )

    validated = stage.run(raw)
    assert len(validated.teams) == 1
    assert len(validated.players) == 1
    assert len(validated.seasons) == 1


def test_transform_stage_deduplicates_records() -> None:
    stage = IngestionTransformStage()
    raw = RawIngestionData(
        teams=[
            {"team_abbr": "BUF", "team_name": "Buffalo", "team_nick": "Bills"},
            {"team_abbr": "BUF", "team_name": "Buffalo", "team_nick": "Bills"},
        ],
        players=[
            {"gsis_id": "00-001", "name": "Jane Doe", "first_name": "Jane", "last_name": "Doe"},
            {"gsis_id": "00-001", "name": "Jane Doe", "first_name": "Jane", "last_name": "Doe"},
        ],
        seasons=[{"season": 2024}, {"season": 2024}, {"season": 2023}],
    )

    transformed = stage.run(raw)
    assert len(transformed.teams) == 1
    assert len(transformed.players) == 1
    assert [season.year for season in transformed.seasons] == [2023, 2024]


@dataclass
class FakeExtractStage:
    def run(self, seasons: list[int]) -> RawIngestionData:
        assert seasons == [2024]
        return RawIngestionData(
            teams=[{"team_abbr": "BUF", "team_name": "Buffalo", "team_nick": "Bills"}],
            players=[{"gsis_id": "00-001", "name": "Jane Doe", "first_name": "Jane", "last_name": "Doe"}],
            seasons=[{"season": 2024}],
        )


@dataclass
class FakeLoadStage:
    loaded_data: IngestionData | None = None

    def run(self, data: IngestionData) -> IngestionCounts:
        self.loaded_data = data
        return IngestionCounts(teams=len(data.teams), players=len(data.players), seasons=len(data.seasons))


@dataclass
class FakeVerifyStage:
    called: bool = False

    def run(self, data: IngestionData) -> None:
        assert data.teams == [TeamRecord(abbreviation="BUF", name="Bills", city="Buffalo")]
        assert data.seasons == [SeasonRecord(year=2024, name="Regular Season")]
        self.called = True


def test_initial_ingestion_job_runs_all_stages() -> None:
    loader = FakeLoadStage()
    verifier = FakeVerifyStage()
    result = run_initial_ingestion_job(
        IngestionConfig(database_url="postgresql://example", seasons=[2024]),
        extract_stage=FakeExtractStage(),
        validate_stage=IngestionValidateStage(),
        transform_stage=IngestionTransformStage(),
        load_stage=loader,
        verify_stage=verifier,
    )

    assert result.extracted == IngestionCounts(teams=1, players=1, seasons=1)
    assert result.loaded == IngestionCounts(teams=1, players=1, seasons=1)
    assert loader.loaded_data is not None
    assert verifier.called
