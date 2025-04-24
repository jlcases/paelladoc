"""Dummy implementation of the UserManagementPort for OSS version."""

import logging
from typing import Optional, Any

from sqlmodel import select
from sqlalchemy.orm import sessionmaker

from paelladoc.ports.output.user_management_port import UserManagementPort
from paelladoc.adapters.output.sqlite.db_models import UserDB  # Import UserDB model

logger = logging.getLogger(__name__)


class DummyUserManagementAdapter(UserManagementPort):
    """
    A simple implementation of the UserManagementPort suitable for the OSS version
    where user management is limited to a single configured user.
    It reads the user identifier from the 'users' table.
    """

    def __init__(self, async_session_factory: sessionmaker):
        """Initialize the adapter with an async session factory."""
        self.async_session = async_session_factory
        logger.info("DummyUserManagementAdapter initialized with session factory.")

    async def get_current_user_id(self) -> Optional[str]:
        """
        Retrieves the user identifier from the single entry in the UserDB table.
        Returns None if the table is empty or has more than one entry (configuration error).
        """
        async with self.async_session() as session:
            try:
                statement = select(UserDB)
                results = await session.execute(statement)
                users = results.scalars().all()

                if len(users) == 1:
                    user_id = users[0].user_identifier
                    logger.debug(
                        f"DummyUserManagementAdapter: Found user ID: {user_id}"
                    )
                    return user_id
                elif len(users) == 0:
                    logger.warning(
                        "DummyUserManagementAdapter: No user found in UserDB. OSS user not configured."
                    )
                    return None
                else:
                    # More than one user means configuration is incorrect for OSS
                    logger.error(
                        "DummyUserManagementAdapter: Found multiple users in UserDB for OSS mode. Configuration error."
                    )
                    return None
            except Exception as e:
                logger.error(
                    f"DummyUserManagementAdapter: Error fetching user: {e}",
                    exc_info=True,
                )
                return None

    async def check_permission(
        self, user_id: Optional[str], action: str, resource_id: Optional[Any] = None
    ) -> bool:
        """
        Returns True only if a valid user_id (not None) is provided.
        This ensures operations are blocked until the OSS user is configured.
        """
        has_permission = user_id is not None
        logger.debug(
            f"DummyUserManagementAdapter: Permission check for user '{user_id}' "
            f"on action '{action}' (resource: '{resource_id}'): {has_permission}"
        )
        return has_permission
