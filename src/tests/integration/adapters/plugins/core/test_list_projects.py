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

# Directory for temporary test databases
TEMP_DB_DIR = Path("src/tests/integration/adapters/plugins/core/temp_dbs_list")


@pytest.fixture(scope="function", autouse=True)
def setup_test_db_dir():
    """Ensure the temporary DB directory exists for each test function."""
    TEMP_DB_DIR.mkdir(parents=True, exist_ok=True)
    yield
    # Cleanup directory if empty
    try:
        TEMP_DB_DIR.rmdir()
    except OSError:
        pass  # Not empty, other tests might still be using it


@pytest.fixture(scope="function")
async def list_test_env(monkeypatch, setup_test_db_dir):
    """Provides an isolated environment (DB, User Manager, Dependencies) for list tests."""
    db_name = f"test_list_projects_{uuid.uuid4()}.db"
    db_path = TEMP_DB_DIR / db_name
    print(f"\nSetting up list_test_env with DB: {db_path}")

    # Create isolated adapter instances
    memory_adapter = SQLiteMemoryAdapter(db_path=str(db_path))
    # Instantiate SQLiteUserManagementAdapter using the same session factory as memory_adapter
    user_manager = SQLiteUserManagementAdapter(
        async_session_factory=memory_adapter.async_session
    )

    # Inject into dependencies using monkeypatch FIRST
    from paelladoc.dependencies import dependencies  # Import here if not already at top

    monkeypatch.setitem(dependencies, MemoryPort, memory_adapter)
    monkeypatch.setitem(dependencies, UserManagementPort, user_manager)

    # NOW Initialize DB tables (important for adapter to work)
    # This will also ensure the default admin user is created if none exist
    await memory_adapter._create_db_and_tables()

    # Yield adapters for potential direct use in tests, although not strictly needed
    # if tests only call the plugin functions which use injected dependencies.
    yield {"memory_adapter": memory_adapter, "user_manager": user_manager}

    # Teardown: Monkeypatch handles reverting dependencies.
    # Close engine and remove DB file.
    print(f"Tearing down list_test_env, closing engine and removing DB: {db_path}")
    # Explicitly dispose the engine associated with this test's adapter
    if memory_adapter.async_engine:
        await memory_adapter.async_engine.dispose()
        print(f"Disposed engine for DB: {db_path}")

    if db_path.exists():
        try:
            os.remove(db_path)
            print(f"Removed DB: {db_path}")
        except Exception as e:
            print(f"Error removing DB {db_path}: {e}")


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

    # Act: Call paella_list. It will use the dependencies injected by the fixture.
    result = await paella_list()  # Remove random_string argument

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
