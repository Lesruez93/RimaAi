"""Shared schema primitives."""

from __future__ import annotations

from pydantic import BaseModel


class Message(BaseModel):
    """Generic message envelope for simple acknowledgements."""

    detail: str


class BoundingBox(BaseModel):
    """A normalized detection box (0-1) with a class label and score."""

    label: str
    confidence: float
    x: float
    y: float
    width: float
    height: float
