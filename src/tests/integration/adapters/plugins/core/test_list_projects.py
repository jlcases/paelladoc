"""
Integration tests for the core.list_projects plugin.
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

# Adapter is needed to pre-populate the DB for the test
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# Import domain models to create test data
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
    Bucket,
    ArtifactMeta,
)
from paelladoc.domain.models.language import SupportedLanguage

# --- Helper Function to create test data --- #


def _create_sample_memory(name_suffix: str) -> ProjectMemory:
    """Helper to create a sample ProjectMemory object."""
    project_name = f"test-project-{name_suffix}-{uuid.uuid4()}"
    # Add a dummy artifact to make it valid
    artifact = ArtifactMeta(
        name="dummy.md", bucket=Bucket.UNKNOWN, path=Path("dummy.md")
    )
    memory = ProjectMemory(
        project_info=ProjectInfo(
            name=project_name,
            interaction_language=SupportedLanguage.EN_US,
            documentation_language=SupportedLanguage.EN_US,
            base_path=Path(f"./docs/{project_name}").resolve(),
            purpose="testing list projects",
            target_audience="devs",
            objectives=["test list"],
        ),
        artifacts={Bucket.UNKNOWN: [artifact]},
        taxonomy_version="0.5",
    )
    return memory


# --- Pytest Fixture for Temporary DB (copied from test_paella) --- #


@pytest.fixture(scope="function")
async def memory_adapter():
    """Provides an initialized SQLiteMemoryAdapter with a temporary DB."""
    test_db_name = f"test_list_projects_{uuid.uuid4()}.db"
    test_dir = Path(__file__).parent / "temp_dbs_list"
    test_db_path = test_dir / test_db_name
    test_db_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"\nSetting up test with DB: {test_db_path}")

    adapter = SQLiteMemoryAdapter(db_path=test_db_path)
    await adapter._create_db_and_tables()

    yield adapter  # Provide the adapter to the test function

    # Teardown
    print(f"Tearing down test, removing DB: {test_db_path}")
    await asyncio.sleep(0.01)
    try:
        if test_db_path.exists():
            os.remove(test_db_path)
            print(f"Removed DB: {test_db_path}")
        try:
            test_db_path.parent.rmdir()
            print(f"Removed test directory: {test_db_path.parent}")
        except OSError:
            pass
    except Exception as e:
        print(f"Error during teardown removing {test_db_path}: {e}")


# --- Test Case --- #


@pytest.mark.asyncio
async def test_list_projects_returns_saved_projects(
    memory_adapter: SQLiteMemoryAdapter,
):
    """
    Verify that core.list_projects correctly lists projects previously saved.
    THIS TEST WILL FAIL until the tool and adapter method are implemented.
    """
    print("\nRunning: test_list_projects_returns_saved_projects")

    # Arrange: Save some projects directly using the adapter
    project1_memory = _create_sample_memory("list1")
    project2_memory = _create_sample_memory("list2")
    await memory_adapter.save_memory(project1_memory)
    await memory_adapter.save_memory(project2_memory)
    expected_project_names = sorted(
        [project1_memory.project_info.name, project2_memory.project_info.name]
    )
    print(f"Saved projects: {expected_project_names}")

    # Act: Call the tool function with our test db_path
    from paelladoc.adapters.plugins.core.list_projects import list_projects

    # Pass the path to our temporary test database
    db_path_str = str(memory_adapter.db_path)
    print(f"Using test DB path: {db_path_str}")
    result = await list_projects(db_path=db_path_str)

    # Assert: Check the response
    assert result["status"] == "ok", f"Expected status ok, got {result.get('status')}"
    assert "projects" in result, "Response missing 'projects' key"
    assert isinstance(result["projects"], list), "'projects' should be a list"

    # Extract names from the ProjectInfo objects returned by the plugin
    returned_project_names = sorted(
        [info.name for info in result["projects"] if isinstance(info, ProjectInfo)]
    )

    # Compare the sorted list of names
    assert returned_project_names == expected_project_names, (
        f"Expected project names {expected_project_names}, but got {returned_project_names}"
    )
