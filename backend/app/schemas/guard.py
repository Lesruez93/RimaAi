"""RimaAI Guard schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BoundingBox


class GuardDetectRequest(BaseModel):
    """Request to run detection on a named sample frame.

    In the MVP the backend ships with sample frames; ``frame_id`` selects one.
    A real deployment would accept an uploaded image instead.
    """

    camera_id: str = "kraal-cam-01"
    frame_id: str = "sample_night_01"


class GuardDetectResponse(BaseModel):
    """Detection result for one frame."""

    camera_id: str
    frame_id: str
    boxes: list[BoundingBox] = Field(default_factory=list)
    is_intrusion: bool = False
    event_id: int | None = None


class GuardEventOut(BaseModel):
    """Public guard event representation for the alert history list."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    camera_id: str
    label: str
    confidence: float
    is_intrusion: bool
    created_at: datetime
