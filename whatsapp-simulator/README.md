# RimaAI WhatsApp Simulator

A tiny static page that lets judges chat with the RimaAI WhatsApp bot without
any Twilio integration. It POSTs to the backend `/whatsapp/webhook` endpoint
using the same `From`/`Body` shape Twilio's WhatsApp webhook uses, so the
exact production handler is exercised.

## Run

1. Start the backend:
   ```bash
   cd ../backend
   uvicorn app.main:app --reload
   ```
2. Open `index.html` in a browser (double-click, or serve it):
   ```bash
   python -m http.server 5500   # then visit http://localhost:5500
   ```
3. In the simulator, type `hi` and press send, then reply with menu numbers
   (`1` to subscribe, then `1`–`5` to pick a category; `3` for a livestock
   symptom check).

Subscriptions created here persist to the same database the app and the alert
dispatcher use, so a WhatsApp subscriber will receive dispatched alerts.

> If you open the file directly (`file://`) and the backend is on a different
> origin, make sure `CORS_ORIGINS=*` (the default) is set for the backend.
