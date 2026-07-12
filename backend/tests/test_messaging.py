"""Tests for the messaging layer (console transport + broadcast)."""

from __future__ import annotations

from app.messaging.console import ConsoleTransport


def test_console_sms_reports_success() -> None:
    """Console SMS always succeeds and is tagged with the console provider."""
    result = ConsoleTransport().send_sms("+263771234567", "hello")
    assert result.ok
    assert result.channel == "sms"
    assert result.provider_id == "console"


def test_console_whatsapp_reports_success() -> None:
    """Console WhatsApp always succeeds."""
    result = ConsoleTransport().send_whatsapp("+263771234567", "hello")
    assert result.ok
    assert result.channel == "whatsapp"


def test_broadcast_hits_every_recipient() -> None:
    """Broadcast returns one result per recipient, all successful."""
    recipients = ["+263771000001", "+263771000002", "+263771000003"]
    results = ConsoleTransport().broadcast(recipients, "alert", channel="sms")
    assert len(results) == 3
    assert all(r.ok for r in results)
    assert [r.to for r in results] == recipients
