"""
Integration tests for the project listing functionality.
"""

import pytest
import sys
import os
from pathlib import Path
import uuid

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Adapter is needed to pre-populate the DB for the test
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# Import the SQLite adapter instead of the dummy one
from paelladoc.adapters.output.sqlite.sqlite_user_management_adapter import (
    SQLiteUserManagementAdapter,
)
from paelladoc.ports.output.user_management_port import UserManagementPort
from paelladoc.ports.output.memory_port import MemoryPort

# Import domain models to create test data
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
    Bucket,
    ArtifactMeta,
)
from paelladoc.domain.models.language import SupportedLanguage

# Import paella_list instead of the deleted module
from paelladoc.adapters.plugins.core.paella import paella_list

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
            platform_taxonomy="test_platform",
            domain_taxonomy="test_domain",
            size_taxonomy="test_size",
            compliance_taxonomy="test_compliance",
            lifecycle_taxonomy="test_lifecycle",
        ),
        artifacts={Bucket.UNKNOWN: [artifact]},
        taxonomy_version="0.5",
        platform_taxonomy="test_platform",
        domain_taxonomy="test_domain",
        size_taxonomy="test_size",
        compliance_taxonomy="test_compliance",
        lifecycle_taxonomy="test_lifecycle",
    )
    return memory


# --- Test Case --- #


@pytest.mark.asyncio
async def test_list_projects_returns_saved_projects(
    list_test_env: dict,  # Use the new environment fixture
):
    """
    Verify that listing projects correctly returns previously saved projects.
    Now using paella_list instead of the deprecated list_projects function.
    """
    print("\nRunning: test_list_projects_returns_saved_projects")
    memory_adapter = list_test_env["memory_adapter"]

    # Arrange: Save some projects directly using the adapter from the fixture
    project1_memory = _create_sample_memory("list1")
    project2_memory = _create_sample_memory("list2")
    await memory_adapter.save_memory(project1_memory)
    await memory_adapter.save_memory(project2_memory)
    expected_project_names = sorted(
        [project1_memory.project_info.name, project2_memory.project_info.name]
    )
    print(f"Saved projects: {expected_project_names}")

    # Create a monkeypatch to temporarily set the DB path for the test
    # Since we can't pass db_path to paella_list directly, we need to monkeypatch
    # the SQLiteMemoryAdapter to use our test DB
    original_init = SQLiteMemoryAdapter.__init__

    def patched_init(self, db_path=None):
        return original_init(self, db_path=memory_adapter.db_path)

    # Apply the monkeypatch for this test
    SQLiteMemoryAdapter.__init__ = patched_init

    try:
        # Act: Call paella_list which now uses our test DB
        print(f"Using test DB path: {memory_adapter.db_path}")
        result = await paella_list()
    finally:
        # Restore the original init method
        SQLiteMemoryAdapter.__init__ = original_init

    # Assert: Check the response
    assert result["status"] == "ok", (
        f"Expected status ok, got {result.get('status')}: {result.get('message')}"
    )
    assert "projects" in result
    assert isinstance(result["projects"], list)

    # Verify project names
    retrieved_project_names = sorted(
        [p["name"] for p in result["projects"]]
    )  # Access name via key again
    print(f"Retrieved projects: {retrieved_project_names}")
    assert retrieved_project_names == expected_project_names
