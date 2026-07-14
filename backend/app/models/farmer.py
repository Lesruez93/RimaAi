"""Farmer (end-user) model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Farmer(Base):
    """A registered farmer.

    Personal data is deliberately minimal (phone number + optional name) to
    stay proportionate under the Data Protection Act [Chapter 11:12].
    ``consent_given`` records the signup consent checkbox required for
    processing the phone number for alerts.
    """

    __tablename__ = "farmers"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    # ISO 639-1 style code: en | sn (Shona) | nd (Ndebele)
    language: Mapped[str] = mapped_column(String(4), default="en")
    region_name: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
