"""USSD router — feature-phone menu tree (Africa's Talking callback format).

Africa's Talking posts ``sessionId``, ``serviceCode``, ``phoneNumber`` and
``text`` (the user's accumulated ``*``-joined inputs). The handler replies with
plain text prefixed ``CON`` (expect more input) or ``END`` (final screen).

This lets judges click through ``*123#`` flows via the bundled web simulator
without any telco integration. Subscriptions created here persist to the same
database the app and alert dispatcher use.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Form
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.farmer import Farmer
from app.models.subscription import Subscription

router = APIRouter(prefix="/ussd", tags=["ussd"])

# Menu option index -> subscription category.
_CATEGORY_MENU = {
    "1": ("weather", "Weather alerts"),
    "2": ("disease", "Disease outbreak alerts"),
    "3": ("tips", "Farming tips"),
    "4": ("livestock", "Livestock tips"),
    "5": ("insurance", "Insurance tips"),
}


def _get_or_create_farmer(db: Session, phone_number: str) -> Farmer:
    """Return the farmer for a phone number, creating a consented one via USSD.

    Dialling the USSD subscription flow constitutes consent to receive alerts on
    that number; this is recorded on the farmer record.
    """
    farmer = db.scalars(
        select(Farmer).where(Farmer.phone_number == phone_number)
    ).first()
    if farmer is None:
        farmer = Farmer(phone_number=phone_number, consent_given=True)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
    return farmer


def _subscribe(db: Session, phone_number: str, category: str) -> None:
    """Idempotently activate an SMS subscription for a category."""
    farmer = _get_or_create_farmer(db, phone_number)
    existing = db.scalars(
        select(Subscription).where(
            Subscription.farmer_id == farmer.id,
            Subscription.category == category,
            Subscription.channel == "sms",
        )
    ).first()
    if existing:
        existing.active = True
    else:
        db.add(
            Subscription(
                farmer_id=farmer.id,
                category=category,
                channel="sms",
                region_name=farmer.region_name,
            )
        )
    db.commit()


@router.post("", response_class=PlainTextResponse)
def ussd_callback(
    phoneNumber: str = Form(...),  # noqa: N803 — telco field name
    text: str = Form(""),
    sessionId: str = Form("sim-session"),  # noqa: N803
    serviceCode: str = Form("*123#"),  # noqa: N803
    db: Session = Depends(get_db),
) -> str:
    """Handle one USSD step and return a ``CON``/``END`` response.

    Menu tree::

        *123#
          1. Subscribe to alerts
             1..5 -> category -> END confirmation
          2. My subscriptions -> END list
          3. About RimaAI -> END info
    """
    parts = [p for p in text.split("*") if p != ""] if text else []

    # Root menu
    if not parts:
        return (
            "CON RimaAI - Smart Farming\n"
            "1. Subscribe to alerts\n"
            "2. My subscriptions\n"
            "3. About RimaAI"
        )

    # Branch 1: subscribe
    if parts[0] == "1":
        if len(parts) == 1:
            lines = "\n".join(f"{k}. {v[1]}" for k, v in _CATEGORY_MENU.items())
            return f"CON Subscribe to:\n{lines}"
        choice = parts[1]
        if choice in _CATEGORY_MENU:
            category, label = _CATEGORY_MENU[choice]
            _subscribe(db, phoneNumber, category)
            return f"END You are subscribed to {label}. Standard SMS rates may apply."
        return "END Invalid option. Dial *123# to try again."

    # Branch 2: list subscriptions
    if parts[0] == "2":
        farmer = db.scalars(
            select(Farmer).where(Farmer.phone_number == phoneNumber)
        ).first()
        if farmer is None:
            return "END You have no subscriptions yet. Dial *123# and choose 1."
        subs = db.scalars(
            select(Subscription).where(
                Subscription.farmer_id == farmer.id, Subscription.active.is_(True)
            )
        ).all()
        if not subs:
            return "END You have no active subscriptions."
        listed = ", ".join(sorted({s.category for s in subs}))
        return f"END Active subscriptions: {listed}."

    # Branch 3: about
    if parts[0] == "3":
        return (
            "END RimaAI helps farmers with disease scans, livestock advice, "
            "forecasts and outbreak alerts. Visit an AGRITEX office to learn more."
        )

    return "END Invalid option. Dial *123# to start again."
