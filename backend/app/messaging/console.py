"""Console transport — logs messages instead of sending them.

Used in development and for judge demos so the full alert pipeline can be
exercised end-to-end without a Twilio account or telco integration.
"""

from __future__ import annotations

import logging

from app.messaging.base import MessageResult, MessageTransport

logger = logging.getLogger("rimaai.messaging.console")


class ConsoleTransport(MessageTransport):
    """A transport that records messages to the application log."""

    name = "console"

    def send_sms(self, to: str, body: str) -> MessageResult:
        """Log an SMS and report success."""
        logger.info("[SMS -> %s] %s", to, body)
        return MessageResult(to=to, channel="sms", ok=True, provider_id="console")

    def send_whatsapp(self, to: str, body: str) -> MessageResult:
        """Log a WhatsApp message and report success."""
        logger.info("[WhatsApp -> %s] %s", to, body)
        return MessageResult(
            to=to, channel="whatsapp", ok=True, provider_id="console"
        )
