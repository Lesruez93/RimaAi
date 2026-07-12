"""Livestock symptom triage service.

Two backends, selected by ``TRIAGE_BACKEND``:

* ``rule`` — a transparent keyword rule engine (documented baseline). It is
  intentionally brittle: it matches keywords in English + some Shona terms and
  fails on paraphrase, negation and mixed-language free text. We ship it as the
  honest baseline that motivates the LLM path (see AI justification in README).
* ``llm`` — Anthropic Claude with a structured prompt, falling back to the rule
  engine on any error so the endpoint never hard-fails offline.

Every response carries an explicit human-oversight escalation and disclaimer:
RimaAI never replaces a veterinarian.
"""

from __future__ import annotations

import json
import logging

from app.core.config import get_settings
from app.schemas.triage import TriageRequest, TriageResponse

logger = logging.getLogger("rimaai.triage")

DISCLAIMER = (
    "RimaAI gives general guidance only and can be wrong. Always confirm with a "
    "veterinarian or AGRITEX officer before treating animals."
)

# Keyword -> (condition, urgency, advice). Includes a few Shona terms to show the
# baseline's narrow reach; anything outside these keywords falls through.
_RULES: list[tuple[tuple[str, ...], tuple[str, str, str]]] = [
    (
        ("tick", "makwashamu", "swollen", "kuzvimba", "fever", "fivha", "january"),
        (
            "Suspected tick-borne disease (theileriosis / January disease)",
            "emergency",
            "Dip or spray with a registered acaricide now and get a vet to check for "
            "January disease. Look for high fever, swollen lymph nodes near the ear, and weakness.",
        ),
    ),
    (
        ("diarrhoea", "diarrhea", "manyoka", "scour", "loose"),
        (
            "Diarrhoea / scours",
            "medium",
            "Provide clean water with rehydration salts, isolate the animal, and check feed. "
            "If bloody or lasting over 24 hours, call a vet.",
        ),
    ),
    (
        ("cough", "kukosora", "nasal", "breathing", "pneumonia"),
        (
            "Respiratory illness",
            "high",
            "Move the animal to a dry, sheltered area away from the herd and consult a vet; "
            "respiratory infections spread quickly.",
        ),
    ),
    (
        ("wound", "ronda", "lesion", "skin", "lumpy"),
        (
            "Skin lesion / wound",
            "medium",
            "Clean the wound, keep flies off, and isolate the animal. Possible lumpy skin "
            "disease — ask a vet about vaccination.",
        ),
    ),
    (
        ("not eating", "haadyi", "off feed", "weak", "kuneta"),
        (
            "Loss of appetite / weakness",
            "high",
            "Many diseases start with going off feed. Check temperature and gums, provide water, "
            "and consult a vet if it persists beyond a day.",
        ),
    ),
]


def _escalation_for(urgency: str) -> str:
    """Return the human-oversight escalation line for an urgency level."""
    if urgency in ("high", "emergency"):
        return "Contact a veterinarian or your nearest AGRITEX/veterinary office immediately."
    return "Monitor the animal and contact AGRITEX or a vet if it worsens."


def triage_rule(req: TriageRequest) -> TriageResponse:
    """Deterministic keyword-based triage (the documented baseline)."""
    text = req.message.lower()
    for keywords, (condition, urgency, advice) in _RULES:
        if any(k in text for k in keywords):
            return TriageResponse(
                condition=condition,
                urgency=urgency,
                advice=advice,
                escalation=_escalation_for(urgency),
                backend="rule",
                disclaimer=DISCLAIMER,
            )
    return TriageResponse(
        condition="Unclear from description",
        urgency="medium",
        advice=(
            "I could not match the symptoms confidently. Describe what you see "
            "(appetite, temperature, skin, dung, behaviour) or take a photo for a scan."
        ),
        escalation=_escalation_for("medium"),
        backend="rule",
        disclaimer=DISCLAIMER,
    )


def _triage_llm(req: TriageRequest) -> TriageResponse:
    """Triage via Anthropic Claude, raising on any failure for fallback."""
    from anthropic import Anthropic  # imported lazily

    settings = get_settings()
    client = Anthropic(api_key=settings.anthropic_api_key)
    system = (
        "You are a livestock health triage assistant for Zimbabwean farmers. "
        "Input may mix Shona/Ndebele/English. Respond ONLY with compact JSON: "
        '{"condition": str, "urgency": "low|medium|high|emergency", "advice": str}. '
        "Be cautious, prioritise tick-borne January disease when relevant, and never "
        "give a definitive diagnosis."
    )
    msg = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=400,
        system=system,
        messages=[{"role": "user", "content": f"Animal: {req.animal}. Symptoms: {req.message}"}],
    )
    data = json.loads(msg.content[0].text)  # type: ignore[union-attr]
    urgency = data.get("urgency", "medium")
    return TriageResponse(
        condition=data.get("condition", "Unclear"),
        urgency=urgency,
        advice=data.get("advice", ""),
        escalation=_escalation_for(urgency),
        backend="llm",
        disclaimer=DISCLAIMER,
    )


def triage(req: TriageRequest) -> TriageResponse:
    """Run triage using the configured backend, falling back to rules on error."""
    settings = get_settings()
    if settings.triage_backend == "llm" and settings.anthropic_api_key:
        try:
            return _triage_llm(req)
        except Exception as exc:  # noqa: BLE001 — resilience over strictness
            logger.warning("LLM triage failed, falling back to rules: %s", exc)
    return triage_rule(req)
