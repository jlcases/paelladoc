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
from paelladoc.domain.models.project import ProjectMemory, ProjectMetadata, Bucket, ArtifactMeta, SupportedLanguage

# --- Helper Function to create test data --- #

def _create_sample_memory(name_suffix: str) -> ProjectMemory:
    """Helper to create a sample ProjectMemory object."""
    project_name = f"test-project-{name_suffix}-{uuid.uuid4()}"
    metadata = ProjectMetadata(
        name=project_name,
        interaction_language=SupportedLanguage.EN_US,
        documentation_language=SupportedLanguage.EN_US,
        base_path=Path(f"./docs/{project_name}").resolve(),
        purpose="testing list projects",
        target_audience="devs",
        objectives=["test list"],
    )
    # Add a dummy artifact to make it valid
    artifact = ArtifactMeta(
        name="dummy.md",
        bucket=Bucket.UNKNOWN,
        path=Path("dummy.md")
    )
    memory = ProjectMemory(
        metadata=metadata,
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

    yield adapter # Provide the adapter to the test function

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
async def test_list_projects_returns_saved_projects(memory_adapter: SQLiteMemoryAdapter):
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
    expected_project_names = sorted([project1_memory.metadata.name, project2_memory.metadata.name])
    print(f"Saved projects: {expected_project_names}")

    # Act: Call the (yet to be implemented/imported) tool function
    # This import will fail initially, or the function call will fail
    try:
        from paelladoc.adapters.plugins.core.list_projects import list_projects
        result = await list_projects()
    except (ImportError, AttributeError, Exception) as e:
        # We expect an error here initially in TDD
        print(f"Expected failure: Could not import or call list_projects - {e}")
        # Force failure to indicate the code needs writing
        pytest.fail(f"list_projects tool or its dependencies not ready: {e}") 
        return # Exit test early, it failed as expected for TDD step 1

    # Assert: Check the response (This part will run only after implementation)
    assert result["status"] == "ok", f"Expected status ok, got {result.get('status')}"
    assert "projects" in result, "Response missing 'projects' key"
    assert isinstance(result["projects"], list), "'projects' should be a list"
    # Sort both lists for comparison
    assert sorted(result["projects"]) == expected_project_names, \
        f"Expected projects {expected_project_names}, but got {result['projects']}" 