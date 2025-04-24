"""SQLite implementation of the UserManagementPort."""

import logging
from typing import Optional, Any, List

from sqlmodel import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, NoResultFound

from paelladoc.ports.output.user_management_port import UserManagementPort
from paelladoc.domain.models.user import User  # User for return type
from .db_models import UserDB  # UserDB for queries

logger = logging.getLogger(__name__)


class SQLiteUserManagementAdapter(UserManagementPort):
    """
    SQLite implementation of the UserManagementPort using SQLModel.
    Handles user creation, retrieval, deletion, and permission checks based on UserDB.
    """

    def __init__(self, async_session_factory: sessionmaker[AsyncSession]):
        """Initialize the adapter with an async session factory."""
        self.async_session = async_session_factory
        logger.info("SQLiteUserManagementAdapter initialized.")

    async def get_current_user_id(self) -> Optional[str]:
        """
        Retrieves the user identifier from the single entry in the UserDB table (OSS assumption).
        Returns None if the table is empty or has more than one entry (configuration error).
        """
        async with self.async_session() as session:
            try:
                statement = select(UserDB)
                results = await session.execute(statement)
                users = results.scalars().all()

                if len(users) == 1:
                    user_id = users[0].user_identifier
                    # logger.debug(f"SQLiteUserManagementAdapter: Found user ID: {user_id}") # Too verbose?
                    return user_id
                elif len(users) == 0:
                    logger.warning(
                        "SQLiteUserManagementAdapter: No user found in UserDB. OSS user not configured."
                    )
                    return None
                else:
                    # More than one user means configuration is incorrect for OSS
                    logger.error(
                        "SQLiteUserManagementAdapter: Found multiple users in UserDB for OSS mode. Configuration error."
                    )
                    # Consider returning the first one? Or None? Returning None is safer.
                    return None
            except Exception as e:
                logger.error(
                    f"SQLiteUserManagementAdapter: Error fetching user: {e}",
                    exc_info=True,
                )
                return None

    async def check_permission(
        self, user_id: Optional[str], action: str, resource_id: Optional[Any] = None
    ) -> bool:
        """
        In OSS mode, returns True only if a valid user_id (not None) is provided.
        This ensures operations are blocked until the OSS user is configured.
        A real implementation would check roles/permissions against the action/resource.
        """
        # Simplified OSS check: Any logged-in user can do anything.
        has_permission = user_id is not None
        # logger.debug(
        #     f"SQLiteUserManagementAdapter: Permission check for user '{user_id}' "
        #     f"on action '{action}' (resource: '{resource_id}'): {has_permission}"
        # )
        return has_permission

    async def create_user(self, user_identifier: str) -> User:
        """Creates a new user in the database."""
        logger.info(f"Attempting to create user: {user_identifier}")
        async with self.async_session() as session:
            async with session.begin():
                try:
                    # Check if user already exists
                    existing_user_stmt = select(UserDB).where(
                        UserDB.user_identifier == user_identifier
                    )
                    result = await session.execute(existing_user_stmt)
                    if result.scalars().first():
                        logger.warning(f"User '{user_identifier}' already exists.")
                        # Consider raising an error or returning the existing user
                        # For simplicity, let's assume we just want to ensure it exists.
                        # Re-fetch to return consistent object
                        return await self.get_user_by_identifier(user_identifier)
                        # raise ValueError(f"User '{user_identifier}' already exists.")

                    new_user_db = UserDB(user_identifier=user_identifier)
                    session.add(new_user_db)
                    await (
                        session.flush()
                    )  # Flush to get ID and handle potential immediate errors
                    await session.refresh(
                        new_user_db
                    )  # Refresh to get all fields populated
                    logger.info(
                        f"Successfully created user: {user_identifier} with ID: {new_user_db.id}"
                    )
                    # Map DB model to Domain model for return
                    return User(
                        id=new_user_db.id,
                        user_identifier=new_user_db.user_identifier,
                        created_at=new_user_db.created_at,
                    )

                except IntegrityError as e:
                    await session.rollback()
                    logger.error(
                        f"Database integrity error creating user '{user_identifier}': {e}",
                        exc_info=True,
                    )
                    raise  # Re-raise after logging
                except Exception as e:
                    await session.rollback()
                    logger.error(
                        f"Unexpected error creating user '{user_identifier}': {e}",
                        exc_info=True,
                    )
                    raise

    async def get_user_by_identifier(self, user_identifier: str) -> Optional[User]:
        """Retrieves a user by their identifier from the database."""
        async with self.async_session() as session:
            try:
                statement = select(UserDB).where(
                    UserDB.user_identifier == user_identifier
                )
                result = await session.execute(statement)
                user_db = result.scalars().one_or_none()  # Use one_or_none for clarity

                if user_db:
                    # Map DB to Domain
                    return User(
                        id=user_db.id,
                        user_identifier=user_db.user_identifier,
                        created_at=user_db.created_at,
                    )
                else:
                    logger.debug(f"User '{user_identifier}' not found.")
                    return None
            except Exception as e:
                logger.error(
                    f"Error retrieving user '{user_identifier}': {e}", exc_info=True
                )
                return None  # Return None on error

    async def get_all_users(self) -> List[User]:
        """Retrieves all users from the database."""
        async with self.async_session() as session:
            try:
                statement = select(UserDB)
                results = await session.execute(statement)
                users_db = results.scalars().all()
                # Map list of DB models to list of Domain models
                return [
                    User(
                        id=u.id,
                        user_identifier=u.user_identifier,
                        created_at=u.created_at,
                    )
                    for u in users_db
                ]
            except Exception as e:
                logger.error(f"Error retrieving all users: {e}", exc_info=True)
                return []  # Return empty list on error

    async def delete_user(self, user_identifier: str) -> bool:
        """Deletes a user by their identifier from the database."""
        logger.info(f"Attempting to delete user: {user_identifier}")
        async with self.async_session() as session:
            async with session.begin():
                try:
                    # Find the user ID first
                    select_stmt = select(UserDB.id).where(
                        UserDB.user_identifier == user_identifier
                    )
                    result = await session.execute(select_stmt)
                    user_id = result.scalar_one_or_none()

                    if user_id is None:
                        logger.warning(
                            f"User '{user_identifier}' not found for deletion."
                        )
                        return False

                    # Delete the user by ID
                    delete_stmt = delete(UserDB).where(UserDB.id == user_id)
                    delete_result = await session.execute(delete_stmt)

                    if delete_result.rowcount == 1:
                        logger.info(f"Successfully deleted user: {user_identifier}")
                        return True
                    else:
                        # This shouldn't happen if we found the ID, but good to check
                        logger.warning(
                            f"User '{user_identifier}' found but deletion failed (rowcount={delete_result.rowcount})."
                        )
                        return False

                except (
                    NoResultFound
                ):  # Should be caught by the scalar_one_or_none check above
                    logger.warning(
                        f"User '{user_identifier}' not found for deletion (NoResultFound)."
                    )
                    return False
                except Exception as e:
                    await session.rollback()
                    logger.error(
                        f"Error deleting user '{user_identifier}': {e}", exc_info=True
                    )
                    raise  # Re-raise error after rollback

    async def check_if_any_user_exists(self) -> bool:
        """Checks if at least one user exists in the UserDB table."""
        async with self.async_session() as session:
            try:
                # Efficiently check for existence using count or limit 1
                statement = select(
                    func.count(UserDB.id)
                )  # Use func.count for efficiency
                result = await session.execute(statement)
                count = result.scalar_one()
                exists = count > 0
                # logger.debug(f"Checked if any user exists: {exists} (Count: {count})")
                return exists
            except Exception as e:
                logger.error(f"Error checking if any user exists: {e}", exc_info=True)
                return False  # Assume false on error? Or raise? False seems safer for initial setup.
