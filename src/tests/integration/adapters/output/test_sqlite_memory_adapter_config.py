"""Integration tests for SQLite adapter configuration."""

import os
import pytest
import asyncio
from pathlib import Path
import uuid

from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from paelladoc.config.database import DEVELOPMENT_DB_PATH, PRODUCTION_DB_PATH
from paelladoc.domain.models.project import ProjectMemory, ProjectMetadata


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
async def test_adapter_uses_custom_path():
    """Test that adapter uses custom path when provided."""
    custom_path = Path("/tmp/custom_test.db")
    adapter = SQLiteMemoryAdapter(db_path=custom_path)
    assert adapter.db_path == custom_path


@pytest.mark.asyncio
async def test_adapter_uses_env_var_path(clean_env):
    """Test that adapter uses PAELLADOC_DB_PATH when set."""
    custom_path = "/tmp/env_test.db"
    os.environ["PAELLADOC_DB_PATH"] = custom_path
    adapter = SQLiteMemoryAdapter()
    assert str(adapter.db_path) == custom_path


@pytest.mark.asyncio
async def test_adapter_uses_development_path(clean_env):
    """Test that adapter uses development path in development mode."""
    os.environ["PAELLADOC_ENV"] = "development"
    adapter = SQLiteMemoryAdapter()
    assert adapter.db_path == DEVELOPMENT_DB_PATH


@pytest.mark.asyncio
async def test_adapter_uses_production_path(clean_env):
    """Test that adapter uses production path by default."""
    adapter = SQLiteMemoryAdapter()
    assert adapter.db_path == PRODUCTION_DB_PATH


@pytest.mark.asyncio
async def test_adapter_creates_parent_directory():
    """Test that adapter creates parent directory if it doesn't exist."""
    test_dir = Path("/tmp/paelladoc_test") / str(uuid.uuid4())
    test_path = test_dir / "test.db"

    # The adapter instantiation triggers the directory creation
    _ = SQLiteMemoryAdapter(
        db_path=test_path
    )  # Assign to _ to indicate intentional non-use
    # adapter = SQLiteMemoryAdapter(db_path=test_path)
    assert test_dir.exists()
    assert test_dir.is_dir()

    # Cleanup
    test_dir.rmdir()


@pytest.mark.asyncio
async def test_adapter_operations_with_custom_path(temp_adapter):
    """Test basic adapter operations with custom path."""
    # Create test project
    project = ProjectMemory(
        metadata=ProjectMetadata(
            name=f"test-project-{uuid.uuid4()}",
            language="python",
            purpose="Test project",
            target_audience="Developers",
            objectives=["Test database configuration"],
        )
    )

    # Test operations
    await temp_adapter.save_memory(project)
    assert await temp_adapter.project_exists(project.metadata.name)

    loaded = await temp_adapter.load_memory(project.metadata.name)
    assert loaded is not None
    assert loaded.metadata.name == project.metadata.name

    projects = await temp_adapter.list_projects()
    assert project.metadata.name in projects
