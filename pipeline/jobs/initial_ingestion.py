from __future__ import annotations

import logging
from logging.config import dictConfig

from pipeline.config.ingestion import IngestionConfig
from pipeline.extract.nflverse import NflverseExtractStage
from pipeline.ingestion import (
    ExtractStage,
    IngestionCounts,
    IngestionJobResult,
    LoadStage,
    TransformStage,
    ValidateStage,
    VerifyStage,
)
from pipeline.load.postgres import PostgresLoadStage
from pipeline.transform.ingestion import IngestionTransformStage
from pipeline.validate.ingestion import IngestionValidateStage
from pipeline.verify.ingestion import IngestionVerifyStage

LOGGER = logging.getLogger(__name__)


def configure_pipeline_logging(log_level: str) -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": log_level,
                }
            },
            "root": {
                "handlers": ["console"],
                "level": log_level,
            },
        }
    )


def run_initial_ingestion_job(
    config: IngestionConfig | None = None,
    *,
    extract_stage: ExtractStage | None = None,
    validate_stage: ValidateStage | None = None,
    transform_stage: TransformStage | None = None,
    load_stage: LoadStage | None = None,
    verify_stage: VerifyStage | None = None,
) -> IngestionJobResult:
    resolved_config = config or IngestionConfig.from_env()
    configure_pipeline_logging(resolved_config.log_level)

    extractor = extract_stage or NflverseExtractStage()
    validator = validate_stage or IngestionValidateStage()
    transformer = transform_stage or IngestionTransformStage()
    loader = load_stage or PostgresLoadStage(database_url=resolved_config.database_url)
    verifier = verify_stage or IngestionVerifyStage(database_url=resolved_config.database_url)

    LOGGER.info("Starting initial ingestion job", extra={"seasons": resolved_config.seasons})
    raw = extractor.run(seasons=resolved_config.seasons)
    extracted_counts = IngestionCounts(
        teams=len(raw.teams),
        players=len(raw.players),
        seasons=len(raw.seasons),
    )

    validated = validator.run(raw)
    transformed = transformer.run(validated)
    loaded_counts = loader.run(transformed)
    verifier.run(transformed)

    result = IngestionJobResult(extracted=extracted_counts, loaded=loaded_counts)
    LOGGER.info(
        "Initial ingestion job complete",
        extra={
            "teams_loaded": result.loaded.teams,
            "players_loaded": result.loaded.players,
            "seasons_loaded": result.loaded.seasons,
        },
    )
    return result


def main() -> None:
    run_initial_ingestion_job()


if __name__ == "__main__":
    main()
