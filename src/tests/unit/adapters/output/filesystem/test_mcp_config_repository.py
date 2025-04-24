"""Unit tests for FileSystemMCPConfigRepository."""

import pytest
from pathlib import Path
import json
from typing import Dict

from paelladoc.adapters.output.filesystem.mcp_config_repository import (
    FileSystemMCPConfigRepository,
)


@pytest.fixture
def mock_config_dir(tmp_path: Path) -> Path:
    """Create a temporary directory with mock MCP config."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def mock_mcp_config(mock_config_dir: Path) -> Dict:
    """Create a mock MCP configuration file."""
    config = {
        "version": "1.0",
        "mcp_configuration": {
            "core": {
                "enabled": True,
                "linked_taxonomies": ["Initiate::CoreSetup"],
                "tools": ["core_help", "paella_init"],
            },
            "product": {
                "enabled": True,
                "linked_taxonomies": ["Elaborate::SpecificationAndPlanning"],
                "tools": ["core_manage_story", "core_manage_task"],
            },
            "disabled_mcp": {
                "enabled": False,
                "linked_taxonomies": ["Test::Disabled"],
                "tools": ["should_not_appear"],
            },
        },
    }

    config_file = mock_config_dir / "mcp_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f)
    return config


@pytest.fixture
def repository(monkeypatch, mock_config_dir: Path) -> FileSystemMCPConfigRepository:
    """Create a repository instance with mocked config path."""
    repo = FileSystemMCPConfigRepository()
    monkeypatch.setattr(repo, "config_path", mock_config_dir / "mcp_config.json")
    return repo


@pytest.mark.asyncio
async def test_get_available_mcps(
    repository: FileSystemMCPConfigRepository, mock_mcp_config: Dict
):
    """Test that only enabled MCPs are returned."""
    mcps = await repository.get_available_mcps()
    assert len(mcps) == 2
    assert "core" in mcps
    assert "product" in mcps
    assert "disabled_mcp" not in mcps


@pytest.mark.asyncio
async def test_get_mcp_config(
    repository: FileSystemMCPConfigRepository, mock_mcp_config: Dict
):
    """Test retrieving specific MCP configuration."""
    config = await repository.get_mcp_config("core")
    assert config is not None
    assert config["enabled"] is True
    assert "core_help" in config["tools"]


@pytest.mark.asyncio
async def test_get_tools_for_taxonomy(
    repository: FileSystemMCPConfigRepository, mock_mcp_config: Dict
):
    """Test getting tools for a specific taxonomy bucket."""
    tools = await repository.get_tools_for_taxonomy("Initiate::CoreSetup")
    assert len(tools) == 2
    assert "core_help" in tools
    assert "paella_init" in tools


@pytest.mark.asyncio
async def test_get_enabled_mcps_for_project(
    repository: FileSystemMCPConfigRepository, mock_mcp_config: Dict
):
    """Test getting enabled MCPs based on project buckets."""
    mcps = await repository.get_enabled_mcps_for_project(
        ["Initiate::CoreSetup", "Elaborate::SpecificationAndPlanning"]
    )
    assert len(mcps) == 2
    assert "core" in mcps
    assert "product" in mcps


@pytest.mark.asyncio
async def test_no_config_file(repository: FileSystemMCPConfigRepository):
    """Test behavior when config file doesn't exist."""
    if repository.config_path.exists():
        repository.config_path.unlink()

    mcps = await repository.get_available_mcps()
    assert len(mcps) == 0


@pytest.mark.asyncio
async def test_invalid_config_file(
    repository: FileSystemMCPConfigRepository, mock_config_dir: Path
):
    """Test behavior with invalid JSON in config file."""
    with open(repository.config_path, "w") as f:
        f.write("invalid json")

    mcps = await repository.get_available_mcps()
    assert len(mcps) == 0


@pytest.mark.asyncio
async def test_cache_behavior(
    repository: FileSystemMCPConfigRepository, mock_mcp_config: Dict
):
    """Test that configuration is properly cached."""
    # First call should read from file
    mcps1 = await repository.get_available_mcps()

    # Delete the file
    repository.config_path.unlink()

    # Second call should use cache
    mcps2 = await repository.get_available_mcps()

    assert mcps1 == mcps2
