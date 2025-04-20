"""Integration tests for Alembic configuration."""

import os
import pytest
from pathlib import Path
import uuid
import subprocess  # Import subprocess
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy.ext.asyncio import create_async_engine
import sys

# Import get_db_path to test its behavior directly
from paelladoc.config.database import get_db_path

# Get project root to build absolute paths if needed
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def clean_env():
    """Remove relevant environment variables before each test."""
    original_db_path = os.environ.get("PAELLADOC_DB_PATH")
    original_env = os.environ.get("PAELLADOC_ENV")

    if "PAELLADOC_DB_PATH" in os.environ:
        del os.environ["PAELLADOC_DB_PATH"]
    if "PAELLADOC_ENV" in os.environ:
        del os.environ["PAELLADOC_ENV"]

    yield

    if original_db_path is not None:
        os.environ["PAELLADOC_DB_PATH"] = original_db_path
    if original_env is not None:
        os.environ["PAELLADOC_ENV"] = original_env


@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    test_db_name = f"test_alembic_{uuid.uuid4()}.db"
    # Use a simpler temp directory structure to avoid potential permission issues
    test_dir = Path("/tmp") / "paelladoc_test_dbs"
    test_db_path = test_dir / test_db_name
    test_db_path.parent.mkdir(parents=True, exist_ok=True)

    yield test_db_path

    # Cleanup
    try:
        if test_db_path.exists():
            # No need for asyncio.sleep here as subprocess runs separately
            os.remove(test_db_path)
        if test_dir.exists() and not any(test_dir.iterdir()):
            test_dir.rmdir()
    except Exception as e:
        print(f"Error during cleanup: {e}")


def run_alembic_command(command: list, env: dict):
    """Helper function to run alembic CLI commands via subprocess."""
    # Ensure alembic is callable, adjust path if needed (e.g., use .venv/bin/alembic)
    alembic_executable = PROJECT_ROOT / ".venv" / "bin" / "alembic"
    if not alembic_executable.exists():
        # Fallback or error if venv structure is different
        pytest.fail(f"Alembic executable not found at {alembic_executable}")

    cmd = [str(alembic_executable)] + command
    print(f"\nRunning subprocess: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env={**os.environ, **env},  # Merge OS env with test-specific env
        cwd=PROJECT_ROOT,  # Run from project root where alembic.ini is
        check=False,  # Don't raise exception on non-zero exit, check manually
    )
    print(f"Subprocess stdout:\n{result.stdout}")
    print(f"Subprocess stderr:\n{result.stderr}")
    if result.returncode != 0:
        pytest.fail(
            f"Alembic command {' '.join(command)} failed with exit code {result.returncode}\nStderr: {result.stderr}"
        )
    return result


def test_alembic_config_uses_db_path_via_env(clean_env, temp_db_path):
    """Test that env.py logic picks up PAELLADOC_DB_PATH."""
    os.environ["PAELLADOC_DB_PATH"] = str(temp_db_path)

    # Verify that get_db_path() returns the expected path
    # as this is what env.py uses to construct the URL.
    resolved_path = get_db_path()
    assert resolved_path == temp_db_path


@pytest.mark.asyncio
async def test_alembic_migrations_work_with_config(clean_env, temp_db_path):
    """Test that migrations work by running alembic upgrade via subprocess."""
    test_env = {"PAELLADOC_DB_PATH": str(temp_db_path)}

    # Ensure the temporary database file exists before running Alembic
    if not temp_db_path.exists():
        temp_db_path.touch()

    # Run alembic upgrade head in a subprocess
    run_alembic_command(["upgrade", "head"], env=test_env)

    # Verify migrations applied using an async engine
    # Need the actual URL alembic used (which comes from env var)
    db_url = f"sqlite+aiosqlite:///{temp_db_path}"
    engine = create_async_engine(db_url)
    try:
        async with engine.connect() as conn:
            # Define a sync function to get revision
            def get_rev_sync(sync_conn):
                # Need alembic config to find script directory
                cfg = Config("alembic.ini")  # Load config to get script location
                migration_context = MigrationContext.configure(
                    connection=sync_conn,
                    opts={"script": ScriptDirectory.from_config(cfg)},
                )
                return migration_context.get_current_revision()

            # Run the sync function using run_sync
            current_rev = await conn.run_sync(get_rev_sync)

            # Get head revision directly from script directory
            cfg = Config("alembic.ini")
            script = ScriptDirectory.from_config(cfg)
            head_rev = script.get_current_head()

            assert current_rev is not None, "DB revision is None after upgrade."
            assert current_rev == head_rev, (
                f"DB revision {current_rev} does not match head {head_rev}"
            )
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_alembic_downgrade_works_with_config(clean_env, temp_db_path):
    """Test that downgrades work by running alembic via subprocess."""
    test_env = {"PAELLADOC_DB_PATH": str(temp_db_path)}

    # Ensure the temporary database file exists before running Alembic
    if not temp_db_path.exists():
        temp_db_path.touch()

    # Run migrations up first
    run_alembic_command(["upgrade", "head"], env=test_env)

    # Run migrations down
    run_alembic_command(["downgrade", "base"], env=test_env)

    # Verify database is at base (no revision)
    db_url = f"sqlite+aiosqlite:///{temp_db_path}"
    engine = create_async_engine(db_url)
    try:
        async with engine.connect() as conn:
            # Define a sync function to get revision
            def get_rev_sync(sync_conn):
                cfg = Config("alembic.ini")  # Load config to get script location
                migration_context = MigrationContext.configure(
                    connection=sync_conn,
                    opts={"script": ScriptDirectory.from_config(cfg)},
                )
                return migration_context.get_current_revision()

            # Run the sync function using run_sync
            current_rev = await conn.run_sync(get_rev_sync)
            assert current_rev is None, (
                f"Expected base revision (None), got {current_rev}"
            )
    finally:
        await engine.dispose()


def test_alembic_respects_environment_precedence(clean_env, temp_db_path):
    """Test that PAELLADOC_DB_PATH takes precedence over PAELLADOC_ENV."""
    # Set both environment variables
    os.environ["PAELLADOC_DB_PATH"] = str(temp_db_path)
    os.environ["PAELLADOC_ENV"] = "development"  # This should be ignored

    # Verify that get_db_path() returns the path from PAELLADOC_DB_PATH
    resolved_path = get_db_path()
    assert resolved_path == temp_db_path
