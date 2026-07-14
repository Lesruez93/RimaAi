"""Outbreaks router — community reporting + risk heat map.

Submitting a report recomputes the district's risk (plain weighted rules). When
a district crosses the high-risk threshold, a region-targeted disease alert is
auto-dispatched to subscribers, closing the crowdsourced early-warning loop.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.outbreak import DistrictRisk, OutbreakReport
from app.models.region import Region
from app.schemas.outbreak import (
    DistrictRiskOut,
    OutbreakReportCreate,
    OutbreakReportOut,
    OutbreakReportResult,
)
from app.services.dispatch import dispatch_alert
from app.services.outbreak import recompute_district_risk

router = APIRouter(prefix="/outbreaks", tags=["outbreaks"])

# Human-readable labels for auto-composed alert bodies.
_TYPE_LABELS = {
    "crop_disease": "crop disease",
    "armyworm": "fall armyworm",
    "locusts": "locust swarms",
    "tick_disease": "tick-borne (January) disease",
    "flood": "flooding",
}


@router.post("/report", response_model=OutbreakReportResult)
def report_outbreak(
    payload: OutbreakReportCreate, db: Session = Depends(get_db)
) -> OutbreakReportResult:
    """Create a community outbreak report and refresh district risk.

    If the district becomes high-risk, auto-dispatch a targeted disease alert.
    """
    # Verified/officer reports would carry higher trust; community default 0.5.
    report = OutbreakReport(**payload.model_dump(), reporter_trust=0.5)
    db.add(report)
    db.flush()

    risk = recompute_district_risk(db, payload.region_name, payload.outbreak_type)

    alert_dispatched = False
    alert_recipients = 0
    if risk.level == "high":
        label = _TYPE_LABELS.get(payload.outbreak_type, payload.outbreak_type)
        body = (
            f"RimaAI ALERT: High {label} risk reported in {payload.region_name}. "
            "Inspect your crops/livestock, act early, and contact AGRITEX/your vet."
        )
        alert = dispatch_alert(
            db,
            category="disease",
            body=body,
            region_name=payload.region_name,
            channel="sms",
            trigger="auto",
        )
        alert_dispatched = True
        alert_recipients = alert.recipients

    db.commit()
    db.refresh(report)
    db.refresh(risk)
    return OutbreakReportResult(
        report=OutbreakReportOut.model_validate(report),
        risk=DistrictRiskOut.model_validate(risk),
        alert_dispatched=alert_dispatched,
        alert_recipients=alert_recipients,
    )


@router.get("/map", response_model=list[DistrictRiskOut])
def outbreak_map(
    outbreak_type: str | None = None, db: Session = Depends(get_db)
) -> list[DistrictRiskOut]:
    """Return per-district risk rows for the heat map, optionally filtered by type.

    District centroid coordinates are joined in from the regions table so the
    app can place coloured markers without a second request.
    """
    stmt = select(DistrictRisk)
    if outbreak_type:
        stmt = stmt.where(DistrictRisk.outbreak_type == outbreak_type)
    rows = db.scalars(stmt).all()

    # Build a name -> centroid lookup once.
    regions = {r.name: r for r in db.scalars(select(Region)).all()}
    out: list[DistrictRiskOut] = []
    for row in rows:
        region = regions.get(row.region_name)
        dto = DistrictRiskOut.model_validate(row)
        if region:
            dto.latitude = region.latitude
            dto.longitude = region.longitude
        out.append(dto)
    return out


@router.get("/reports", response_model=list[OutbreakReportOut])
def list_reports(limit: int = 100, db: Session = Depends(get_db)) -> list[OutbreakReport]:
    """List recent outbreak reports, newest first."""
    return list(
        db.scalars(
            select(OutbreakReport).order_by(OutbreakReport.id.desc()).limit(limit)
        ).all()
    )
