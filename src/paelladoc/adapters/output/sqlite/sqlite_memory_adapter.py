"""SQLite adapter for project memory persistence."""

import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
import subprocess
import os
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, Row

# Ports and Domain Models
from paelladoc.ports.output.memory_port import MemoryPort
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
)

# Database Models for this adapter
from .db_models import ProjectMemoryDB

# Import UserDB model from the correct location

# Import the new mapper functions
from .mapper import map_db_to_domain, map_domain_to_db, sync_artifacts_db

# Configuration
from paelladoc.config.database import get_db_path

# Dependency Injection for User Management Port
# from paelladoc.dependencies import dependencies # Assuming dict-based DI
from paelladoc.ports.output.user_management_port import UserManagementPort

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

    async def _run_migrations(self):
        """Run database migrations using alembic."""
        try:
            logger.info("Running database migrations...")
            # Get the project root directory where alembic.ini is located
            project_root = Path(__file__).parent.parent.parent.parent.parent.absolute()

            # Set PAELLADOC_DB_PATH environment variable for alembic
            os.environ["PAELLADOC_DB_PATH"] = str(self.db_path)

            # Run alembic upgrade
            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                capture_output=True,
                text=True,
                check=False,
                cwd=project_root,  # Run from project root where alembic.ini is
            )

            if result.returncode == 0:
                logger.info("Database migrations completed successfully")
                if result.stdout:
                    logger.debug(f"Migration output:\n{result.stdout}")
            else:
                logger.error(f"Database migration failed with error:\n{result.stderr}")
                # Instead of raising an error, just create tables directly in test environments
                if "test" in str(self.db_path):
                    logger.warning(
                        "Test environment detected, creating tables directly..."
                    )
                    async with self.async_engine.begin() as conn:
                        await conn.run_sync(SQLModel.metadata.create_all)
                    return
                raise RuntimeError("Database migration failed")

        except Exception as e:
            logger.error(f"Error running migrations: {e}")
            raise

    async def _create_db_and_tables(self):
        """Creates the database and tables if they don't exist and ensures initial admin user."""
        # Wrap the entire process to catch and log any unexpected errors
        try:
            # First run migrations - TEMPORARILY COMMENTED OUT due to subprocess issues
            # logger.info("Attempting to run migrations via adapter...") # Add log
            # await self._run_migrations()
            # logger.info("Migrations finished (or skipped if failed/not needed).") # Add log

            # Ensure all tables exist using SQLModel metadata
            # This is safe even if migrations didn't run, but relies on external migration for schema updates.
            logger.info(
                "Ensuring tables exist via SQLModel.metadata.create_all..."
            )  # Add log
            async with self.async_engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables checked/created via SQLModel.")

            # --- Add initial OSS admin user ---
            # Get the potentially patched dependency HERE
            from paelladoc.dependencies import dependencies

            user_port_instance = dependencies.get(UserManagementPort)
            await self._ensure_initial_admin_user(
                user_port_instance
            )  # Pasar la instancia
            # --- End add initial OSS admin user ---

        except Exception as e:
            # Log the full traceback if anything goes wrong here
            logger.error(
                f"Critical error during database/table creation or initial user setup: {e}",
                exc_info=True,
            )
            # Re-raise the exception to allow higher-level handlers to catch it if needed
            raise

    async def _ensure_initial_admin_user(
        self, user_management_port: UserManagementPort
    ):
        """Checks if any user exists and creates the initial admin user if none are found."""
        # Wrap the core logic to log detailed errors
        try:
            logger.debug("Attempting to use provided UserManagementPort...")
            if not user_management_port:
                logger.error(
                    "UserManagementPort instance was not provided. Cannot create initial admin user."
                )
                return
            logger.debug("UserManagementPort obtained via argument.")

            # Check if any user exists directly via the port
            logger.debug("Checking if any user exists via port...")
            user_exists = await user_management_port.check_if_any_user_exists()
            logger.debug(f"Result from check_if_any_user_exists: {user_exists}")

            if not user_exists:
                admin_user_identifier = os.getenv(
                    "PAELLADOC_OSS_ADMIN_USER", "admin@paelladoc.default"
                )
                logger.info(
                    f"No users found. Attempting to create initial admin user: {admin_user_identifier}"
                )
                try:
                    # The create_user method should handle hashing and saving
                    await user_management_port.create_user(admin_user_identifier)
                    logger.info(
                        f"Successfully created initial admin user: {admin_user_identifier}"
                    )
                except Exception as create_err:
                    # Log the specific error during user creation
                    logger.error(
                        f"Failed to create initial admin user '{admin_user_identifier}': {create_err}",
                        exc_info=True,
                    )
                    # Decide if this should raise an error or just log - re-raising for now
                    raise create_err
            else:
                logger.debug(
                    "Users already exist in the database. Skipping initial admin user creation."
                )

        except Exception as e:
            # Log the full traceback if any error occurs during the process
            logger.error(f"Error ensuring initial admin user: {e}", exc_info=True)
            # Re-raise the exception
            raise

    # --- MemoryPort Implementation --- #

    async def save_memory(self, memory: ProjectMemory) -> None:
        """Saves the project memory state (including artifacts) to SQLite using the mapper."""
        project_name = memory.project_info.name
        logger.debug(f"Attempting to save memory for project: {project_name}")
        await self._create_db_and_tables()

        # Import dependencies dictionary *inside* the method to break circular import (already done)
        from paelladoc.dependencies import dependencies

        # Get User Management Port from dependencies
        user_management_port: UserManagementPort = dependencies.get(UserManagementPort)
        if not user_management_port:
            # Fallback or error handling if port is not registered
            logger.warning(
                "UserManagementPort not found in dependencies. Cannot set created_by/modified_by."
            )
            current_user_id = None
        else:
            current_user_id = await user_management_port.get_current_user_id()
            logger.debug(f"Retrieved current user ID: {current_user_id}")

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

                    # Set created_by only if it's a new project
                    if not existing_db_memory and current_user_id:
                        memory.project_info.created_by = current_user_id

                    # Always set modified_by
                    if current_user_id:
                        memory.project_info.modified_by = current_user_id

                    # Use mapper to map domain object to DB object (create or update fields)
                    db_memory = map_domain_to_db(memory, existing_db_memory)

                    # Ensure DB model also gets the updated user IDs
                    if not existing_db_memory and current_user_id:
                        db_memory.created_by = current_user_id
                    if current_user_id:
                        db_memory.modified_by = current_user_id

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

    async def list_projects(self) -> List[Dict[str, Any]]:
        """Lists info for all projects stored in the database, including active status."""
        logger.debug("Listing all projects info from database.")
        await self._create_db_and_tables()

        projects_data: List[Dict[str, Any]] = []
        async with self.async_session() as session:
            try:
                # Select necessary columns INCLUDING is_active
                statement = select(
                    ProjectMemoryDB.name,
                    ProjectMemoryDB.is_active,
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
                    ProjectMemoryDB.lifecycle_taxonomy,
                    ProjectMemoryDB.custom_taxonomy,
                    ProjectMemoryDB.taxonomy_validation,
                    # Add audit fields if needed by the list view
                    ProjectMemoryDB.created_at,
                    ProjectMemoryDB.created_by,
                    ProjectMemoryDB.last_updated_at,
                    ProjectMemoryDB.modified_by,
                )
                results = await session.execute(statement)
                rows: List[Row] = results.all()

                for row in rows:
                    # Map row to dictionary
                    try:
                        # Use ._mapping to access row data as a dictionary
                        row_dict = row._mapping
                        # Create the dictionary, converting Path if necessary
                        project_dict = {
                            key: (str(value) if isinstance(value, Path) else value)
                            for key, value in row_dict.items()
                        }
                        # Ensure base_path is string even if None initially (though should be str from DB)
                        if (
                            "base_path" in project_dict
                            and project_dict["base_path"] is not None
                        ):
                            project_dict["base_path"] = str(
                                Path(project_dict["base_path"])
                            )  # Ensure it's string path
                        elif "base_path" in project_dict:
                            project_dict["base_path"] = (
                                None  # Handle potential None explicitly
                            )

                        # Clean up None objectives to empty list if needed by consumers
                        if (
                            "objectives" in project_dict
                            and project_dict["objectives"] is None
                        ):
                            project_dict["objectives"] = []

                        # Ensure taxonomies are dicts if None
                        if (
                            "custom_taxonomy" in project_dict
                            and project_dict["custom_taxonomy"] is None
                        ):
                            project_dict["custom_taxonomy"] = {}
                        if (
                            "taxonomy_validation" in project_dict
                            and project_dict["taxonomy_validation"] is None
                        ):
                            project_dict["taxonomy_validation"] = {}

                        projects_data.append(project_dict)

                    except Exception as map_error:  # Catch mapping errors
                        logger.error(
                            f"Error mapping project dict for '{getattr(row, 'name', 'UNKNOWN')}': {map_error}",
                            exc_info=True,
                        )
                        continue  # Skip projects that fail mapping

                logger.debug(f"Found {len(projects_data)} projects.")
                return projects_data
            except Exception as e:
                logger.error(f"Error listing projects: {e}", exc_info=True)
                return []  # Return empty list on error

    # list_projects_names removed as list_projects now returns ProjectInfo

    async def delete_memory(self, project_name: str) -> None:
        """Delete a project memory and its artifacts from the database.

        Args:
            project_name: Name of the project to delete.

        Raises:
            ValueError: If project doesn't exist.
        """
        logger.debug(f"Attempting to delete project: {project_name}")
        await self._create_db_and_tables()

        async with self.async_session() as session:
            async with session.begin():
                try:
                    # Find the project
                    statement = (
                        select(ProjectMemoryDB)
                        .where(ProjectMemoryDB.name == project_name)
                        .options(selectinload(ProjectMemoryDB.artifacts))
                    )
                    results = await session.execute(statement)
                    project_db = results.scalars().first()

                    if not project_db:
                        raise ValueError(f"Project '{project_name}' not found.")

                    # Delete all artifacts first (due to foreign key constraint)
                    if project_db.artifacts:
                        for artifact in project_db.artifacts:
                            await session.delete(artifact)

                    # Delete the project
                    await session.delete(project_db)

                    logger.info(f"Successfully deleted project: {project_name}")

                except Exception as e:
                    logger.error(
                        f"Error deleting project '{project_name}': {e}", exc_info=True
                    )
                    raise

    async def get_active_project(self) -> Optional[ProjectInfo]:
        """Gets the currently active project, if any."""
        await self._create_db_and_tables()  # Ensure DB exists
        async with self.async_session() as session:
            statement = select(ProjectMemoryDB).where(ProjectMemoryDB.is_active)
            results = await session.execute(statement)
            active_db_project = results.scalars().first()
            if active_db_project:
                # Convert only the necessary fields to ProjectInfo
                # This avoids loading the full ProjectMemory
                return ProjectInfo(
                    name=active_db_project.name,
                    language=active_db_project.language,
                    purpose=active_db_project.purpose,
                    target_audience=active_db_project.target_audience,
                    base_path=active_db_project.base_path,
                    interaction_language=active_db_project.interaction_language,
                    documentation_language=active_db_project.documentation_language,
                    platform_taxonomy=active_db_project.platform_taxonomy,
                    domain_taxonomy=active_db_project.domain_taxonomy,
                    size_taxonomy=active_db_project.size_taxonomy,
                    compliance_taxonomy=active_db_project.compliance_taxonomy,
                    lifecycle_taxonomy=active_db_project.lifecycle_taxonomy,
                )
            return None

    async def set_active_project(self, project_name: str) -> bool:
        """Sets the specified project as active, deactivating others. Returns True on success."""
        logger.info(f"Attempting to set project '{project_name}' as active.")
        await self._create_db_and_tables()  # Ensure DB exists
        async with self.async_session() as session:
            async with session.begin():  # Start transaction
                try:
                    # Step 1: Deactivate all currently active projects
                    update_stmt_deactivate = (
                        update(ProjectMemoryDB)
                        .where(ProjectMemoryDB.is_active)
                        .values(is_active=False)
                    )
                    await session.execute(update_stmt_deactivate)
                    logger.debug("Deactivated previously active projects.")

                    # Step 2: Activate the target project
                    update_stmt_activate = (
                        update(ProjectMemoryDB)
                        .where(ProjectMemoryDB.name == project_name)
                        .values(is_active=True)
                        .returning(ProjectMemoryDB.id)  # Check if update happened
                    )
                    result = await session.execute(update_stmt_activate)

                    if result.scalar_one_or_none() is None:
                        logger.warning(
                            f"Project '{project_name}' not found to activate. Rolling back."
                        )
                        # Transaction will be rolled back automatically by context manager
                        return False

                    logger.info(f"Successfully set project '{project_name}' as active.")
                    # Transaction commits automatically here
                    return True

                except Exception as e:
                    logger.error(
                        f"Error setting active project '{project_name}': {e}",
                        exc_info=True,
                    )
                    # Transaction will be rolled back automatically
                    return False

    # Remove ensure_utc helper method from the adapter (should be in mapper)
    # def ensure_utc(self, dt: datetime.datetime) -> datetime.datetime:
    #     ...
