"""
Integration tests for project CRUD operations.
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path
import uuid
from typing import Dict, Any

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

from paelladoc.domain.models.language import SupportedLanguage
from paelladoc.adapters.plugins.core.paella import paella_init, paella_list
from paelladoc.adapters.plugins.core.project_crud import (
    update_project,
    delete_project,
    get_project,
)
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from paelladoc.adapters.plugins.core.project_utils import (
    validate_project_updates,
    format_project_info,
)

# --- Test Fixtures --- #


@pytest.fixture(scope="function")
async def memory_adapter():
    """Provides an initialized SQLiteMemoryAdapter with a temporary DB."""
    test_db_name = f"test_crud_{uuid.uuid4()}.db"
    test_dir = Path(__file__).parent / "temp_dbs"
    test_db_path = test_dir / test_db_name
    test_db_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"\nSetting up test with DB: {test_db_path}")

    adapter = SQLiteMemoryAdapter(db_path=test_db_path)
    await adapter._create_db_and_tables()

    yield adapter

    print(f"Tearing down test, removing DB: {test_db_path}")
    await asyncio.sleep(0.01)  # Brief pause for file lock release
    try:
        if test_db_path.exists():
            os.remove(test_db_path)
            print(f"Removed DB: {test_db_path}")
        try:
            test_db_path.parent.rmdir()
            print(f"Removed test directory: {test_db_path.parent}")
        except OSError:
            pass  # Directory not empty
    except Exception as e:
        print(f"Error during teardown removing {test_db_path}: {e}")


@pytest.fixture
async def test_project(memory_adapter, monkeypatch) -> Dict[str, Any]:
    """Creates a test project and returns its details."""
    # Patch get_db_path to use our test DB
    monkeypatch.setattr(
        "paelladoc.adapters.output.sqlite.sqlite_memory_adapter.get_db_path",
        lambda: memory_adapter.db_path,
    )

    project_name = f"test-project-{uuid.uuid4()}"
    base_path = f"./test_projects/{project_name}"

    # Create project
    result = await paella_init(
        base_path=base_path,
        documentation_language=SupportedLanguage.EN_US.value,
        interaction_language=SupportedLanguage.EN_US.value,
        new_project_name=project_name,
        platform_taxonomy="test_platform",
        domain_taxonomy="test_domain",
        size_taxonomy="test_size",
        compliance_taxonomy="test_compliance",
        lifecycle_taxonomy="test_lifecycle",
    )

    assert result["status"] == "ok"

    # Clean up base_path after test
    yield {
        "name": project_name,
        "base_path": base_path,
        "abs_base_path": str(Path(base_path).resolve()),
    }

    if Path(base_path).exists():
        import shutil

        shutil.rmtree(Path(base_path))


# --- Test Cases --- #


@pytest.mark.asyncio
async def test_get_project_returns_correct_info(test_project):
    """Test that get_project returns the correct project information."""
    result = await get_project(project_name=test_project["name"])

    assert result["status"] == "ok"
    assert result["project"]["name"] == test_project["name"]
    assert result["project"]["base_path"] == test_project["abs_base_path"]


@pytest.mark.asyncio
async def test_get_project_returns_error_for_nonexistent_project():
    """Test that get_project handles nonexistent projects correctly."""
    result = await get_project(project_name="nonexistent-project")

    assert result["status"] == "error"
    assert "not found" in result["message"].lower()


@pytest.mark.asyncio
async def test_update_project_modifies_specific_fields(test_project):
    """Test that update_project can modify specific fields."""
    new_purpose = "Updated project purpose"
    new_target_audience = "Updated target audience"

    result = await update_project(
        project_name=test_project["name"],
        updates={
            "purpose": new_purpose,
            "target_audience": new_target_audience,
        },
    )

    assert result["status"] == "ok"

    # Verify changes
    get_result = await get_project(project_name=test_project["name"])
    assert get_result["project"]["purpose"] == new_purpose
    assert get_result["project"]["target_audience"] == new_target_audience


@pytest.mark.asyncio
async def test_update_project_validates_fields(test_project):
    """Test that update_project validates field values."""
    result = await update_project(
        project_name=test_project["name"],
        updates={
            "documentation_language": "invalid_language",
        },
    )

    assert result["status"] == "error"
    assert "invalid" in result["message"].lower()


@pytest.mark.asyncio
async def test_update_project_validates_multiple_fields(test_project):
    """Test that update_project validates multiple fields correctly."""
    result = await update_project(
        project_name=test_project["name"],
        updates={
            "documentation_language": "invalid_lang",
            "interaction_language": "bad_lang",
            "name": "",  # Empty name
        },
    )

    assert result["status"] == "error"
    assert "validation failed" in result["message"].lower()
    assert "documentation_language" in result["message"].lower()
    assert "interaction_language" in result["message"].lower()
    assert "name" in result["message"].lower()


@pytest.mark.asyncio
async def test_delete_project_removes_project_and_files(test_project):
    """Test that delete_project removes both DB entry and files."""
    # First verify project exists
    list_result = await paella_list()
    assert any(p.name == test_project["name"] for p in list_result["projects"])

    # Delete project
    result = await delete_project(
        project_name=test_project["name"],
        confirm=True,
    )

    assert result["status"] == "ok"

    # Verify project is gone from DB
    list_result = await paella_list()
    assert not any(p.name == test_project["name"] for p in list_result["projects"])

    # Verify files are gone
    assert not Path(test_project["base_path"]).exists()


@pytest.mark.asyncio
async def test_delete_project_requires_confirmation(test_project):
    """Test that delete_project requires explicit confirmation."""
    result = await delete_project(
        project_name=test_project["name"],
        confirm=False,
    )

    assert result["status"] == "error"
    assert "confirmation required" in result["message"].lower()

    # Verify project still exists
    list_result = await paella_list()
    assert any(p.name == test_project["name"] for p in list_result["projects"])


@pytest.mark.asyncio
async def test_delete_project_creates_backup(test_project):
    """Test that delete_project creates a backup before deletion."""
    result = await delete_project(
        project_name=test_project["name"],
        confirm=True,
        create_backup=True,
    )

    assert result["status"] == "ok"
    assert "backup_path" in result
    assert Path(result["backup_path"]).exists()

    # Clean up backup
    if Path(result["backup_path"]).exists():
        os.remove(result["backup_path"])


# --- Utility Function Tests --- #


def test_validate_project_updates_checks_languages():
    """Test that validate_project_updates validates language fields."""
    updates = {
        "documentation_language": "invalid",
        "interaction_language": "bad",
    }

    errors = validate_project_updates(updates)
    assert len(errors) == 2
    assert any("documentation_language" in e.lower() for e in errors)
    assert any("interaction_language" in e.lower() for e in errors)


def test_validate_project_updates_checks_base_path():
    """Test that validate_project_updates validates base_path."""
    updates = {"base_path": ""}
    errors = validate_project_updates(updates)
    assert len(errors) == 1
    assert "base_path" in errors[0].lower()


def test_format_project_info_converts_paths():
    """Test that format_project_info converts Path objects to strings."""
    test_path = Path("/test/path")
    info = {
        "base_path": test_path,
        "other_path": test_path,
        "normal_field": "value",
    }

    formatted = format_project_info(info)
    assert isinstance(formatted["base_path"], str)
    assert isinstance(formatted["other_path"], str)
    assert formatted["base_path"] == str(test_path)
    assert formatted["normal_field"] == "value"
