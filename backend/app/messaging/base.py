"""Messaging transport interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class MessageResult:
    """Outcome of a single send attempt."""

    to: str
    channel: str  # "sms" | "whatsapp"
    ok: bool
    provider_id: str | None = None
    error: str | None = None


class MessageTransport(ABC):
    """Abstract transport that can deliver SMS and WhatsApp messages.

    Concrete implementations must be safe to construct without side effects and
    should never raise on a single failed recipient — return a
    :class:`MessageResult` with ``ok=False`` instead.
    """

    name: str = "base"

    @abstractmethod
    def send_sms(self, to: str, body: str) -> MessageResult:
        """Send a single SMS message."""

    @abstractmethod
    def send_whatsapp(self, to: str, body: str) -> MessageResult:
        """Send a single WhatsApp message."""

    def broadcast(
        self, recipients: list[str], body: str, channel: str = "sms"
    ) -> list[MessageResult]:
        """Send ``body`` to many recipients on the given channel.

        Args:
            recipients: Destination phone numbers (E.164 recommended).
            body: Message text.
            channel: ``"sms"`` or ``"whatsapp"``.

        Returns:
            One :class:`MessageResult` per recipient, in order.
        """
        send = self.send_whatsapp if channel == "whatsapp" else self.send_sms
        return [send(to, body) for to in recipients]
