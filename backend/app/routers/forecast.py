"""Forecast router — planting-window / rainfall guidance."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.forecast import ForecastResponse
from app.services.forecast import get_forecast

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("", response_model=ForecastResponse)
def forecast(region_name: str, season: str = "2026/27") -> ForecastResponse:
    """Return seeded planting-window guidance for a region."""
    return get_forecast(region_name, season)
