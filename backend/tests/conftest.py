"""Pytest fixtures.

A throwaway SQLite database is configured *before* the app is imported so the
engine binds to it. Each test session gets a clean schema.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterator

import pytest

# Point the app at an isolated temp DB before any app import binds the engine.
_TMP_DB = os.path.join(tempfile.mkdtemp(prefix="rimaai_test_"), "test.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_TMP_DB}"
os.environ["MESSAGING_TRANSPORT"] = "console"
os.environ["TRIAGE_BACKEND"] = "rule"

from fastapi.testclient import TestClient  # noqa: E402

from app.core.database import init_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _prepare_db() -> Iterator[None]:
    """Create all tables once for the test session."""
    init_db()
    yield


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Return a TestClient bound to the app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def consented_farmer(client: TestClient) -> dict:
    """Register and return a consented farmer for reuse in tests."""
    import uuid

    phone = f"+26377{uuid.uuid4().int % 10_000_000:07d}"
    resp = client.post(
        "/farmers",
        json={
            "phone_number": phone,
            "name": "Test Farmer",
            "language": "en",
            "region_name": "Gokwe",
            "consent_given": True,
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()
