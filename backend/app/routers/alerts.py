"""Alerts router — compose and dispatch alerts to subscribers."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertDispatchRequest, AlertOut
from app.services.dispatch import dispatch_alert

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("/dispatch", response_model=AlertOut)
def dispatch(payload: AlertDispatchRequest, db: Session = Depends(get_db)) -> Alert:
    """Compose an alert and dispatch it to matching subscribers.

    Delivery uses the configured messaging transport (console in dev). An audit
    row is persisted with the number of recipients reached.
    """
    alert = dispatch_alert(
        db,
        category=payload.category,
        body=payload.body,
        region_name=payload.region_name,
        channel=payload.channel,
        trigger="manual",
    )
    db.commit()
    db.refresh(alert)
    return alert


@router.get("", response_model=list[AlertOut])
def list_alerts(limit: int = 50, db: Session = Depends(get_db)) -> list[Alert]:
    """List recent dispatched alerts, newest first."""
    return list(
        db.scalars(select(Alert).order_by(Alert.id.desc()).limit(limit)).all()
    )
