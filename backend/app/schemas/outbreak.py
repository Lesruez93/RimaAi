"""Outbreak reporting + heat map schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OutbreakReportCreate(BaseModel):
    """Create a community outbreak report."""

    region_name: str
    outbreak_type: str = Field(
        pattern="^(crop_disease|armyworm|locusts|tick_disease|flood)$"
    )
    description: str | None = None
    farmer_id: int | None = None
    image_path: str | None = None


class OutbreakReportOut(BaseModel):
    """Public outbreak report representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    region_name: str
    outbreak_type: str
    description: str | None
    reporter_trust: float
    created_at: datetime


class DistrictRiskOut(BaseModel):
    """Aggregated risk for one district + outbreak type, for the heat map."""

    model_config = ConfigDict(from_attributes=True)

    region_name: str
    outbreak_type: str
    score: float
    level: str
    report_count: int
    latitude: float = 0.0
    longitude: float = 0.0


class OutbreakReportResult(BaseModel):
    """Result of submitting a report, including any auto-triggered alert."""

    report: OutbreakReportOut
    risk: DistrictRiskOut
    alert_dispatched: bool = False
    alert_recipients: int = 0
