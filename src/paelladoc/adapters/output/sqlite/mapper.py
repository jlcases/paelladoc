"""
Mapping functions between domain models and SQLite DB models.
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path
import datetime
import uuid

# Domain Models
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
    ArtifactMeta,
    Bucket,  # Import if needed for mapping logic (e.g., default status)
)

# Database Models
from .db_models import ProjectMemoryDB, ArtifactMetaDB

logger = logging.getLogger(__name__)


def _ensure_utc(dt: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
    """Ensures a datetime object is UTC, converting naive datetimes."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        # Assume naive datetimes from DB are UTC, or handle conversion if needed
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)


def map_db_to_domain(db_memory: ProjectMemoryDB) -> ProjectMemory:
    """Maps a ProjectMemoryDB instance to a ProjectMemory domain model."""
    # Map ProjectInfo
    domain_project_info = ProjectInfo(
        name=db_memory.name,
        language=db_memory.language,
        purpose=db_memory.purpose,
        target_audience=db_memory.target_audience,
        objectives=db_memory.objectives or [],
        base_path=Path(db_memory.base_path) if db_memory.base_path else None,
        interaction_language=db_memory.interaction_language,
        documentation_language=db_memory.documentation_language,
        taxonomy_version=db_memory.taxonomy_version,
        # Map taxonomy fields
        platform_taxonomy=db_memory.platform_taxonomy,
        domain_taxonomy=db_memory.domain_taxonomy,
        size_taxonomy=db_memory.size_taxonomy,
        compliance_taxonomy=db_memory.compliance_taxonomy,
        lifecycle_taxonomy=db_memory.lifecycle_taxonomy,
        custom_taxonomy=db_memory.custom_taxonomy or {},
        taxonomy_validation=db_memory.taxonomy_validation or {},
    )

    # Map Artifacts
    domain_artifacts: Dict[Bucket, List[ArtifactMeta]] = {}
    if db_memory.artifacts:
        for db_artifact in db_memory.artifacts:
            bucket = db_artifact.bucket
            if bucket not in domain_artifacts:
                domain_artifacts[bucket] = []
            domain_artifacts[bucket].append(
                ArtifactMeta(
                    id=db_artifact.id,
                    name=db_artifact.name,
                    bucket=bucket,
                    path=Path(db_artifact.path) if db_artifact.path else None,
                    created_at=_ensure_utc(db_artifact.created_at),
                    updated_at=_ensure_utc(db_artifact.updated_at),
                    created_by=db_artifact.created_by,
                    modified_by=db_artifact.modified_by,
                    status=db_artifact.status,
                )
            )

    # Create the domain model
    return ProjectMemory(
        project_info=domain_project_info,
        # Assuming the old 'documents' field is not needed or handled separately
        # documents={}, # If needed, map from a potential documents JSON field
        artifacts=domain_artifacts,
        taxonomy_version=db_memory.taxonomy_version,
        created_at=_ensure_utc(db_memory.created_at),
        last_updated_at=_ensure_utc(db_memory.last_updated_at),
        created_by=db_memory.created_by,
        modified_by=db_memory.modified_by,
        # Map taxonomy fields directly to ProjectMemory as well
        platform_taxonomy=db_memory.platform_taxonomy,
        domain_taxonomy=db_memory.domain_taxonomy,
        size_taxonomy=db_memory.size_taxonomy,
        compliance_taxonomy=db_memory.compliance_taxonomy,
        lifecycle_taxonomy=db_memory.lifecycle_taxonomy,
        custom_taxonomy=db_memory.custom_taxonomy or {},
        taxonomy_validation=db_memory.taxonomy_validation or {},
    )


def map_domain_artifact_to_db(
    domain_artifact: ArtifactMeta, project_memory_id: Optional[uuid.UUID] = None
) -> ArtifactMetaDB:
    """Maps a domain ArtifactMeta to a DB ArtifactMetaDB."""
    return ArtifactMetaDB(
        id=domain_artifact.id,
        project_memory_id=project_memory_id,
        name=domain_artifact.name,
        bucket=domain_artifact.bucket,
        path=str(domain_artifact.path),
        created_at=_ensure_utc(domain_artifact.created_at)
        if domain_artifact.created_at
        else datetime.datetime.now(datetime.timezone.utc),
        updated_at=_ensure_utc(domain_artifact.updated_at)
        if domain_artifact.updated_at
        else datetime.datetime.now(datetime.timezone.utc),
        created_by=domain_artifact.created_by,
        modified_by=domain_artifact.modified_by,
        status=domain_artifact.status,
    )


def map_domain_to_db(
    domain_memory: ProjectMemory, existing_db_model: Optional[ProjectMemoryDB] = None
) -> ProjectMemoryDB:
    """Maps a ProjectMemory domain model to a ProjectMemoryDB instance, excluding artifacts."""
    if existing_db_model:
        db_memory = existing_db_model
    else:
        db_memory = ProjectMemoryDB()
        # Set ID for new object if domain object has one (e.g., from deserialization)
        # Otherwise, rely on DB default_factory
        # db_memory.id = domain_memory.id # Assuming ProjectMemory doesn't have an ID field directly

    # Map fields from ProjectInfo
    if domain_memory.project_info:
        db_memory.name = domain_memory.project_info.name
        db_memory.language = domain_memory.project_info.language
        db_memory.purpose = domain_memory.project_info.purpose
        db_memory.target_audience = domain_memory.project_info.target_audience
        db_memory.objectives = domain_memory.project_info.objectives
        db_memory.base_path = (
            str(domain_memory.project_info.base_path)
            if domain_memory.project_info.base_path
            else None
        )
        db_memory.interaction_language = domain_memory.project_info.interaction_language
        db_memory.documentation_language = (
            domain_memory.project_info.documentation_language
        )
        db_memory.taxonomy_version = (
            domain_memory.taxonomy_version
        )  # Use ProjectMemory version
        db_memory.platform_taxonomy = domain_memory.project_info.platform_taxonomy
        db_memory.domain_taxonomy = domain_memory.project_info.domain_taxonomy
        db_memory.size_taxonomy = domain_memory.project_info.size_taxonomy
        db_memory.compliance_taxonomy = domain_memory.project_info.compliance_taxonomy
        db_memory.lifecycle_taxonomy = domain_memory.project_info.lifecycle_taxonomy
        db_memory.custom_taxonomy = domain_memory.project_info.custom_taxonomy
        db_memory.taxonomy_validation = domain_memory.project_info.taxonomy_validation

    # Map top-level fields from ProjectMemory (overwriting if needed)
    db_memory.taxonomy_version = domain_memory.taxonomy_version
    db_memory.created_at = (
        _ensure_utc(domain_memory.created_at)
        if domain_memory.created_at and not existing_db_model  # Only set on creation
        else (
            existing_db_model.created_at
            if existing_db_model
            else datetime.datetime.now(datetime.timezone.utc)
        )
    )
    db_memory.last_updated_at = datetime.datetime.now(datetime.timezone.utc)
    db_memory.created_by = domain_memory.created_by
    db_memory.modified_by = domain_memory.modified_by

    # Map taxonomy fields directly from ProjectMemory (ensure these overwrite ProjectInfo ones)
    db_memory.platform_taxonomy = domain_memory.platform_taxonomy
    db_memory.domain_taxonomy = domain_memory.domain_taxonomy
    db_memory.size_taxonomy = domain_memory.size_taxonomy
    db_memory.compliance_taxonomy = domain_memory.compliance_taxonomy
    db_memory.lifecycle_taxonomy = domain_memory.lifecycle_taxonomy
    db_memory.custom_taxonomy = domain_memory.custom_taxonomy
    db_memory.taxonomy_validation = domain_memory.taxonomy_validation

    # DO NOT map artifacts here, handled by sync_artifacts_db

    return db_memory


def sync_artifacts_db(
    session,  # Pass the SQLAlchemy session
    domain_memory: ProjectMemory,
    db_memory: ProjectMemoryDB,  # The DB object being saved (might be new or existing)
    existing_db_memory: Optional[
        ProjectMemoryDB
    ],  # The state loaded from DB (if exists)
) -> List[ArtifactMetaDB]:  # Return list of artifacts to delete
    """
    Synchronizes the ArtifactMetaDB entries based on the domain model's artifacts.
    Should be called within the adapter's session context after the ProjectMemoryDB
    object exists and has an ID.
    Returns a list of ArtifactMetaDB objects that should be deleted.
    """

    if not db_memory.id:
        logger.error("Cannot sync artifacts: ProjectMemoryDB object has no ID.")
        raise ValueError("ProjectMemoryDB must have an ID before syncing artifacts.")

    # Base the current DB state on the eager-loaded existing_db_memory if available
    if existing_db_memory and existing_db_memory.artifacts is not None:
        db_artifacts_map: Dict[uuid.UUID, ArtifactMetaDB] = {
            a.id: a for a in existing_db_memory.artifacts
        }
    else:
        db_artifacts_map: Dict[uuid.UUID, ArtifactMetaDB] = {}  # No existing artifacts

    domain_artifact_ids = set()
    artifacts_to_add = []
    artifacts_to_delete = []

    for bucket, domain_artifact_list in domain_memory.artifacts.items():
        for domain_artifact in domain_artifact_list:
            if not isinstance(domain_artifact, ArtifactMeta):
                logger.warning(
                    f"Skipping non-ArtifactMeta item found in domain artifacts: {domain_artifact}"
                )
                continue

            domain_artifact_ids.add(domain_artifact.id)
            db_artifact = db_artifacts_map.get(domain_artifact.id)

            if db_artifact:
                # Update existing artifact fields found in the map
                db_artifact.name = domain_artifact.name
                db_artifact.bucket = domain_artifact.bucket
                db_artifact.path = str(domain_artifact.path)
                db_artifact.status = domain_artifact.status
                db_artifact.updated_at = _ensure_utc(
                    domain_artifact.updated_at
                ) or datetime.datetime.now(datetime.timezone.utc)
                db_artifact.modified_by = domain_artifact.modified_by
                # IMPORTANT: Add the updated artifact to the session if its state changed
                # This might be implicitly handled by modifying the object while attached?
                # session.add(db_artifact) # Usually not needed for updates on attached objects
            else:
                # Artifact exists in domain but not in the loaded DB state -> Add it
                new_db_artifact = map_domain_artifact_to_db(
                    domain_artifact, project_memory_id=db_memory.id
                )
                artifacts_to_add.append(new_db_artifact)

    # Identify artifacts to delete (present in DB map but not in domain IDs)
    for db_artifact_id, db_artifact in db_artifacts_map.items():
        if db_artifact_id not in domain_artifact_ids:
            artifacts_to_delete.append(db_artifact)

    # Add new artifacts to the session
    if artifacts_to_add:
        session.add_all(artifacts_to_add)
        logger.debug(
            f"Adding {len(artifacts_to_add)} new artifacts to session for project {db_memory.name}."
        )

    # Return artifacts to be deleted by the caller (adapter)
    return artifacts_to_delete
