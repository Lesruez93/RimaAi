"""Alert composer + dispatcher.

Finds the farmers subscribed to a category (optionally region-scoped), sends the
message via the configured transport, and records an :class:`Alert` audit row.
Subscriptions and alert scheduling are plain rules — no AI is involved here.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.messaging import get_transport
from app.models.alert import Alert
from app.models.farmer import Farmer
from app.models.subscription import Subscription


def _recipients_for(
    db: Session, category: str, channel: str, region_name: str | None
) -> list[str]:
    """Return phone numbers of active subscribers matching the alert.

    Region matching: if ``region_name`` is given, include subscriptions scoped
    to that region OR to no region (national). Consent is required.
    """
    stmt = (
        select(Farmer.phone_number)
        .join(Subscription, Subscription.farmer_id == Farmer.id)
        .where(
            Subscription.category == category,
            Subscription.channel == channel,
            Subscription.active.is_(True),
            Farmer.consent_given.is_(True),
        )
    )
    if region_name is not None:
        stmt = stmt.where(
            (Subscription.region_name == region_name)
            | (Subscription.region_name.is_(None))
        )
    return list(db.scalars(stmt).all())


def dispatch_alert(
    db: Session,
    *,
    category: str,
    body: str,
    region_name: str | None = None,
    channel: str = "sms",
    trigger: str = "manual",
) -> Alert:
    """Compose and dispatch an alert, persisting an audit record.

    Args:
        db: Active DB session.
        category: Alert category to target.
        body: Message text.
        region_name: Optional region to scope delivery.
        channel: Delivery channel (``sms``/``whatsapp``/``ussd``).
        trigger: ``"manual"`` or ``"auto"`` (outbreak threshold).

    Returns:
        The persisted :class:`Alert` with the reached-recipient count.
    """
    recipients = _recipients_for(db, category, channel, region_name)
    transport = get_transport()
    # USSD is pull-based; deliver its alerts over SMS.
    send_channel = "whatsapp" if channel == "whatsapp" else "sms"
    results = transport.broadcast(recipients, body, channel=send_channel)
    reached = sum(1 for r in results if r.ok)

    alert = Alert(
        category=category,
        region_name=region_name,
        channel=channel,
        body=body,
        recipients=reached,
        trigger=trigger,
    )
    db.add(alert)
    db.flush()
    return alert
