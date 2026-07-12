"""Region (district / province) model."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Region(Base):
    """A Zimbabwean administrative region used for targeting alerts and maps."""

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    province: Mapped[str] = mapped_column(String(120), index=True)
    # Centroid coordinates used to place the district on the outbreak heat map.
    latitude: Mapped[float] = mapped_column(default=0.0)
    longitude: Mapped[float] = mapped_column(default=0.0)
