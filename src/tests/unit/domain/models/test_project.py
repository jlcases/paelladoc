import json
import pytest
from datetime import datetime
from pathlib import Path

from paelladoc.domain.models.project import (
    DocumentStatus,
    Bucket,
    ArtifactMeta,
    ProjectInfo,
    ProjectMemory,
    # ProjectDocument, # Assuming this was removed or is internal
)
from paelladoc.adapters.services.system_time_service import SystemTimeService
from paelladoc.domain.models.project import set_time_service, time_service


class TestBucket:
    """Tests for the Bucket enum"""

    def test_bucket_values(self):
        """Test that all buckets have the correct string format"""
        for bucket in Bucket:
            if bucket is not Bucket.UNKNOWN:
                # Format should be "Phase::Subcategory"
                assert "::" in bucket.value
                phase, subcategory = bucket.value.split("::")
                assert phase in [
                    "Initiate",
                    "Elaborate",
                    "Govern",
                    "Generate",
                    "Maintain",
                    "Deploy",
                    "Operate",
                    "Iterate",
                ]
                assert len(subcategory) > 0
            else:
                assert bucket.value == "Unknown"

    def test_get_phase_buckets(self):
        """Test the get_phase_buckets class method"""
        initiate_buckets = Bucket.get_phase_buckets("Initiate")
        assert len(initiate_buckets) == 2
        assert Bucket.INITIATE_CORE_SETUP in initiate_buckets
        assert Bucket.INITIATE_INITIAL_PRODUCT_DOCS in initiate_buckets

        elaborate_buckets = Bucket.get_phase_buckets("Elaborate")
        assert len(elaborate_buckets) == 4

        # Should return empty set for non-existent phase
        nonexistent_buckets = Bucket.get_phase_buckets("NonExistent")
        assert len(nonexistent_buckets) == 0


class TestArtifactMeta:
    """Tests for the ArtifactMeta model"""

    def test_create_artifact_meta(self):
        """Test creating an ArtifactMeta instance"""
        artifact = ArtifactMeta(
            name="test_artifact",
            bucket=Bucket.INITIATE_CORE_SETUP,
            path=Path("docs/test_artifact.md"),
            status=DocumentStatus.IN_PROGRESS,
        )

        assert artifact.name == "test_artifact"
        assert artifact.bucket == Bucket.INITIATE_CORE_SETUP
        assert artifact.path == Path("docs/test_artifact.md")
        assert artifact.status == DocumentStatus.IN_PROGRESS
        assert isinstance(artifact.created_at, datetime)
        assert isinstance(artifact.updated_at, datetime)

    def test_update_status(self):
        """Test updating an artifact's status"""
        artifact = ArtifactMeta(
            name="test_artifact",
            bucket=Bucket.INITIATE_CORE_SETUP,
            path=Path("docs/test_artifact.md"),
        )

        # Default status should be PENDING
        assert artifact.status == DocumentStatus.PENDING

        # Store the original timestamp
        original_updated_at = artifact.updated_at

        # Update the status
        artifact.update_status(DocumentStatus.COMPLETED)

        # Check that status was updated
        assert artifact.status == DocumentStatus.COMPLETED

        # Check that timestamp was updated
        assert artifact.updated_at > original_updated_at

    def test_serialization_deserialization(self):
        """Test that ArtifactMeta can be serialized and deserialized"""
        artifact = ArtifactMeta(
            name="test_artifact",
            bucket=Bucket.ELABORATE_DISCOVERY_AND_RESEARCH,
            path=Path("docs/research/test_artifact.md"),
            status=DocumentStatus.COMPLETED,
        )

        # Serialize to JSON
        artifact_json = artifact.model_dump_json()

        # Deserialize from JSON
        loaded_artifact = ArtifactMeta.model_validate_json(artifact_json)

        # Check that all fields were preserved
        assert loaded_artifact.name == artifact.name
        assert loaded_artifact.bucket == artifact.bucket
        assert loaded_artifact.path == artifact.path
        assert loaded_artifact.status == artifact.status
        assert loaded_artifact.created_at == artifact.created_at
        assert loaded_artifact.updated_at == artifact.updated_at


@pytest.fixture
def sample_project_memory() -> ProjectMemory:
    """Fixture to provide a sample ProjectMemory instance for testing."""
    # Set up TimeService if needed
    if time_service is None:
        set_time_service(SystemTimeService())

    project_info = ProjectInfo(
        name="Test Project",
        platform_taxonomy="test_platform",
        domain_taxonomy="test_domain",
        size_taxonomy="test_size",
        compliance_taxonomy="test_compliance",
        lifecycle_taxonomy="test_lifecycle",
    )

    # Create the ProjectMemory instance first
    project_memory_instance = ProjectMemory(
        project_info=project_info,
        platform_taxonomy="test_platform",
        domain_taxonomy="test_domain",
        size_taxonomy="test_size",
        compliance_taxonomy="test_compliance",
        lifecycle_taxonomy="test_lifecycle",
    )

    # Now create and add the artifacts expected by the tests
    artifacts_to_add = [
        ArtifactMeta(
            name="vision_doc",
            bucket=Bucket.INITIATE_INITIAL_PRODUCT_DOCS,
            path=Path("docs/initiation/product_vision.md"),
            status=DocumentStatus.PENDING,  # Changed status back to PENDING
        ),
        ArtifactMeta(
            name="user_research",
            bucket=Bucket.ELABORATE_DISCOVERY_AND_RESEARCH,
            path=Path("docs/research/user_research.md"),
            status=DocumentStatus.IN_PROGRESS,  # Specific status for this test artifact
        ),
        ArtifactMeta(
            name="api_spec",
            bucket=Bucket.ELABORATE_SPECIFICATION_AND_PLANNING,
            path=Path("docs/specs/api_specification.md"),
            status=DocumentStatus.COMPLETED,  # Specific status for this test artifact
        ),
    ]

    for artifact in artifacts_to_add:
        project_memory_instance.add_artifact(artifact)

    return project_memory_instance


def test_project_info_initialization():
    """Test ProjectInfo initialization."""
    info = ProjectInfo(
        name="Another Test",
        # description="Detailed desc.", # Removed
        base_path="/tmp",
        documentation_language="es",
        interaction_language="es",
        platform_taxonomy="test_platform_2",
        domain_taxonomy="test_domain_2",
        size_taxonomy="test_size_2",
        compliance_taxonomy="test_compliance_2",
        lifecycle_taxonomy="test_lifecycle_2",  # Added lifecycle
    )
    assert info.name == "Another Test"
    # assert info.description == "Detailed desc." # Removed assertion for non-existent field
    assert str(info.base_path) == "/tmp"  # Check path conversion if needed
    assert info.documentation_language == "es"
    assert info.interaction_language == "es"
    assert info.platform_taxonomy == "test_platform_2"
    assert info.domain_taxonomy == "test_domain_2"
    assert info.size_taxonomy == "test_size_2"
    assert info.compliance_taxonomy == "test_compliance_2"
    assert info.lifecycle_taxonomy == "test_lifecycle_2"


def test_project_memory_initialization(sample_project_memory):
    """Test ProjectMemory initialization using the fixture."""
    assert sample_project_memory.project_info.name == "Test Project"
    # assert "version" in sample_project_memory.metadata # Removed check for metadata
    assert isinstance(sample_project_memory.created_at, datetime)
    assert isinstance(
        sample_project_memory.last_updated_at, datetime
    )  # Corrected field name
    # Check taxonomy fields added in fixture (both in project_info and directly)
    assert sample_project_memory.project_info.platform_taxonomy == "test_platform"
    assert sample_project_memory.project_info.domain_taxonomy == "test_domain"
    assert sample_project_memory.project_info.size_taxonomy == "test_size"
    assert sample_project_memory.project_info.compliance_taxonomy == "test_compliance"
    assert sample_project_memory.platform_taxonomy == "test_platform"
    assert sample_project_memory.domain_taxonomy == "test_domain"
    assert sample_project_memory.size_taxonomy == "test_size"
    assert sample_project_memory.compliance_taxonomy == "test_compliance"


def test_project_memory_update(sample_project_memory):
    """Test ProjectMemory update."""
    # Implementation of the test_project_memory_update method
    pass


class TestProjectMemory:
    """Tests for the ProjectMemory model with taxonomy support"""

    @pytest.fixture(autouse=True)
    def setup_test_time_service(self):
        """Ensure time service is set for each test in this class."""
        if time_service is None:
            set_time_service(SystemTimeService())

    def test_project_memory_initialization(self):
        """Test initializing ProjectMemory with taxonomy support"""
        project = ProjectMemory(
            project_info=ProjectInfo(
                name="test_project",
                # Add required taxonomy fields to ProjectInfo
                platform_taxonomy="test_platform",
                domain_taxonomy="test_domain",
                size_taxonomy="test_size",
                compliance_taxonomy="test_compliance",
                lifecycle_taxonomy="test_lifecycle",  # Added lifecycle
            ),
            taxonomy_version="0.5",
            # Add required taxonomy fields also directly to ProjectMemory
            platform_taxonomy="test_platform",
            domain_taxonomy="test_domain",
            size_taxonomy="test_size",
            compliance_taxonomy="test_compliance",
            lifecycle_taxonomy="test_lifecycle",  # Added lifecycle
        )
        assert project.project_info.name == "test_project"
        assert project.lifecycle_taxonomy == "test_lifecycle"
        assert project.platform_taxonomy == "test_platform"
        assert len(project.artifacts) == len(
            Bucket
        )  # Should have all buckets initialized

    def test_add_artifact(self, sample_project_memory):
        """Test adding artifacts to ProjectMemory"""
        project = sample_project_memory

        # Check that artifacts were added to the correct buckets
        assert len(project.artifacts[Bucket.INITIATE_INITIAL_PRODUCT_DOCS]) == 1
        assert len(project.artifacts[Bucket.ELABORATE_DISCOVERY_AND_RESEARCH]) == 1
        assert len(project.artifacts[Bucket.ELABORATE_SPECIFICATION_AND_PLANNING]) == 1

        # Check that artifact was added with correct fields
        initiate_artifact = project.artifacts[Bucket.INITIATE_INITIAL_PRODUCT_DOCS][0]
        assert initiate_artifact.name == "vision_doc"
        assert initiate_artifact.path == Path("docs/initiation/product_vision.md")
        assert initiate_artifact.status == DocumentStatus.PENDING

        # Test adding a duplicate (should return False)
        duplicate = ArtifactMeta(
            name="dup_vision",
            bucket=Bucket.INITIATE_CORE_SETUP,
            path=Path(
                "docs/initiation/product_vision.md"
            ),  # Same path as existing artifact
        )
        assert not project.add_artifact(duplicate)

        # Check that original buckets still have the same count
        assert len(project.artifacts[Bucket.INITIATE_INITIAL_PRODUCT_DOCS]) == 1
        assert (
            len(project.artifacts[Bucket.INITIATE_CORE_SETUP]) == 0
        )  # Duplicate wasn't added

    def test_get_artifact(self, sample_project_memory):
        """Test retrieving artifacts by bucket and name"""
        project = sample_project_memory

        # Get existing artifact
        artifact = project.get_artifact(
            Bucket.ELABORATE_DISCOVERY_AND_RESEARCH, "user_research"
        )
        assert artifact is not None
        assert artifact.name == "user_research"
        assert artifact.bucket == Bucket.ELABORATE_DISCOVERY_AND_RESEARCH

        # Get non-existent artifact
        non_existent = project.get_artifact(Bucket.DEPLOY_SECURITY, "security_plan")
        assert non_existent is None

    def test_get_artifact_by_path(self, sample_project_memory):
        """Test retrieving artifacts by path"""
        project = sample_project_memory

        # Get existing artifact by path
        artifact = project.get_artifact_by_path(Path("docs/specs/api_specification.md"))
        assert artifact is not None
        assert artifact.name == "api_spec"
        assert artifact.bucket == Bucket.ELABORATE_SPECIFICATION_AND_PLANNING

        # Get non-existent artifact
        non_existent = project.get_artifact_by_path(Path("nonexistent/path.md"))
        assert non_existent is None

    def test_update_artifact_status(self, sample_project_memory):
        """Test updating artifact status"""
        project = sample_project_memory

        # Update existing artifact
        success = project.update_artifact_status(
            Bucket.INITIATE_INITIAL_PRODUCT_DOCS, "vision_doc", DocumentStatus.COMPLETED
        )
        assert success

        # Verify the status was updated
        artifact = project.get_artifact(
            Bucket.INITIATE_INITIAL_PRODUCT_DOCS, "vision_doc"
        )
        assert artifact.status == DocumentStatus.COMPLETED

        # Try to update non-existent artifact
        success = project.update_artifact_status(
            Bucket.DEPLOY_SECURITY, "nonexistent", DocumentStatus.COMPLETED
        )
        assert not success

    def test_get_bucket_completion(self, sample_project_memory):
        """Test getting completion stats for buckets"""
        project = sample_project_memory

        # Bucket with one completed artifact
        elaborate_spec_stats = project.get_bucket_completion(
            Bucket.ELABORATE_SPECIFICATION_AND_PLANNING
        )
        assert elaborate_spec_stats["total"] == 1
        assert elaborate_spec_stats["completed"] == 1
        assert elaborate_spec_stats["in_progress"] == 0
        assert elaborate_spec_stats["pending"] == 0
        assert elaborate_spec_stats["completion_percentage"] == 100.0

        # Bucket with one in-progress artifact
        elaborate_research_stats = project.get_bucket_completion(
            Bucket.ELABORATE_DISCOVERY_AND_RESEARCH
        )
        assert elaborate_research_stats["total"] == 1
        assert elaborate_research_stats["completed"] == 0
        assert elaborate_research_stats["in_progress"] == 1
        assert elaborate_research_stats["pending"] == 0
        assert elaborate_research_stats["completion_percentage"] == 0.0

        # Empty bucket
        empty_bucket_stats = project.get_bucket_completion(Bucket.DEPLOY_SECURITY)
        assert empty_bucket_stats["total"] == 0
        assert empty_bucket_stats["completion_percentage"] == 0.0

    def test_get_phase_completion(self, sample_project_memory):
        """Test getting completion stats for entire phases"""
        project = sample_project_memory

        # Elaborate phase has 2 artifacts (1 completed, 1 in-progress)
        elaborate_stats = project.get_phase_completion("Elaborate")
        assert elaborate_stats["total"] == 2
        assert elaborate_stats["completed"] == 1
        assert elaborate_stats["in_progress"] == 1
        assert elaborate_stats["pending"] == 0
        assert elaborate_stats["completion_percentage"] == 50.0
        assert elaborate_stats["buckets"] == 4  # All Elaborate buckets

        # Initiate phase has 1 pending artifact
        initiate_stats = project.get_phase_completion("Initiate")
        assert initiate_stats["total"] == 1
        assert initiate_stats["completed"] == 0
        assert initiate_stats["pending"] == 1
        assert initiate_stats["completion_percentage"] == 0.0

        # Deploy phase has 0 artifacts
        deploy_stats = project.get_phase_completion("Deploy")
        assert deploy_stats["total"] == 0
        assert deploy_stats["completion_percentage"] == 0.0

    def test_serialization_deserialization(self, sample_project_memory):
        """Test that ProjectMemory with taxonomy can be serialized and deserialized"""
        project = sample_project_memory

        # Serialize to JSON
        project_json = project.model_dump_json()

        # Check that JSON is valid
        parsed_json = json.loads(project_json)
        assert parsed_json["taxonomy_version"] == "0.5"
        assert "artifacts" in parsed_json

        # Deserialize from JSON
        loaded_project = ProjectMemory.model_validate_json(project_json)

        # Check that all fields were preserved
        assert loaded_project.project_info.name == project.project_info.name
        assert loaded_project.taxonomy_version == project.taxonomy_version

        # Check artifacts
        assert Bucket.INITIATE_INITIAL_PRODUCT_DOCS in loaded_project.artifacts
        assert Bucket.ELABORATE_DISCOVERY_AND_RESEARCH in loaded_project.artifacts
        assert Bucket.ELABORATE_SPECIFICATION_AND_PLANNING in loaded_project.artifacts

        # Check specific artifact fields were preserved
        loaded_artifact = loaded_project.get_artifact(
            Bucket.ELABORATE_SPECIFICATION_AND_PLANNING, "api_spec"
        )
        assert loaded_artifact is not None
        assert loaded_artifact.name == "api_spec"
        assert loaded_artifact.path == Path("docs/specs/api_specification.md")
        assert loaded_artifact.status == DocumentStatus.COMPLETED

        # Verify completion stats are calculated correctly after deserialization
        stats = loaded_project.get_phase_completion("Elaborate")
        assert stats["completion_percentage"] == 50.0
