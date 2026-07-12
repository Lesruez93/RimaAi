"""Tests for the rule-based triage baseline and its documented failure modes."""

from __future__ import annotations

from app.schemas.triage import TriageRequest
from app.services.triage import triage_rule


def test_tick_keyword_flags_january_disease() -> None:
    """A clear tick/swelling description escalates to an emergency."""
    resp = triage_rule(TriageRequest(message="My cow has many ticks and swollen neck"))
    assert "theileriosis" in resp.condition.lower()
    assert resp.urgency == "emergency"
    assert "vet" in resp.escalation.lower()


def test_shona_keyword_is_matched() -> None:
    """A Shona keyword (makwashamu = ticks) is caught by the baseline."""
    resp = triage_rule(TriageRequest(message="mombe ine makwashamu", language="sn"))
    assert resp.urgency == "emergency"


def test_paraphrase_breaks_the_baseline() -> None:
    """Documented weakness: paraphrase with no keyword yields the fallback.

    This is exactly why an LLM path exists — the rule engine cannot understand
    natural-language symptom descriptions.
    """
    resp = triage_rule(
        TriageRequest(message="the beast keeps trembling and its ears drooped overnight")
    )
    assert resp.condition == "Unclear from description"


def test_every_response_has_disclaimer() -> None:
    """Human-oversight disclaimer must always be present."""
    resp = triage_rule(TriageRequest(message="anything"))
    assert resp.disclaimer
    assert resp.backend == "rule"
