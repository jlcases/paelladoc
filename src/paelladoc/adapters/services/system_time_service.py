"""System implementation of the time service."""

import datetime
from ...domain.services.time_service import TimeService


class SystemTimeService(TimeService):
    """System implementation of TimeService using system clock."""

    def get_current_time(self) -> datetime.datetime:
        """Get current timestamp in UTC using system clock."""
        return datetime.datetime.now(datetime.timezone.utc)

    def ensure_utc(self, dt: datetime.datetime) -> datetime.datetime:
        """Convert a datetime to UTC.

        If the datetime has no timezone info, assumes it's in UTC.
        """
        if dt.tzinfo is None:
            return dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc)
