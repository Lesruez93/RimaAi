"""Subscription model — per-farmer alert channel opt-ins."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

# Alert categories a farmer can subscribe to.
ALERT_CATEGORIES = (
    "weather",
    "disease",
    "tips",
    "livestock",
    "insurance",
)

# Delivery channels.
CHANNELS = ("sms", "ussd", "whatsapp")


class Subscription(Base):
    """A farmer's opt-in to one alert category on one channel for a region."""

    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    farmer_id: Mapped[int] = mapped_column(
        ForeignKey("farmers.id", ondelete="CASCADE"), index=True
    )
    category: Mapped[str] = mapped_column(String(24), index=True)
    channel: Mapped[str] = mapped_column(String(12), default="sms")
    region_name: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
