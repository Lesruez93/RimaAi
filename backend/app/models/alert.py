"""Alert model — a composed message dispatched to subscribers."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Alert(Base):
    """A dispatched (or attempted) alert broadcast.

    Records what was sent, to which category/region, and how many recipients
    were reached, so the dispatcher is auditable during the demo.
    """

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(24), index=True)
    region_name: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    channel: Mapped[str] = mapped_column(String(12), default="sms")
    body: Mapped[str] = mapped_column(Text)
    recipients: Mapped[int] = mapped_column(Integer, default=0)
    # "auto" when triggered by the outbreak risk threshold, else "manual".
    trigger: Mapped[str] = mapped_column(String(12), default="manual")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
