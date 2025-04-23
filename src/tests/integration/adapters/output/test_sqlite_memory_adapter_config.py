"""Integration tests for SQLite adapter configuration."""

import os
import pytest
import asyncio
from pathlib import Path
import uuid

from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
)


@pytest.fixture
def clean_env():
    """Remove relevant environment variables before each test."""
    original_db_path = os.environ.get("PAELLADOC_DB_PATH")
    original_env = os.environ.get("PAELLADOC_ENV")

    if "PAELLADOC_DB_PATH" in os.environ:
        del os.environ["PAELLADOC_DB_PATH"]
    if "PAELLADOC_ENV" in os.environ:
        del os.environ["PAELLADOC_ENV"]

    yield

    if original_db_path is not None:
        os.environ["PAELLADOC_DB_PATH"] = original_db_path
    if original_env is not None:
        os.environ["PAELLADOC_ENV"] = original_env


@pytest.fixture
async def temp_adapter():
    """Create a temporary adapter with a unique database."""
    test_db_name = f"test_config_{uuid.uuid4()}.db"
    test_dir = Path(__file__).parent / "temp_dbs"
    test_db_path = test_dir / test_db_name
    test_db_path.parent.mkdir(parents=True, exist_ok=True)

    adapter = SQLiteMemoryAdapter(db_path=test_db_path)
    await adapter._create_db_and_tables()

    yield adapter

    # Cleanup
    await asyncio.sleep(0.01)  # Brief pause for file lock release
    try:
        if test_db_path.exists():
            os.remove(test_db_path)
        test_db_path.parent.rmdir()
    except Exception as e:
        print(f"Error during cleanup: {e}")


@pytest.mark.asyncio
async def test_adapter_uses_custom_path(clean_env):
    """Verify adapter uses the path provided in __init__."""
    custom_path = create_temp_db_path()
    adapter = SQLiteMemoryAdapter(db_path=custom_path)
    assert adapter.db_path == custom_path
    # Clean up the test file if it was created
    if custom_path.exists():
        os.remove(custom_path)


@pytest.mark.asyncio
async def test_adapter_uses_env_var_path(clean_env):
    """Verify adapter uses PAELLADOC_DB_PATH environment variable if set."""
    env_path = create_temp_db_path()
    os.environ["PAELLADOC_DB_PATH"] = str(env_path)
    adapter = SQLiteMemoryAdapter()  # No path given, should use env var
    assert adapter.db_path == env_path
    if env_path.exists():
        os.remove(env_path)


@pytest.mark.asyncio
async def test_adapter_uses_production_path(clean_env):
    """Verify adapter uses PRODUCTION_DB_PATH by default."""
    # Ensure no env vars are set that override the default
    os.environ.pop("PAELLADOC_DB_PATH", None)
    os.environ.pop("PAELLADOC_ENV", None)
    adapter = SQLiteMemoryAdapter()
    expected_path = Path.home() / ".paelladoc" / "memory.db"  # Get default directly
    assert adapter.db_path == expected_path


@pytest.mark.asyncio
async def test_adapter_creates_parent_directory(clean_env):
    """Verify the adapter ensures the parent directory for the DB exists."""
    test_subdir = Path.home() / ".paelladoc_test_dir" / str(uuid.uuid4())
    custom_path = test_subdir / "test_creation.db"
    # Ensure the directory does not exist initially
    if test_subdir.exists():
        for item in test_subdir.iterdir():  # Clear if exists
            os.remove(item)
        os.rmdir(test_subdir)

    assert not test_subdir.exists()

    # The adapter instantiation triggers the directory creation
    _ = SQLiteMemoryAdapter(db_path=custom_path)  # Assign to _ as intentionally unused
    # Initialization should create the parent directory
    assert test_subdir.exists()
    assert test_subdir.is_dir()

    # Clean up
    if custom_path.exists():
        os.remove(custom_path)
    if test_subdir.exists():
        os.rmdir(test_subdir)


@pytest.mark.asyncio
async def test_adapter_operations_with_custom_path(temp_adapter):
    """Test basic adapter operations with custom path."""
    # Create test project
    project = ProjectMemory(
        project_info=ProjectInfo(
            name=f"test-project-{uuid.uuid4()}",
            language="python",  # This might need updating if language model changed
            purpose="Test project",
            target_audience="Developers",
            objectives=["Test database configuration"],
            # Add required taxonomy fields
            platform_taxonomy="test_platform",
            domain_taxonomy="test_domain",
            size_taxonomy="test_size",
            compliance_taxonomy="test_compliance",
            lifecycle_taxonomy="test_lifecycle",
        ),
        # Add required taxonomy fields also directly to ProjectMemory
        platform_taxonomy="test_platform",
        domain_taxonomy="test_domain",
        size_taxonomy="test_size",
        compliance_taxonomy="test_compliance",
        lifecycle_taxonomy="test_lifecycle",
    )

    # Test operations
    await temp_adapter.save_memory(project)
    assert await temp_adapter.project_exists(project.project_info.name)

    loaded = await temp_adapter.load_memory(project.project_info.name)
    assert loaded is not None
    assert loaded.project_info.name == project.project_info.name

    projects_info = await temp_adapter.list_projects()
    # Extract names from the returned ProjectInfo objects
    project_names = [info.name for info in projects_info]
    assert project.project_info.name in project_names


# Helper function to create a unique temporary DB path
def create_temp_db_path(prefix="test_adapter_config") -> Path:
    test_db_name = f"{prefix}_{uuid.uuid4()}.db"
    # Use /tmp or a similar temporary directory standard across systems
    test_db_path = Path("/tmp") / test_db_name
    # test_db_path.parent.mkdir(parents=True, exist_ok=True) # /tmp should exist
    print(f"\nGenerated temporary DB path: {test_db_path}")
    return test_db_path
