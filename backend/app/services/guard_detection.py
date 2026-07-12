"""RimaAI Guard object-detection service.

Detects human/vehicle intrusion near kraals/paddocks. The MVP ships a small set
of *sample frames* with pre-baked detections so the alert flow is demonstrable
without a real YOLO weight download or camera hardware. The public interface
(``detect(frame_id)`` -> boxes + intrusion flag) matches a real YOLOv8n session,
so swapping in ``ultralytics`` is a drop-in change (documented in api.md).

Why object detection and not motion thresholding: at night cattle move, tree
shadows shift and insects cross the lens — naive motion detection would raise
constant false alarms. Class-aware detection (person/vehicle vs animal) is what
makes the alert trustworthy.
"""

from __future__ import annotations

from app.schemas.common import BoundingBox

# Intrusion classes — a detection of any of these near the kraal is an event.
_INTRUSION_CLASSES = {"person", "vehicle"}

# Pre-baked sample detections keyed by frame id (normalized 0-1 coordinates).
_SAMPLE_FRAMES: dict[str, list[BoundingBox]] = {
    "sample_night_01": [
        BoundingBox(label="person", confidence=0.91, x=0.44, y=0.38, width=0.10, height=0.34),
    ],
    "sample_night_02": [
        BoundingBox(label="person", confidence=0.87, x=0.20, y=0.40, width=0.09, height=0.31),
        BoundingBox(label="vehicle", confidence=0.83, x=0.55, y=0.52, width=0.30, height=0.22),
    ],
    "sample_quiet_01": [
        BoundingBox(label="cattle", confidence=0.94, x=0.30, y=0.55, width=0.22, height=0.25),
    ],
    "sample_empty_01": [],
}


class GuardDetector:
    """Wraps sample-frame detection behind a real-detector-shaped interface."""

    def detect(self, frame_id: str) -> tuple[list[BoundingBox], bool]:
        """Return (boxes, is_intrusion) for a sample frame id.

        ``is_intrusion`` is True when any detected box is an intrusion class.
        """
        boxes = _SAMPLE_FRAMES.get(frame_id, [])
        is_intrusion = any(b.label in _INTRUSION_CLASSES for b in boxes)
        return boxes, is_intrusion


_detector = GuardDetector()


def detect(frame_id: str) -> tuple[list[BoundingBox], bool]:
    """Module-level convenience wrapper around the shared detector."""
    return _detector.detect(frame_id)


def top_detection(boxes: list[BoundingBox]) -> BoundingBox | None:
    """Return the highest-confidence box, or None if there were no detections."""
    return max(boxes, key=lambda b: b.confidence, default=None)
