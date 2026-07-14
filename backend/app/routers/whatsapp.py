"""WhatsApp router — conversational menu bot (Twilio webhook shape).

Twilio's WhatsApp webhook posts ``From`` (``whatsapp:+263...``) and ``Body``
(the free-text message) for each inbound message — one message at a time, with
no session id like USSD. We keep a small in-memory state machine per phone
number to support the numbered-menu flow (subscribe, my subscriptions,
livestock triage, about), matching what a farmer would see in a real WhatsApp
conversation.

This lets judges try RimaAI's WhatsApp channel via the bundled web simulator
without any Twilio integration. Subscriptions created here persist to the same
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
from app.schemas.triage import TriageRequest
from app.services.triage import triage as run_triage

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

# Menu option index -> subscription category.
_CATEGORY_MENU = {
    "1": ("weather", "Weather alerts"),
    "2": ("disease", "Disease outbreak alerts"),
    "3": ("tips", "Farming tips"),
    "4": ("livestock", "Livestock tips"),
    "5": ("insurance", "Insurance tips"),
}

_MAIN_MENU = (
    "RimaAI - Smart Farming\n"
    "1. Subscribe to alerts\n"
    "2. My subscriptions\n"
    "3. Livestock symptom check\n"
    "4. About RimaAI\n\n"
    "Reply with a number."
)

# Per-phone conversation state, keyed by E.164 number. In-memory: fine for a
# demo/simulator, resets on restart. A production deployment would persist
# this (or design the flow to be stateless via Twilio Content templates).
_SESSIONS: dict[str, str] = {}


def _get_or_create_farmer(db: Session, phone_number: str) -> Farmer:
    """Return the farmer for a phone number, creating a consented one via WhatsApp.

    Messaging the RimaAI WhatsApp number constitutes consent to receive alerts
    on that number; this is recorded on the farmer record.
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
    """Idempotently activate a WhatsApp subscription for a category."""
    farmer = _get_or_create_farmer(db, phone_number)
    existing = db.scalars(
        select(Subscription).where(
            Subscription.farmer_id == farmer.id,
            Subscription.category == category,
            Subscription.channel == "whatsapp",
        )
    ).first()
    if existing:
        existing.active = True
    else:
        db.add(
            Subscription(
                farmer_id=farmer.id,
                category=category,
                channel="whatsapp",
                region_name=farmer.region_name,
            )
        )
    db.commit()


@router.post("/webhook", response_class=PlainTextResponse)
def whatsapp_webhook(
    From: str = Form(...),  # noqa: N803 — Twilio field name
    Body: str = Form(""),  # noqa: N803 — Twilio field name
    db: Session = Depends(get_db),
) -> str:
    """Handle one inbound WhatsApp message and reply with the next screen.

    Menu tree::

        (any message)
          1. Subscribe to alerts -> 1..5 -> category -> confirmation
          2. My subscriptions -> list
          3. Livestock symptom check -> free text -> triage result
          4. About RimaAI -> info
    """
    phone = From.removeprefix("whatsapp:").strip()
    text = Body.strip()
    state = _SESSIONS.get(phone, "menu")

    if state == "await_subscribe_category":
        _SESSIONS.pop(phone, None)
        if text in _CATEGORY_MENU:
            category, label = _CATEGORY_MENU[text]
            _subscribe(db, phone, category)
            return f"You're subscribed to {label} over WhatsApp.\n\n" + _MAIN_MENU
        return "Invalid option.\n\n" + _MAIN_MENU

    if state == "await_triage_symptoms":
        _SESSIONS.pop(phone, None)
        result = run_triage(TriageRequest(message=text or "no symptoms given"))
        return (
            f"{result.condition} ({result.urgency} urgency)\n\n"
            f"{result.advice}\n\n"
            f"{result.escalation}\n\n{result.disclaimer}"
        )

    # Idle / main menu state.
    if text == "1":
        lines = "\n".join(f"{k}. {v[1]}" for k, v in _CATEGORY_MENU.items())
        _SESSIONS[phone] = "await_subscribe_category"
        return f"Subscribe to:\n{lines}"

    if text == "2":
        farmer = db.scalars(
            select(Farmer).where(Farmer.phone_number == phone)
        ).first()
        if farmer is None:
            return "You have no subscriptions yet. Reply 1 to subscribe."
        subs = db.scalars(
            select(Subscription).where(
                Subscription.farmer_id == farmer.id, Subscription.active.is_(True)
            )
        ).all()
        if not subs:
            return "You have no active subscriptions."
        listed = ", ".join(sorted({s.category for s in subs}))
        return f"Active subscriptions: {listed}."

    if text == "3":
        _SESSIONS[phone] = "await_triage_symptoms"
        return "Describe what you're seeing in the animal (e.g. swelling, coughing, diarrhoea)."

    if text == "4":
        return (
            "RimaAI helps farmers with disease scans, livestock advice, forecasts "
            "and outbreak alerts. Visit an AGRITEX office to learn more."
        )

    return "Welcome to RimaAI!\n\n" + _MAIN_MENU
