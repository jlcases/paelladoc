"""SQLite adapter for project memory persistence."""

import logging
from typing import Optional, List
from pathlib import Path

from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.exc import IntegrityError

# Ports and Domain Models
from paelladoc.ports.output.memory_port import MemoryPort
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
)

# Database Models for this adapter
from .db_models import ProjectMemoryDB

# Import the new mapper functions
from .mapper import map_db_to_domain, map_domain_to_db, sync_artifacts_db

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

    # --- MemoryPort Implementation --- #

    async def save_memory(self, memory: ProjectMemory) -> None:
        """Saves the project memory state (including artifacts) to SQLite using the mapper."""
        project_name = memory.project_info.name
        logger.debug(f"Attempting to save memory for project: {project_name}")
        await self._create_db_and_tables()

        async with self.async_session() as session:
            async with (
                session.begin()
            ):  # Use session.begin() for transaction management
                try:
                    # Try to load existing DB object WITH artifacts
                    statement = (
                        select(ProjectMemoryDB)
                        .where(ProjectMemoryDB.name == project_name)
                        .options(selectinload(ProjectMemoryDB.artifacts))
                    )
                    results = await session.execute(statement)
                    existing_db_memory = results.scalars().first()

                    # Use mapper to map domain object to DB object (create or update fields)
                    db_memory = map_domain_to_db(memory, existing_db_memory)

                    # Add the main object to the session (SQLModel handles INSERT or UPDATE)
                    # If existing_db_memory is None, this adds a new object.
                    # If existing_db_memory is not None, this adds the *updated* existing object back.
                    session.add(db_memory)

                    # Flush to get the ID if it's a new project before syncing artifacts
                    if not existing_db_memory:
                        await session.flush()
                        logger.debug(
                            f"Flushed new project {db_memory.name} with ID {db_memory.id}"
                        )
                    elif db_memory.id is None:
                        # Should not happen if existing_db_memory was found and mapped correctly
                        await session.flush()
                        logger.warning(
                            f"Flushed existing project {db_memory.name} which unexpectedly had no ID before flush."
                        )
                    # We need db_memory.id for syncing artifacts below
                    if db_memory.id is None:
                        # If ID is still None after potential flush, something is wrong
                        raise RuntimeError(
                            f"Could not obtain ID for project {project_name} before syncing artifacts."
                        )

                    # Sync artifacts using the dedicated function, passing the loaded state
                    artifacts_to_delete = sync_artifacts_db(
                        session, memory, db_memory, existing_db_memory
                    )

                    # Perform deletions
                    if artifacts_to_delete:
                        logger.debug(
                            f"Deleting {len(artifacts_to_delete)} artifacts from session for project {project_name}"
                        )
                        for artifact_to_del in artifacts_to_delete:
                            await session.delete(artifact_to_del)

                    # Commit is handled by session.begin() context manager
                    logger.info(
                        f"Successfully saved memory for project: {project_name}"
                    )

                except IntegrityError as e:
                    logger.error(
                        f"Integrity error saving project '{project_name}': {e}",
                        exc_info=True,
                    )
                    raise ValueError(
                        f"Project '{project_name}' might already exist or another integrity issue occurred."
                    ) from e
                except Exception as e:
                    logger.error(
                        f"Unexpected error saving project '{project_name}': {e}",
                        exc_info=True,
                    )
                    raise

    async def load_memory(self, project_name: str) -> Optional[ProjectMemory]:
        """Loads project memory (including artifacts) from SQLite using the mapper."""
        logger.debug(f"Attempting to load memory for project: {project_name}")
        await self._create_db_and_tables()

        async with self.async_session() as session:
            try:
                statement = (
                    select(ProjectMemoryDB)
                    .where(ProjectMemoryDB.name == project_name)
                    .options(
                        selectinload(ProjectMemoryDB.artifacts)
                    )  # Eager load artifacts
                )
                results = await session.execute(statement)
                db_memory = results.scalars().first()

                if db_memory:
                    logger.debug(
                        f"Found project '{project_name}' in DB, mapping to domain model."
                    )
                    # Use the mapper function
                    return map_db_to_domain(db_memory)
                else:
                    logger.debug(f"Project '{project_name}' not found in DB.")
                    return None
            except Exception as e:
                logger.error(
                    f"Error loading project '{project_name}': {e}", exc_info=True
                )
                # Optional: Re-raise a custom domain exception?
                return None  # Return None on error for now

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

    async def list_projects(self) -> List[ProjectInfo]:  # Return ProjectInfo objects
        """Lists basic info for all projects stored in the database."""
        logger.debug("Listing all projects info from database.")
        await self._create_db_and_tables()

        projects_info: List[ProjectInfo] = []
        async with self.async_session() as session:
            try:
                # Select necessary columns for ProjectInfo
                statement = select(
                    ProjectMemoryDB.name,
                    ProjectMemoryDB.language,
                    ProjectMemoryDB.purpose,
                    ProjectMemoryDB.target_audience,
                    ProjectMemoryDB.objectives,
                    ProjectMemoryDB.base_path,
                    ProjectMemoryDB.interaction_language,
                    ProjectMemoryDB.documentation_language,
                    ProjectMemoryDB.taxonomy_version,
                    ProjectMemoryDB.platform_taxonomy,
                    ProjectMemoryDB.domain_taxonomy,
                    ProjectMemoryDB.size_taxonomy,
                    ProjectMemoryDB.compliance_taxonomy,
                    ProjectMemoryDB.lifecycle_taxonomy,  # Ensure lifecycle is selected
                    ProjectMemoryDB.custom_taxonomy,
                    ProjectMemoryDB.taxonomy_validation,
                )
                results = await session.execute(statement)

                for row in results.all():
                    # Manually map row to ProjectInfo domain model
                    try:
                        info = ProjectInfo(
                            name=row.name,
                            language=row.language,
                            purpose=row.purpose,
                            target_audience=row.target_audience,
                            objectives=row.objectives if row.objectives else [],
                            base_path=Path(row.base_path) if row.base_path else None,
                            interaction_language=row.interaction_language,
                            documentation_language=row.documentation_language,
                            taxonomy_version=row.taxonomy_version,
                            platform_taxonomy=row.platform_taxonomy,
                            domain_taxonomy=row.domain_taxonomy,
                            size_taxonomy=row.size_taxonomy,
                            compliance_taxonomy=row.compliance_taxonomy,
                            lifecycle_taxonomy=row.lifecycle_taxonomy,  # Map lifecycle
                            custom_taxonomy=row.custom_taxonomy
                            if row.custom_taxonomy
                            else {},
                            taxonomy_validation=row.taxonomy_validation
                            if row.taxonomy_validation
                            else {},
                        )
                        projects_info.append(info)
                    except Exception as map_error:  # Catch validation/mapping errors
                        logger.error(
                            f"Error mapping project info for '{row.name}': {map_error}",
                            exc_info=True,
                        )
                        # Optionally skip this project or handle differently
                        continue  # Skip projects that fail validation

                logger.debug(f"Found {len(projects_info)} projects.")
                return projects_info
            except Exception as e:
                logger.error(f"Error listing projects: {e}", exc_info=True)
                return []  # Return empty list on error

    # list_projects_names removed as list_projects now returns ProjectInfo

    # Remove ensure_utc helper method from the adapter (should be in mapper)
    # def ensure_utc(self, dt: datetime.datetime) -> datetime.datetime:
    #     ...
