"""Guard router — RimaAI Guard intrusion detection + event history."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.guard import CameraSettings, GuardEvent
from app.schemas.guard import (
    CameraSettingsOut,
    CameraSettingsUpdate,
    GuardDetectRequest,
    GuardDetectResponse,
    GuardEventOut,
)
from app.services.guard_detection import detect, top_detection

router = APIRouter(prefix="/guard", tags=["guard"])


@router.post("/detect", response_model=GuardDetectResponse)
def guard_detect(
    payload: GuardDetectRequest, db: Session = Depends(get_db)
) -> GuardDetectResponse:
    """Run detection on a sample frame; persist an event on intrusion.

    Returns bounding boxes for UI overlay and whether the frame is an intrusion.
    Only intrusions (person/vehicle) create a :class:`GuardEvent`.
    """
    boxes, is_intrusion = detect(payload.frame_id)
    event_id: int | None = None
    if is_intrusion:
        top = top_detection([b for b in boxes if b.label in {"person", "vehicle"}])
        event = GuardEvent(
            camera_id=payload.camera_id,
            label=top.label if top else "unknown",
            confidence=top.confidence if top else 0.0,
            boxes_json=json.dumps([b.model_dump() for b in boxes]),
            is_intrusion=True,
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        event_id = event.id

    return GuardDetectResponse(
        camera_id=payload.camera_id,
        frame_id=payload.frame_id,
        boxes=boxes,
        is_intrusion=is_intrusion,
        event_id=event_id,
    )


@router.get("/events", response_model=list[GuardEventOut])
def list_events(limit: int = 50, db: Session = Depends(get_db)) -> list[GuardEvent]:
    """List recent guard events, newest first."""
    return list(
        db.scalars(select(GuardEvent).order_by(GuardEvent.id.desc()).limit(limit)).all()
    )


@router.get("/camera", response_model=CameraSettingsOut)
def get_camera_settings(
    camera_id: str = "kraal-cam-01", db: Session = Depends(get_db)
) -> CameraSettings:
    """Fetch a camera's stream configuration, creating a default row on first use."""
    settings = db.get(CameraSettings, camera_id)
    if settings is None:
        settings = CameraSettings(camera_id=camera_id, stream_url=None, mode="demo")
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.put("/camera", response_model=CameraSettingsOut)
def update_camera_settings(
    payload: CameraSettingsUpdate, db: Session = Depends(get_db)
) -> CameraSettings:
    """Create or update a camera's stream URL and demo/live mode.

    Shared by the app and the dashboard so configuring a camera from either
    surface is immediately reflected on the other.
    """
    settings = db.get(CameraSettings, payload.camera_id)
    if settings is None:
        settings = CameraSettings(camera_id=payload.camera_id)
        db.add(settings)
    settings.stream_url = payload.stream_url
    settings.mode = payload.mode
    db.commit()
    db.refresh(settings)
    return settings
