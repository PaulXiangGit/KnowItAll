from fastapi import APIRouter
from pydantic import BaseModel

from knowitall import __version__
from knowitall.config import get_settings

router = APIRouter(tags=["system"])


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", version=__version__, environment=settings.environment)


@router.get("/ready", response_model=HealthResponse)
async def ready() -> HealthResponse:
    # Dependency checks are added when persistence adapters land in P01-T02.
    settings = get_settings()
    return HealthResponse(status="ready", version=__version__, environment=settings.environment)
