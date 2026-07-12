# Dataset Statement

Honesty about data provenance is a scored criterion (AI4I rubric C3) and, more
importantly, the right thing to do when advice affects farmers' livelihoods.
This document states exactly what is **real**, **simulated**, or **still
needed** in the RimaAI MVP.

## Summary table

| Component | Status in MVP | Source / plan |
|-----------|---------------|---------------|
| Crop disease model | Simulated (placeholder classifier) | Roadmap: fine-tune MobileNetV3 on **PlantVillage** (public) subset for maize/tomato/tobacco, then collect Zimbabwean field images with AGRITEX. |
| Livestock condition model | Simulated / limited demo | Roadmap: partner with veterinary services for labelled tick-load / skin-condition images. |
| Livestock triage (rules) | Real, transparent | Hand-authored keyword rules + curated advice. LLM path is pluggable. |
| Weather / forecast | Seeded historical sample | Roadmap: Meteorological Services Department (MSD) + satellite time-series. |
| Guard detection | Simulated (sample frames) | Roadmap: YOLOv8n fine-tuned on night kraal footage. |
| Outbreak risk aggregation | Real (plain rules) | Not ML — see below. |
| Agronomic/vet advice text | Curated reference | To be reviewed & signed off by AGRITEX / veterinary services before pilot. |

## Detail

### Crop & livestock disease models
The MVP ships a **deterministic placeholder classifier**
(`backend/app/services/inference.py`) so the full pipeline — capture → inference
→ trilingual advice → history → offline sync — is demonstrable **without**
bundling a large model binary or making unverifiable accuracy claims. The
placeholder implements the exact interface a real TFLite/ONNX session would, so
swapping in a trained model requires no caller changes.

A full, reproducible training pipeline exists in [`ml/`](../ml/):
`train_crop_model.py` transfer-learns MobileNetV3-Small and exports a quantized
int8 TFLite model + `labels.txt`; `evaluate.py` reports accuracy and latency
against the edge budget (<256 MB, <100 ms). Running it requires a GPU/CCE and a
PlantVillage subset; the trained `.tflite` is not committed (kept out of git for
size). The backend can load the resulting model for its `/scan` fallback via
`CROP_MODEL_PATH` (else it uses the placeholder).

**Known limitation:** PlantVillage images are captured under controlled
conditions and do **not** represent Zimbabwean field lighting, soil background,
or the specific local strains (e.g. Maize Lethal Necrosis). Field accuracy will
be lower until local data is collected. This is disclosed to users through the
"consult AGRITEX/vet" escalation shown on every result.

### Livestock triage
The rule baseline is intentionally brittle and its failure modes are covered by
tests (`backend/tests/test_triage.py::test_paraphrase_breaks_the_baseline`).
This documents *why* language understanding (the LLM path) is warranted rather
than assuming it.

### Outbreak risk — explicitly NOT AI
District risk is `Σ (reporter_trust × recency_weight)` over recent reports,
banded into low/moderate/high by fixed thresholds. It is transparent and
auditable. Outbreak **spread prediction** (a genuine ML task) is deferred until
real report volume exists, to avoid a "sledgehammer" model on sparse data.

## Personal data & consent
The only personal data processed is a **phone number** (and optional name/
region) for farmers who opt in to alerts. Registration is refused server-side
without explicit consent (`consent_given`), satisfying the Data Protection Act
[Chapter 11:12]. USSD subscription constitutes consent, recorded on the farmer
record. No location tracking beyond a self-selected district. Row Level Security
(`sample_data/schema.sql`) restricts each farmer to their own records.

## Licences
- **PlantVillage**: released for research use; attribution required. RimaAI will
  comply with its terms for any model trained on it.
- **OpenStreetMap** tiles (outbreak map): © OpenStreetMap contributors, ODbL.
- All RimaAI code: MIT (see `LICENSE`).
