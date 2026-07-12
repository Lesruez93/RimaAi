"""Outbreak risk aggregation (plain weighted rules — explicitly NOT AI).

Per district + outbreak type we compute:

    score = sum over recent reports of ( reporter_trust * recency_weight )

where ``recency_weight`` decays linearly from 1.0 (today) to 0.0 at the edge of
the configured window. The score maps to low/moderate/high bands via thresholds.

This is deliberately transparent and auditable. Outbreak *spread prediction*
(an ML task) is on the roadmap once real report volume exists — see README.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.outbreak import DistrictRisk, OutbreakReport


def _recency_weight(created_at: datetime, window_days: int, now: datetime) -> float:
    """Linear recency decay in [0, 1]; 1.0 today, 0.0 at the window edge."""
    # Normalise naive timestamps (SQLite) to UTC-aware for safe subtraction.
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    age_days = (now - created_at).total_seconds() / 86400.0
    if age_days >= window_days:
        return 0.0
    return max(0.0, 1.0 - age_days / window_days)


def level_for(score: float) -> str:
    """Map an aggregate score to a risk level using configured thresholds."""
    s = get_settings()
    if score >= s.outbreak_high_risk_threshold:
        return "high"
    if score >= s.outbreak_moderate_risk_threshold:
        return "moderate"
    return "low"


def recompute_district_risk(
    db: Session, region_name: str, outbreak_type: str
) -> DistrictRisk:
    """Recompute and persist the cached risk row for a district + outbreak type.

    Returns the up-to-date :class:`DistrictRisk` (created if absent).
    """
    settings = get_settings()
    now = datetime.now(timezone.utc)
    window = settings.outbreak_recency_window_days
    cutoff = now - timedelta(days=window)

    reports = db.scalars(
        select(OutbreakReport).where(
            OutbreakReport.region_name == region_name,
            OutbreakReport.outbreak_type == outbreak_type,
            OutbreakReport.created_at >= cutoff,
        )
    ).all()

    score = sum(
        r.reporter_trust * _recency_weight(r.created_at, window, now) for r in reports
    )
    score = round(score, 3)

    risk = db.scalars(
        select(DistrictRisk).where(
            DistrictRisk.region_name == region_name,
            DistrictRisk.outbreak_type == outbreak_type,
        )
    ).first()
    if risk is None:
        risk = DistrictRisk(region_name=region_name, outbreak_type=outbreak_type)
        db.add(risk)

    risk.score = score
    risk.level = level_for(score)
    risk.report_count = len(reports)
    db.flush()
    return risk
