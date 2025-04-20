import logging
from typing import Optional, Dict, List
from pathlib import Path
import datetime
import uuid

from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.exc import IntegrityError

# Ports and Domain Models
from paelladoc.ports.output.memory_port import MemoryPort
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectMetadata,
    ArtifactMeta,
    Bucket,
)

# Database Models for this adapter
from .db_models import ProjectMemoryDB, ArtifactMetaDB

logger = logging.getLogger(__name__)

# Calculate project root based on this file's location
# src/paelladoc/adapters/output/sqlite/sqlite_memory_adapter.py -> project_root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
logger.info(f"Project root calculated as: {PROJECT_ROOT.resolve()}")
# Use the project root directory for the default database path
DEFAULT_DB_PATH = PROJECT_ROOT / "paelladoc_memory.db"
logger.info(f"Default database path set to project root: {DEFAULT_DB_PATH.resolve()}")


class SQLiteMemoryAdapter(MemoryPort):
    """SQLite implementation of the MemoryPort using new MECE/Artifact models."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        logger.info(f"Using database path: {self.db_path.resolve()}")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine_url = f"sqlite+aiosqlite:///{self.db_path.resolve()}"
        logger.info(f"SQLite engine URL: {self.engine_url}")
        self.async_engine = create_async_engine(self.engine_url, echo=False)
        self.AsyncSessionFactory = sessionmaker(
            bind=self.async_engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info(f"SQLiteMemoryAdapter initialized with database at: {self.db_path}")

    async def _create_db_and_tables(self):
        """Creates the database and tables if they don't exist."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables checked/created.")

    # --- Helper for mapping DB to Domain --- #
    def _map_db_to_domain(self, db_memory: ProjectMemoryDB) -> ProjectMemory:
        """Maps the DB model hierarchy to the domain ProjectMemory model."""
        domain_metadata = ProjectMetadata(
            name=db_memory.name,
            language=db_memory.language,
            purpose=db_memory.purpose,
            target_audience=db_memory.target_audience,
            objectives=db_memory.objectives,
            interaction_language=db_memory.interaction_language,
            documentation_language=db_memory.documentation_language,
        )

        # Handle base_path if present, converting from string to Path
        if db_memory.base_path:
            domain_metadata.base_path = Path(db_memory.base_path)

        # Reconstruct the artifacts dictionary from the flat list
        domain_artifacts: Dict[Bucket, List[ArtifactMeta]] = {
            bucket: [] for bucket in Bucket
        }
        for db_artifact in db_memory.artifacts:
            # Ensure timestamps are UTC before creating domain object
            created_at_utc = self.ensure_utc(db_artifact.created_at)  # Ensure UTC
            updated_at_utc = self.ensure_utc(db_artifact.updated_at)  # Ensure UTC

            domain_artifact = ArtifactMeta(
                id=db_artifact.id,
                name=db_artifact.name,
                bucket=db_artifact.bucket,
                path=db_artifact.path_obj,
                created_at=created_at_utc,
                updated_at=updated_at_utc,
                status=db_artifact.status,
            )
            if db_artifact.bucket in domain_artifacts:
                domain_artifacts[db_artifact.bucket].append(domain_artifact)
            else:
                # Should not happen if DB is consistent, but handle defensively
                logger.warning(
                    f"Artifact {db_artifact.id} has unknown bucket {db_artifact.bucket}, placing in UNKNOWN."
                )
                domain_artifacts[Bucket.UNKNOWN].append(domain_artifact)

        # Ensure ProjectMemory timestamps are UTC
        created_at_utc = self.ensure_utc(db_memory.created_at)
        last_updated_at_utc = self.ensure_utc(db_memory.last_updated_at)

        domain_memory = ProjectMemory(
            metadata=domain_metadata,
            artifacts=domain_artifacts,
            taxonomy_version=db_memory.taxonomy_version,
            created_at=created_at_utc,
            last_updated_at=last_updated_at_utc,
        )
        return domain_memory

    # --- MemoryPort Implementation --- #

    async def save_memory(self, memory: ProjectMemory) -> None:
        """Saves the project memory state (including artifacts) to SQLite."""
        project_name = memory.metadata.name
        logger.debug(f"Attempting to save memory for project: {project_name}")
        await self._create_db_and_tables()

        async with self.AsyncSessionFactory() as session:
            try:
                # Check if project exists
                statement = (
                    select(ProjectMemoryDB)
                    .where(ProjectMemoryDB.name == project_name)
                    .options(selectinload(ProjectMemoryDB.artifacts))
                )
                results = await session.execute(statement)
                db_memory = results.scalars().first()

                # Get current UTC time using TimeService
                # Import at the top level or pass as dependency if preferred
                from paelladoc.domain.models.project import time_service

                now = time_service.get_current_time()  # Use TimeService

                memory.update_timestamp()  # This already uses TimeService

                if db_memory:
                    # --- Update Existing Project ---
                    logger.debug(f"Project '{project_name}' found. Updating...")
                    # Use UTC time obtained from TimeService
                    db_memory.last_updated_at = now  # Use UTC time
                    db_memory.language = memory.metadata.language
                    db_memory.purpose = memory.metadata.purpose
                    db_memory.target_audience = memory.metadata.target_audience
                    db_memory.objectives = memory.metadata.objectives
                    db_memory.taxonomy_version = memory.taxonomy_version

                    # Handle new fields
                    db_memory.interaction_language = (
                        memory.metadata.interaction_language
                    )
                    db_memory.documentation_language = (
                        memory.metadata.documentation_language
                    )

                    # Convert Path to string if present
                    if memory.metadata.base_path:
                        db_memory.base_path = str(memory.metadata.base_path)
                    else:
                        db_memory.base_path = None

                    # Sync Artifacts (more complex: compare domain dict with db list)
                    db_artifacts_map: Dict[uuid.UUID, ArtifactMetaDB] = {
                        a.id: a for a in db_memory.artifacts
                    }
                    domain_artifact_ids = set()

                    for bucket, domain_artifact_list in memory.artifacts.items():
                        for domain_artifact in domain_artifact_list:
                            domain_artifact_ids.add(domain_artifact.id)
                            db_artifact = db_artifacts_map.get(domain_artifact.id)

                            if db_artifact:
                                # Update existing artifact in DB
                                db_artifact.name = domain_artifact.name
                                db_artifact.bucket = domain_artifact.bucket
                                db_artifact.path = str(domain_artifact.path)
                                db_artifact.status = domain_artifact.status
                                # Domain model update_timestamp already uses TimeService
                                db_artifact.updated_at = domain_artifact.updated_at
                            else:
                                # Add new artifact to DB
                                # Ensure timestamps are UTC before saving
                                created_at_utc = self.ensure_utc(
                                    domain_artifact.created_at
                                )
                                updated_at_utc = self.ensure_utc(
                                    domain_artifact.updated_at
                                )
                                new_db_artifact = ArtifactMetaDB(
                                    id=domain_artifact.id,
                                    project_memory_id=db_memory.id,
                                    name=domain_artifact.name,
                                    bucket=domain_artifact.bucket,
                                    path=str(domain_artifact.path),
                                    created_at=created_at_utc,
                                    updated_at=updated_at_utc,
                                    status=domain_artifact.status,
                                )
                                session.add(new_db_artifact)

                    # Delete artifacts that are in DB but not in domain model anymore
                    for db_artifact_id, db_artifact in db_artifacts_map.items():
                        if db_artifact_id not in domain_artifact_ids:
                            logger.debug(
                                f"Deleting artifact {db_artifact_id} ({db_artifact.name}) from project {project_name}"
                            )
                            await session.delete(db_artifact)

                    session.add(db_memory)

                else:
                    # --- Create New Project ---
                    logger.debug(f"Project '{project_name}' not found. Creating...")
                    # Ensure domain timestamps are set via TimeService before saving
                    created_at_utc = self.ensure_utc(memory.created_at)
                    last_updated_at_utc = self.ensure_utc(memory.last_updated_at)

                    db_memory = ProjectMemoryDB(
                        name=memory.metadata.name,
                        language=memory.metadata.language,
                        purpose=memory.metadata.purpose,
                        target_audience=memory.metadata.target_audience,
                        objectives=memory.metadata.objectives,
                        taxonomy_version=memory.taxonomy_version,
                        created_at=created_at_utc,  # Use UTC time
                        last_updated_at=last_updated_at_utc,  # Use UTC time
                        artifacts=[],
                        # Add new fields
                        interaction_language=memory.metadata.interaction_language,
                        documentation_language=memory.metadata.documentation_language,
                        # Convert Path to string if present
                        base_path=str(memory.metadata.base_path)
                        if memory.metadata.base_path
                        else None,
                    )
                    session.add(db_memory)
                    await session.flush()

                    # Add all artifacts from the domain model
                    for bucket, domain_artifact_list in memory.artifacts.items():
                        for domain_artifact in domain_artifact_list:
                            # Ensure artifact timestamps are UTC before saving
                            artifact_created_at_utc = self.ensure_utc(
                                domain_artifact.created_at
                            )
                            artifact_updated_at_utc = self.ensure_utc(
                                domain_artifact.updated_at
                            )
                            new_db_artifact = ArtifactMetaDB(
                                id=domain_artifact.id,
                                project_memory_id=db_memory.id,
                                name=domain_artifact.name,
                                bucket=domain_artifact.bucket,
                                path=str(domain_artifact.path),
                                created_at=artifact_created_at_utc,
                                updated_at=artifact_updated_at_utc,
                                status=domain_artifact.status,
                            )
                            session.add(new_db_artifact)

                await session.commit()
                logger.info(f"Successfully saved memory for project: {project_name}")

            except IntegrityError as e:
                await session.rollback()
                logger.error(
                    f"Integrity error saving project '{project_name}': {e}",
                    exc_info=True,
                )
                raise ValueError(
                    f"Project '{project_name}' might already exist or another integrity issue occurred."
                ) from e
            except Exception as e:
                await session.rollback()
                logger.error(
                    f"Unexpected error saving project '{project_name}': {e}",
                    exc_info=True,
                )
                raise

    async def load_memory(self, project_name: str) -> Optional[ProjectMemory]:
        """Loads project memory (including artifacts) from SQLite."""
        logger.debug(f"Attempting to load memory for project: {project_name}")
        await self._create_db_and_tables()

        async with self.AsyncSessionFactory() as session:
            try:
                statement = (
                    select(ProjectMemoryDB)
                    .where(ProjectMemoryDB.name == project_name)
                    .options(selectinload(ProjectMemoryDB.artifacts))
                )
                results = await session.execute(statement)
                db_memory = results.scalars().first()

                if db_memory:
                    logger.debug(
                        f"Found project '{project_name}' in DB, mapping to domain model."
                    )
                    return self._map_db_to_domain(db_memory)
                else:
                    logger.debug(f"Project '{project_name}' not found in DB.")
                    return None
            except Exception as e:
                logger.error(
                    f"Error loading project '{project_name}': {e}", exc_info=True
                )
                return None

    async def project_exists(self, project_name: str) -> bool:
        """Checks if a project memory exists in the SQLite database."""
        logger.debug(f"Checking existence for project: {project_name}")
        await self._create_db_and_tables()

        async with self.AsyncSessionFactory() as session:
            try:
                statement = select(ProjectMemoryDB.id).where(
                    ProjectMemoryDB.name == project_name
                )
                results = await session.execute(statement)
                exists = results.scalars().first() is not None
                logger.debug(f"Project '{project_name}' exists: {exists}")
                return exists
            except Exception as e:
                logger.error(
                    f"Error checking project existence for '{project_name}': {e}",
                    exc_info=True,
                )
                return False

    async def list_projects(self) -> List[str]:
        """Lists the names of all projects stored in the database.

        Returns:
            A list of project names as strings. Empty list if no projects or error.
        """
        logger.debug("Listing all project names from database.")
        await self._create_db_and_tables()

        async with self.AsyncSessionFactory() as session:
            try:
                statement = select(ProjectMemoryDB.name)
                results = await session.execute(statement)
                project_names = results.scalars().all()
                logger.debug(f"Found {len(project_names)} projects.")
                return list(project_names)  # Ensure we return a Python list
            except Exception as e:
                logger.error(
                    f"Error listing projects: {e}", exc_info=True
                )  # Log original error
                # Return empty list on error to be consistent with interface
                return []

    # Add ensure_utc helper method to the adapter
    def ensure_utc(self, dt: datetime.datetime) -> datetime.datetime:
        """Ensure a datetime is in UTC.

        If the datetime has no timezone info, assumes it's in UTC.
        """
        if dt.tzinfo is None:
            return dt.replace(tzinfo=datetime.timezone.utc)
        return dt.astimezone(datetime.timezone.utc)
