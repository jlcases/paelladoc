import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4

# Modules to test
from paelladoc.adapters.plugins.core import verification
from paelladoc.domain.models.project import ProjectMemory, Metadata, DocumentStatus, Bucket

# Mock data
MOCK_VALID_TAXONOMIES = {
    "platform": ["ios-native", "web-frontend"],
    "domain": ["ecommerce", "ai-ml"],
    "size": ["personal", "enterprise"],
    "compliance": ["gdpr"]
}

# --- Tests for validate_mece_structure --- 

@pytest.fixture
def mock_project_memory() -> ProjectMemory:
    """Creates a mock ProjectMemory object."""
    metadata = Metadata(name="test-project", base_path="/fake/path", taxonomy_version="1.0")
    memory = ProjectMemory(metadata=metadata)
    # Set default valid taxonomies for most tests
    memory.platform_taxonomy = "web-frontend"
    memory.domain_taxonomy = "ecommerce"
    memory.size_taxonomy = "enterprise"
    memory.compliance_taxonomy = "gdpr"
    return memory

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_PROVIDER')
def test_validate_mece_valid(mock_provider, mock_project_memory):
    """Test validation with a valid MECE structure."""
    mock_provider.get_available_taxonomies.return_value = MOCK_VALID_TAXONOMIES
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == True
    assert not result["missing_dimensions"]
    assert not result["invalid_combinations"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_PROVIDER')
def test_validate_mece_missing_dimension(mock_provider, mock_project_memory):
    """Test validation when a required dimension is missing."""
    mock_provider.get_available_taxonomies.return_value = MOCK_VALID_TAXONOMIES
    mock_project_memory.domain_taxonomy = None  # Missing domain
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == False
    assert "domain" in result["missing_dimensions"]
    assert not result["invalid_combinations"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_PROVIDER')
def test_validate_mece_invalid_value(mock_provider, mock_project_memory):
    """Test validation with an invalid taxonomy value for a dimension."""
    mock_provider.get_available_taxonomies.return_value = MOCK_VALID_TAXONOMIES
    mock_project_memory.platform_taxonomy = "invalid-platform" # Invalid platform
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == False
    assert not result["missing_dimensions"]
    assert "Invalid platform taxonomy: invalid-platform" in result["invalid_combinations"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_PROVIDER')
def test_validate_mece_invalid_optional_compliance(mock_provider, mock_project_memory):
    """Test validation with an invalid optional compliance value."""
    mock_provider.get_available_taxonomies.return_value = MOCK_VALID_TAXONOMIES
    mock_project_memory.compliance_taxonomy = "invalid-compliance"
    result = verification.validate_mece_structure(mock_project_memory)
    # Should still be technically valid, but have an invalid combination listed
    assert result["is_valid"] == False # An invalid value makes it invalid overall
    assert "Invalid compliance taxonomy: invalid-compliance" in result["invalid_combinations"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_PROVIDER')
def test_validate_mece_no_compliance(mock_provider, mock_project_memory):
    """Test validation when optional compliance is not provided."""
    mock_provider.get_available_taxonomies.return_value = MOCK_VALID_TAXONOMIES
    mock_project_memory.compliance_taxonomy = None
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == True
    assert not result["invalid_combinations"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_PROVIDER')
def test_validate_mece_warning_combination(mock_provider, mock_project_memory):
    """Test validation warning for specific disallowed combinations (e.g., mobile+cms)."""
    mock_provider.get_available_taxonomies.return_value = {
        **MOCK_VALID_TAXONOMIES,
         "platform": ["ios-native", "web-frontend"],
         "domain": ["cms", "ecommerce"]
         }
    mock_project_memory.platform_taxonomy = "ios-native"
    mock_project_memory.domain_taxonomy = "cms"
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == True # Warnings don't make it invalid
    assert "Mobile platforms rarely implement full CMS functionality" in result["warnings"]

@patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_PROVIDER')
def test_validate_mece_provider_error(mock_provider, mock_project_memory, caplog):
    """Test validation when the taxonomy provider fails."""
    mock_provider.get_available_taxonomies.side_effect = Exception("Provider error")
    result = verification.validate_mece_structure(mock_project_memory)
    assert result["is_valid"] == False
    assert "Could not load taxonomy definitions for validation." in result["warnings"]
    assert "Failed to load taxonomies for validation" in caplog.text

# --- Tests for core_verification (Higher Level) ---
# Basic tests, more comprehensive ones would mock the DB adapter too

@pytest.mark.asyncio
@patch('paelladoc.adapters.plugins.core.verification.validate_mece_structure')
@patch('paelladoc.adapters.plugins.core.verification.SQLiteMemoryAdapter')
async def test_core_verification_invalid_mece(mock_adapter_cls, mock_validate, mock_project_memory):
    """Test core_verification returns error if MECE validation fails."""
    # Mock the adapter instance and its load_memory method
    mock_adapter_instance = MagicMock()
    mock_adapter_instance.load_memory.return_value = mock_project_memory
    mock_adapter_cls.return_value = mock_adapter_instance
    
    # Mock MECE validation to return invalid
    mock_validate.return_value = {"is_valid": False, "reason": "Test invalid MECE"}
    
    result = await verification.core_verification("test-project")
    
    assert result["status"] == "error"
    assert result["message"] == "Invalid MECE taxonomy structure"
    assert result["validation"] == {"is_valid": False, "reason": "Test invalid MECE"}
    mock_validate.assert_called_once_with(mock_project_memory)
    mock_adapter_instance.load_memory.assert_called_once_with("test-project")

@pytest.mark.asyncio
@patch('paelladoc.adapters.plugins.core.verification.validate_mece_structure')
@patch('paelladoc.adapters.plugins.core.verification.SQLiteMemoryAdapter')
async def test_core_verification_valid_mece_calculates_coverage(mock_adapter_cls, mock_validate, mock_project_memory):
    """Test core_verification proceeds to coverage calculation if MECE is valid."""
    # Mock the adapter instance and its load_memory method
    mock_adapter_instance = MagicMock()
    mock_adapter_instance.load_memory.return_value = mock_project_memory
    mock_adapter_cls.return_value = mock_adapter_instance
    
    # Mock MECE validation to return valid
    mock_validate.return_value = {"is_valid": True}
    
    # Add some artifacts for coverage calculation
    # (Simplified - real test might need more detailed artifacts)
    mock_project_memory.artifacts = { 
        Bucket.INITIATE_CORE_SETUP: [MagicMock(status=DocumentStatus.COMPLETED)],
        Bucket.GENERATE_CORE_FUNCTIONALITY: [MagicMock(status=DocumentStatus.PENDING)]
    }

    # Use the actual provider for this test
    with patch('paelladoc.adapters.plugins.core.verification.TAXONOMY_PROVIDER') as mock_provider:
        mock_provider.get_available_taxonomies.return_value = MOCK_VALID_TAXONOMIES
        result = await verification.core_verification("test-project")
    
    assert result["status"] == "ok"
    assert "completion_percentage" in result
    assert result["mece_validation"] == {"is_valid": True}
    assert result["taxonomy_structure"]["platform"] == "web-frontend"
    mock_validate.assert_called_once_with(mock_project_memory)
    mock_adapter_instance.load_memory.assert_called_once_with("test-project")

# TODO: Add tests for project not found, DB adapter errors, coverage edge cases. 