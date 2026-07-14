"""Train + quantize the RimaAI on-device crop-disease classifier.

Transfer-learns a MobileNetV3-Small on a PlantVillage subset and exports a
**full-integer (int8) quantized TFLite** model plus a ``labels.txt``, sized for
on-device inference (edge budget: < 256 MB RAM, < 100 ms latency — verified by
``evaluate.py``).

The script is dataset-source-agnostic: point ``--data-dir`` at any folder laid
out as ``<class_name>/<image>.jpg`` (the standard PlantVillage / Keras
``image_dataset_from_directory`` layout). See ``ml/README.md`` for how to fetch a
PlantVillage subset.

Usage::

    python train_crop_model.py \
        --data-dir data/plantvillage \
        --out ../app/assets/models \
        --epochs 8

Design notes:
* MobileNetV3-Small is chosen for its tiny footprint and mobile-optimised ops.
* We freeze the backbone first (fast head training), then optionally fine-tune
  the top blocks at a low learning rate.
* Full-integer quantization uses a representative dataset so activations are
  calibrated — this is what keeps latency low on mid-range Android hardware.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import tensorflow as tf

IMG_SIZE = 224  # MobileNetV3 default input
AUTOTUNE = tf.data.AUTOTUNE


def build_datasets(
    data_dir: Path, batch_size: int, val_split: float
) -> tuple[tf.data.Dataset, tf.data.Dataset, list[str]]:
    """Load train/val datasets and the class-name list from a folder tree."""
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="training",
        seed=42,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size,
        label_mode="int",
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="validation",
        seed=42,
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size,
        label_mode="int",
    )
    class_names = train_ds.class_names
    return (
        train_ds.prefetch(AUTOTUNE),
        val_ds.prefetch(AUTOTUNE),
        class_names,
    )


def build_model(num_classes: int) -> tf.keras.Model:
    """Build a MobileNetV3-Small transfer-learning classifier."""
    # MobileNetV3 expects raw [0, 255] inputs; its preprocessing is built in.
    inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    augment = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
        ],
        name="augment",
    )
    backbone = tf.keras.applications.MobileNetV3Small(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
        pooling="avg",
    )
    backbone.trainable = False

    x = augment(inputs)
    x = backbone(x, training=False)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs, name="rimaai_crop_mobilenetv3")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def fine_tune(model: tf.keras.Model, train_ds, val_ds, epochs: int):  # type: ignore[no-untyped-def]
    """Unfreeze the backbone's top and fine-tune at a low learning rate."""
    backbone = model.get_layer("MobilenetV3small")
    backbone.trainable = True
    # Keep the early layers frozen; only fine-tune the last ~30 layers.
    for layer in backbone.layers[:-30]:
        layer.trainable = False
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model.fit(train_ds, validation_data=val_ds, epochs=epochs)


def export_tflite(
    model: tf.keras.Model, train_ds: tf.data.Dataset, out_path: Path
) -> None:
    """Export a full-integer (int8) quantized TFLite model.

    A representative dataset calibrates activation ranges; inputs/outputs are
    kept int8 for the smallest, fastest on-device model.
    """

    def representative_dataset():
        for images, _ in train_ds.take(100):
            for i in range(images.shape[0]):
                yield [tf.expand_dims(images[i], 0)]

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = representative_dataset
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    tflite_model = converter.convert()
    out_path.write_bytes(tflite_model)
    size_mb = len(tflite_model) / (1024 * 1024)
    print(f"Wrote {out_path} ({size_mb:.2f} MB)")


def main() -> None:
    """Parse args, train, fine-tune and export the TFLite model + labels."""
    parser = argparse.ArgumentParser(description="Train RimaAI crop model")
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("../app/assets/models"))
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--fine-tune-epochs", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--val-split", type=float, default=0.2)
    parser.add_argument(
        "--name", default="crop_disease_mobilenetv3_int8.tflite"
    )
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    train_ds, val_ds, class_names = build_datasets(
        args.data_dir, args.batch_size, args.val_split
    )
    print(f"Classes ({len(class_names)}): {class_names}")

    model = build_model(len(class_names))
    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs)
    if args.fine_tune_epochs > 0:
        fine_tune(model, train_ds, val_ds, args.fine_tune_epochs)

    export_tflite(model, train_ds, args.out / args.name)
    (args.out / "labels.txt").write_text("\n".join(class_names))
    print(f"Wrote {args.out / 'labels.txt'}")


if __name__ == "__main__":
    main()
