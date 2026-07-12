"""Application configuration.

All configuration is environment-driven so the service can be promoted from a
local demo (SQLite + console messaging) to production (Postgres/Supabase +
Twilio) without code changes. Never hard-code secrets; see ``.env.example``.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables / ``.env``."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- General ---
    app_name: str = "RimaAI Backend"
    environment: str = "dev"  # dev | staging | prod
    debug: bool = True

    # --- Database ---
    # Defaults to a local SQLite file so the demo runs with zero setup.
    # In production set DATABASE_URL to the Supabase/Postgres connection string.
    database_url: str = "sqlite:///./rimaai.db"

    # --- Messaging transport ---
    # console -> logs messages instead of sending (safe default for demos)
    # twilio  -> uses Twilio SMS/WhatsApp (requires credentials below)
    messaging_transport: str = "console"
    twilio_account_sid: str | None = None
    twilio_auth_token: str | None = None
    twilio_sms_from: str | None = None
    twilio_whatsapp_from: str | None = None  # e.g. "whatsapp:+14155238886"

    # --- Triage / LLM ---
    # rule -> deterministic rule-based triage (no external calls, default)
    # llm  -> Anthropic Claude with rule-based fallback on error
    triage_backend: str = "rule"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-opus-4-8"

    # --- Outbreak risk aggregation (plain rules, NOT AI) ---
    outbreak_high_risk_threshold: float = 6.0
    outbreak_moderate_risk_threshold: float = 3.0
    outbreak_recency_window_days: int = 14

    # --- CORS ---
    cors_origins: str = "*"


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    return Settings()
