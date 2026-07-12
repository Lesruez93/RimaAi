"""Outbreak reporting + per-district risk aggregation models."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

# Outbreak types farmers can report from the app.
OUTBREAK_TYPES = (
    "crop_disease",
    "armyworm",
    "locusts",
    "tick_disease",
    "flood",
)

RISK_LEVELS = ("low", "moderate", "high")


class OutbreakReport(Base):
    """A community-submitted outbreak report."""

    __tablename__ = "outbreak_reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    farmer_id: Mapped[int | None] = mapped_column(nullable=True, index=True)
    region_name: Mapped[str] = mapped_column(String(120), index=True)
    outbreak_type: Mapped[str] = mapped_column(String(32), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # Reporter trust weight in [0, 1]; verified/officer reports weigh more.
    reporter_trust: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class DistrictRisk(Base):
    """Cached, aggregated risk level per district + outbreak type.

    NOTE: This is computed by plain weighted rules (report count x recency x
    reporter trust), NOT by any AI/ML model. See ``services/outbreak.py``.
    """

    __tablename__ = "district_risk"

    id: Mapped[int] = mapped_column(primary_key=True)
    region_name: Mapped[str] = mapped_column(String(120), index=True)
    outbreak_type: Mapped[str] = mapped_column(String(32), index=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    level: Mapped[str] = mapped_column(String(12), default="low")
    report_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
