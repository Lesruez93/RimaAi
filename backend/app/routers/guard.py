"""Guard router — RimaAI Guard intrusion detection + event history."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.guard import GuardEvent
from app.schemas.guard import GuardDetectRequest, GuardDetectResponse, GuardEventOut
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
