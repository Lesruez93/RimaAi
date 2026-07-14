"""Guard event model — RimaAI Guard intrusion detections."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GuardEvent(Base):
    """An intrusion event flagged by the Guard object-detection service."""

    __tablename__ = "guard_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    camera_id: Mapped[str] = mapped_column(String(64), index=True)
    # Detected class that triggered the event: "person" or "vehicle".
    label: Mapped[str] = mapped_column(String(32))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    # JSON-encoded bounding boxes for the frame, for UI overlay.
    boxes_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_intrusion: Mapped[bool] = mapped_column(Boolean, default=False)
    frame_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
