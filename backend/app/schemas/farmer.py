"""Farmer + subscription schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FarmerCreate(BaseModel):
    """Payload to register a farmer. ``consent_given`` must be true to store data."""

    phone_number: str = Field(min_length=6, max_length=24)
    name: str | None = None
    language: str = Field(default="en", pattern="^(en|sn|nd)$")
    region_name: str | None = None
    consent_given: bool = False


class FarmerOut(BaseModel):
    """Public farmer representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    phone_number: str
    name: str | None
    language: str
    region_name: str | None
    consent_given: bool
    created_at: datetime


class SubscriptionCreate(BaseModel):
    """Create/toggle a subscription for a farmer."""

    farmer_id: int
    category: str = Field(pattern="^(weather|disease|tips|livestock|insurance)$")
    channel: str = Field(default="sms", pattern="^(sms|ussd|whatsapp)$")
    region_name: str | None = None
    active: bool = True


class SubscriptionOut(BaseModel):
    """Public subscription representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    farmer_id: int
    category: str
    channel: str
    region_name: str | None
    active: bool
    created_at: datetime
