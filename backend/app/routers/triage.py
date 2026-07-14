"""Triage router — livestock symptom triage."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.triage import TriageRequest, TriageResponse
from app.services.triage import triage as run_triage

router = APIRouter(prefix="/triage", tags=["triage"])


@router.post("", response_model=TriageResponse)
def triage_symptoms(req: TriageRequest) -> TriageResponse:
    """Triage a free-text livestock symptom description.

    Uses the configured backend (rule engine or LLM with rule fallback). The
    response always includes a human-oversight escalation and disclaimer.
    """
    return run_triage(req)
