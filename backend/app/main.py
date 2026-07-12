"""RimaAI FastAPI application entry point."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import init_db
from app.routers import (
    alerts,
    forecast,
    guard,
    outbreaks,
    scan,
    subscriptions,
    triage,
    ussd,
)

logging.basicConfig(level=logging.INFO)
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Create database tables on startup (idempotent)."""
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "AI-powered smart farming companion for Zimbabwean farmers: crop/livestock "
        "disease scanning, triage, forecasts, multi-channel alerts, Guard "
        "surveillance and community outbreak mapping."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
def health() -> dict[str, str]:
    """Liveness probe with the active messaging/triage backends."""
    return {
        "status": "ok",
        "environment": settings.environment,
        "messaging_transport": settings.messaging_transport,
        "triage_backend": settings.triage_backend,
    }


for _router in (
    scan.router,
    triage.router,
    forecast.router,
    subscriptions.router,
    alerts.router,
    guard.router,
    outbreaks.router,
    ussd.router,
):
    app.include_router(_router)
