"""Database engine, session factory and declarative base.

Uses SQLAlchemy so the same models run on SQLite (zero-setup demo) and on
Postgres/Supabase in production simply by changing ``DATABASE_URL``.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# ``check_same_thread`` is only needed for SQLite; it is ignored by Postgres.
_connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)

engine = create_engine(settings.database_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a scoped database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables. Idempotent; safe to call on startup."""
    # Import models so they are registered on ``Base.metadata`` before create_all.
    from app import models  # noqa: F401  (side-effect import)

    Base.metadata.create_all(bind=engine)
