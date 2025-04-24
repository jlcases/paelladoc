"""
Integration tests for the core.paella plugin.
"""

import pytest
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

# Adapter for verification
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from paelladoc.adapters.output.sqlite.sqlite_user_management_adapter import (
    SQLiteUserManagementAdapter,
)
from paelladoc.dependencies import dependencies
from paelladoc.ports.output.memory_port import MemoryPort
from paelladoc.ports.output.user_management_port import UserManagementPort

# --- Fixtures ---

TEMP_DB_DIR = Path("src/tests/integration/adapters/plugins/core/temp_dbs")


@pytest.fixture(scope="function", autouse=True)
def setup_test_db_dir():
    """Ensure the temporary DB directory exists for each test function."""
    TEMP_DB_DIR.mkdir(parents=True, exist_ok=True)
    yield
    # No cleanup here, let the adapter fixture handle its own DB file


@pytest.fixture(scope="function")
async def paella_test_env(monkeypatch, setup_test_db_dir):
    """Provides an isolated environment (DB, User Manager, Dependencies) for paella plugin tests."""
    db_name = f"test_paella_plugin_{uuid.uuid4()}.db"
    db_path = TEMP_DB_DIR / db_name
    print(f"\nSetting up paella_test_env with DB: {db_path}")

    # Create isolated adapter instances
    memory_adapter = SQLiteMemoryAdapter(db_path=str(db_path))
    # Instantiate SQLiteUserManagementAdapter using the same session factory
    user_manager = SQLiteUserManagementAdapter(
        async_session_factory=memory_adapter.async_session
    )

    # Initialize DB tables (will create default admin user)
    await memory_adapter._create_db_and_tables()

    # Ensure a test user exists (similar logic as other test)
    user_id = f"test_paella_user_{uuid.uuid4()}"
    try:
        await user_manager.create_user(user_id)
        print(f"Ensured test user '{user_id}' exists for paella test.")
    except Exception as e:
        print(
            f"Could not create test user '{user_id}' (may already exist or error): {e}"
        )
        all_users = await user_manager.get_all_users()
        if all_users:
            user_id = all_users[0].user_identifier
            print(f"Using existing user: {user_id}")
        else:
            print("Warning: No user found after attempting creation.")
            user_id = None

    # Inject into dependencies using monkeypatch

    # No need to store originals, monkeypatch handles revert
    # original_memory = dependencies.get(MemoryPort)
    # original_user = dependencies.get(UserManagementPort)

    monkeypatch.setitem(dependencies, MemoryPort, memory_adapter)
    monkeypatch.setitem(dependencies, UserManagementPort, user_manager)

    yield {"memory_adapter": memory_adapter, "user_manager": user_manager}

    # Teardown: Monkeypatch reverts. Close engine and remove DB file.
    print(f"Tearing down paella_test_env, closing engine and removing DB: {db_path}")
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


# --- Test Cases --- #


@pytest.mark.asyncio
async def test_create_new_project_asks_for_base_path_and_saves_it(
    paella_test_env: dict,  # Use the environment fixture
    monkeypatch,  # Keep monkeypatch if still needed, otherwise remove
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
    # Get adapter from the environment fixture
    memory_adapter = paella_test_env["memory_adapter"]

    interaction_lang = SupportedLanguage.EN_US.value
    doc_lang = SupportedLanguage.EN_US.value
    project_name = f"test-project-{uuid.uuid4()}"
    base_path_input = "./test_paella_docs"  # Relative path input
    expected_abs_base_path = Path(base_path_input).resolve()

    # Act: Call paella_init directly - dependencies are injected via fixtures
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

    assert init_result["status"] == "ok", (
        f"paella_init failed: {init_result.get('message')}"
    )
    # Check returned values directly
    assert init_result["project_name"] == project_name
    assert Path(init_result["base_path"]) == expected_abs_base_path
    assert Path(init_result["base_path"]).is_absolute()

    # Assert: Verify project was saved in the adapter
    # Use the adapter provided by the fixture
    loaded_memory = await memory_adapter.load_memory(project_name)
    assert loaded_memory is not None
    assert loaded_memory.project_info.name == project_name
    assert (
        Path(loaded_memory.project_info.base_path).resolve() == expected_abs_base_path
    )
    # Verify other saved fields if necessary
    assert loaded_memory.project_info.documentation_language == doc_lang
    assert loaded_memory.platform_taxonomy == "test_platform"

    # Cleanup the created directory
    if expected_abs_base_path.exists():
        import shutil

        shutil.rmtree(expected_abs_base_path)
        print(f"Cleaned up test project dir: {expected_abs_base_path}")


@pytest.mark.asyncio
async def test_paella_workflow(paella_test_env: dict):  # Use the environment fixture
    """Test the complete PAELLA workflow: init -> list -> select."""
    # Get adapter from the environment fixture
    memory_adapter = paella_test_env["memory_adapter"]
    # Test data
    project_name = f"test_project_{uuid.uuid4().hex[:8]}"
    base_path = f"docs/{project_name}"
    doc_language = SupportedLanguage.EN_US.value
    int_language = SupportedLanguage.EN_US.value

    # 1. Initialize project - dependencies are injected
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
    assert init_result["status"] == "ok", (
        f"paella_init failed: {init_result.get('message')}"
    )
    # Check returned project name directly
    created_project_name = init_result["project_name"]
    assert created_project_name == project_name

    # 2. List projects - dependencies are injected
    list_result = await paella_list()
    assert list_result["status"] == "ok"
    assert isinstance(list_result["projects"], list)
    # Find the created project in the list (accessing dict keys)
    found_project = next(
        (p for p in list_result["projects"] if p["name"] == project_name), None
    )
    assert found_project is not None
    assert found_project["is_active"] is False  # Access key

    # 3. Select the project - dependencies are injected
    select_result = await paella_select(project_name=project_name)
    assert select_result["status"] == "ok"
    assert (
        f"Project '{project_name}' selected and activated" in select_result["message"]
    )

    # Verify it's active via the adapter
    active_project = await memory_adapter.get_active_project()
    assert active_project is not None
    assert active_project.name == project_name

    # List again to check active status
    list_result_after_select = await paella_list()
    found_project_after_select = next(
        (p for p in list_result_after_select["projects"] if p["name"] == project_name),
        None,
    )
    assert found_project_after_select is not None
    assert found_project_after_select["is_active"] is True  # Access key

    # Cleanup project directory
    abs_base_path = Path(base_path).resolve()
    if abs_base_path.exists():
        import shutil

        shutil.rmtree(abs_base_path)
        print(f"Cleaned up test project dir: {abs_base_path}")
