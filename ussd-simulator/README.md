# RimaAI USSD Simulator

A tiny static page that lets judges click through the `*123#` USSD menu without
any telco integration. It POSTs to the backend `/ussd` endpoint using the same
callback format Africa's Talking uses, so the exact production handler is exercised.

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
3. In the simulator, type `*123#` and press **Send**, then reply with menu
   numbers (`1` to subscribe, then `1`–`5` to pick a category).

Subscriptions created here persist to the same database the app and the alert
dispatcher use, so a USSD subscriber will receive dispatched alerts.

> If you open the file directly (`file://`) and the backend is on a different
> origin, make sure `CORS_ORIGINS=*` (the default) is set for the backend.
