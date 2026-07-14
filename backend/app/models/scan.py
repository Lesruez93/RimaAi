"""Scan history model — crop/livestock image classification results."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ScanHistory(Base):
    """A single disease-scan result, from either on-device or server inference."""

    __tablename__ = "scan_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    farmer_id: Mapped[int | None] = mapped_column(
        ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    # "crop" or "livestock"
    scan_type: Mapped[str] = mapped_column(String(16), default="crop")
    label: Mapped[str] = mapped_column(String(120))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    advice: Mapped[str | None] = mapped_column(Text, nullable=True)
    # "device" (TFLite on-device) or "server" (fallback API)
    source: Mapped[str] = mapped_column(String(12), default="device")
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
