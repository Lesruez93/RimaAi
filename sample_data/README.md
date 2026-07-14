# Sample data & schema

| File | Purpose |
|------|---------|
| `schema.sql` | Production Postgres/Supabase DDL incl. Row Level Security policies. |
| `../backend/app/seed.py` | Populates the demo DB (regions, farmers, subscriptions, outbreak reports so Gokwe tips into **high** tick-disease risk, scan history, a guard event). |

## Seed the demo database

```bash
cd ../backend
python -m app.seed
```

## Sample media (roadmap)

Real sample crop/livestock images and a short kraal-camera night clip will be
added under `images/` and `guard/` respectively. The MVP's Guard service uses
pre-baked sample-frame detections (see `backend/app/services/guard_detection.py`)
so the alert flow is demonstrable without shipping large binaries in git.

See `../docs/dataset_statement.md` for exactly what data is real vs simulated.
