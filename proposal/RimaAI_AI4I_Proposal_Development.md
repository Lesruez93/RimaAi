<!--
Formatting target for PDF export: Avenir/Arial 11pt, 1.15 line spacing,
1-inch margins, max 10 A4 pages TOTAL including this cover page (official
submission limit). This markdown is the full working draft/reference;
the condensed, page-budgeted submission file is
proposal/RimaAI_AI4I_Proposal_Development.docx.
-->

<div align="center">

# RimaAI
### AI-Powered Smart Farming Companion for Zimbabwean Farmers

**AI4I 2026 (POTRAZ) — Track 3: Development**

| | |
|---|---|
| **Project Title** | RimaAI — Smart Farming Companion |
| **Track** | Development |
| **Team Name** | Team RimaAI |
| **Team Members** | Lester Rusike (Lead Innovator — Backend, ML & Mobile) · Agnes Goora (Frontend Developer) |
| **Contact** | lesterrusike@gmail.com |
| **Live Demo** | https://rimai.vercel.app/ — single hub for the UI demo, Android APK, and GitHub source (see Appendix A) |
| **Date** | 14 July 2026 |

</div>

---

## Section 1 — Problem Definition & Strategic Alignment

### 1.1 The problem: information, not incurability, is the killer

Zimbabwean agriculture employs the majority of the rural population and
underpins food security, yet smallholders repeatedly suffer **avoidable** crop
and livestock losses. The defining pattern is that the diseases and shocks
involved are **preventable or treatable** — what is missing is *timely,
trusted, local-language information*.

The clearest evidence is the **January disease (theileriosis)** crisis. This
tick-borne cattle disease killed on the order of **hundreds of thousands of
cattle between 2017 and 2021**. It is prevented by regular dipping and treated
with readily available medicines; the mass deaths happened because farmers did
not know the correct dipping schedules or which medicines to use, and because
extension coverage collapsed. Information access was the killer.

The same pattern repeats across the sector:

| Problem (evidence-led) | RimaAI answer |
|---|---|
| January disease devastated the national herd; treatable but farmers lacked info on medicines/dipping | Livestock advisor + SMS/USSD dipping & vaccination reminders + outbreak alerts |
| Crop diseases (Maize Lethal Necrosis, tomato blight, fall armyworm) identified too late | Offline photo scanner with instant treatment advice |
| Erratic rainfall / climate shift → wrong planting windows | Localized planting-window forecasts |
| Rural connectivity is poor and data is expensive | Offline-first app + USSD/SMS/WhatsApp channels |
| AGRITEX extension officers are stretched — one officer serves hundreds of farmers | AI triage handles first-line questions; officers get a dashboard of flagged cases |
| Stock theft is rampant, especially for commercial farmers | RimaAI Guard surveillance module |
| Low insurance literacy → total loss on disaster | Insurance-tips channel + partner linkage |
| Most agricultural content is English-only | Shona / Ndebele / English throughout |

### 1.2 Why existing channels fall short

Extension services (AGRITEX) are severely under-resourced relative to the number
of farmers, so first-line advice does not reach people in time. Smartphone apps
alone exclude the large share of rural farmers on feature phones or with
intermittent, costly data. Any credible solution must therefore be **offline-
first on smartphones** *and* **reachable over USSD/SMS/WhatsApp** on basic
phones — and it must speak the farmer's language.

### 1.3 Strategic alignment

RimaAI aligns directly with national priorities:

- **Zimbabwe National AI Strategy** — agriculture and food systems are a named
  priority domain; RimaAI is a concrete, deployable application of AI in that
  domain, plus digital-inclusion by design (multi-channel, trilingual).
- **NDS1 (National Development Strategy 1)** — agricultural productivity, food
  security, and rural digital transformation.
- **Digital & financial inclusion** — the USSD/SMS layer and the insurance-
  literacy channel extend services to farmers usually left out of app-only tools.

RimaAI is not a demo of AI for its own sake: it targets a documented, high-cost,
information-shaped problem with a channel strategy matched to rural realities.

---

## Section 2 — Technical Design & Product Logic

### 2.1 Architecture overview

A single FastAPI backend serves three farmer segments — smartphone (offline-
first Flutter app), feature phone (USSD/SMS), and commercial (Guard) — over a
Supabase/Postgres datastore.

```
Farmer (smartphone) ──► Flutter app (offline-first, TFLite on-device)
Farmer (feature phone) ─► USSD menu / SMS ─┐
Farmer (WhatsApp) ─────► WhatsApp bot ─────┤
                                           ▼
                              Python FastAPI backend
                              ├─ Inference service (TFLite/ONNX server models)
                              ├─ Triage service (LLM w/ rule fallback)
                              ├─ Forecast service (seeded → MSD/satellite)
                              ├─ Guard detection (YOLOv8n)
                              ├─ Outbreak risk (plain weighted rules)
                              └─ Alert composer + dispatcher
                                           │
                              Supabase (Auth, Postgres, Storage)
```

A rendered Mermaid version is in `docs/architecture.md`.

### 2.2 Models and the AI justification

| Capability | Model / method | Why AI is warranted |
|---|---|---|
| Crop/livestock disease scan | **MobileNetV3, quantized TFLite**, on-device | Image classification is impossible with rules/SQL — a genuine CV task. |
| Livestock triage | **LLM (Claude) with a transparent rule fallback** | Mixed Shona/English symptom text needs language understanding; the keyword baseline provably fails on paraphrase. |
| Guard intrusion | **YOLOv8n** object detection, server-side | Must distinguish person/vehicle from moving cattle at night — class-aware detection, not motion-pixel thresholding (which would false-alarm constantly). |
| Forecast | Time-series over MSD + satellite data (seeded stub today) | Sparse, noisy regional weather data. |

**Where AI is deliberately *not* used** — to avoid "sledgehammer" design:
subscriptions, alert scheduling, and **outbreak risk aggregation**. District
risk is a plain weighted rule, `Σ(reporter_trust × recency_weight)`, banded into
low/moderate/high. It is transparent and auditable. Outbreak *spread prediction*
is a **roadmap** ML use case, unlocked only once real report volume exists.

### 2.3 On-device inference & edge budget

Disease scans run **entirely on-device** so they work with zero connectivity;
results queue locally and sync to `scan_history` when a connection returns. The
server `/scan` endpoint is a fallback for devices that cannot run TFLite.

Edge targets for the quantized MobileNetV3 model: **< 256 MB RAM** and
**< 100 ms inference** on a mid-range Android device. *These targets will be
reported as measured numbers from the demo model during the bootcamp; the MVP
currently ships a documented placeholder classifier implementing the identical
inference interface (see `docs/dataset_statement.md`), so swapping in trained
weights requires no application changes.*

### 2.4 API layer

Eight routers expose the product surface: `scan`, `triage`, `forecast`,
`subscriptions`, `alerts`, `guard`, `outbreaks`, `ussd`. The USSD router
implements the Africa's Talking callback contract (a stateless menu-tree over
the accumulated `text` field), so the exact production handler is exercised by
the bundled web simulator. Full reference: `docs/api.md`.

### 2.5 Offline-sync design

The app is offline-first: (1) on-device inference needs no network; (2) writes
(scans, outbreak reports, subscription toggles) are optimistic and queued
locally; (3) a sync pass replays the queue when connectivity returns, keyed for
idempotency so retries are safe. Alerts outbound to farmers use the pull-based
USSD channel or store-and-forward SMS, both tolerant of intermittent coverage.

### 2.6 Database schema (summary)

`regions`, `farmers`, `subscriptions`, `alerts`, `scan_history`,
`guard_events`, `outbreak_reports`, `district_risk`. Full Postgres DDL with Row
Level Security is in `sample_data/schema.sql`. Personal data is minimised to a
phone number (plus optional name/region), stored only after explicit consent.

### 2.7 The community early-warning loop

Community outbreak reports recompute per-district risk on every submission; when
a district crosses the high-risk threshold, a **region-targeted disease alert is
auto-dispatched** to that district's subscribers over SMS. Crowdsourced reports
thus close the loop back into the alerts system — early-warning intelligence
generated by farmers, for farmers.

---

## Section 3 — Deliverables & CCE Implementation Roadmap

### 3.1 Current MVP deliverables (this submission)

- FastAPI backend with all eight routers, pluggable messaging (console/Twilio)
  and triage (rule/LLM) backends, seed data, and **20 passing pytest tests**.
- Flutter app (feature-first): onboarding + trilingual UI, crop scan, livestock
  triage chat, consent-gated alert subscriptions, Guard camera/detection view,
  outbreak heat map + community report flow; widget tests included.
- USSD web simulator, Supabase schema with RLS, and full documentation
  (`README`, architecture, API, dataset statement).

### 3.2 Milestones

| Horizon | Milestone |
|---|---|
| **Through bootcamp (27 Jul–1 Aug)** | Train the first real MobileNetV3 crop model on a PlantVillage subset; measure and report on-device RAM/latency; wire one live Twilio sandbox for SMS; deploy the backend into the ZCHPC CCE and run the full test suite there. |
| **3 months** | Field-collect Zimbabwean crop images with AGRITEX in one pilot district; harden offline sync; live USSD shortcode pilot; YOLOv8n Guard model on real night footage. |
| **6 months** | MSD weather integration for real forecasts; AGRITEX officer dashboard of flagged triage cases; WhatsApp bot in production; expand crop/livestock classes. |
| **12 months** | Outbreak spread-prediction ML model on accumulated report data; multi-district scale-out; institutional integrations (insurers, NGOs). |

### 3.3 Compute needs & testing in the CCE

Training is modest (transfer-learning on MobileNetV3 / YOLOv8n): a single mid-
range GPU suffices for the initial models. Serving is CPU-friendly (the on-
device model offloads most inference to the phone; the server model is a
fallback). We will use the **ZCHPC CCE** to (a) run reproducible training jobs
from locked manifests, (b) host the FastAPI backend + Postgres for the pilot,
and (c) execute the automated test suite in CI on every change.

### 3.4 Locked dependency manifests

- Backend: `backend/requirements.in` (top-level) compiled to a pinned
  `backend/requirements.txt` lockfile.
- App: `app/pubspec.yaml` with `pubspec.lock` generated by `flutter pub get`.

Reproducibility is a first-class requirement for CCE testing.

---

## Section 4 — Compliance & Risk Mitigation

### 4.1 Data Protection Act [Chapter 11:12]

- **Data minimisation:** the only personal data processed is a phone number
  (plus optional name/region) for opt-in alerts. No location tracking beyond a
  self-selected district.
- **Consent:** registration is **refused server-side** without an explicit
  `consent_given` flag; the app presents a trilingual consent checkbox at
  signup, and dialling the USSD subscription flow is recorded as consent.
- **Access control:** Supabase **Row Level Security** restricts each farmer to
  their own records (`sample_data/schema.sql`); alerts and guard events are
  written only by the backend service role.

### 4.2 Misdiagnosis risk & human oversight

AI advice can be wrong, and wrong advice about animals or crops has real cost.
RimaAI mitigates this by design:

- **Every** scan and triage result carries a disclaimer and an explicit
  **escalation to AGRITEX or a veterinarian** — the AI is framed as first-line
  guidance, never a replacement for an expert.
- Urgent triage outcomes (high/emergency) surface a "contact a vet immediately"
  message.
- Advice content is curated reference material to be **reviewed and signed off
  by AGRITEX / veterinary services** before the pilot.

### 4.3 Model testing approach

The rule-based triage baseline is unit-tested, **including its documented
failure mode** (paraphrase with no keyword), which justifies the LLM path rather
than assuming it. Model changes will be gated in CI on a held-out evaluation
set, with accuracy/latency reported against the edge budget before any release.

### 4.4 Cybersecurity basics

Supabase Auth for identity; RLS for authorization; Pydantic schema validation on
every request (typed, constrained inputs); secrets only via environment
variables with a committed `.env.example` and **no keys in the repository**;
messaging and LLM integrations are import-guarded and fail safe (the app never
hard-fails offline — triage falls back to rules, alerts fall back to console).

---

## Section 5 — Sustainability & Future Adoption

### 5.1 Business model — freemium

- **Free for smallholders:** disease/livestock scans, triage, forecasts, and
  core alerts — maximising reach and impact where ability to pay is lowest.
- **Paid — RimaAI Guard (commercial farmers):** camera-based stock-theft
  surveillance and intrusion alerts, billed per camera / per site.
- **Paid — institutional licensing:** agritech firms, insurers, and NGOs license
  aggregated (privacy-preserving) outbreak intelligence, the alert dispatch
  rails, and white-label deployments.

### 5.2 Cost drivers

Hosting (backend + Postgres + storage), **SMS costs** (the main variable cost of
the alert channel — mitigated by USSD/WhatsApp and by targeting alerts to
affected districts only), and model serving (kept low by on-device inference).

### 5.3 Indicative budgets (honest, rough)

| Item | 3-month pilot (1 district) | 1-year scale (multi-district) |
|---|---|---|
| Cloud hosting + database | US$ 300–600 | US$ 3,000–6,000 |
| SMS / USSD (telco) | US$ 500–1,500 | US$ 8,000–20,000 |
| Model training / compute | US$ 200–500 (CCE-subsidised) | US$ 2,000–5,000 |
| Field data collection (with AGRITEX) | US$ 1,000–2,000 | US$ 6,000–12,000 |
| Personnel (part-time) | US$ 3,000–5,000 | US$ 30,000–50,000 |
| **Indicative total** | **≈ US$ 5–9k** | **≈ US$ 50–90k** |

These are planning estimates to be refined with telco and hosting quotes.

### 5.4 Pilot site

A **single district reached through AGRITEX** — a district with both smallholder
livestock (January-disease exposure) and maize cropping, so all core modules are
exercised. Success metrics: farmers reached per channel, scan/triage usage,
alert delivery rates, and (with AGRITEX) qualitative impact on early treatment.

---

## Appendix A — Demo access & repository

**Everything a judge needs is reachable from one URL: https://rimai.vercel.app/**
That page is the single hub for this submission — it links directly to:
- **UI demo** — the live AGRITEX officer dashboard (`/dashboard`), reading real
  district risk, alerts and Guard events from the deployed backend; no install
  required.
- **Android APK** — a release build (arm64), pre-configured to point at the
  live backend by default (`/downloads/RimaAI.apk`), installable directly on a
  test device.
- **GitHub source** — the full repository (backend, Flutter app, web
  dashboard, docs, tests).

To run locally instead: see `README.md`. Backend: `pip install -r
backend/requirements.txt` → `python -m app.seed` → `uvicorn app.main:app
--reload` → `pytest`. App: `flutter create . && flutter pub get && flutter
run`. USSD: open `ussd-simulator/index.html`.

## Appendix B — Honesty statement (data provenance)
Disease/livestock models are placeholder classifiers in the MVP; forecast and
Guard use seeded/sample data. Full detail and licences in
`docs/dataset_statement.md`. All advice is framed as guidance pending
AGRITEX/veterinary sign-off.
