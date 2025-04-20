"""
Integration tests for the core.paella plugin.
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path
import uuid
from typing import Optional

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Module to test
from paelladoc.adapters.plugins.core.paella import core_paella, SupportedLanguage

# Adapter for verification
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from paelladoc.domain.models.project import (
    ProjectMemory,
)  # Import ProjectMemory for verification

# --- Pytest Fixture for Temporary DB --- #


@pytest.fixture(scope="function")  # Recreate DB for each test function
async def memory_adapter():
    """Provides an initialized SQLiteMemoryAdapter with a temporary DB."""
    test_db_name = f"test_paella_{uuid.uuid4()}.db"
    # Store temp dbs inside the test directory for easier cleanup?
    test_dir = Path(__file__).parent / "temp_dbs"
    test_db_path = test_dir / test_db_name
    test_db_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"\nSetting up test with DB: {test_db_path}")

    adapter = SQLiteMemoryAdapter(db_path=test_db_path)
    await adapter._create_db_and_tables()

    yield adapter  # Provide the adapter to the test function

    # Teardown: clean up the database
    print(f"Tearing down test, removing DB: {test_db_path}")
    # Dispose engine if needed (optional, depends on connection handling)
    # await adapter.async_engine.dispose()
    await asyncio.sleep(0.01)  # Brief pause for file lock release
    try:
        if test_db_path.exists():
            os.remove(test_db_path)
            print(f"Removed DB: {test_db_path}")
        # Attempt to remove the directory if it's empty
        try:
            test_db_path.parent.rmdir()
            print(f"Removed test directory: {test_db_path.parent}")
        except OSError:
            pass  # Directory not empty, likely other tests running concurrently
    except Exception as e:
        print(f"Error during teardown removing {test_db_path}: {e}")


# --- Test Cases --- #


@pytest.mark.asyncio
async def test_create_new_project_asks_for_base_path_and_saves_it(
    memory_adapter: SQLiteMemoryAdapter,
):
    """
    Verify the interactive flow for creating a new project:
    1. Asks for interaction language.
    2. Asks action (create new).
    3. Asks for documentation language.
    4. Asks for new project name.
    5. **Asks for base path.** <-- Test focus
    6. Creates the project and saves the absolute base path in metadata.
    """
    print("\nRunning: test_create_new_project_asks_for_base_path_and_saves_it")

    interaction_lang = SupportedLanguage.EN_US
    doc_lang = SupportedLanguage.EN_US
    project_name = f"test-project-{uuid.uuid4()}"
    base_path_input = "./test_paella_docs"  # Relative path input
    expected_abs_base_path = Path(base_path_input).resolve()

    # Simulate the conversation step-by-step

    # Initial call -> asks for interaction language
    response1 = await core_paella()
    assert response1["status"] == "input_needed"
    assert response1["next_param"] == "interaction_language"
    assert response1["halt"] is True

    # Provide interaction language -> asks for action
    response2 = await core_paella(interaction_language=interaction_lang)
    assert response2["status"] == "input_needed"
    assert response2["next_param"] == "action"
    assert response2["halt"] is True

    # Provide action 'create_new' -> asks for documentation language
    response3 = await core_paella(
        interaction_language=interaction_lang, action="create_new"
    )
    assert response3["status"] == "input_needed"
    assert response3["next_param"] == "documentation_language"
    assert response3["halt"] is True

    # Provide documentation language -> asks for new project name
    response4 = await core_paella(
        interaction_language=interaction_lang,
        action="create_new",
        documentation_language=doc_lang,
    )
    assert response4["status"] == "input_needed"
    assert response4["next_param"] == "new_project_name"
    assert response4["halt"] is True

    # Provide new project name -> SHOULD ask for base_path (THIS WILL FAIL INITIALLY)
    response5 = await core_paella(
        interaction_language=interaction_lang,
        action="create_new",
        documentation_language=doc_lang,
        new_project_name=project_name,
    )
    assert response5["status"] == "input_needed", (
        f"Expected input_needed, got {response5.get('status')}"
    )
    assert response5["next_param"] == "base_path", (
        f"Expected next_param base_path, got {response5.get('next_param')}"
    )
    assert response5["halt"] is True, "Expected halt=True when asking for base_path"
    assert "path" in response5.get("message", "").lower(), "Message should ask for path"

    # Provide base_path -> SHOULD succeed
    response6 = await core_paella(
        interaction_language=interaction_lang,
        action="create_new",
        documentation_language=doc_lang,
        new_project_name=project_name,
        base_path=base_path_input,
        memory_adapter_instance=memory_adapter,  # Pass the fixture instance
    )  # Pass the relative path
    assert response6["status"] == "ok", (
        f"Expected status ok, got {response6.get('status')}: {response6.get('message')}"
    )
    assert response6.get("project_name") == project_name

    # Verification: Check if project saved with correct absolute base_path
    saved_memory: Optional[ProjectMemory] = await memory_adapter.load_memory(
        project_name
    )
    assert saved_memory is not None, (
        f"Project '{project_name}' not found in DB after creation."
    )
    assert saved_memory.metadata.base_path is not None, (
        "Saved metadata base_path is None."
    )
    assert saved_memory.metadata.base_path == expected_abs_base_path, (
        f"Expected base_path {expected_abs_base_path}, but got {saved_memory.metadata.base_path}"
    )

    # Cleanup the created directory (optional but good practice)
    if expected_abs_base_path.exists() and expected_abs_base_path.is_dir():
        try:
            # Remove files first if any were created (future tests might do this)
            for item in expected_abs_base_path.iterdir():
                item.unlink()
            expected_abs_base_path.rmdir()
            print(f"Cleaned up test directory: {expected_abs_base_path}")
        except Exception as e:
            print(
                f"Warning: Could not clean up test directory {expected_abs_base_path}: {e}"
            )
