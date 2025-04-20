"""Time service for domain timestamp handling."""

from abc import ABC, abstractmethod
import datetime


class TimeService(ABC):
    """Abstract base class for time operations in the domain."""

    @abstractmethod
    def get_current_time(self) -> datetime.datetime:
        """Get current timestamp in UTC.

        Returns:
            datetime.datetime: Current time in UTC.
        """
        pass

    @abstractmethod
    def ensure_utc(self, dt: datetime.datetime) -> datetime.datetime:
        """Ensure a datetime is in UTC.

        If the datetime has no timezone info, assumes it's in UTC.

        Args:
            dt: Datetime to convert

        Returns:
            datetime.datetime: UTC datetime with timezone info
        """
        pass
