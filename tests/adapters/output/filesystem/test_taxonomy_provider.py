import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from paelladoc.adapters.output.filesystem.taxonomy_provider import FileSystemTaxonomyProvider

# Helper function to create dummy taxonomy files
def create_dummy_taxonomies(base_path: Path, structure: dict):
    for category, files in structure.items():
        cat_path = base_path / category
        cat_path.mkdir(parents=True, exist_ok=True)
        for file_name in files:
            (cat_path / f"{file_name}.json").touch()

@pytest.fixture
def mock_taxonomy_structure(tmp_path: Path) -> Path:
    """Creates a temporary directory structure mimicking the taxonomies folder."""
    tax_base = tmp_path / "taxonomies"
    structure = {
        "platform": ["ios-native", "web-frontend"],
        "domain": ["ecommerce", "ai-ml"],
        "size": ["personal", "enterprise"],
        "compliance": ["gdpr"]
        # Intentionally leave one category empty
        # "other": [] 
    }
    create_dummy_taxonomies(tax_base, structure)
    # Create an empty category dir
    (tax_base / "empty_cat").mkdir()
    return tax_base

def test_load_valid_taxonomies(mock_taxonomy_structure: Path):
    """Test loading taxonomies from a valid structure."""
    provider = FileSystemTaxonomyProvider(base_path=mock_taxonomy_structure)
    taxonomies = provider.get_available_taxonomies()

    assert "platform" in taxonomies
    assert sorted(taxonomies["platform"]) == ["ios-native", "web-frontend"]
    assert "domain" in taxonomies
    assert sorted(taxonomies["domain"]) == ["ai-ml", "ecommerce"]
    assert "size" in taxonomies
    assert sorted(taxonomies["size"]) == ["enterprise", "personal"]
    assert "compliance" in taxonomies
    assert sorted(taxonomies["compliance"]) == ["gdpr"]
    # Check for standard categories even if dir doesn't exist or is empty
    assert "empty_cat" not in taxonomies # Should only include known categories

def test_load_taxonomies_uses_cache(mock_taxonomy_structure: Path):
    """Test that subsequent calls use the cache."""
    provider = FileSystemTaxonomyProvider(base_path=mock_taxonomy_structure)
    
    # Mock the Path.glob method to see if it's called again
    with patch.object(Path, 'glob', wraps=Path.glob) as mock_glob:
        # First call - should scan
        taxonomies1 = provider.get_available_taxonomies()
        assert mock_glob.called # Should have been called
        call_count1 = mock_glob.call_count
        
        # Second call - should use cache
        taxonomies2 = provider.get_available_taxonomies()
        # The call count should NOT have increased
        assert mock_glob.call_count == call_count1 
        
        assert taxonomies1 == taxonomies2

def test_load_taxonomies_missing_base_path(tmp_path: Path):
    """Test behavior when the base taxonomy directory does not exist."""
    missing_path = tmp_path / "non_existent_taxonomies"
    provider = FileSystemTaxonomyProvider(base_path=missing_path)
    taxonomies = provider.get_available_taxonomies()

    # Should return empty lists for all standard categories
    assert taxonomies == {"platform": [], "domain": [], "size": [], "compliance": []}

def test_load_taxonomies_missing_category_dir(mock_taxonomy_structure: Path):
    """Test behavior when a specific category directory is missing."""
    # Remove the 'domain' directory from the mocked structure
    domain_path = mock_taxonomy_structure / "domain"
    if domain_path.exists():
        import shutil
        shutil.rmtree(domain_path)
        
    provider = FileSystemTaxonomyProvider(base_path=mock_taxonomy_structure)
     # Clear cache if exists from previous tests in the same object instance (if fixture scope allows)
    provider._cached_taxonomies = None 
    taxonomies = provider.get_available_taxonomies()

    assert "domain" in taxonomies
    assert taxonomies["domain"] == [] # Domain should be empty
    assert taxonomies["platform"] # Other categories should still load

def test_load_taxonomies_empty_category_dir(mock_taxonomy_structure: Path):
    """Test behavior when a category directory exists but is empty."""
    empty_cat_path = mock_taxonomy_structure / "platform"
    # Clear the platform directory
    for item in empty_cat_path.iterdir():
        item.unlink()

    provider = FileSystemTaxonomyProvider(base_path=mock_taxonomy_structure)
    provider._cached_taxonomies = None # Clear cache
    taxonomies = provider.get_available_taxonomies()
    
    assert "platform" in taxonomies
    assert taxonomies["platform"] == [] # Platform should now be empty
    assert taxonomies["domain"] # Domain should still have items

# Optional: Test error handling during file scanning if needed
# def test_load_taxonomies_os_error(mock_taxonomy_structure: Path, caplog):
#     """Test handling of OSError during glob."""
#     with patch.object(Path, 'glob', side_effect=OSError("Test OS error")):
#         provider = FileSystemTaxonomyProvider(base_path=mock_taxonomy_structure)
#         taxonomies = provider.get_available_taxonomies()
#         assert taxonomies == {"platform": [], "domain": [], "size": [], "compliance": []}
#         assert "Error reading taxonomy directory" in caplog.text 