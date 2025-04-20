import pytest
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Import TimeService components
from paelladoc.domain.services.time_service import TimeService
from paelladoc.domain.models.project import set_time_service


class MockTimeService(TimeService):
    """Mock time service for testing."""

    def __init__(self, fixed_time=None):
        """Initialize with optional fixed time."""
        self.fixed_time = fixed_time or datetime.now(timezone.utc)
        self.call_count = 0

    def get_current_time(self) -> datetime:
        """Get the mocked current time, incrementing by microseconds on each call."""
        # Increment call count
        self.call_count += 1

        # Return fixed time plus microseconds based on call count to ensure
        # timestamps are different when multiple calls happen in sequence
        return self.fixed_time + timedelta(microseconds=self.call_count)

    def ensure_utc(self, dt: datetime) -> datetime:
        """Ensure a datetime is in UTC."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)


@pytest.fixture(scope="session", autouse=True)
def setup_time_service():
    """Set up the time service globally for all tests."""
    # Using a fixed time for consistent testing
    fixed_time = datetime(2025, 4, 20, 12, 0, 0, tzinfo=timezone.utc)
    mock_service = MockTimeService(fixed_time)
    set_time_service(mock_service)
    return mock_service
