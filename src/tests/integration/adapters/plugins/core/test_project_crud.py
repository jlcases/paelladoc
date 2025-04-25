"""
Integration tests for project CRUD operations.
"""

import pytest
import sys
import os
from pathlib import Path
import uuid
from typing import Dict, Any
import shutil

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

from paelladoc.domain.models.language import SupportedLanguage
from paelladoc.adapters.plugins.core.paella import paella_init
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
from paelladoc.ports.output.user_management_port import UserManagementPort
from paelladoc.ports.output.mcp_config_port import MCPConfigPort
from paelladoc.ports.output.memory_port import MemoryPort
from paelladoc.adapters.output.sqlite.sqlite_user_management_adapter import (
    SQLiteUserManagementAdapter,
)
from paelladoc.adapters.output.filesystem.mcp_config_repository import (
    FileSystemMCPConfigRepository,
)
from paelladoc.dependencies import dependencies

# --- Test Fixtures --- #

# Directory for temporary test databases
TEMP_DB_DIR = Path("src/tests/integration/adapters/plugins/core/temp_dbs")
TEMP_PROJECTS_DIR = Path("test_projects")  # Base for test project files


@pytest.fixture(scope="function", autouse=True)
def setup_test_dirs():
    """Create temporary directories for DBs and project files."""
    TEMP_DB_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\nCreated directories: {TEMP_DB_DIR}, {TEMP_PROJECTS_DIR}")
    yield
    # Teardown: remove directories after tests in the module run
    # Scope is function, so this runs after each test
    try:
        if TEMP_DB_DIR.exists():
            shutil.rmtree(TEMP_DB_DIR)
            print(f"Removed directory: {TEMP_DB_DIR}")
        if TEMP_PROJECTS_DIR.exists():
            shutil.rmtree(TEMP_PROJECTS_DIR)
            print(f"Removed directory: {TEMP_PROJECTS_DIR}")
    except Exception as e:
        print(f"Error during teardown: {e}")


@pytest.fixture(scope="function")
async def crud_test_env(monkeypatch, setup_test_dirs):
    """Provides an isolated environment (DB, User Manager, Dependencies) for CRUD tests."""
    db_name = f"test_project_crud_{uuid.uuid4()}.db"
    db_path = TEMP_DB_DIR / db_name
    print(f"\nSetting up crud_test_env with DB: {db_path}")

    # Use the global session factory from the container - NOT USED, REMOVED
    # global_session_factory = container._async_session_factory

    # Create isolated adapter instances
    # Pass the db_path to SQLiteMemoryAdapter, it will create its own engine/session factory for that path
    memory_adapter = SQLiteMemoryAdapter(db_path=str(db_path))
    # Pass the *global* session factory to the user manager - THIS IS LIKELY WRONG if DBs are separate
    # The user manager needs to operate on the *same DB* as the memory adapter for the test.
    # Let's pass the session factory created by the specific memory_adapter instance for THIS test DB.
    user_manager = SQLiteUserManagementAdapter(
        async_session_factory=memory_adapter.async_session
    )
    mcp_config_adapter = FileSystemMCPConfigRepository()

    # Inject into dependencies using monkeypatch FIRST
    monkeypatch.setitem(dependencies, MemoryPort, memory_adapter)
    monkeypatch.setitem(dependencies, UserManagementPort, user_manager)
    monkeypatch.setitem(dependencies, MCPConfigPort, mcp_config_adapter)

    # NOW initialize DB tables using the correct, injected dependencies
    # _ensure_initial_admin_user will now get the patched user_manager
    await memory_adapter._create_db_and_tables()

    # NO need to setitem again here

    yield {"memory_adapter": memory_adapter, "user_manager": user_manager}

    # Teardown: Monkeypatch reverts. Close engine and remove DB file.
    print(f"Tearing down crud_test_env, closing engine and removing DB: {db_path}")
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


@pytest.fixture
async def test_project(
    crud_test_env: Dict[str, Any],
) -> Dict[str, Any]:  # Use the env fixture
    """Creates a test project within the isolated environment."""
    # Dependencies are already injected by crud_test_env

    project_name = f"test-project-{uuid.uuid4()}"
    # Place project files inside the managed TEMP_PROJECTS_DIR
    base_path = TEMP_PROJECTS_DIR / project_name
    base_path_str = str(base_path.resolve())  # Use absolute path for consistency

    # Create project using the dependency-injected adapter
    init_result = await paella_init(
        base_path=base_path_str,
        documentation_language=SupportedLanguage.EN_US.value,
        interaction_language=SupportedLanguage.EN_US.value,
        new_project_name=project_name,
        platform_taxonomy="test_platform",
        domain_taxonomy="test_domain",
        size_taxonomy="test_size",
        compliance_taxonomy="test_compliance",
        lifecycle_taxonomy="test_lifecycle",
    )

    assert init_result["status"] == "ok", (
        f"Failed to initialize test project: {init_result.get('message', 'Unknown error')}"
    )
    # Verify base path creation directly from init_result
    returned_base_path = Path(init_result["base_path"])
    assert returned_base_path.exists(), (
        "Project base path directory was not created by paella_init"
    )
    assert returned_base_path == base_path.resolve(), (
        "Returned base path does not match expected resolved path"
    )

    # Fetch the project details AFTER creation using get_project
    # This ensures we test the full flow and get the complete ProjectInfo
    get_result = await get_project(project_name=project_name)
    assert get_result["status"] == "ok", (
        f"Failed to retrieve project '{project_name}' after creation."
    )
    initial_data = get_result["project"]  # Get the full project data as stored

    # Return info needed by tests
    return {
        "project_name": project_name,
        "base_path": base_path,  # Return Path object for easier manipulation
        "initial_data": initial_data,  # Return the fetched full project data
    }


# --- Test Cases (Injecting Dependencies) --- #


@pytest.mark.asyncio
async def test_get_project_returns_correct_info(crud_test_env, test_project):
    """Test retrieving a project returns all expected fields."""
    project_name = test_project["project_name"]
    initial_data = test_project["initial_data"]  # Use the fetched initial data

    # Call get_project - dependencies resolved internally
    result = await get_project(project_name=project_name)

    assert result["status"] == "ok"
    assert (
        result["project"] == initial_data
    )  # Compare fetched data with originally fetched data
    assert result["project"]["name"] == project_name
    assert Path(result["project"]["base_path"]) == test_project["base_path"].resolve()
    assert result["project"]["platform_taxonomy"] == "test_platform"


@pytest.mark.asyncio
async def test_get_project_returns_error_for_nonexistent_project(crud_test_env):
    """Test that get_project handles nonexistent projects correctly."""
    # Call get_project - dependencies resolved internally
    result = await get_project(
        project_name="nonexistent-project",
        # REMOVE: memory_adapter=crud_test_env["memory_adapter"] # No longer injected
    )
    assert result["status"] == "error"
    assert "not found" in result["message"]


@pytest.mark.asyncio
async def test_update_project_modifies_specific_fields(crud_test_env, test_project):
    """Test updating specific fields like purpose and language."""
    project_name = test_project["project_name"]
    updates = {
        "purpose": "Updated test purpose",
        "documentation_language": SupportedLanguage.ES_ES.value,
        "platform_taxonomy": "updated_platform",  # Example of updating taxonomy
    }

    # Call update_project - dependencies resolved internally
    update_result = await update_project(
        project_name=project_name,
        updates=updates,
        create_backup=False,  # Disable backup for simplicity
    )

    assert update_result["status"] == "ok"
    updated_project_info = update_result["project"]
    assert updated_project_info["purpose"] == "Updated test purpose"
    assert (
        updated_project_info["documentation_language"] == SupportedLanguage.ES_ES.value
    )
    assert updated_project_info["platform_taxonomy"] == "updated_platform"

    # Verify persistence by reading again
    get_result = await get_project(project_name=project_name)
    assert get_result["status"] == "ok"
    assert get_result["project"]["purpose"] == "Updated test purpose"
    assert get_result["project"]["platform_taxonomy"] == "updated_platform"


@pytest.mark.asyncio
async def test_update_project_validates_fields(crud_test_env, test_project):
    """Test that updates fail with invalid language codes."""
    project_name = test_project["project_name"]
    updates = {"documentation_language": "invalid-lang-code"}

    update_result = await update_project(
        project_name=project_name,
        updates=updates,
    )

    assert update_result["status"] == "error"
    assert "Validation failed" in update_result["message"]
    assert "documentation_language" in update_result["message"]


@pytest.mark.asyncio
async def test_update_project_validates_multiple_fields(crud_test_env, test_project):
    """Test that multiple invalid fields are reported."""
    project_name = test_project["project_name"]
    updates = {
        "documentation_language": "invalid-lang",
        "interaction_language": "also-invalid",
    }

    update_result = await update_project(
        project_name=project_name,
        updates=updates,
    )

    assert update_result["status"] == "error"
    assert "Validation failed" in update_result["message"]
    assert "documentation_language" in update_result["message"]
    assert "interaction_language" in update_result["message"]


@pytest.mark.asyncio
async def test_delete_project_removes_project_and_files(crud_test_env, test_project):
    """Test deleting a project removes DB entry and files."""
    project_name = test_project["project_name"]
    base_path = test_project["base_path"]

    # Create a dummy file in the project directory
    dummy_file = base_path / "dummy.txt"
    dummy_file.touch()
    assert dummy_file.exists()
    assert base_path.exists()

    # Call delete_project - dependencies resolved internally
    delete_result = await delete_project(
        project_name=project_name, confirm=True, create_backup=False
    )

    assert delete_result["status"] == "ok"

    # Verify deletion from DB
    get_result = await get_project(project_name=project_name)
    assert get_result["status"] == "error"
    assert "not found" in get_result["message"]

    # Verify directory deletion
    assert not base_path.exists(), f"Project directory {base_path} was not deleted."


@pytest.mark.asyncio
async def test_delete_project_requires_confirmation(crud_test_env, test_project):
    """Test delete fails without explicit confirmation."""
    project_name = test_project["project_name"]

    # Call delete_project without confirm=True
    delete_result = await delete_project(
        project_name=project_name,
        confirm=False,  # Default is False, but explicit here
        create_backup=False,
    )

    assert delete_result["status"] == "error"
    assert (
        "Deletion requires explicit confirmation. Set 'confirm=True'."
        in delete_result["message"]
    )

    # Verify project still exists
    get_result = await get_project(project_name=project_name)
    assert get_result["status"] == "ok"


@pytest.mark.asyncio
async def test_delete_project_creates_backup(crud_test_env, test_project):
    """Test that delete creates a backup when requested."""
    project_name = test_project["project_name"]
    base_path = test_project["base_path"]

    # Call delete_project with create_backup=True
    delete_result = await delete_project(
        project_name=project_name, confirm=True, create_backup=True
    )

    assert delete_result["status"] == "ok"
    assert "backup_path" in delete_result
    backup_path = Path(delete_result["backup_path"])
    assert backup_path.exists()
    assert backup_path.is_file()
    assert backup_path.name.endswith(".zip")

    # Clean up backup file
    if backup_path.exists():
        backup_path.unlink()

    # Verify project itself is deleted
    get_result = await get_project(project_name=project_name)
    assert get_result["status"] == "error"
    assert not base_path.exists()


# --- Utility Function Tests --- #


@pytest.mark.asyncio
async def test_validate_project_updates_checks_languages():
    """Test validation of language fields."""
    valid_updates = {"documentation_language": "en-US", "interaction_language": "es-ES"}
    invalid_updates = {"documentation_language": "xx-XX"}
    multiple_invalid = {
        "documentation_language": "yy-YY",
        "interaction_language": "zz-ZZ",
    }

    assert not validate_project_updates(valid_updates)
    errors = validate_project_updates(invalid_updates)
    assert len(errors) == 1
    assert "documentation_language" in errors[0]

    errors_multi = validate_project_updates(multiple_invalid)
    assert len(errors_multi) == 2
    assert any("documentation_language" in e for e in errors_multi)
    assert any("interaction_language" in e for e in errors_multi)


@pytest.mark.asyncio
async def test_validate_project_updates_checks_base_path():
    """Test validation that base_path cannot be updated directly."""
    updates = {"base_path": "/new/path"}
    errors = validate_project_updates(updates)
    assert len(errors) == 1
    assert "base_path cannot be updated" in errors[0]


@pytest.mark.asyncio
async def test_format_project_info_converts_paths():
    """Test that format_project_info converts Path objects to strings."""
    project_info_dict = {
        "name": "test",
        "base_path": Path("/absolute/path/to/project"),
        "other_field": 123,
    }
    formatted = format_project_info(project_info_dict)
    assert isinstance(formatted["base_path"], str)
    assert formatted["base_path"] == "/absolute/path/to/project"
    assert formatted["other_field"] == 123
