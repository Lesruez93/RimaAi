"""Scan (crop/livestock inference) schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScanResult(BaseModel):
    """Inference result returned to the app."""

    label: str
    confidence: float
    advice: str
    scan_type: str
    source: str = "server"
    # Localized advice keyed by language code for offline caching in the app.
    advice_i18n: dict[str, str] = Field(default_factory=dict)
