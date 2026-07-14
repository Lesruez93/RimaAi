"""Pluggable messaging layer (SMS / WhatsApp).

The transport is selected at runtime from ``MESSAGING_TRANSPORT``:

* ``console`` — logs messages to stdout (safe default; no credentials needed).
* ``twilio``  — sends via Twilio SMS + WhatsApp (requires credentials).

Import :func:`get_transport` to obtain the configured transport.
"""

from app.messaging.base import MessageResult, MessageTransport
from app.messaging.factory import get_transport

__all__ = ["MessageResult", "MessageTransport", "get_transport"]
