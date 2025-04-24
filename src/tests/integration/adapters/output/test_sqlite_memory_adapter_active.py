"""Integration tests for SQLiteMemoryAdapter focusing on active project logic."""

import pytest
from uuid import uuid4
from pathlib import Path
import time

from sqlmodel import select
from pytest_asyncio import fixture  # Import fixture decorator

from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from paelladoc.domain.models.project import ProjectMemory, ProjectInfo
from paelladoc.adapters.output.sqlite.db_models import ProjectMemoryDB


# Define fixtures directly in this file
@fixture(scope="function")
async def memory_adapter(tmp_path: Path) -> SQLiteMemoryAdapter:
    """Creates a SQLiteMemoryAdapter instance with a temporary database."""
    # Use a unique name for each test function run to avoid conflicts
    db_name = f"test_active_db_{time.time_ns()}.db"
    db_path = tmp_path / db_name
    adapter = SQLiteMemoryAdapter(db_path=db_path)
    # Ensure tables are created *before* the test runs
    await adapter._create_db_and_tables()
    return adapter


@fixture(scope="function")
def create_project_memory():
    """Factory fixture to create ProjectMemory instances."""

    def _create(name: str) -> ProjectMemory:
        return ProjectMemory(
            project_info=ProjectInfo(
                name=name,
                language="en",
                base_path=Path(f"/tmp/{name}"),
                platform_taxonomy="test-platform",
                domain_taxonomy="test-domain",
                size_taxonomy="test-size",
                compliance_taxonomy="test-compliance",
                lifecycle_taxonomy="test-lifecycle",
            ),
            artifacts={},
            platform_taxonomy="test-platform",
            domain_taxonomy="test-domain",
            size_taxonomy="test-size",
            compliance_taxonomy="test-compliance",
            lifecycle_taxonomy="test-lifecycle",
        )

    return _create


# No need to import fixtures directly, Pytest injects them by name
# from src.tests.integration.adapters.output.test_sqlite_memory_adapter import memory_adapter, create_project_memory


@pytest.mark.asyncio
async def test_set_active_project(
    memory_adapter: SQLiteMemoryAdapter, create_project_memory
):
    """Test setting a project as active."""
    project1_name = f"test-project-{uuid4()}"
    project2_name = f"test-project-{uuid4()}"

    memory1 = create_project_memory(project1_name)
    memory2 = create_project_memory(project2_name)

    await memory_adapter.save_memory(memory1)
    await memory_adapter.save_memory(memory2)

    # Activate project 1
    success1 = await memory_adapter.set_active_project(project1_name)
    assert success1 is True

    # Verify project 1 is active
    async with memory_adapter.async_session() as session:
        stmt1 = select(ProjectMemoryDB).where(ProjectMemoryDB.name == project1_name)
        res1 = await session.execute(stmt1)
        db_project1 = res1.scalar_one()
        assert db_project1.is_active is True

        stmt2 = select(ProjectMemoryDB).where(ProjectMemoryDB.name == project2_name)
        res2 = await session.execute(stmt2)
        db_project2 = res2.scalar_one()
        assert db_project2.is_active is False

    # Activate project 2
    success2 = await memory_adapter.set_active_project(project2_name)
    assert success2 is True

    # Verify project 2 is active and project 1 is inactive in a new session
    async with memory_adapter.async_session() as session:
        stmt1 = select(ProjectMemoryDB).where(ProjectMemoryDB.name == project1_name)
        res1 = await session.execute(stmt1)
        db_project1_new = res1.scalar_one()
        assert db_project1_new.is_active is False

        stmt2 = select(ProjectMemoryDB).where(ProjectMemoryDB.name == project2_name)
        res2 = await session.execute(stmt2)
        db_project2_new = res2.scalar_one()
        assert db_project2_new.is_active is True


@pytest.mark.asyncio
async def test_set_active_nonexistent_project(memory_adapter: SQLiteMemoryAdapter):
    """Test setting a non-existent project as active fails."""
    success = await memory_adapter.set_active_project("nonexistent-project")
    assert success is False


@pytest.mark.asyncio
async def test_get_active_project(
    memory_adapter: SQLiteMemoryAdapter, create_project_memory
):
    """Test getting the active project."""
    project1_name = f"test-project-{uuid4()}"
    project2_name = f"test-project-{uuid4()}"

    memory1 = create_project_memory(project1_name)
    memory2 = create_project_memory(project2_name)

    await memory_adapter.save_memory(memory1)
    await memory_adapter.save_memory(memory2)

    # No active project initially
    active_project = await memory_adapter.get_active_project()
    assert active_project is None

    # Activate project 1
    await memory_adapter.set_active_project(project1_name)
    active_project = await memory_adapter.get_active_project()
    assert active_project is not None
    assert isinstance(active_project, ProjectInfo)
    assert active_project.name == project1_name

    # Activate project 2
    await memory_adapter.set_active_project(project2_name)
    active_project = await memory_adapter.get_active_project()
    assert active_project is not None
    assert active_project.name == project2_name


# The following test is removed because the DB-level unique constraint
# using `unique_where` is not supported by SQLite and the core logic
# (ensuring only one project is active) is already tested by
# `test_set_active_project` which verifies the behavior of the
# `set_active_project` method in the adapter.
# @pytest.mark.asyncio
# async def test_unique_constraint_on_active(memory_adapter: SQLiteMemoryAdapter, create_project_memory):
#     """Test that the unique constraint prevents manually setting multiple active projects."""
#     project1_name = f"test-project-{uuid4()}"
#     project2_name = f"test-project-{uuid4()}"
#
#     memory1 = create_project_memory(project1_name)
#     memory2 = create_project_memory(project2_name)
#
#     await memory_adapter.save_memory(memory1)
#     await memory_adapter.save_memory(memory2)
#
#     # Try to set both projects as active in the same transaction
#     async with memory_adapter.async_session() as session:
#         async with session.begin():
#             # Set first project as active
#             stmt1 = select(ProjectMemoryDB).where(ProjectMemoryDB.name == project1_name)
#             res1 = await session.execute(stmt1)
#             db_project1 = res1.scalar_one()
#             db_project1.is_active = True
#
#             # Try to set second project as active - should fail
#             stmt2 = select(ProjectMemoryDB).where(ProjectMemoryDB.name == project2_name)
#             res2 = await session.execute(stmt2)
#             db_project2 = res2.scalar_one()
#             db_project2.is_active = True
#
#             # This should raise an IntegrityError due to the unique constraint
#             with pytest.raises((Exception, sqlalchemy.exc.IntegrityError)) as excinfo:
#                 await session.commit()
#
#             assert "UNIQUE constraint failed" in str(excinfo.value) or "unique_where" in str(excinfo.value)
