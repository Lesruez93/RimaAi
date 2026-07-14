"""Server-side inference service (fallback for when the device can't run TFLite).

Two classifiers share one interface — ``classify(image_bytes, scan_type)``:

* :class:`PlaceholderClassifier` (default) — a deterministic, hash-based stand-in
  so the full pipeline (upload -> inference -> advice -> history) is demonstrable
  without bundling a large model binary. Documented in
  ``docs/dataset_statement.md``.
* :class:`TFLiteClassifier` — loads a real quantized ``.tflite`` model produced
  by ``ml/train_crop_model.py`` when ``CROP_MODEL_PATH`` is configured *and* a
  TFLite runtime + Pillow/numpy are installed. If anything is missing it falls
  back to the placeholder, so the default demo path never breaks.
"""

from __future__ import annotations

import hashlib
import logging

from app.core.config import get_settings
from app.schemas.scan import ScanResult
from app.services import knowledge

logger = logging.getLogger("rimaai.inference")

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


class TFLiteClassifier:
    """Real quantized-TFLite classifier (int8 MobileNetV3).

    Lazily loads the interpreter + labels on first use. Preprocessing matches
    ``ml/train_crop_model.py``: 224x224 RGB, quantized to the model's int8 input
    domain. Heavy deps (a TFLite runtime, Pillow, numpy) are imported lazily so
    they remain optional for the console demo.
    """

    def __init__(self, model_path: str, labels_path: str | None) -> None:
        self._model_path = model_path
        self._labels_path = labels_path
        self._interpreter = None
        self._labels: list[str] = []

    def _ensure_loaded(self) -> None:
        """Load the interpreter and labels once, raising if unavailable."""
        if self._interpreter is not None:
            return
        try:
            from ai_edge_litert.interpreter import Interpreter  # type: ignore
        except ImportError:
            from tflite_runtime.interpreter import Interpreter  # type: ignore
        interpreter = Interpreter(model_path=self._model_path)
        interpreter.allocate_tensors()
        self._interpreter = interpreter
        if self._labels_path:
            with open(self._labels_path) as fh:
                self._labels = [line.strip() for line in fh if line.strip()]

    def classify(self, image_bytes: bytes, scan_type: str) -> tuple[str, float]:
        """Return a (label, confidence) pair from the real model."""
        import io

        import numpy as np
        from PIL import Image

        self._ensure_loaded()
        assert self._interpreter is not None

        in_detail = self._interpreter.get_input_details()[0]
        out_detail = self._interpreter.get_output_details()[0]
        _, height, width, _ = in_detail["shape"]

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize((width, height))
        arr = np.asarray(img, dtype=np.float32)
        scale, zero_point = in_detail["quantization"]
        if scale:  # int8 quantized input
            arr = (arr / scale + zero_point).round().astype(in_detail["dtype"])
        else:
            arr = arr.astype(in_detail["dtype"])

        self._interpreter.set_tensor(in_detail["index"], arr[np.newaxis, ...])
        self._interpreter.invoke()
        output = self._interpreter.get_tensor(out_detail["index"])[0].astype(np.float32)
        o_scale, o_zp = out_detail["quantization"]
        if o_scale:
            output = (output - o_zp) * o_scale

        idx = int(np.argmax(output))
        total = float(output.sum()) or 1.0
        confidence = round(float(output[idx]) / total, 4)
        label = self._labels[idx] if idx < len(self._labels) else str(idx)
        return label, confidence


def _build_classifier(model_path: str | None):  # type: ignore[no-untyped-def]
    """Return a real classifier for ``model_path`` or the placeholder.

    A real model is used only when a path is configured; any load/runtime error
    logs a warning and reverts to the placeholder so the demo never hard-fails.
    """
    if model_path:
        settings = get_settings()
        try:
            clf = TFLiteClassifier(model_path, settings.model_labels_path)
            clf._ensure_loaded()  # fail fast at startup if deps/model missing
            logger.info("Using real TFLite model: %s", model_path)
            return clf
        except Exception as exc:  # noqa: BLE001 — resilience over strictness
            logger.warning(
                "Could not load TFLite model (%s); using placeholder classifier.",
                exc,
            )
    return PlaceholderClassifier()


# One classifier per scan type so a crop model never serves livestock scans.
_settings = get_settings()
_classifiers = {
    "crop": _build_classifier(_settings.crop_model_path),
    "livestock": _build_classifier(_settings.livestock_model_path),
}


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
    classifier = _classifiers.get(scan_type, _classifiers["crop"])
    label, confidence = classifier.classify(image_bytes, scan_type)
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
