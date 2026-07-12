"""SQLAlchemy ORM models for RimaAI.

Importing this package registers every model on ``Base.metadata`` so that
``init_db()`` can create the full schema.
"""

from app.models.alert import Alert
from app.models.farmer import Farmer
from app.models.guard import GuardEvent
from app.models.outbreak import DistrictRisk, OutbreakReport
from app.models.region import Region
from app.models.scan import ScanHistory
from app.models.subscription import Subscription

__all__ = [
    "Alert",
    "DistrictRisk",
    "Farmer",
    "GuardEvent",
    "OutbreakReport",
    "Region",
    "ScanHistory",
    "Subscription",
]
