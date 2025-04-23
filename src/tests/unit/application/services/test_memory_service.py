"""
Unit tests for the MemoryService.
"""

from unittest.mock import AsyncMock  # Use AsyncMock for async methods
import sys
from pathlib import Path
import pytest

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Modules to test
from paelladoc.application.services.memory_service import MemoryService
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,  # Ensure this line is correct
)
from paelladoc.ports.output.memory_port import MemoryPort

# --- Pytest Fixtures ---


@pytest.fixture
def mock_memory_port() -> AsyncMock:
    """Provides a mocked MemoryPort instance for tests."""
    return AsyncMock(spec=MemoryPort)


@pytest.fixture
def memory_service(mock_memory_port: AsyncMock) -> MemoryService:
    """Provides a MemoryService instance initialized with a mocked port."""
    return MemoryService(memory_port=mock_memory_port)


# --- Tests for Taxonomy Events (Pytest Style) ---


@pytest.mark.asyncio
async def test_update_project_memory_emits_taxonomy_updated_event(
    memory_service: MemoryService, mock_memory_port: AsyncMock
):
    """Test that taxonomy_updated event is emitted when taxonomy fields change."""
    # Arrange
    project_name = "tax-event-project"
    old_memory = ProjectMemory(
        project_info=ProjectInfo(
            name=project_name,
            base_path="/fake",
            taxonomy_version="1.0",
            platform_taxonomy="web-frontend",
            domain_taxonomy="ecommerce",
            size_taxonomy="smb",
            compliance_taxonomy="none",
            lifecycle_taxonomy="test_lifecycle_old",
        ),
        platform_taxonomy="web-frontend",
        domain_taxonomy="ecommerce",
        size_taxonomy="smb",
        compliance_taxonomy="none",
        lifecycle_taxonomy="test_lifecycle_old",
    )

    new_memory = ProjectMemory(
        project_info=ProjectInfo(
            name=project_name,
            base_path="/fake",
            taxonomy_version="1.0",
            platform_taxonomy="ios-native",
            domain_taxonomy="ecommerce",
            size_taxonomy="enterprise",
            compliance_taxonomy="gdpr",
            lifecycle_taxonomy="test_lifecycle_new",
        ),
        platform_taxonomy="ios-native",
        domain_taxonomy="ecommerce",
        size_taxonomy="enterprise",
        compliance_taxonomy="gdpr",
        lifecycle_taxonomy="test_lifecycle_new",
    )

    # Mock the port methods
    mock_memory_port.project_exists.return_value = True
    mock_memory_port.load_memory.return_value = old_memory
    mock_memory_port.save_memory.return_value = None  # Async function returns None

    # Create and register a mock event handler
    mock_handler = AsyncMock()
    memory_service.register_event_handler("taxonomy_updated", mock_handler)
    # Also register for project_updated to ensure it's still called
    mock_project_updated_handler = AsyncMock()
    memory_service.register_event_handler(
        "project_updated", mock_project_updated_handler
    )

    # Act
    await memory_service.update_project_memory(new_memory)

    # Assert
    mock_memory_port.save_memory.assert_awaited_once_with(new_memory)

    # Check project_updated event was called
    mock_project_updated_handler.assert_awaited_once()
    assert mock_project_updated_handler.await_args[0][0] == "project_updated"

    # Check taxonomy_updated event was called with correct data
    mock_handler.assert_awaited_once()
    event_name, event_data = mock_handler.await_args[0]
    assert event_name == "taxonomy_updated"
    assert event_data["project_name"] == project_name
    assert event_data["new_taxonomy"] == {
        "platform": "ios-native",
        "domain": "ecommerce",
        "size": "enterprise",
        "compliance": "gdpr",
    }
    assert event_data["old_taxonomy"] == {
        "platform": "web-frontend",
        "domain": "ecommerce",
        "size": "smb",
        "compliance": "none",
    }


@pytest.mark.asyncio
async def test_update_project_memory_no_taxonomy_change_no_event(
    memory_service: MemoryService, mock_memory_port: AsyncMock
):
    """Test that taxonomy_updated event is NOT emitted if taxonomy fields don't change."""
    # Arrange
    project_name = "no-tax-event-project"
    old_memory = ProjectMemory(
        project_info=ProjectInfo(
            name=project_name,
            base_path="/fake",
            taxonomy_version="1.0",
            platform_taxonomy="web-frontend",
            domain_taxonomy="ecommerce",
            size_taxonomy="smb",
            compliance_taxonomy="none",
            lifecycle_taxonomy="test_lifecycle",
        ),
        platform_taxonomy="web-frontend",
        domain_taxonomy="ecommerce",
        size_taxonomy="smb",
        compliance_taxonomy="none",
        lifecycle_taxonomy="test_lifecycle",
    )

    new_memory = ProjectMemory(
        project_info=ProjectInfo(
            name=project_name,
            base_path="/fake",
            taxonomy_version="1.0",
            platform_taxonomy="web-frontend",
            domain_taxonomy="ecommerce",
            size_taxonomy="smb",
            compliance_taxonomy="none",
            lifecycle_taxonomy="test_lifecycle",
        ),
        platform_taxonomy="web-frontend",
        domain_taxonomy="ecommerce",
        size_taxonomy="smb",
        compliance_taxonomy="none",
        lifecycle_taxonomy="test_lifecycle",
    )
    # Make some other change to trigger update
    new_memory.project_info.taxonomy_version = "1.1"

    # Mock the port methods
    mock_memory_port.project_exists.return_value = True
    mock_memory_port.load_memory.return_value = old_memory
    mock_memory_port.save_memory.return_value = None

    # Create and register a mock event handler
    mock_handler = AsyncMock()
    memory_service.register_event_handler("taxonomy_updated", mock_handler)
    # Also register for project_updated to ensure it's still called
    mock_project_updated_handler = AsyncMock()
    memory_service.register_event_handler(
        "project_updated", mock_project_updated_handler
    )

    # Act
    await memory_service.update_project_memory(new_memory)

    # Assert
    mock_memory_port.save_memory.assert_awaited_once_with(new_memory)

    # Check project_updated event was called (because metadata changed)
    mock_project_updated_handler.assert_awaited_once()

    # Check taxonomy_updated event was NOT called
    mock_handler.assert_not_awaited()


# NOTE: Keep the existing unittest class for other tests for now, or refactor all later.
# If keeping both styles, ensure imports and module structure support it.

# class TestMemoryService(unittest.IsolatedAsyncioTestCase):
#    ... (existing unittest tests) ...
