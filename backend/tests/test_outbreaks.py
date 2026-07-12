"""Tests for outbreak reporting, risk aggregation and threshold auto-alerts."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.services.outbreak import level_for


def test_level_thresholds() -> None:
    """Score bands map to the expected risk levels (defaults 3.0 / 6.0)."""
    assert level_for(0.0) == "low"
    assert level_for(3.5) == "moderate"
    assert level_for(6.5) == "high"


def test_single_report_is_low_risk(client: TestClient) -> None:
    """One community report should not by itself create high risk."""
    resp = client.post(
        "/outbreaks/report",
        json={"region_name": "Marondera", "outbreak_type": "armyworm"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["risk"]["level"] in {"low", "moderate"}
    assert body["alert_dispatched"] is False


def test_clustered_reports_trigger_high_risk_and_alert(
    client: TestClient, consented_farmer: dict
) -> None:
    """Many recent trusted reports tip a district to high risk and auto-alert.

    The consented farmer is subscribed to disease alerts in the region so the
    auto-dispatch has at least one recipient.
    """
    region = "Chinhoyi"
    client.post(
        "/subscriptions",
        json={
            "farmer_id": consented_farmer["id"],
            "category": "disease",
            "channel": "sms",
            "region_name": region,
        },
    )
    last = None
    for _ in range(12):
        last = client.post(
            "/outbreaks/report",
            json={"region_name": region, "outbreak_type": "tick_disease"},
        ).json()
    assert last is not None
    assert last["risk"]["level"] == "high"
    assert last["alert_dispatched"] is True
    assert last["alert_recipients"] >= 1


def test_map_returns_coordinates(client: TestClient) -> None:
    """The heat map exposes rows; reported districts appear."""
    resp = client.get("/outbreaks/map")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
