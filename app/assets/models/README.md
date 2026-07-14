# On-device models

The production app bundles a **quantized MobileNetV3 TFLite** crop/livestock
disease classifier here (e.g. `crop_disease_mobilenetv3_int8.tflite`) for fully
offline scanning.

The model binary is **not committed** to keep the repository lightweight and
because the demo uses the server-side fallback (`POST /scan`) with a documented
placeholder classifier. See `docs/dataset_statement.md` for training data
provenance and `backend/app/services/inference.py` for the inference interface
the on-device model implements.

To wire a real model:
1. Drop the `.tflite` file in this directory and list it under `assets:` in
   `pubspec.yaml` (already covered by `assets/models/`).
2. Add the `tflite_flutter` dependency (commented in `pubspec.yaml`).
3. Implement an on-device `ScanRepository` variant with the same
   `Future<ScanResult> scanImage(...)` contract.
