"""End-to-end router tests for the core API surface."""

from __future__ import annotations

import io

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    """Health endpoint reports ok and the active backends."""
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["messaging_transport"] == "console"


def test_registration_requires_consent(client: TestClient) -> None:
    """Registration is refused without explicit consent (DPA compliance)."""
    resp = client.post(
        "/farmers",
        json={"phone_number": "+263779999999", "consent_given": False},
    )
    assert resp.status_code == 400


def test_scan_returns_label_and_advice(client: TestClient) -> None:
    """Uploading an image returns a label, confidence and trilingual advice."""
    files = {"file": ("leaf.jpg", io.BytesIO(b"fake-image-bytes"), "image/jpeg")}
    resp = client.post("/scan", files=files, data={"scan_type": "crop", "language": "sn"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["label"]
    assert 0.0 <= body["confidence"] <= 1.0
    assert body["advice"]


def test_forecast_known_region(client: TestClient) -> None:
    """Forecast returns seeded guidance for a known region."""
    body = client.get("/forecast", params={"region_name": "Bulawayo"}).json()
    assert body["region_name"] == "Bulawayo"
    assert body["expected_rainfall_mm"] > 0


def test_guard_intrusion_creates_event(client: TestClient) -> None:
    """A person-in-frame sample yields an intrusion and a persisted event."""
    resp = client.post(
        "/guard/detect",
        json={"camera_id": "kraal-cam-01", "frame_id": "sample_night_01"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_intrusion"] is True
    assert body["event_id"] is not None
    assert len(body["boxes"]) >= 1


def test_guard_quiet_frame_no_event(client: TestClient) -> None:
    """A cattle-only frame is not an intrusion."""
    body = client.post(
        "/guard/detect", json={"frame_id": "sample_quiet_01"}
    ).json()
    assert body["is_intrusion"] is False
    assert body["event_id"] is None


def test_subscription_lifecycle(client: TestClient, consented_farmer: dict) -> None:
    """Create, list and cancel a subscription."""
    fid = consented_farmer["id"]
    created = client.post(
        "/subscriptions",
        json={"farmer_id": fid, "category": "weather", "channel": "sms"},
    )
    assert created.status_code == 201, created.text
    sub_id = created.json()["id"]

    listed = client.get(f"/subscriptions/{fid}").json()
    assert any(s["id"] == sub_id for s in listed)

    assert client.delete(f"/subscriptions/{sub_id}").status_code == 204


def test_ussd_root_and_subscribe_flow(client: TestClient) -> None:
    """The USSD menu tree walks from root to a subscription confirmation."""
    root = client.post("/ussd", data={"phoneNumber": "+263770000009", "text": ""})
    assert root.text.startswith("CON")
    assert "Subscribe" in root.text

    menu = client.post("/ussd", data={"phoneNumber": "+263770000009", "text": "1"})
    assert menu.text.startswith("CON")

    done = client.post("/ussd", data={"phoneNumber": "+263770000009", "text": "1*1"})
    assert done.text.startswith("END")
    assert "subscribed" in done.text.lower()

    # The subscription created via USSD should now be listed back.
    mine = client.post("/ussd", data={"phoneNumber": "+263770000009", "text": "2"})
    assert "weather" in mine.text.lower()


def test_whatsapp_menu_and_subscribe_flow(client: TestClient) -> None:
    """The WhatsApp bot walks from the main menu to a subscription confirmation."""
    phone = "whatsapp:+263770000011"

    greeting = client.post("/whatsapp/webhook", data={"From": phone, "Body": "hi"})
    assert "Subscribe to alerts" in greeting.text

    menu = client.post("/whatsapp/webhook", data={"From": phone, "Body": "1"})
    assert "Weather alerts" in menu.text

    done = client.post("/whatsapp/webhook", data={"From": phone, "Body": "1"})
    assert "subscribed" in done.text.lower()

    # The subscription created via WhatsApp should now be listed back.
    mine = client.post("/whatsapp/webhook", data={"From": phone, "Body": "2"})
    assert "weather" in mine.text.lower()


def test_whatsapp_livestock_triage_flow(client: TestClient) -> None:
    """Option 3 collects free-text symptoms and returns a triage result."""
    phone = "whatsapp:+263770000012"

    client.post("/whatsapp/webhook", data={"From": phone, "Body": "hi"})
    prompt = client.post("/whatsapp/webhook", data={"From": phone, "Body": "3"})
    assert "describe" in prompt.text.lower()

    result = client.post(
        "/whatsapp/webhook", data={"From": phone, "Body": "swollen glands and fever"}
    )
    assert "urgency" in result.text.lower()


def test_alert_dispatch(client: TestClient, consented_farmer: dict) -> None:
    """Dispatching an alert reaches consented subscribers via the console transport."""
    fid = consented_farmer["id"]
    client.post(
        "/subscriptions",
        json={
            "farmer_id": fid,
            "category": "tips",
            "channel": "sms",
            "region_name": "Gokwe",
        },
    )
    resp = client.post(
        "/alerts/dispatch",
        json={
            "category": "tips",
            "body": "Dip your cattle weekly this season.",
            "region_name": "Gokwe",
        },
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["recipients"] >= 1
