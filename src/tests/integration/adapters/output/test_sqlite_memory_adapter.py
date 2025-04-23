"""
Integration tests for the SQLiteMemoryAdapter.
"""

import pytest  # Use pytest
import asyncio
import sys
import os
from pathlib import Path
import uuid
import datetime
from typing import Dict, List

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Module to test
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# Import updated domain models
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
    ArtifactMeta,
    DocumentStatus,
    Bucket,
)

# --- Pytest Fixture for Temporary DB --- #


@pytest.fixture(scope="function")  # Recreate DB for each test function
async def memory_adapter():
    """Provides an initialized SQLiteMemoryAdapter with a temporary DB."""
    test_db_name = f"test_memory_{uuid.uuid4()}.db"
    test_db_path = Path("./temp_test_dbs") / test_db_name
    test_db_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"\nSetting up test with DB: {test_db_path}")

    adapter = SQLiteMemoryAdapter(db_path=test_db_path)
    await adapter._create_db_and_tables()

    yield adapter  # Provide the adapter to the test function

    # Teardown: clean up the database
    print(f"Tearing down test, removing DB: {test_db_path}")
    # Dispose engine if needed
    # await adapter.async_engine.dispose()
    await asyncio.sleep(0.01)
    try:
        if test_db_path.exists():
            os.remove(test_db_path)
            print(f"Removed DB: {test_db_path}")
            try:
                test_db_path.parent.rmdir()
                print(f"Removed test directory: {test_db_path.parent}")
            except OSError:
                pass  # Directory not empty or other issue
    except Exception as e:
        print(f"Error during teardown removing {test_db_path}: {e}")


# --- Helper Function --- #


def _create_sample_memory(name_suffix: str) -> ProjectMemory:
    """Helper to create a sample ProjectMemory object with Artifacts."""
    project_name = f"test-project-{name_suffix}"

    # Create sample artifacts
    artifact1 = ArtifactMeta(
        name="README",
        bucket=Bucket.INITIATE_INITIAL_PRODUCT_DOCS,
        path=Path("README.md"),
        status=DocumentStatus.PENDING,
    )
    artifact2 = ArtifactMeta(
        name="main.py generation script",
        bucket=Bucket.GENERATE_SUPPORTING_ELEMENTS,
        path=Path("scripts/generate_main.py"),
        status=DocumentStatus.IN_PROGRESS,
    )

    artifacts_dict: Dict[Bucket, List[ArtifactMeta]] = {
        Bucket.INITIATE_INITIAL_PRODUCT_DOCS: [artifact1],
        Bucket.GENERATE_SUPPORTING_ELEMENTS: [artifact2],
    }

    # Set up TimeService first if needed by ArtifactMeta or ProjectMemory\/Info
    # from paelladoc.adapters.services.system_time_service import SystemTimeService
    # from paelladoc.domain.models.project import set_time_service, time_service
    # if time_service is None:
    #     set_time_service(SystemTimeService())

    memory = ProjectMemory(
        project_info=ProjectInfo(
            name=project_name,
            # language="python", # Removed
            # purpose="testing adapter v2", # Removed
            # target_audience="devs", # Removed
            # objectives=["test save artifacts", "test load artifacts"], # Removed
            # Add required taxonomy fields
            platform_taxonomy="test_platform_adapter",
            domain_taxonomy="test_domain_adapter",
            size_taxonomy="test_size_adapter",
            compliance_taxonomy="test_compliance_adapter",
            lifecycle_taxonomy="test_lifecycle_adapter",
            # Assuming base_path, langs are optional or set elsewhere
        ),
        artifacts=artifacts_dict,
        taxonomy_version="0.5",
        # Add required taxonomy fields also directly to ProjectMemory
        platform_taxonomy="test_platform_adapter",
        domain_taxonomy="test_domain_adapter",
        size_taxonomy="test_size_adapter",
        compliance_taxonomy="test_compliance_adapter",
        lifecycle_taxonomy="test_lifecycle_adapter",
    )

    return memory


# --- Test Cases (using pytest and pytest-asyncio) --- #


@pytest.mark.asyncio
async def test_project_exists_on_empty_db(memory_adapter: SQLiteMemoryAdapter):
    """Test project_exists returns False when the DB is empty/project not saved."""
    print("Running: test_project_exists_on_empty_db")
    exists = await memory_adapter.project_exists("nonexistent-project")
    assert not exists


@pytest.mark.asyncio
async def test_load_memory_on_empty_db(memory_adapter: SQLiteMemoryAdapter):
    """Test load_memory returns None when the DB is empty/project not saved."""
    print("Running: test_load_memory_on_empty_db")
    loaded_memory = await memory_adapter.load_memory("nonexistent-project")
    assert loaded_memory is None


@pytest.mark.asyncio
async def test_save_and_load_new_project(memory_adapter: SQLiteMemoryAdapter):
    """Test saving a new project with artifacts and loading it back."""
    print("Running: test_save_and_load_new_project")
    original_memory = _create_sample_memory("save-load-artifacts")
    project_name = original_memory.project_info.name
    original_artifacts = original_memory.artifacts
    artifact1_id = original_artifacts[Bucket.INITIATE_INITIAL_PRODUCT_DOCS][0].id
    artifact2_id = original_artifacts[Bucket.GENERATE_SUPPORTING_ELEMENTS][0].id

    # Save
    await memory_adapter.save_memory(original_memory)
    print(f"Saved project: {project_name}")

    # Load
    loaded_memory = await memory_adapter.load_memory(project_name)
    print(f"Loaded project: {project_name}")

    # Assertions
    assert loaded_memory is not None
    assert loaded_memory.project_info.name == original_memory.project_info.name
    assert loaded_memory.project_info.language == original_memory.project_info.language
    assert (
        loaded_memory.project_info.objectives == original_memory.project_info.objectives
    )
    assert loaded_memory.taxonomy_version == original_memory.taxonomy_version

    # Check artifacts dictionary structure
    # Note: If the adapter pads with empty buckets, adjust this check
    # For now, assume only buckets with artifacts are loaded
    assert Bucket.INITIATE_INITIAL_PRODUCT_DOCS in loaded_memory.artifacts
    assert Bucket.GENERATE_SUPPORTING_ELEMENTS in loaded_memory.artifacts
    assert len(loaded_memory.artifacts[Bucket.INITIATE_INITIAL_PRODUCT_DOCS]) == 1
    assert len(loaded_memory.artifacts[Bucket.GENERATE_SUPPORTING_ELEMENTS]) == 1
    # assert len(loaded_memory.artifacts[Bucket.DEPLOY_SECURITY]) == 0 # Check depends on adapter behavior

    # Check artifact details
    loaded_artifact1 = loaded_memory.get_artifact_by_path(Path("README.md"))
    assert loaded_artifact1 is not None
    assert loaded_artifact1.id == artifact1_id
    assert loaded_artifact1.name == "README"
    assert loaded_artifact1.bucket == Bucket.INITIATE_INITIAL_PRODUCT_DOCS
    assert loaded_artifact1.status == DocumentStatus.PENDING

    loaded_artifact2 = loaded_memory.get_artifact_by_path(
        Path("scripts/generate_main.py")
    )
    assert loaded_artifact2 is not None
    assert loaded_artifact2.id == artifact2_id
    assert loaded_artifact2.name == "main.py generation script"
    assert loaded_artifact2.bucket == Bucket.GENERATE_SUPPORTING_ELEMENTS
    assert loaded_artifact2.status == DocumentStatus.IN_PROGRESS

    # Check timestamps - don't compare exact values since they'll be different due to persistence/mocking
    # Just verify that created_at is a valid UTC timestamp
    assert loaded_memory.created_at.tzinfo == datetime.timezone.utc
    assert isinstance(loaded_memory.created_at, datetime.datetime)
    assert isinstance(loaded_memory.last_updated_at, datetime.datetime)

    # Verify the loaded timestamps are in a reasonable range
    # Current time should be >= last_updated_at
    assert datetime.datetime.now(datetime.timezone.utc) >= loaded_memory.last_updated_at


@pytest.mark.asyncio
async def test_project_exists_after_save(memory_adapter: SQLiteMemoryAdapter):
    """Test project_exists returns True after a project is saved."""
    print("Running: test_project_exists_after_save")
    memory_to_save = _create_sample_memory("exists-artifacts")
    project_name = memory_to_save.project_info.name

    await memory_adapter.save_memory(memory_to_save)
    print(f"Saved project: {project_name}")

    exists = await memory_adapter.project_exists(project_name)
    assert exists


@pytest.mark.asyncio
async def test_save_updates_project(memory_adapter: SQLiteMemoryAdapter):
    """Test saving updates: changing artifact status, adding, removing."""
    print("Running: test_save_updates_project")
    # 1. Create and save initial state
    memory = _create_sample_memory("update-artifacts")
    project_name = memory.project_info.name
    artifact1 = memory.artifacts[Bucket.INITIATE_INITIAL_PRODUCT_DOCS][0]
    # artifact2 = memory.artifacts[Bucket.GENERATE_SUPPORTING_ELEMENTS][0] # No need to store if removing
    await memory_adapter.save_memory(memory)
    print(f"Initial save for {project_name}")

    # 2. Modify the domain object
    artifact1.update_status(DocumentStatus.COMPLETED)
    artifact3 = ArtifactMeta(
        name="Deployment Script",
        bucket=Bucket.DEPLOY_PIPELINES_AND_AUTOMATION,
        path=Path("deploy.sh"),
    )
    # Add artifact3 - ensure bucket exists in dict first
    if artifact3.bucket not in memory.artifacts:
        memory.artifacts[artifact3.bucket] = []
    memory.artifacts[artifact3.bucket].append(artifact3)
    # Remove artifact2 - remove the list if it becomes empty
    del memory.artifacts[Bucket.GENERATE_SUPPORTING_ELEMENTS][0]
    if not memory.artifacts[Bucket.GENERATE_SUPPORTING_ELEMENTS]:
        del memory.artifacts[Bucket.GENERATE_SUPPORTING_ELEMENTS]

    # 3. Save the updated memory
    await memory_adapter.save_memory(memory)
    print(f"Saved updates for {project_name}")

    # 4. Load and verify
    loaded_memory = await memory_adapter.load_memory(project_name)
    assert loaded_memory is not None

    # Verify artifact1 status updated
    loaded_artifact1 = loaded_memory.get_artifact_by_path(Path("README.md"))
    assert loaded_artifact1 is not None
    assert loaded_artifact1.status == DocumentStatus.COMPLETED
    assert loaded_artifact1.id == artifact1.id

    # Verify artifact2 removed
    loaded_artifact2 = loaded_memory.get_artifact_by_path(
        Path("scripts/generate_main.py")
    )
    assert loaded_artifact2 is None
    assert not loaded_memory.artifacts.get(Bucket.GENERATE_SUPPORTING_ELEMENTS)

    # Verify artifact3 added
    loaded_artifact3 = loaded_memory.get_artifact_by_path(Path("deploy.sh"))
    assert loaded_artifact3 is not None
    assert loaded_artifact3.name == "Deployment Script"
    assert loaded_artifact3.bucket == Bucket.DEPLOY_PIPELINES_AND_AUTOMATION
    assert loaded_artifact3.status == DocumentStatus.PENDING
    assert loaded_artifact3.id == artifact3.id


# Run tests if executed directly (optional, better via test runner)
# if __name__ == "__main__":
#     # Consider using asyncio.run() if needed for top-level execution
#     unittest.main()
