from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
import datetime
from pathlib import Path
import uuid
from .enums import DocumentStatus, Bucket
from ..services.time_service import TimeService

# Singleton instance of the time service
# This will be injected by the application layer
time_service: TimeService = None


def set_time_service(service: TimeService):
    """Set the time service instance to be used by the domain models."""
    global time_service
    time_service = service


class ProjectDocument(BaseModel):
    name: str  # e.g., "README.md", "CONTRIBUTING.md"
    template_origin: Optional[str] = None  # Path or identifier of the template used
    status: DocumentStatus = DocumentStatus.PENDING


class ArtifactMeta(BaseModel):
    """Metadata for an artifact categorized according to the MECE taxonomy"""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    bucket: Bucket
    path: Path  # Relative path from project root
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    status: DocumentStatus = DocumentStatus.PENDING

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not time_service:
            raise RuntimeError("TimeService not initialized")

        now = time_service.get_current_time()
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now

        if self.created_by is not None and self.modified_by is None:
            self.modified_by = self.created_by

    def update_timestamp(self, modifier: Optional[str] = None):
        if not time_service:
            raise RuntimeError("TimeService not initialized")
        self.updated_at = time_service.get_current_time()
        if modifier:
            self.modified_by = modifier

    def update_status(self, status: DocumentStatus, modifier: Optional[str] = None):
        self.status = status
        self.update_timestamp(modifier=modifier)


class ProjectMetadata(BaseModel):
    name: str = Field(..., description="Unique name of the project")
    language: Optional[str] = None
    purpose: Optional[str] = None
    target_audience: Optional[str] = None
    objectives: Optional[List[str]] = None
    base_path: Optional[Path] = None
    interaction_language: Optional[str] = None
    documentation_language: Optional[str] = None
    # Add other relevant metadata fields as needed


class ProjectMemory(BaseModel):
    metadata: ProjectMetadata
    documents: Dict[str, ProjectDocument] = {}  # Dict key is document name/path
    # New taxonomy-based structure
    taxonomy_version: str = "0.5"
    artifacts: Dict[Bucket, List[ArtifactMeta]] = Field(
        default_factory=lambda: {bucket: [] for bucket in Bucket}
    )
    # Consider adding: achievements, issues, decisions later?
    created_at: datetime.datetime = None
    last_updated_at: datetime.datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        if not time_service:
            raise RuntimeError("TimeService not initialized")
        if self.created_at is None:
            self.created_at = time_service.get_current_time()
        if self.last_updated_at is None:
            self.last_updated_at = time_service.get_current_time()

    def update_timestamp(self):
        if not time_service:
            raise RuntimeError("TimeService not initialized")
        self.last_updated_at = time_service.get_current_time()

    def get_document(self, name: str) -> Optional[ProjectDocument]:
        return self.documents.get(name)

    def update_document_status(self, name: str, status: DocumentStatus):
        doc = self.get_document(name)
        if doc:
            doc.status = status
            self.update_timestamp()
        else:
            # TODO: Decide error handling (log or raise?)
            # For now, just pass
            # Consider logging: logger.warning(
            #     f"Attempted to update status for non-existent doc: {name}"
            # )
            pass

    def add_document(self, doc: ProjectDocument):
        if doc.name not in self.documents:
            self.documents[doc.name] = doc
            self.update_timestamp()
        else:
            # TODO: Decide error handling (log or raise?)
            # For now, just pass
            # Consider logging: logger.warning(
            #     f"Attempted to add duplicate document: {doc.name}"
            # )
            pass

    # New methods for artifact management
    def get_artifact(self, bucket: Bucket, name: str) -> Optional[ArtifactMeta]:
        """Get an artifact by bucket and name"""
        for artifact in self.artifacts.get(bucket, []):
            if artifact.name == name:
                return artifact
        return None

    def get_artifact_by_path(self, path: Path) -> Optional[ArtifactMeta]:
        """Get an artifact by path, searching across all buckets"""
        path_str = str(path)
        for bucket_artifacts in self.artifacts.values():
            for artifact in bucket_artifacts:
                if str(artifact.path) == path_str:
                    return artifact
        return None

    def add_artifact(self, artifact: ArtifactMeta) -> bool:
        """Add artifact to the appropriate bucket.

        Returns:
            bool: True if added, False if duplicate path exists.
        """
        bucket = artifact.bucket
        if bucket not in self.artifacts:
            self.artifacts[bucket] = []

        # Check if artifact with same path already exists in any bucket
        existing = self.get_artifact_by_path(artifact.path)
        if existing:
            # TODO: Decide error handling (log or raise?)
            # For now, just return False
            return False

        self.artifacts[bucket].append(artifact)
        self.update_timestamp()
        return True

    def update_artifact_status(
        self,
        bucket: Bucket,
        name: str,
        status: DocumentStatus,
        modifier: Optional[str] = None,
    ) -> bool:
        """Update an artifact's status. Returns True if updated, False if not found."""
        artifact = self.get_artifact(bucket, name)
        if artifact:
            artifact.update_status(status, modifier=modifier)
            self.update_timestamp()
            return True
        return False

    def get_bucket_completion(self, bucket: Bucket) -> dict:
        """Get completion stats for a bucket"""
        artifacts = self.artifacts.get(bucket, [])
        total = len(artifacts)
        completed = sum(1 for a in artifacts if a.status == DocumentStatus.COMPLETED)
        in_progress = sum(
            1 for a in artifacts if a.status == DocumentStatus.IN_PROGRESS
        )
        pending = total - completed - in_progress

        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "completion_percentage": (completed / total * 100) if total > 0 else 0,
        }

    def get_phase_completion(self, phase: str) -> dict:
        """Get completion stats for an entire phase"""
        phase_buckets = Bucket.get_phase_buckets(phase)

        total = 0
        completed = 0
        in_progress = 0

        for bucket in phase_buckets:
            stats = self.get_bucket_completion(bucket)
            total += stats["total"]
            completed += stats["completed"]
            in_progress += stats["in_progress"]

        pending = total - completed - in_progress

        return {
            "phase": phase,
            "buckets": len(phase_buckets),
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "completion_percentage": (completed / total * 100) if total > 0 else 0,
        }
