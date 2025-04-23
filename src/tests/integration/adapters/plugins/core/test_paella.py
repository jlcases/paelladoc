"""
Integration tests for the core.paella plugin.
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path
import uuid

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

from paelladoc.domain.models.language import SupportedLanguage
from paelladoc.adapters.plugins.core.paella import (
    paella_init,
    paella_list,
    paella_select,
)
from paelladoc.domain.models.project import (
    ProjectInfo,  # Import Metadata and rename
)

# Adapter for verification
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# --- Pytest Fixture for Temporary DB --- #


@pytest.fixture(scope="function")
async def memory_adapter():
    """Provides an initialized SQLiteMemoryAdapter with a temporary DB."""
    test_db_name = f"test_paella_{uuid.uuid4()}.db"
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
            pass  # Directory not empty, likely other tests running concurrently
    except Exception as e:
        print(f"Error during teardown removing {test_db_path}: {e}")


# --- Test Cases --- #


@pytest.mark.asyncio
async def test_create_new_project_asks_for_base_path_and_saves_it(
    memory_adapter,
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

    interaction_lang = SupportedLanguage.EN_US.value
    doc_lang = SupportedLanguage.EN_US.value
    project_name = f"test-project-{uuid.uuid4()}"
    base_path_input = "./test_paella_docs"  # Relative path input
    expected_abs_base_path = Path(base_path_input).resolve()

    # --- Monkeypatch the database path resolution ---
    # Patch get_db_path where SQLiteMemoryAdapter imports it,
    # so core_paella uses the temporary DB path when it creates its own adapter.
    monkeypatch.setattr(
        "paelladoc.adapters.output.sqlite.sqlite_memory_adapter.get_db_path",
        lambda: memory_adapter.db_path,  # Return the path from the fixture
    )

    # Initialize project
    init_result = await paella_init(
        base_path=base_path_input,
        documentation_language=doc_lang,
        interaction_language=interaction_lang,
        new_project_name=project_name,
        platform_taxonomy="test_platform",
        domain_taxonomy="test_domain",
        size_taxonomy="test_size",
        compliance_taxonomy="test_compliance",
        lifecycle_taxonomy="test_lifecycle",
    )
    assert init_result["status"] == "ok"
    assert init_result["project_name"] == project_name
    assert init_result["base_path"] == str(expected_abs_base_path)

    # Clean up
    if expected_abs_base_path.exists():
        import shutil

        shutil.rmtree(expected_abs_base_path)


@pytest.mark.asyncio
async def test_paella_workflow():
    """Test the complete PAELLA workflow."""
    # Test data
    project_name = f"test_project_{uuid.uuid4().hex[:8]}"
    base_path = f"docs/{project_name}"
    doc_language = SupportedLanguage.EN_US.value
    int_language = SupportedLanguage.EN_US.value

    # Initialize project
    init_result = await paella_init(
        base_path=base_path,
        documentation_language=doc_language,
        interaction_language=int_language,
        new_project_name=project_name,
        platform_taxonomy="test_platform",
        domain_taxonomy="test_domain",
        size_taxonomy="test_size",
        compliance_taxonomy="test_compliance",
        lifecycle_taxonomy="test_lifecycle",
    )
    assert init_result["status"] == "ok"
    assert init_result["project_name"] == project_name
    assert init_result["base_path"] == str(Path(base_path).expanduser().resolve())

    # List projects
    list_result = await paella_list()
    assert list_result["status"] == "ok"
    assert isinstance(list_result["projects"], list)
    # Extract names from ProjectInfo objects before checking membership
    project_names_list = [
        info.name for info in list_result["projects"] if isinstance(info, ProjectInfo)
    ]
    assert project_name in project_names_list

    # Select project
    select_result = await paella_select(project_name=project_name)
    assert select_result["status"] == "ok"
    assert select_result["project_name"] == project_name

    # Clean up
    project_dir = Path(base_path)
    if project_dir.exists():
        import shutil

        shutil.rmtree(project_dir)
