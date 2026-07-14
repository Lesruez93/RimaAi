"""Transport factory — selects and builds the configured messaging transport."""

from __future__ import annotations

from functools import lru_cache

from app.core.config import Settings, get_settings
from app.messaging.base import MessageResult, MessageTransport
from app.messaging.console import ConsoleTransport
from app.messaging.twilio_sms import TwilioSmsTransport
from app.messaging.twilio_whatsapp import TwilioWhatsAppTransport


class TwilioTransport(MessageTransport):
    """Composite transport delegating SMS and WhatsApp to their Twilio backends."""

    name = "twilio"

    def __init__(self, settings: Settings) -> None:
        self._sms = TwilioSmsTransport(settings)
        self._whatsapp = TwilioWhatsAppTransport(settings)

    def send_sms(self, to: str, body: str) -> MessageResult:
        """Delegate to the Twilio SMS transport."""
        return self._sms.send_sms(to, body)

    def send_whatsapp(self, to: str, body: str) -> MessageResult:
        """Delegate to the Twilio WhatsApp transport."""
        return self._whatsapp.send_whatsapp(to, body)


@lru_cache
def get_transport() -> MessageTransport:
    """Return the configured messaging transport (cached).

    Falls back to the console transport for any unknown value so the demo
    always works.
    """
    settings = get_settings()
    if settings.messaging_transport == "twilio":
        return TwilioTransport(settings)
    return ConsoleTransport()
