"""Subscriptions router — farmer registration + alert subscription CRUD."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.farmer import Farmer
from app.models.subscription import Subscription
from app.schemas.farmer import (
    FarmerCreate,
    FarmerOut,
    SubscriptionCreate,
    SubscriptionOut,
)

router = APIRouter(tags=["subscriptions"])


@router.post("/farmers", response_model=FarmerOut, status_code=status.HTTP_201_CREATED)
def register_farmer(payload: FarmerCreate, db: Session = Depends(get_db)) -> Farmer:
    """Register a farmer.

    Consent is mandatory under the Data Protection Act [Chapter 11:12]: without
    ``consent_given`` we refuse to store the phone number.
    """
    if not payload.consent_given:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consent is required to store your phone number for alerts.",
        )
    existing = db.scalars(
        select(Farmer).where(Farmer.phone_number == payload.phone_number)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A farmer with this phone number already exists.",
        )
    farmer = Farmer(**payload.model_dump())
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    return farmer


@router.get("/farmers/{farmer_id}", response_model=FarmerOut)
def get_farmer(farmer_id: int, db: Session = Depends(get_db)) -> Farmer:
    """Fetch a single farmer by id."""
    farmer = db.get(Farmer, farmer_id)
    if farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer


@router.post(
    "/subscriptions",
    response_model=SubscriptionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_subscription(
    payload: SubscriptionCreate, db: Session = Depends(get_db)
) -> Subscription:
    """Create or re-activate a subscription (idempotent per farmer/category/channel)."""
    if db.get(Farmer, payload.farmer_id) is None:
        raise HTTPException(status_code=404, detail="Farmer not found")

    existing = db.scalars(
        select(Subscription).where(
            Subscription.farmer_id == payload.farmer_id,
            Subscription.category == payload.category,
            Subscription.channel == payload.channel,
        )
    ).first()
    if existing:
        existing.active = payload.active
        existing.region_name = payload.region_name
        db.commit()
        db.refresh(existing)
        return existing

    sub = Subscription(**payload.model_dump())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


@router.get("/subscriptions/{farmer_id}", response_model=list[SubscriptionOut])
def list_subscriptions(
    farmer_id: int, db: Session = Depends(get_db)
) -> list[Subscription]:
    """List all subscriptions for a farmer."""
    return list(
        db.scalars(
            select(Subscription).where(Subscription.farmer_id == farmer_id)
        ).all()
    )


@router.delete("/subscriptions/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_subscription(subscription_id: int, db: Session = Depends(get_db)) -> None:
    """Deactivate (soft-cancel) a subscription."""
    sub = db.get(Subscription, subscription_id)
    if sub is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    sub.active = False
    db.commit()
