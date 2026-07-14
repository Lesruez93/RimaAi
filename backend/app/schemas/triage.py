"""Livestock triage schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TriageRequest(BaseModel):
    """A free-text symptom description, optionally mixed Shona/English."""

    message: str = Field(min_length=2, max_length=1000)
    animal: str = Field(default="cattle")
    language: str = Field(default="en", pattern="^(en|sn|nd)$")


class TriageResponse(BaseModel):
    """Triage guidance with an explicit escalation to human experts."""

    condition: str
    urgency: str  # low | medium | high | emergency
    advice: str
    escalation: str
    backend: str  # "rule" or "llm" — which path produced the answer
    disclaimer: str
