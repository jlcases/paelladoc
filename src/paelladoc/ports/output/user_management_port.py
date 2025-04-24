"""Port interface for User Management operations."""

from abc import ABC, abstractmethod
from typing import Optional, Any, List
from paelladoc.domain.models.user import User


class UserManagementPort(ABC):
    """
    Abstract interface defining operations related to user identity and permissions.
    This allows decoupling the core application from specific user management implementations
    (e.g., a simple dummy one for OSS, a complex one for SaaS).
    """

    @abstractmethod
    async def get_current_user_id(self) -> Optional[str]:
        """
        Retrieves the unique identifier of the user making the current request.

        Returns:
            A string representing the user ID, or None if the user is anonymous
            or identity cannot be determined.
        """
        pass

    @abstractmethod
    async def check_permission(
        self, user_id: Optional[str], action: str, resource_id: Optional[Any] = None
    ) -> bool:
        """
        Checks if a given user has permission to perform a specific action,
        optionally on a specific resource.

        Args:
            user_id: The unique identifier of the user to check permissions for.
                     Can be None for anonymous users.
            action: A string identifying the action being attempted
                    (e.g., 'core_delete_project', 'core_update_template').
                    It's recommended to use the MCP tool name or a similar unique identifier.
            resource_id: (Optional) The identifier of the resource being accessed
                         (e.g., project name, template ID). Used for object-level permissions.

        Returns:
            True if the user has the necessary permission, False otherwise.
        """
        pass

    @abstractmethod
    async def create_user(self, user_identifier: str) -> User:
        """Creates a new user."""
        pass

    @abstractmethod
    async def get_user_by_identifier(self, user_identifier: str) -> Optional[User]:
        """Retrieves a user by their identifier."""
        pass

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        """Retrieves all users."""
        pass

    @abstractmethod
    async def delete_user(self, user_identifier: str) -> bool:
        """Deletes a user by their identifier."""
        pass

    @abstractmethod
    async def check_if_any_user_exists(self) -> bool:
        """Checks if at least one user exists in the system."""
        pass

    # Potential future methods:
    # async def get_user_display_name(self, user_id: str) -> Optional[str]: ...
    # async def get_user_roles(self, user_id: str) -> List[str]: ...
