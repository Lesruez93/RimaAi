"""Planting-window / rainfall forecast service (seeded-data stub).

Reads from a small seeded historical table baked into this module. In production
this is replaced by a time-series model over Meteorological Services Department
(MSD) + satellite data. The interface (``get_forecast(region)``) stays the same.
"""

from __future__ import annotations

from app.schemas.forecast import ForecastResponse

# Seeded per-region climatological summary for the 2026/27 main season.
# Values are illustrative demo data, NOT a live forecast.
_SEEDED: dict[str, dict[str, object]] = {
    "Harare": {
        "planting_window": "15 Nov - 10 Dec",
        "expected_rainfall_mm": 780.0,
        "confidence": "medium",
        "advice": "Plant medium-maturity maize after the first effective rains (>25mm over 2 days).",
    },
    "Bulawayo": {
        "planting_window": "25 Nov - 20 Dec",
        "expected_rainfall_mm": 520.0,
        "confidence": "medium",
        "advice": "Drier region — favour small grains (sorghum, millet) and short-season maize.",
    },
    "Mutare": {
        "planting_window": "10 Nov - 5 Dec",
        "expected_rainfall_mm": 900.0,
        "confidence": "high",
        "advice": "Higher rainfall — long-season maize viable; watch for leaf blight in wet spells.",
    },
    "Masvingo": {
        "planting_window": "20 Nov - 15 Dec",
        "expected_rainfall_mm": 560.0,
        "confidence": "low",
        "advice": "Erratic rains — stagger planting and keep drought-tolerant varieties ready.",
    },
    "Gweru": {
        "planting_window": "18 Nov - 12 Dec",
        "expected_rainfall_mm": 640.0,
        "confidence": "medium",
        "advice": "Prepare land early; apply basal fertiliser at planting for even establishment.",
    },
}

_DEFAULT = {
    "planting_window": "20 Nov - 15 Dec",
    "expected_rainfall_mm": 650.0,
    "confidence": "low",
    "advice": "No local record yet — follow provincial AGRITEX planting guidance and monitor rains.",
}


def get_forecast(region_name: str, season: str = "2026/27") -> ForecastResponse:
    """Return the seeded planting-window forecast for a region."""
    data = _SEEDED.get(region_name, _DEFAULT)
    return ForecastResponse(
        region_name=region_name,
        season=season,
        planting_window=str(data["planting_window"]),
        expected_rainfall_mm=float(data["expected_rainfall_mm"]),  # type: ignore[arg-type]
        confidence=str(data["confidence"]),
        advice=str(data["advice"]),
    )
