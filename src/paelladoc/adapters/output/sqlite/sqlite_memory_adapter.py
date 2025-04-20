"""SQLite adapter for project memory persistence."""

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

# Configuration
from paelladoc.config.database import get_db_path

# Default database path (obtained via config logic)
# DEFAULT_DB_PATH = get_db_path() # No longer needed as constant? __init__ uses get_db_path()

logger = logging.getLogger(__name__)

# Remove redundant/fragile PROJECT_ROOT calculation
# PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
# logger.info(f"Project root calculated as: {PROJECT_ROOT.resolve()}")
# DEFAULT_DB_PATH = PROJECT_ROOT / "paelladoc_memory.db"
# logger.info(f"Default database path set to: {DEFAULT_DB_PATH.resolve()}")


class SQLiteMemoryAdapter(MemoryPort):
    """SQLite implementation of the MemoryPort using new MECE/Artifact models."""

    # Keep __init__ from HEAD (using get_db_path)
    def __init__(self, db_path: str | Path | None = None):
        """
        Initialize the SQLite adapter.

        Args:
            db_path: Optional custom database path. If not provided, uses the configured default.
        """
        self.db_path = Path(db_path) if db_path else get_db_path()
        logger.info(
            f"Initializing SQLite adapter with database path: {self.db_path.resolve()}"
        )

        # Ensure the parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Create async engine
        self.async_engine = create_async_engine(
            f"sqlite+aiosqlite:///{self.db_path}",
            echo=False,  # Set to True for SQL query logging
            connect_args={"check_same_thread": False},  # Necessary for SQLite async
        )

        # Create async session factory (named async_session)
        self.async_session = sessionmaker(
            self.async_engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info("SQLiteMemoryAdapter initialized.")

    async def _create_db_and_tables(self):
        """Creates the database and tables if they don't exist."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables checked/created.")

    # --- Helper for mapping DB to Domain --- #
    # This mapping logic should ideally move to a separate mapper module/class (SOLID)
    # For now, keep it here, but ensure ensure_utc is removed later.
    def _map_db_to_domain(self, db_memory: ProjectMemoryDB) -> ProjectMemory:
        """Maps the DB model hierarchy to the domain ProjectMemory model."""

        # TODO: Replace ensure_utc calls here if it's moved
        # For now, define it locally if needed, or assume timestamps are ok
        def _ensure_utc_local(dt: datetime.datetime) -> datetime.datetime:
            if dt.tzinfo is None:
                return dt.replace(tzinfo=datetime.timezone.utc)
            return dt.astimezone(datetime.timezone.utc)

        domain_metadata = ProjectMetadata(
            name=db_memory.name,
            language=db_memory.language,
            purpose=db_memory.purpose,
            target_audience=db_memory.target_audience,
            objectives=db_memory.objectives,
            interaction_language=db_memory.interaction_language,
            documentation_language=db_memory.documentation_language,
        )

        if db_memory.base_path:
            domain_metadata.base_path = Path(db_memory.base_path)

        domain_artifacts: Dict[Bucket, List[ArtifactMeta]] = {
            bucket: [] for bucket in Bucket
        }
        for db_artifact in db_memory.artifacts:
            created_at_utc = _ensure_utc_local(db_artifact.created_at)
            updated_at_utc = _ensure_utc_local(db_artifact.updated_at)

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
                logger.warning(
                    f"Artifact {db_artifact.id} has unknown bucket {db_artifact.bucket}, placing in UNKNOWN."
                )
                domain_artifacts[Bucket.UNKNOWN].append(domain_artifact)

        created_at_utc = _ensure_utc_local(db_memory.created_at)
        last_updated_at_utc = _ensure_utc_local(db_memory.last_updated_at)

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

        # TODO: Use mapper if refactored
        def _ensure_utc_local(dt: datetime.datetime) -> datetime.datetime:
            if dt.tzinfo is None:
                return dt.replace(tzinfo=datetime.timezone.utc)
            return dt.astimezone(datetime.timezone.utc)

        project_name = memory.metadata.name
        logger.debug(f"Attempting to save memory for project: {project_name}")
        await self._create_db_and_tables()

        async with self.async_session() as session:
            try:
                statement = (
                    select(ProjectMemoryDB)
                    .where(ProjectMemoryDB.name == project_name)
                    .options(selectinload(ProjectMemoryDB.artifacts))
                )
                results = await session.execute(statement)
                db_memory = results.scalars().first()

                # now = time_service.get_current_time() # Removed as unused
                memory.update_timestamp()

                if db_memory:
                    logger.debug(f"Project '{project_name}' found. Updating...")
                    db_memory.last_updated_at = _ensure_utc_local(
                        memory.last_updated_at
                    )
                    db_memory.language = memory.metadata.language
                    db_memory.purpose = memory.metadata.purpose
                    db_memory.target_audience = memory.metadata.target_audience
                    db_memory.objectives = memory.metadata.objectives
                    db_memory.taxonomy_version = memory.taxonomy_version
                    db_memory.interaction_language = (
                        memory.metadata.interaction_language
                    )
                    db_memory.documentation_language = (
                        memory.metadata.documentation_language
                    )
                    db_memory.base_path = (
                        str(memory.metadata.base_path)
                        if memory.metadata.base_path
                        else None
                    )

                    db_artifacts_map: Dict[uuid.UUID, ArtifactMetaDB] = {
                        a.id: a for a in db_memory.artifacts
                    }
                    domain_artifact_ids = set()

                    for bucket, domain_artifact_list in memory.artifacts.items():
                        for domain_artifact in domain_artifact_list:
                            domain_artifact_ids.add(domain_artifact.id)
                            db_artifact = db_artifacts_map.get(domain_artifact.id)

                            if db_artifact:
                                db_artifact.name = domain_artifact.name
                                db_artifact.bucket = domain_artifact.bucket
                                db_artifact.path = str(domain_artifact.path)
                                db_artifact.status = domain_artifact.status
                                db_artifact.updated_at = _ensure_utc_local(
                                    domain_artifact.updated_at
                                )
                            else:
                                created_at_utc = _ensure_utc_local(
                                    domain_artifact.created_at
                                )
                                updated_at_utc = _ensure_utc_local(
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

                    for db_artifact_id, db_artifact in db_artifacts_map.items():
                        if db_artifact_id not in domain_artifact_ids:
                            logger.debug(
                                f"Deleting artifact {db_artifact_id} ({db_artifact.name}) from project {project_name}"
                            )
                            await session.delete(db_artifact)

                    session.add(db_memory)

                else:
                    logger.debug(f"Project '{project_name}' not found. Creating...")
                    created_at_utc = _ensure_utc_local(memory.created_at)
                    last_updated_at_utc = _ensure_utc_local(memory.last_updated_at)

                    db_memory = ProjectMemoryDB(
                        name=memory.metadata.name,
                        language=memory.metadata.language,
                        purpose=memory.metadata.purpose,
                        target_audience=memory.metadata.target_audience,
                        objectives=memory.metadata.objectives,
                        taxonomy_version=memory.taxonomy_version,
                        created_at=created_at_utc,
                        last_updated_at=last_updated_at_utc,
                        artifacts=[],
                        interaction_language=memory.metadata.interaction_language,
                        documentation_language=memory.metadata.documentation_language,
                        base_path=str(memory.metadata.base_path)
                        if memory.metadata.base_path
                        else None,
                    )
                    session.add(db_memory)
                    await session.flush()

                    for bucket, domain_artifact_list in memory.artifacts.items():
                        for domain_artifact in domain_artifact_list:
                            artifact_created_at_utc = _ensure_utc_local(
                                domain_artifact.created_at
                            )
                            artifact_updated_at_utc = _ensure_utc_local(
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

        async with self.async_session() as session:
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

        async with self.async_session() as session:
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

        # Keep HEAD's sessionmaker name
        async with self.async_session() as session:
            try:
                statement = select(ProjectMemoryDB.name)
                results = await session.execute(statement)
                project_names = results.scalars().all()
                logger.debug(f"Found {len(project_names)} projects.")
                return list(project_names)
            except Exception as e:
                logger.error(f"Error listing projects: {e}", exc_info=True)
                return []

    # Remove ensure_utc helper method from the adapter (should be in mapper)
    # def ensure_utc(self, dt: datetime.datetime) -> datetime.datetime:
    #     ...
