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
    """Maps the DB model hierarchy to the domain ProjectMemory model."""

    # Map ProjectInfo (formerly metadata)
    domain_project_info = ProjectInfo(
        name=db_memory.name,
        language=db_memory.language,
        purpose=db_memory.purpose,
        target_audience=db_memory.target_audience,
        objectives=db_memory.objectives
        if db_memory.objectives
        else [],  # Handle potential None from DB
        base_path=Path(db_memory.base_path) if db_memory.base_path else None,
        interaction_language=db_memory.interaction_language,
        documentation_language=db_memory.documentation_language,
        taxonomy_version=db_memory.taxonomy_version,
        platform_taxonomy=db_memory.platform_taxonomy,
        domain_taxonomy=db_memory.domain_taxonomy,
        size_taxonomy=db_memory.size_taxonomy,
        compliance_taxonomy=db_memory.compliance_taxonomy,
        custom_taxonomy=db_memory.custom_taxonomy
        if db_memory.custom_taxonomy
        else {},  # Handle potential None
        taxonomy_validation=db_memory.taxonomy_validation
        if db_memory.taxonomy_validation
        else {},  # Handle potential None
    )

    # Map Artifacts
    domain_artifacts: Dict[Bucket, List[ArtifactMeta]] = {
        bucket: []
        for bucket in Bucket  # Initialize all buckets
    }
    if db_memory.artifacts:  # Check if artifacts relationship is loaded/exists
        for db_artifact in db_memory.artifacts:
            try:
                # Attempt to get the bucket enum member; default to UNKNOWN if invalid
                bucket_enum = Bucket(db_artifact.bucket)
            except ValueError:
                logger.warning(
                    f"Artifact {db_artifact.id} has invalid bucket value '{db_artifact.bucket}' stored in DB. Mapping to UNKNOWN."
                )
                bucket_enum = Bucket.UNKNOWN

            domain_artifact = ArtifactMeta(
                id=db_artifact.id,
                name=db_artifact.name,
                bucket=bucket_enum,
                path=Path(db_artifact.path),  # Use path string directly
                created_at=_ensure_utc(db_artifact.created_at),
                updated_at=_ensure_utc(db_artifact.updated_at),
                created_by=db_artifact.created_by,
                modified_by=db_artifact.modified_by,
                status=db_artifact.status,
            )
            # Append to the correct bucket list, handle UNKNOWN explicitly if needed elsewhere
            domain_artifacts[bucket_enum].append(domain_artifact)

    # Remove empty buckets if desired (or keep them as per domain logic)
    # domain_artifacts = {k: v for k, v in domain_artifacts.items() if v}

    # Assemble the final domain ProjectMemory object
    domain_memory = ProjectMemory(
        project_info=domain_project_info,
        artifacts=domain_artifacts,
        taxonomy_version=db_memory.taxonomy_version,
        created_at=_ensure_utc(db_memory.created_at),
        last_updated_at=_ensure_utc(db_memory.last_updated_at),
        created_by=db_memory.created_by,
        modified_by=db_memory.modified_by,
        # Map taxonomy fields from ProjectMemoryDB to ProjectMemory
        platform_taxonomy=db_memory.platform_taxonomy,
        domain_taxonomy=db_memory.domain_taxonomy,
        size_taxonomy=db_memory.size_taxonomy,
        compliance_taxonomy=db_memory.compliance_taxonomy,
        custom_taxonomy=db_memory.custom_taxonomy if db_memory.custom_taxonomy else {},
        taxonomy_validation=db_memory.taxonomy_validation
        if db_memory.taxonomy_validation
        else {},
    )

    return domain_memory


def map_domain_to_db(
    domain_memory: ProjectMemory, existing_db_memory: Optional[ProjectMemoryDB] = None
) -> ProjectMemoryDB:
    """
    Maps the domain ProjectMemory model to a ProjectMemoryDB model.
    Handles both creating a new DB object and updating an existing one.
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    # --- Map Project Info / Top-Level Fields ---
    project_info = domain_memory.project_info
    if existing_db_memory:
        db_memory = existing_db_memory
        # Update fields from ProjectInfo
        db_memory.language = project_info.language
        db_memory.purpose = project_info.purpose
        db_memory.target_audience = project_info.target_audience
        db_memory.objectives = project_info.objectives
        db_memory.base_path = (
            str(project_info.base_path) if project_info.base_path else None
        )
        db_memory.interaction_language = project_info.interaction_language
        db_memory.documentation_language = project_info.documentation_language
        # Update fields from ProjectMemory
        db_memory.taxonomy_version = domain_memory.taxonomy_version
        db_memory.last_updated_at = (
            _ensure_utc(domain_memory.last_updated_at) or now_utc
        )
        db_memory.modified_by = domain_memory.modified_by
        db_memory.platform_taxonomy = domain_memory.platform_taxonomy
        db_memory.domain_taxonomy = domain_memory.domain_taxonomy
        db_memory.size_taxonomy = domain_memory.size_taxonomy
        db_memory.compliance_taxonomy = domain_memory.compliance_taxonomy
        db_memory.custom_taxonomy = domain_memory.custom_taxonomy
        db_memory.taxonomy_validation = domain_memory.taxonomy_validation

    else:
        # Create new ProjectMemoryDB
        db_memory = ProjectMemoryDB(
            name=project_info.name,
            language=project_info.language,
            purpose=project_info.purpose,
            target_audience=project_info.target_audience,
            objectives=project_info.objectives,
            base_path=str(project_info.base_path) if project_info.base_path else None,
            interaction_language=project_info.interaction_language,
            documentation_language=project_info.documentation_language,
            taxonomy_version=domain_memory.taxonomy_version,
            created_at=_ensure_utc(domain_memory.created_at) or now_utc,
            last_updated_at=_ensure_utc(domain_memory.last_updated_at) or now_utc,
            created_by=domain_memory.created_by,
            modified_by=domain_memory.modified_by,
            platform_taxonomy=domain_memory.platform_taxonomy,
            domain_taxonomy=domain_memory.domain_taxonomy,
            size_taxonomy=domain_memory.size_taxonomy,
            compliance_taxonomy=domain_memory.compliance_taxonomy,
            custom_taxonomy=domain_memory.custom_taxonomy,
            taxonomy_validation=domain_memory.taxonomy_validation,
            artifacts=[],  # Initialize relationship list
        )

    # --- Map Artifacts ---
    # This logic needs the db_memory.id if creating new artifacts,
    # so it's better handled within the adapter's session context after flushing.
    # This function will return the populated/updated ProjectMemoryDB *without*
    # fully resolved artifacts if it's a new object. The adapter will handle artifact sync.
    # If updating, we can potentially return the artifact list structure needed?
    # For simplicity, let's return the main object mapping and let the adapter handle artifact sync.

    return db_memory


def sync_artifacts_db(
    session,  # Pass the SQLAlchemy session
    domain_memory: ProjectMemory,
    db_memory: ProjectMemoryDB,  # Assumes db_memory exists and has an ID
) -> None:
    """
    Synchronizes the ArtifactMetaDB entries based on the domain model's artifacts.
    This function should be called within the adapter's session context *after*
    the ProjectMemoryDB object exists and has an ID (i.e., after adding and flushing if new).

    Args:
        session: The active SQLAlchemy AsyncSession.
        domain_memory: The source domain model.
        db_memory: The target database model (must have an ID).
    """

    if not db_memory.id:
        logger.error("Cannot sync artifacts: ProjectMemoryDB object has no ID.")
        # Or raise an error?
        return

    # Use eager loading if artifacts aren't already loaded
    # This check might be redundant depending on how db_memory was obtained
    if "artifacts" not in db_memory.__dict__:  # Basic check if relationship is loaded
        logger.warning(
            "Artifacts relationship not loaded on db_memory. Explicit loading might be needed."
        )
        # Potentially load it here if necessary, but ideally it's loaded beforehand
        # await session.refresh(db_memory, attribute_names=['artifacts'])

    db_artifacts_map: Dict[uuid.UUID, ArtifactMetaDB] = {
        a.id: a for a in db_memory.artifacts
    }
    domain_artifact_ids = set()
    artifacts_to_add = []
    artifacts_to_delete = []

    for bucket, domain_artifact_list in domain_memory.artifacts.items():
        for domain_artifact in domain_artifact_list:
            if not isinstance(domain_artifact, ArtifactMeta):
                logger.warning(
                    f"Skipping non-ArtifactMeta item found in domain artifacts: {domain_artifact}"
                )
                continue  # Skip if somehow a non-artifact is in the list

            domain_artifact_ids.add(domain_artifact.id)
            db_artifact = db_artifacts_map.get(domain_artifact.id)

            if db_artifact:
                # Update existing artifact
                db_artifact.name = domain_artifact.name
                db_artifact.bucket = domain_artifact.bucket  # Store enum directly
                db_artifact.path = str(domain_artifact.path)
                db_artifact.status = domain_artifact.status  # Store enum directly
                db_artifact.updated_at = _ensure_utc(
                    domain_artifact.updated_at
                ) or datetime.datetime.now(datetime.timezone.utc)
                db_artifact.modified_by = domain_artifact.modified_by
                # No need to add to session explicitly if object is already managed
            else:
                # Create new artifact DB object
                new_db_artifact = ArtifactMetaDB(
                    id=domain_artifact.id,
                    project_memory_id=db_memory.id,  # Link to parent
                    name=domain_artifact.name,
                    bucket=domain_artifact.bucket,
                    path=str(domain_artifact.path),
                    created_at=_ensure_utc(domain_artifact.created_at)
                    or datetime.datetime.now(datetime.timezone.utc),
                    updated_at=_ensure_utc(domain_artifact.updated_at)
                    or datetime.datetime.now(datetime.timezone.utc),
                    created_by=domain_artifact.created_by,
                    modified_by=domain_artifact.modified_by,
                    status=domain_artifact.status,
                )
                artifacts_to_add.append(new_db_artifact)

    # Identify artifacts to delete
    for db_artifact_id, db_artifact in db_artifacts_map.items():
        if db_artifact_id not in domain_artifact_ids:
            artifacts_to_delete.append(db_artifact)

    # Perform session operations (caller should handle commit/rollback)
    if artifacts_to_add:
        session.add_all(artifacts_to_add)
        logger.debug(
            f"Adding {len(artifacts_to_add)} new artifacts to session for project {db_memory.name}."
        )

    # Deleting requires awaiting async session.delete for each
    # This needs to be done carefully within the async context of the adapter
    # This function CANNOT await session.delete directly if it's synchronous.
    # Let's return the list of objects to delete.

    # Instead of deleting here, return the list to the async adapter method
    # for artifact_to_delete in artifacts_to_delete:
    #     logger.debug(f"Marking artifact {artifact_to_delete.id} ({artifact_to_delete.name}) for deletion from project {db_memory.name}.")
    #     # await session.delete(artifact_to_delete) # Cannot do async op here

    return artifacts_to_delete  # Return list of DB objects to be deleted by the caller
