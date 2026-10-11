from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from knowitall import __version__
from knowitall.api.routers import analyses, health
from knowitall.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    get_settings()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="KnowItAll API",
        version=__version__,
        description="Evidence-first business analysis agent API",
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(analyses.router, prefix="/api/v1")
    return app


app = create_app()


def run() -> None:
    settings = get_settings()
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
