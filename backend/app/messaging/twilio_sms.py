"""Twilio SMS transport.

Full, correct SMS sending via Twilio. The Twilio client is imported lazily so
the package remains optional for the console-only demo path.
"""

from __future__ import annotations

import logging

from app.core.config import Settings
from app.messaging.base import MessageResult, MessageTransport

logger = logging.getLogger("rimaai.messaging.twilio_sms")


class TwilioSmsTransport(MessageTransport):
    """Send SMS via the Twilio REST API."""

    name = "twilio_sms"

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
        """Send one SMS via Twilio, capturing any provider error."""
        try:
            msg = self._get_client().messages.create(
                to=to, from_=self._settings.twilio_sms_from, body=body
            )
            return MessageResult(
                to=to, channel="sms", ok=True, provider_id=msg.sid
            )
        except Exception as exc:  # noqa: BLE001 — never break a broadcast
            logger.error("Twilio SMS to %s failed: %s", to, exc)
            return MessageResult(to=to, channel="sms", ok=False, error=str(exc))

    def send_whatsapp(self, to: str, body: str) -> MessageResult:
        """Not supported here; use :class:`TwilioWhatsAppTransport`."""
        raise NotImplementedError("Use TwilioWhatsAppTransport for WhatsApp")
