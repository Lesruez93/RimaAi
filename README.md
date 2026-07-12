# RimaAI 🌱

**AI-powered smart farming companion for Zimbabwean farmers.**
*"Rima" (chiShona) = to farm / to plough.*

RimaAI is a single, multi-channel app that puts an agricultural extension officer
in every farmer's pocket — working **offline** on smartphones and reaching
feature phones via **USSD/SMS/WhatsApp**. Built for **AI4I 2026 (POTRAZ),
Track 3: Development**.

---

## Why RimaAI

Zimbabwe's smallholders lose crops and livestock to problems that are
**preventable and treatable** — the killer is *lack of timely information*, not
the absence of a cure.

- **January disease (theileriosis)** — a tick-borne cattle disease — killed
  **hundreds of thousands of cattle (2017–2021)**. It is preventable by dipping
  and treatable with the right medicines; farmers simply didn't know the
  schedules. RimaAI delivers dipping/vaccination reminders and outbreak alerts.
- **Crop diseases** (Maize Lethal Necrosis, tomato blight, fall armyworm) are
  spotted too late → RimaAI offers an **offline photo scanner** with instant advice.
- **AGRITEX extension officers** are stretched thin (one officer to hundreds of
  farmers) → AI handles first-line triage; officers get flagged cases.
- **Rural connectivity is poor and data is expensive** → offline-first app +
  USSD/SMS/WhatsApp channels.

| Problem | RimaAI answer |
|---|---|
| January disease devastated the herd; treatable but info-starved | Livestock advisor + SMS/USSD dipping & vaccination reminders + outbreak alerts |
| Crop diseases identified too late | Offline photo scanner with instant treatment advice |
| Erratic rainfall → wrong planting windows | Localized planting-window forecasts |
| Poor rural connectivity | Offline-first app + USSD/SMS/WhatsApp |
| Thin AGRITEX coverage | AI triage first-line; officer dashboard (roadmap) |
| Rampant stock theft | RimaAI Guard surveillance module |
| Low insurance literacy | Insurance tips channel |
| Language barriers (English-only content) | Shona / Ndebele / English throughout |

---

## What's in the MVP

| Module | What it does |
|--------|--------------|
| **Crop Scanner** | Photo → disease class → trilingual treatment advice (on-device TFLite; server fallback). |
| **Livestock Advisor** | Photo health check + free-text symptom **triage chat** (rule baseline + pluggable LLM). |
| **Forecasts** | Planting-window / rainfall guidance per district. |
| **Alerts & Subscriptions** | Opt-in to weather/disease/tips/livestock/insurance alerts; **consent-gated**. |
| **USSD / SMS / WhatsApp** | Feature-phone `*123#` menu tree + code-complete Twilio SMS/WhatsApp transports. |
| **RimaAI Guard** | Simulated kraal camera + object-detection intrusion alerts (commercial). |
| **Outbreak Heat Map** | Community reports → per-district risk map → auto-alerts to subscribers. |

---

## Why this needs AI (rubric C2)

- **Disease recognition from photos** is impossible with rules/SQL — a genuine
  computer-vision task (CNN / MobileNetV3).
- **Triage** of mixed Shona/English symptom text needs language understanding;
  the keyword baseline provably fails on paraphrase
  (`backend/tests/test_triage.py`), which is exactly why the LLM path exists.
- **Guard** intrusion detection must be *class-aware* (person/vehicle vs. moving
  cattle at night) — naive motion-pixel thresholding would fire constantly.
- **Forecasting** is time-series over sparse, noisy regional weather data.

**Where AI is deliberately NOT used:** subscriptions, alert scheduling, and
**outbreak risk aggregation** (plain weighted rules: count × recency × trust).
No sledgehammers. Outbreak *spread prediction* is a roadmap ML use case once
real report volume exists.

---

## Repository layout

```
rimaai/
├── app/            # Flutter app (feature-first): scan, livestock, alerts, guard, outbreaks
├── backend/        # FastAPI: routers, services, messaging, models, tests
├── ml/             # Reproducible MobileNetV3 → quantized TFLite training pipeline
├── ussd-simulator/ # Static page to click through *123# flows
├── sample_data/    # Postgres/Supabase schema (+ RLS) and seed docs
├── docs/           # architecture, api, dataset_statement, screenshots
└── proposal/       # AI4I 10-page development proposal
```

---

## Quick start

### 1. Backend (zero-setup demo — SQLite + console messaging)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed            # seed demo data (Gokwe → HIGH tick-disease risk)
uvicorn app.main:app --reload # http://localhost:8000/docs
```

Run the tests:
```bash
pytest            # 20 tests
```

### 2. USSD simulator
Open `ussd-simulator/index.html` in a browser (backend running). Type `*123#`,
Send, then reply with menu numbers. See `ussd-simulator/README.md`.

### 3. Flutter app
> Platform folders (`android/`, `ios/`) are generated per machine — run
> `flutter create .` inside `app/` once to add them, then:

```bash
cd app
flutter create .          # generates android/ios/ scaffolding (first run only)
flutter pub get
# Android emulator reaches the host backend at 10.0.2.2:
flutter run --dart-define=RIMAAI_API_BASE=http://10.0.2.2:8000
flutter test              # widget tests
```

---

## Demo script (5 minutes)

1. **Onboard** → pick language (EN/SN/ND).
2. **Scan** a crop leaf photo → disease + trilingual advice card.
3. **Livestock** → type *"my cow has many ticks and a swollen neck"* → emergency
   triage flagging January disease + "consult a vet" escalation.
4. **Alerts** → register (consent checkbox) → toggle subscriptions.
5. **Outbreak map** → open Gokwe (🔴 high) → **Report** a tick-disease outbreak
   in a new district and watch it tip to high risk + auto-dispatch an SMS alert
   (visible in the backend console log).
6. **USSD simulator** → `*123#` → subscribe on a "feature phone".
7. **Guard** → cycle camera frames → intrusion box + alert history.

---

## Tech stack

- **App:** Flutter (Material 3), provider, flutter_map, image_picker.
- **Backend:** FastAPI, SQLAlchemy, Pydantic v2. SQLite (demo) / Postgres (prod).
- **AI (target):** MobileNetV3 TFLite on-device; YOLOv8n server-side; LLM triage
  (Anthropic Claude) with rule fallback.
- **Data:** Supabase (Auth, Postgres, Storage) with Row Level Security.
- **Messaging:** Twilio SMS + WhatsApp (code-complete); console transport in dev.

---

## Continuous integration & deployment

- **CI** (`.github/workflows/ci.yml`): lints + tests the backend (ruff, pytest,
  seed smoke-test) and analyzes + tests the Flutter app on every push/PR.
- **Container**: `backend/Dockerfile` + `docker-compose.yml` run the backend in
  one command (`make docker-up`), with a commented Postgres service matching the
  Supabase target — this is the path for deploying into the ZCHPC CCE.
- **Make targets**: `make help` lists backend/app/docker shortcuts.

## Known limitations (honest list)

- Disease/livestock models are **placeholder classifiers** in the MVP — the
  pipeline is real, the weights are not yet trained on Zimbabwean data. See
  [`docs/dataset_statement.md`](docs/dataset_statement.md).
- Forecast + Guard use **seeded/sample data**, not live feeds.
- No live telco/Twilio account wired (console transport by default).
- `app/` ships `lib/`, `test/`, `pubspec.yaml`; platform folders are generated
  with `flutter create .`. `pubspec.lock` is produced by `flutter pub get`.
- Auth in the app is a lightweight local session; production uses Supabase Auth.

## Roadmap
Local image collection with AGRITEX · MSD weather partnership · trained TFLite &
YOLO models · outbreak spread prediction (ML) · AGRITEX officer dashboard ·
payments for Guard/institutional tiers.

## Compliance
Consent-gated phone-number storage, minimal PII, RLS, and human-oversight
framing on all advice — Data Protection Act [Chapter 11:12]. Full detail in the
[proposal](proposal/RimaAI_AI4I_Proposal_Development.md), Section 4.

## Licence
MIT — see [`LICENSE`](LICENSE). Advice content is for guidance only; always
confirm with AGRITEX or a veterinarian.
