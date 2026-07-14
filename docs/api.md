# RimaAI API Reference

Base URL (dev): `http://localhost:8000`. Interactive docs at `/docs` (Swagger)
and `/redoc` when the server is running.

All endpoints return JSON unless noted. The USSD endpoint returns plain text.

---

## Meta

### `GET /health`
Liveness probe. Returns the active messaging + triage backends.
```json
{ "status": "ok", "environment": "dev", "messaging_transport": "console", "triage_backend": "rule" }
```

---

## Scan — `POST /scan`
Server-side fallback inference. `multipart/form-data`.

| Field | Type | Notes |
|-------|------|-------|
| `file` | file | crop/livestock photo (required) |
| `scan_type` | str | `crop` (default) or `livestock` |
| `language` | str | `en` / `sn` / `nd` |
| `farmer_id` | int | optional, stores to history |

Response `ScanResult`:
```json
{ "label": "tomato_late_blight", "confidence": 0.88, "advice": "...",
  "scan_type": "crop", "source": "server", "advice_i18n": {"en": "...", "sn": "..."} }
```
> On-device scans use the bundled TFLite model and never hit this endpoint.

---

## Triage — `POST /triage`
Livestock symptom triage. Body:
```json
{ "message": "my cow has many ticks and swollen neck", "animal": "cattle", "language": "en" }
```
Response `TriageResponse` always includes an escalation + disclaimer:
```json
{ "condition": "Suspected tick-borne disease (theileriosis / January disease)",
  "urgency": "emergency", "advice": "...", "escalation": "Contact a veterinarian...",
  "backend": "rule", "disclaimer": "RimaAI gives general guidance only..." }
```
`urgency` ∈ `low|medium|high|emergency`. `backend` is `rule` or `llm`.

---

## Forecast — `GET /forecast?region_name=Bulawayo&season=2026/27`
Seeded planting-window guidance.
```json
{ "region_name": "Bulawayo", "season": "2026/27", "planting_window": "25 Nov - 20 Dec",
  "expected_rainfall_mm": 520.0, "confidence": "medium", "advice": "...", "source": "seeded_historical" }
```

---

## Farmers & Subscriptions

### `POST /farmers`
Register a farmer. **Consent is mandatory** (`consent_given: true`), else `400`.
```json
{ "phone_number": "+263771234567", "name": "Tendai", "language": "sn",
  "region_name": "Gokwe", "consent_given": true }
```

### `GET /farmers/{id}`
Fetch a farmer.

### `POST /subscriptions`
Create/toggle a subscription (idempotent per farmer+category+channel).
```json
{ "farmer_id": 1, "category": "livestock", "channel": "sms", "region_name": "Gokwe", "active": true }
```
`category` ∈ `weather|disease|tips|livestock|insurance`, `channel` ∈ `sms|ussd|whatsapp`.

### `GET /subscriptions/{farmer_id}` · `DELETE /subscriptions/{id}`
List / soft-cancel subscriptions.

---

## Alerts

### `POST /alerts/dispatch`
Compose and send an alert to matching subscribers via the messaging transport.
```json
{ "category": "tips", "body": "Dip your cattle weekly this season.", "region_name": "Gokwe", "channel": "sms" }
```
Returns the persisted `Alert` with `recipients` reached.

### `GET /alerts?limit=50`
Recent dispatched alerts (audit log).

---

## Guard

### `POST /guard/detect`
Run detection on a sample frame; persists an event on intrusion.
```json
{ "camera_id": "kraal-cam-01", "frame_id": "sample_night_01" }
```
Sample frames: `sample_quiet_01`, `sample_night_01`, `sample_night_02`, `sample_empty_01`.
Response includes normalized `boxes` and `is_intrusion`.

### `GET /guard/events?limit=50`
Intrusion event history.

---

## Outbreaks

### `POST /outbreaks/report`
Submit a community report; recomputes district risk; auto-alerts on high risk.
```json
{ "region_name": "Gokwe", "outbreak_type": "tick_disease", "description": "many sick cattle", "farmer_id": 1 }
```
`outbreak_type` ∈ `crop_disease|armyworm|locusts|tick_disease|flood`.
Response:
```json
{ "report": {...}, "risk": {"region_name":"Gokwe","level":"high","score":6.3,"report_count":10},
  "alert_dispatched": true, "alert_recipients": 4 }
```

### `GET /outbreaks/map?outbreak_type=tick_disease`
Per-district aggregated risk with centroid coordinates (for the heat map).

### `GET /outbreaks/reports?limit=100`
Recent reports.

---

## USSD — `POST /ussd`
Africa's Talking callback format. `application/x-www-form-urlencoded`:
`phoneNumber`, `text` (accumulated `*`-joined inputs), `sessionId`, `serviceCode`.
Returns plain text prefixed `CON` (more input expected) or `END` (final screen).

Menu tree:
```
*123#
  1. Subscribe to alerts → 1..5 category → END confirmation
  2. My subscriptions → END list
  3. About RimaAI → END info
```
Try it via the [USSD simulator](../ussd-simulator/).

---

## WhatsApp — `POST /whatsapp/webhook`
Twilio WhatsApp webhook shape. `application/x-www-form-urlencoded`:
`From` (`whatsapp:+263...`), `Body` (the message text). One message per
request, no session id — conversation state is kept in-memory per phone
number. Returns plain text with the bot's reply.

Menu tree:
```
(any message)
  1. Subscribe to alerts → 1..5 category → confirmation
  2. My subscriptions → list
  3. Livestock symptom check → free text → triage result
  4. About RimaAI → info
```
Try it via the [WhatsApp simulator](../whatsapp-simulator/).
