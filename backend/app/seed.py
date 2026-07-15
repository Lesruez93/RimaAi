"""Seed the database with demo data so screens look alive during the demo.

Run with:  ``python -m app.seed``

Idempotent-ish: it clears the demo tables first, then repopulates. Safe for the
SQLite demo database; do NOT run against production.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.core.database import SessionLocal, init_db
from app.models import (
    Alert,
    CameraSettings,
    DistrictRisk,
    Farmer,
    GuardEvent,
    OutbreakReport,
    Region,
    ScanHistory,
    Subscription,
)
from app.services.outbreak import recompute_district_risk

# Public demo HLS stream used to fill the Guard camera view when no real
# camera has been configured yet, so the feature looks alive out of the box.
DEMO_STREAM_URL = (
    "https://hls-harbor-livepush.akamaized.net/live_cdn/nsqIStpj8PaG-Ev/"
    "emcQJ0pGpremocy/index.m3u8"
)

# (name, province, lat, lon) — approximate district centroids.
REGIONS = [
    ("Harare", "Harare", -17.83, 31.05),
    ("Bulawayo", "Bulawayo", -20.15, 28.58),
    ("Mutare", "Manicaland", -18.97, 32.67),
    ("Masvingo", "Masvingo", -20.07, 30.83),
    ("Gweru", "Midlands", -19.45, 29.82),
    ("Gokwe", "Midlands", -18.21, 28.93),
    ("Chinhoyi", "Mashonaland West", -17.36, 30.20),
    ("Marondera", "Mashonaland East", -18.19, 31.55),
]

FARMERS = [
    # (phone, name, language, region)
    ("+263771000001", "Tendai Moyo", "sn", "Gokwe"),
    ("+263771000002", "Sipho Ndlovu", "nd", "Bulawayo"),
    ("+263771000003", "Rutendo Chikafu", "sn", "Mutare"),
    ("+263771000004", "Blessing Dube", "en", "Masvingo"),
    ("+263771000005", "Farai Ncube", "sn", "Gokwe"),
    ("+263771000006", "Nomsa Sibanda", "nd", "Gweru"),
]


def _clear(db) -> None:  # type: ignore[no-untyped-def]
    """Delete demo rows in FK-safe order."""
    for model in (
        Alert,
        Subscription,
        ScanHistory,
        GuardEvent,
        CameraSettings,
        OutbreakReport,
        DistrictRisk,
        Farmer,
        Region,
    ):
        db.query(model).delete()
    db.commit()


def seed() -> None:
    """Populate the database with demo regions, farmers, subs and outbreaks."""
    init_db()
    db = SessionLocal()
    try:
        _clear(db)

        # Regions
        for name, province, lat, lon in REGIONS:
            db.add(Region(name=name, province=province, latitude=lat, longitude=lon))
        db.commit()

        # Farmers (all consented) + a livestock + weather subscription each
        farmers: list[Farmer] = []
        for phone, name, lang, region in FARMERS:
            f = Farmer(
                phone_number=phone,
                name=name,
                language=lang,
                region_name=region,
                consent_given=True,
            )
            db.add(f)
            farmers.append(f)
        db.commit()

        for f in farmers:
            db.add_all(
                [
                    Subscription(farmer_id=f.id, category="livestock", channel="sms", region_name=f.region_name),
                    Subscription(farmer_id=f.id, category="weather", channel="sms", region_name=f.region_name),
                    Subscription(farmer_id=f.id, category="disease", channel="sms", region_name=f.region_name),
                ]
            )
        db.commit()

        # Outbreak reports: cluster several recent tick_disease reports in Gokwe
        # so it tips into HIGH risk (demonstrates the auto-alert threshold).
        now = datetime.now(UTC)
        recent_reports = [
            ("Gokwe", "tick_disease", 0, 0.7),
            ("Gokwe", "tick_disease", 1, 0.6),
            ("Gokwe", "tick_disease", 2, 0.9),
            ("Gokwe", "tick_disease", 3, 0.8),
            ("Gokwe", "tick_disease", 1, 0.7),
            ("Gokwe", "tick_disease", 4, 0.8),
            ("Gokwe", "tick_disease", 2, 0.9),
            ("Gokwe", "tick_disease", 5, 0.7),
            ("Gokwe", "tick_disease", 6, 0.8),
            ("Gokwe", "tick_disease", 3, 0.9),
            ("Mutare", "crop_disease", 1, 0.6),
            ("Mutare", "crop_disease", 3, 0.7),
            ("Masvingo", "armyworm", 2, 0.6),
            ("Bulawayo", "flood", 5, 0.5),
        ]
        for region, otype, days_ago, trust in recent_reports:
            db.add(
                OutbreakReport(
                    region_name=region,
                    outbreak_type=otype,
                    description=f"Seeded demo report: {otype} in {region}.",
                    reporter_trust=trust,
                    created_at=now - timedelta(days=days_ago),
                )
            )
        db.commit()

        # Recompute risk for every reported (region, type) pair.
        for region, otype, *_ in recent_reports:
            recompute_district_risk(db, region, otype)
        db.commit()

        # A couple of scan history rows and a guard event for populated screens.
        db.add_all(
            [
                ScanHistory(scan_type="crop", label="tomato_late_blight", confidence=0.88, advice="Remove infected plants; apply fungicide.", source="device"),
                ScanHistory(scan_type="livestock", label="cattle_heavy_tick_load", confidence=0.82, advice="Dip now; watch for January disease.", source="device"),
                GuardEvent(camera_id="kraal-cam-01", label="person", confidence=0.91, is_intrusion=True),
                CameraSettings(camera_id="kraal-cam-01", stream_url=DEMO_STREAM_URL, mode="demo"),
            ]
        )
        db.commit()

        gokwe_risk = (
            db.query(DistrictRisk)
            .filter_by(region_name="Gokwe", outbreak_type="tick_disease")
            .first()
        )
        print("Seed complete.")
        print(f"  Regions: {len(REGIONS)}  Farmers: {len(FARMERS)}")
        if gokwe_risk:
            print(
                f"  Gokwe tick_disease risk: {gokwe_risk.level} "
                f"(score={gokwe_risk.score}, reports={gokwe_risk.report_count})"
            )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
