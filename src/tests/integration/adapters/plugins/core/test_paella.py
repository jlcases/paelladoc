"""
Integration tests for the core.paella plugin.
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path
import uuid
from unittest.mock import AsyncMock, MagicMock

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Module to test
from paelladoc.adapters.plugins.core.paella import (
    core_paella,
    SupportedLanguage,
)

# Adapter for verification
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from paelladoc.domain.models.project import (
    ProjectMemory,
    Bucket,
)  # Import ProjectMemory and Bucket for verification

# --- Pytest Fixture for Temporary DB --- #


@pytest.fixture
async def memory_adapter():
    """Provides a SQLiteMemoryAdapter with a unique, temporary DB."""
    # Create a unique temporary database file path
    # Use /tmp for potentially better cross-platform compatibility/permissions
    test_db_name = f"test_paella_{uuid.uuid4()}.db"
    temp_dir = Path("/tmp") / "paelladoc_test_dbs_paella"
    temp_dir.mkdir(parents=True, exist_ok=True)
    test_db_path = temp_dir / test_db_name
    print(f"\nSetting up test with DB: {test_db_path}")

    adapter = SQLiteMemoryAdapter(db_path=test_db_path)
    await adapter._create_db_and_tables()  # Ensure tables exist

    yield adapter

    # Cleanup: remove the database file and directory if empty
    print(f"Tearing down test, removing DB: {test_db_path}")
    try:
        if test_db_path.exists():
            # Add small delay before deleting, might help with file locks
            await asyncio.sleep(0.05)
            os.remove(test_db_path)
            print(f"Removed DB: {test_db_path}")
        # Attempt to remove directory only if it's empty
        if temp_dir.exists() and not any(temp_dir.iterdir()):
            temp_dir.rmdir()
            print(f"Removed test directory: {temp_dir}")
        elif temp_dir.exists():
            print(f"Test directory not empty, not removing: {temp_dir}")
    except Exception as e:
        print(f"Error during cleanup: {e}")


# --- Test Cases --- #


@pytest.mark.asyncio
async def test_create_new_project_asks_for_base_path_and_saves_it(
    memory_adapter: SQLiteMemoryAdapter,
    monkeypatch,
):
    """
    Verify the interactive flow for creating a new project:
    1. Asks for interaction language.
    2. Lists projects (if any) and asks action (create new).
    3. Asks for documentation language.
    4. Asks for new project name (checks for existence).
    5. Asks for base path.
    6. Creates the project, saves absolute base path, saves initial memory.
    """
    print("\nRunning: test_create_new_project_asks_for_base_path_and_saves_it")

    interaction_lang = SupportedLanguage.EN_US
    doc_lang = SupportedLanguage.EN_US
    project_name = f"test-project-{uuid.uuid4()}"
    base_path_input = "./test_paella_docs_temp"  # Use a unique temp dir
    expected_abs_base_path = Path(base_path_input).expanduser().resolve()

    # --- Mocking and Patching --- #

    # 1. Mock list_projects to return empty initially
    mock_list_projects = AsyncMock(return_value=[])
    monkeypatch.setattr(memory_adapter, "list_projects", mock_list_projects)

    # 2. Mock project_exists to return False initially
    mock_project_exists = AsyncMock(return_value=False)
    monkeypatch.setattr(memory_adapter, "project_exists", mock_project_exists)

    # 3. Mock save_memory to just check it's called (optional, but good practice)
    mock_save_memory = AsyncMock()
    monkeypatch.setattr(memory_adapter, "save_memory", mock_save_memory)

    # 4. CRUCIAL: Patch the SQLiteMemoryAdapter class *within the core_paella module*
    #    to make core_paella use *our* test adapter instance.
    #    We create a mock class that returns our fixture adapter when called.
    MockAdapterClass = MagicMock(return_value=memory_adapter)
    monkeypatch.setattr(
        "paelladoc.adapters.plugins.core.paella.SQLiteMemoryAdapter", MockAdapterClass
    )

    # --- Simulate the conversation step-by-step --- #

    # Initial call -> asks for interaction language
    response1 = await core_paella()
    print(f"Response 1: {response1}")
    assert response1["status"] == "input_needed"
    assert response1["next_param"] == "interaction_language"
    assert response1["halt"] is True

    # Provide interaction language -> asks for action (listing projects)
    response2 = await core_paella(interaction_language=interaction_lang)
    print(f"Response 2: {response2}")
    assert response2["status"] == "input_needed"
    assert response2["next_param"] == "action"
    assert response2["halt"] is True
    mock_list_projects.assert_called_once()  # Verify list_projects was called

    # Provide action 'create_new' -> asks for documentation language
    response3 = await core_paella(
        interaction_language=interaction_lang, action="create_new"
    )
    print(f"Response 3: {response3}")
    assert response3["status"] == "input_needed"
    assert response3["next_param"] == "documentation_language"
    assert response3["halt"] is True

    # Provide documentation language -> asks for new project name
    response4 = await core_paella(
        interaction_language=interaction_lang,
        action="create_new",
        documentation_language=doc_lang,
    )
    print(f"Response 4: {response4}")
    assert response4["status"] == "input_needed"
    assert response4["next_param"] == "new_project_name"
    assert response4["halt"] is True

    # Provide new project name -> Checks existence, then asks for base_path
    response5 = await core_paella(
        interaction_language=interaction_lang,
        action="create_new",
        documentation_language=doc_lang,
        new_project_name=project_name,
    )
    print(f"Response 5: {response5}")
    mock_project_exists.assert_called_once_with(project_name)  # Verify check
    assert response5["status"] == "input_needed", (
        f"Expected input_needed, got {response5.get('status')}"
    )
    assert response5["next_param"] == "base_path", (
        f"Expected next_param base_path, got {response5.get('next_param')}"
    )
    assert response5["halt"] is True, "Expected halt=True when asking for base_path"
    assert "path" in response5.get("message", "").lower(), "Message should ask for path"

    # Provide base_path -> SHOULD succeed and save
    response6 = await core_paella(
        interaction_language=interaction_lang,
        action="create_new",
        documentation_language=doc_lang,
        new_project_name=project_name,
        base_path=base_path_input,
    )
    print(f"Response 6: {response6}")
    assert response6["status"] == "ok", (
        f"Expected status ok, got {response6.get('status')}: {response6.get('message')}"
    )
    assert response6.get("project_name") == project_name
    assert Path(response6.get("base_path")) == expected_abs_base_path

    # --- Verification --- #
    # Check that save_memory was called correctly
    mock_save_memory.assert_called_once()
    # Inspect the arguments passed to save_memory
    saved_memory_arg: ProjectMemory = mock_save_memory.call_args[0][0]

    assert isinstance(saved_memory_arg, ProjectMemory)
    assert saved_memory_arg.metadata.name == project_name
    assert saved_memory_arg.metadata.interaction_language == interaction_lang
    assert saved_memory_arg.metadata.documentation_language == doc_lang
    assert saved_memory_arg.metadata.base_path == expected_abs_base_path
    assert len(saved_memory_arg.artifacts[Bucket.INITIATE_INITIAL_PRODUCT_DOCS]) == 1
    initial_artifact = saved_memory_arg.artifacts[Bucket.INITIATE_INITIAL_PRODUCT_DOCS][
        0
    ]
    assert "charter" in initial_artifact.name.lower()

    # Optional: Clean up the created directory if needed (though Path might handle it)
    if expected_abs_base_path.exists():
        try:
            # Remove files first if any were created (though unlikely in this test)
            for item in expected_abs_base_path.iterdir():
                item.unlink()
            expected_abs_base_path.rmdir()
            print(f"Cleaned up created base path: {expected_abs_base_path}")
        except Exception as e:
            print(
                f"Warning: Could not clean up base path {expected_abs_base_path}: {e}"
            )
