# RimaAI — model training pipeline

Reproducible pipeline for the on-device crop-disease classifier: transfer-learn
**MobileNetV3-Small** on a PlantVillage subset and export a **full-integer (int8)
quantized TFLite** model for offline inference in the Flutter app.

> This directory is the *training* toolchain. It is intentionally separate from
> `backend/` (runtime) so the API stays lightweight. It runs on a machine/GPU or
> the **ZCHPC CCE** — not in the demo container.

## Contents

| File | Purpose |
|------|---------|
| `train_crop_model.py` | Train + fine-tune + export int8 TFLite + `labels.txt`. |
| `evaluate.py` | Top-1 accuracy + latency vs. the edge budget (<256 MB, <100 ms). |
| `requirements.txt` | Pinned TensorFlow toolchain. |

## 1. Get data

Use a **PlantVillage** subset covering RimaAI's target crops (maize, tomato,
tobacco). Lay it out as one folder per class:

```
data/plantvillage/
  maize_healthy/            *.jpg
  maize_lethal_necrosis/    *.jpg
  tomato_early_blight/      *.jpg
  ...
```

PlantVillage is available on Kaggle. Example fetch:
```python
import kagglehub
path = kagglehub.dataset_download("abdallahalidev/plantvillage-dataset")
# then reorganise / symlink the relevant classes into data/plantvillage/
```
Folder names become the model's class labels, so name them to match the advice
keys in `backend/app/services/knowledge.py` where possible.

**Licence:** PlantVillage is provided for research use with attribution. See
`docs/dataset_statement.md`. It does not yet represent Zimbabwean field
conditions — local collection with AGRITEX is on the roadmap.

## 2. Train + export

```bash
pip install -r requirements.txt
python train_crop_model.py \
    --data-dir data/plantvillage \
    --out ../app/assets/models \
    --epochs 8 --fine-tune-epochs 4
```
Outputs `crop_disease_mobilenetv3_int8.tflite` + `labels.txt` into the app's
`assets/models/`. Add the `.tflite` filename to `app/pubspec.yaml` assets and
implement the on-device `ScanRepository` variant (see
`app/assets/models/README.md`).

## 3. Evaluate against the edge budget

```bash
python evaluate.py \
    --model ../app/assets/models/crop_disease_mobilenetv3_int8.tflite \
    --labels ../app/assets/models/labels.txt \
    --data-dir data/plantvillage_val
```
Prints size, median latency, and top-1 accuracy with PASS/FAIL against the
proposal's stated targets — these are the *measured* numbers to quote at the
bootcamp.

## Server-side use (optional)

The FastAPI backend can also load this model for its `/scan` fallback: set
`CROP_MODEL_PATH` to the `.tflite` path and install a TFLite runtime
(`ai-edge-litert` or `tflite-runtime`). If unset or unavailable, the backend
uses the documented placeholder classifier. See
`backend/app/services/inference.py`.
