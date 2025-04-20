import pytest
from datetime import datetime, timezone
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

    def get_current_time(self) -> datetime:
        """Get the mocked current time."""
        return self.fixed_time

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
