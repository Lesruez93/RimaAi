"""Forecast schemas."""

from __future__ import annotations

from pydantic import BaseModel


class ForecastResponse(BaseModel):
    """Planting-window / rainfall guidance for a region."""

    region_name: str
    season: str
    planting_window: str
    expected_rainfall_mm: float
    confidence: str
    advice: str
    source: str = "seeded_historical"
