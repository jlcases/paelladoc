from abc import ABC, abstractmethod
from typing import Optional, List

# Import the domain model it needs to interact with
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
)


class MemoryPort(ABC):
    """Output Port defining operations for project memory persistence."""

    @abstractmethod
    async def save_memory(self, memory: ProjectMemory) -> None:
        """Saves the entire project memory state.

        Args:
            memory: The ProjectMemory object to save.
        """
        pass

    @abstractmethod
    async def load_memory(self, project_name: str) -> Optional[ProjectMemory]:
        """Loads the project memory state for a given project name.

        Args:
            project_name: The unique name of the project to load.

        Returns:
            The ProjectMemory object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def project_exists(self, project_name: str) -> bool:
        """Checks if a project memory exists for the given name.

        Args:
            project_name: The unique name of the project to check.

        Returns:
            True if the project memory exists, False otherwise.
        """
        pass

    @abstractmethod
    async def list_projects(self) -> List[ProjectInfo]:
        """Lists the names of all existing projects.

        Returns:
            A list of project names as strings. Returns an empty list if no projects exist.
        """
        pass

    @abstractmethod
    async def delete_memory(self, project_name: str) -> None:
        """Deletes the project memory state."""
        pass

    @abstractmethod
    async def get_active_project(self) -> Optional[ProjectInfo]:
        """Gets the currently active project, if any."""
        pass

    @abstractmethod
    async def set_active_project(self, project_name: str) -> bool:
        """Sets the specified project as active, deactivating others. Returns True on success."""
        pass

    # Potentially add other methods later if needed, e.g., delete_memory
