"""Twilio WhatsApp transport.

WhatsApp uses the same Twilio REST client but requires ``whatsapp:`` prefixed
addresses on both ends.
"""

from __future__ import annotations

import logging

from app.core.config import Settings
from app.messaging.base import MessageResult, MessageTransport

logger = logging.getLogger("rimaai.messaging.twilio_whatsapp")


def _ensure_prefix(number: str) -> str:
    """Ensure a number carries the Twilio ``whatsapp:`` channel prefix."""
    return number if number.startswith("whatsapp:") else f"whatsapp:{number}"


class TwilioWhatsAppTransport(MessageTransport):
    """Send WhatsApp messages via the Twilio REST API."""

    name = "twilio_whatsapp"

    def __init__(self, settings: Settings) -> None:
        """Store credentials; the client is created lazily on first send."""
        self._settings = settings
        self._client = None

    def _get_client(self):  # type: ignore[no-untyped-def]
        """Lazily construct and cache the Twilio client."""
        if self._client is None:
            from twilio.rest import Client  # imported lazily

            self._client = Client(
                self._settings.twilio_account_sid,
                self._settings.twilio_auth_token,
            )
        return self._client

    def send_sms(self, to: str, body: str) -> MessageResult:
        """Not supported here; use :class:`TwilioSmsTransport`."""
        raise NotImplementedError("Use TwilioSmsTransport for SMS")

    def send_whatsapp(self, to: str, body: str) -> MessageResult:
        """Send one WhatsApp message via Twilio, capturing any provider error."""
        try:
            msg = self._get_client().messages.create(
                to=_ensure_prefix(to),
                from_=self._settings.twilio_whatsapp_from,
                body=body,
            )
            return MessageResult(
                to=to, channel="whatsapp", ok=True, provider_id=msg.sid
            )
        except Exception as exc:  # noqa: BLE001 — never break a broadcast
            logger.error("Twilio WhatsApp to %s failed: %s", to, exc)
            return MessageResult(
                to=to, channel="whatsapp", ok=False, error=str(exc)
            )
