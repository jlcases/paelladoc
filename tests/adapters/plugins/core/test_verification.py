import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from uuid import uuid4
from pathlib import Path

# Modules to test
from paelladoc.adapters.plugins.core import verification
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
    DocumentStatus,
    Bucket,
    ArtifactMeta,
    set_time_service
)
from paelladoc.domain.services.time_service import TimeService
from paelladoc.adapters.services.system_time_service import SystemTimeService

# Mock data
MOCK_VALID_TAXONOMIES = {
    "platform": ["ios-native", "web-frontend"],
    "domain": ["ecommerce", "ai-ml"],
    "size": ["personal", "enterprise"],
    "lifecycle": ["mvp", "growth"],  # Added required lifecycle dimension
    "compliance": ["gdpr"]
}

@pytest.fixture(autouse=True)
def setup_time_service():
    """Initialize TimeService before each test."""
    service = SystemTimeService()
    set_time_service(service)
    yield
    set_time_service(None)  # Reset the service after test

# --- Tests for validate_mece_structure --- 

@pytest.fixture
def mock_project_memory() -> ProjectMemory:
    """Creates a mock ProjectMemory object."""
    project_info = ProjectInfo(
        name="test-project",
        base_path=Path("/fake/path"),
        taxonomy_version="1.0",
        platform_taxonomy="web-frontend",
        domain_taxonomy="ecommerce",
        size_taxonomy="enterprise",
        lifecycle_taxonomy="mvp",  # Required lifecycle
        compliance_taxonomy="gdpr"  # Optional compliance
    )
    memory = ProjectMemory(
        project_info=project_info,
        platform_taxonomy="web-frontend",
        domain_taxonomy="ecommerce",
        size_taxonomy="enterprise",
        lifecycle_taxonomy="mvp",  # Required lifecycle
        compliance_taxonomy="gdpr"  # Optional compliance
    )
    return memory

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_valid(mock_repository, mock_project_memory):
    """Test validation with a valid MECE structure."""
    mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
    mock_repository.get_dimension_values.side_effect = lambda dim: MOCK_VALID_TAXONOMIES[dim]
    
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == True
    assert not result["missing_dimensions"]
    assert not result["invalid_combinations"]
    assert not result.get("invalid_dimensions", [])

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_missing_dimension(mock_repository, mock_project_memory):
    """Test validation when a required dimension is missing."""
    mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
    mock_repository.get_dimension_values.side_effect = lambda dim: MOCK_VALID_TAXONOMIES[dim]
    
    mock_project_memory.domain_taxonomy = None  # Missing required domain
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == False
    assert "domain" in result["missing_dimensions"]
    assert not result["invalid_combinations"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_invalid_value(mock_repository, mock_project_memory):
    """Test validation with an invalid taxonomy value for a dimension."""
    mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
    mock_repository.get_dimension_values.side_effect = lambda dim: MOCK_VALID_TAXONOMIES[dim]
    
    mock_project_memory.platform_taxonomy = "invalid-platform"  # Invalid platform
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == False
    assert not result["missing_dimensions"]
    assert any("Invalid platform taxonomy" in msg for msg in result["invalid_combinations"])

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_invalid_optional_compliance(mock_repository, mock_project_memory):
    """Test validation with an invalid optional compliance value."""
    mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
    mock_repository.get_dimension_values.side_effect = lambda dim: MOCK_VALID_TAXONOMIES[dim]
    
    mock_project_memory.compliance_taxonomy = "invalid-compliance"
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == False
    assert any("Invalid compliance taxonomy" in msg for msg in result["invalid_combinations"])

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_no_compliance(mock_repository, mock_project_memory):
    """Test validation when optional compliance is not provided."""
    mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
    mock_repository.get_dimension_values.side_effect = lambda dim: MOCK_VALID_TAXONOMIES[dim]
    
    mock_project_memory.compliance_taxonomy = None
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == True
    assert not result["invalid_combinations"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_missing_lifecycle(mock_repository, mock_project_memory):
    """Test validation when required lifecycle is missing."""
    mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
    mock_repository.get_dimension_values.side_effect = lambda dim: MOCK_VALID_TAXONOMIES[dim]
    
    mock_project_memory.lifecycle_taxonomy = None  # Missing required lifecycle
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == False
    assert "lifecycle" in result["missing_dimensions"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_warning_combination(mock_repository, mock_project_memory):
    """Test validation warning for specific disallowed combinations (e.g., mobile+cms)."""
    mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
    mock_repository.get_dimension_values.side_effect = lambda dim: {
        **MOCK_VALID_TAXONOMIES,
        "platform": ["ios-native", "web-frontend"],
        "domain": ["cms", "ecommerce"]
    }[dim]
    
    mock_project_memory.platform_taxonomy = "ios-native"
    mock_project_memory.domain_taxonomy = "cms"
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == True  # Warnings don't make it invalid
    assert "Mobile platforms rarely implement full CMS functionality" in result["warnings"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_repository_error(mock_repository, mock_project_memory, caplog):
    """Test validation when the taxonomy repository fails."""
    mock_repository.get_available_dimensions.side_effect = Exception("Repository error")
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == False
    assert any("Failed to load taxonomy dimensions" in msg for msg in result["warnings"])

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY')
def test_validate_mece_unauthorized_dimension(mock_repository):
    """Test validation rejects unauthorized dimensions."""
    mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
    mock_repository.get_dimension_values.side_effect = lambda dim: MOCK_VALID_TAXONOMIES[dim]
    
    # Create a project memory with standard fields
    project_memory = ProjectMemory(
        project_info=ProjectInfo(
            name="test-project",
            base_path=Path("/fake/path"),
            platform_taxonomy="web-frontend",
            domain_taxonomy="ecommerce",
            size_taxonomy="enterprise",
            lifecycle_taxonomy="mvp",
            compliance_taxonomy="gdpr"
        ),
        platform_taxonomy="web-frontend",
        domain_taxonomy="ecommerce",
        size_taxonomy="enterprise",
        lifecycle_taxonomy="mvp",
        compliance_taxonomy="gdpr",
        # Add a custom dimension through custom_taxonomy (this should be allowed)
        custom_taxonomy={"custom_dimension": "custom-value"}
    )
    
    # Verify that custom dimensions in custom_taxonomy are allowed
    result = verification.validate_mece_structure(project_memory)
    assert result["is_valid"] == True
    assert "custom_dimension" not in result["invalid_dimensions"]
    
    # Verify that adding unauthorized taxonomy fields is not allowed
    with pytest.raises(ValueError) as exc_info:
        ProjectMemory(
            project_info=ProjectInfo(
                name="test-project",
                base_path=Path("/fake/path"),
                platform_taxonomy="web-frontend",
                domain_taxonomy="ecommerce",
                size_taxonomy="enterprise",
                lifecycle_taxonomy="mvp",
                compliance_taxonomy="gdpr"
            ),
            platform_taxonomy="web-frontend",
            domain_taxonomy="ecommerce",
            size_taxonomy="enterprise",
            lifecycle_taxonomy="mvp",
            compliance_taxonomy="gdpr",
            unauthorized_taxonomy="some-value"  # This should raise an error
        )
    assert "unauthorized_taxonomy" in str(exc_info.value)

# --- Tests for core_verification (Higher Level) ---

@pytest.mark.asyncio
@patch('paelladoc.adapters.plugins.core.verification.validate_mece_structure')
@patch('paelladoc.adapters.plugins.core.verification.SQLiteMemoryAdapter')
async def test_core_verification_invalid_mece(mock_adapter_cls, mock_validate, mock_project_memory):
    """Test core_verification returns error if MECE validation fails."""
    mock_adapter_instance = MagicMock()
    mock_adapter_instance.load_memory.return_value = mock_project_memory
    # Make load_memory return a coroutine
    mock_adapter_instance.load_memory = AsyncMock(return_value=mock_project_memory)
    mock_adapter_cls.return_value = mock_adapter_instance
    
    mock_validate.return_value = {
        "is_valid": False,
        "missing_dimensions": ["lifecycle"],
        "invalid_combinations": [],
        "invalid_dimensions": []
    }
    
    result = await verification.core_verification("test-project")
    
    assert result["status"] == "error"
    assert result["message"] == "Invalid MECE taxonomy structure"
    mock_validate.assert_called_once_with(mock_project_memory)
    mock_adapter_instance.load_memory.assert_called_once_with("test-project")

@pytest.mark.asyncio
@patch('paelladoc.adapters.plugins.core.verification.validate_mece_structure')
@patch('paelladoc.adapters.plugins.core.verification.SQLiteMemoryAdapter')
async def test_core_verification_valid_mece_calculates_coverage(
    mock_adapter_cls, mock_validate, mock_project_memory
):
    """Test core_verification proceeds to coverage calculation if MECE is valid."""
    mock_adapter_instance = MagicMock()
    # Make load_memory return a coroutine
    mock_adapter_instance.load_memory = AsyncMock(return_value=mock_project_memory)
    mock_adapter_cls.return_value = mock_adapter_instance
    
    mock_validate.return_value = {"is_valid": True}
    
    # Add some artifacts for coverage calculation using real ArtifactMeta instances
    mock_project_memory.artifacts = {
        Bucket.INITIATE_CORE_SETUP: [
            ArtifactMeta(
                name="Setup Doc",
                bucket=Bucket.INITIATE_CORE_SETUP,
                path=Path("setup.md"),
                status=DocumentStatus.COMPLETED
            )
        ],
        Bucket.GENERATE_CORE_FUNCTIONALITY: [
            ArtifactMeta(
                name="Core Doc",
                bucket=Bucket.GENERATE_CORE_FUNCTIONALITY,
                path=Path("core.md"),
                status=DocumentStatus.PENDING
            )
        ]
    }

    with patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_REPOSITORY') as mock_repository:
        mock_repository.get_available_dimensions.return_value = list(MOCK_VALID_TAXONOMIES.keys())
        mock_repository.get_dimension_values.side_effect = lambda dim: MOCK_VALID_TAXONOMIES[dim]
        result = await verification.core_verification("test-project")
    
    assert result["status"] == "ok"
    assert "completion_percentage" in result
    assert result["mece_validation"]["is_valid"] == True
    assert result["taxonomy_structure"]["platform"] == "web-frontend"
    assert result["taxonomy_structure"]["lifecycle"] == "mvp"  # Check lifecycle is included
    mock_validate.assert_called_once_with(mock_project_memory)
    mock_adapter_instance.load_memory.assert_called_once_with("test-project")

# TODO: Add tests for project not found, DB adapter errors, coverage edge cases. 