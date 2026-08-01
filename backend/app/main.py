import logging

from fastapi import FastAPI

from app.api.router import api_router
from app.core.logging import configure_logging
from app.core.settings import get_settings

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="NFL Analytics Backend", version="0.1.0")
app.include_router(api_router)


@app.get("/", summary="Service info")
def root() -> dict[str, str]:
    logger.debug("Root route requested")
    return {"service": "nfl-analytics-backend", "status": "running"}
