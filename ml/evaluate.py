"""Evaluate a quantized TFLite crop model against the RimaAI edge budget.

Reports top-1 accuracy on a validation folder and median single-image inference
latency, checked against the targets stated in the proposal:

* model size  < 256 MB (proxy for RAM footprint)
* latency     < 100 ms per image (CPU, single thread)

Usage::

    python evaluate.py \
        --model ../app/assets/models/crop_disease_mobilenetv3_int8.tflite \
        --labels ../app/assets/models/labels.txt \
        --data-dir data/plantvillage_val
"""

from __future__ import annotations

import argparse
import statistics
import time
from pathlib import Path

import numpy as np
import tensorflow as tf

IMG_SIZE = 224
RAM_BUDGET_MB = 256
LATENCY_BUDGET_MS = 100


def _quantize_input(img: np.ndarray, scale: float, zero_point: int) -> np.ndarray:
    """Quantize a float image to the model's int8 input domain."""
    return (img / scale + zero_point).round().astype(np.int8)


def evaluate(model_path: Path, labels_path: Path, data_dir: Path) -> None:
    """Run accuracy + latency evaluation and print a budget verdict."""
    labels = labels_path.read_text().splitlines()

    interpreter = tf.lite.Interpreter(model_path=str(model_path))
    interpreter.allocate_tensors()
    in_detail = interpreter.get_input_details()[0]
    out_detail = interpreter.get_output_details()[0]
    in_scale, in_zp = in_detail["quantization"]

    ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=1,
        shuffle=False,
        label_mode="int",
    )
    class_names = ds.class_names

    correct = 0
    total = 0
    latencies_ms: list[float] = []

    for image, label in ds:
        img = image.numpy()[0]
        quantized = _quantize_input(img, in_scale, in_zp)[np.newaxis, ...]

        start = time.perf_counter()
        interpreter.set_tensor(in_detail["index"], quantized)
        interpreter.invoke()
        output = interpreter.get_tensor(out_detail["index"])[0]
        latencies_ms.append((time.perf_counter() - start) * 1000)

        pred_idx = int(np.argmax(output))
        if labels[pred_idx] == class_names[int(label.numpy()[0])]:
            correct += 1
        total += 1

    size_mb = model_path.stat().st_size / (1024 * 1024)
    median_ms = statistics.median(latencies_ms)
    acc = correct / total if total else 0.0

    print(f"Model:       {model_path.name}")
    print(f"Size:        {size_mb:.2f} MB (budget < {RAM_BUDGET_MB} MB) "
          f"-> {'PASS' if size_mb < RAM_BUDGET_MB else 'FAIL'}")
    print(f"Latency:     {median_ms:.1f} ms median (budget < {LATENCY_BUDGET_MS} ms) "
          f"-> {'PASS' if median_ms < LATENCY_BUDGET_MS else 'FAIL'}")
    print(f"Top-1 acc:   {acc:.3f} on {total} images")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Evaluate RimaAI TFLite model")
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--labels", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    args = parser.parse_args()
    evaluate(args.model, args.labels, args.data_dir)


if __name__ == "__main__":
    main()
