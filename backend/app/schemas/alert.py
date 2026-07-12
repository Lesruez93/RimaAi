"""Alert dispatch schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AlertDispatchRequest(BaseModel):
    """Compose and dispatch an alert to matching subscribers."""

    category: str = Field(pattern="^(weather|disease|tips|livestock|insurance)$")
    body: str = Field(min_length=1, max_length=640)
    region_name: str | None = None
    channel: str = Field(default="sms", pattern="^(sms|ussd|whatsapp)$")


class AlertOut(BaseModel):
    """Public alert representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    region_name: str | None
    channel: str
    body: str
    recipients: int
    trigger: str
    created_at: datetime
