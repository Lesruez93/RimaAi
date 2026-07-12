"""Server-side inference service (fallback for when the device can't run TFLite).

The MVP ships a *deterministic placeholder classifier* so the full pipeline
(upload -> inference -> advice -> history) is demonstrable without bundling a
large model binary. It hashes the image bytes to pick a class from the demo
label set. This is honestly documented in ``docs/dataset_statement.md``:
replace :class:`PlaceholderClassifier` with a real TFLite/ONNX MobileNetV3
session (same interface) for production accuracy.
"""

from __future__ import annotations

import hashlib

from app.schemas.scan import ScanResult
from app.services import knowledge

# Demo class label sets. These mirror the on-device model's output classes.
CROP_CLASSES = list(knowledge.CROP_ADVICE.keys())
LIVESTOCK_CLASSES = list(knowledge.LIVESTOCK_ADVICE.keys())


class PlaceholderClassifier:
    """Deterministic stand-in for the on-device MobileNetV3 TFLite model.

    Interface intentionally matches a real inference session so it can be
    swapped without touching callers: ``classify(image_bytes, scan_type)``.
    """

    def classify(self, image_bytes: bytes, scan_type: str) -> tuple[str, float]:
        """Return a (label, confidence) pair derived from the image bytes.

        The mapping is deterministic (hash-based) so demos are reproducible.
        Confidence is synthesised in a plausible 0.72-0.98 range.
        """
        classes = LIVESTOCK_CLASSES if scan_type == "livestock" else CROP_CLASSES
        digest = hashlib.sha256(image_bytes or b"seed").digest()
        idx = digest[0] % len(classes)
        confidence = 0.72 + (digest[1] % 27) / 100.0
        return classes[idx], round(confidence, 4)


_classifier = PlaceholderClassifier()


def run_inference(
    image_bytes: bytes, scan_type: str = "crop", language: str = "en"
) -> ScanResult:
    """Classify an image and attach trilingual treatment advice.

    Args:
        image_bytes: Raw image content.
        scan_type: ``"crop"`` or ``"livestock"``.
        language: Preferred advice language (``en``/``sn``/``nd``).

    Returns:
        A fully populated :class:`ScanResult`.
    """
    label, confidence = _classifier.classify(image_bytes, scan_type)
    if scan_type == "livestock":
        advice, i18n = knowledge.livestock_advice(label, language)
    else:
        advice, i18n = knowledge.crop_advice(label, language)
    return ScanResult(
        label=label,
        confidence=confidence,
        advice=advice,
        scan_type=scan_type,
        source="server",
        advice_i18n=i18n,
    )
