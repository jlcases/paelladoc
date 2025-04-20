import logging
from typing import Optional

# Domain Models
from paelladoc.domain.models.project import ProjectMemory, DocumentStatus

# Ports
from paelladoc.ports.output.memory_port import MemoryPort

logger = logging.getLogger(__name__)


class MemoryService:
    """Application service for managing project memory operations.

    Uses the MemoryPort to interact with the persistence layer.
    """

    def __init__(self, memory_port: MemoryPort):
        """Initializes the service with a MemoryPort implementation."""
        self.memory_port = memory_port
        logger.info(
            f"MemoryService initialized with port: {type(memory_port).__name__}"
        )

    async def get_project_memory(self, project_name: str) -> Optional[ProjectMemory]:
        """Retrieves the memory for a specific project."""
        logger.debug(f"Service: Attempting to get memory for project '{project_name}'")
        return await self.memory_port.load_memory(project_name)

    async def check_project_exists(self, project_name: str) -> bool:
        """Checks if a project memory already exists."""
        logger.debug(f"Service: Checking existence for project '{project_name}'")
        return await self.memory_port.project_exists(project_name)

    async def create_project_memory(self, memory: ProjectMemory) -> ProjectMemory:
        """Creates a new project memory entry.

        Raises:
            ValueError: If a project with the same name already exists.
        """
        project_name = memory.metadata.name
        logger.debug(
            f"Service: Attempting to create memory for project '{project_name}'"
        )

        exists = await self.check_project_exists(project_name)
        if exists:
            logger.error(f"Cannot create project '{project_name}': already exists.")
            raise ValueError(f"Project memory for '{project_name}' already exists.")

        await self.memory_port.save_memory(memory)
        logger.info(
            f"Service: Successfully created memory for project '{project_name}'"
        )
        return memory  # Return the saved object (could also reload it)

    async def update_project_memory(self, memory: ProjectMemory) -> ProjectMemory:
        """Updates an existing project memory entry.

        Raises:
            ValueError: If the project does not exist.
        """
        project_name = memory.metadata.name
        logger.debug(
            f"Service: Attempting to update memory for project '{project_name}'"
        )

        # Ensure the project exists before attempting an update
        # Note: save_memory itself handles the create/update logic, but this check
        # makes the service layer's intent clearer and prevents accidental creation.
        exists = await self.check_project_exists(project_name)
        if not exists:
            logger.error(f"Cannot update project '{project_name}': does not exist.")
            raise ValueError(
                f"Project memory for '{project_name}' does not exist. Use create_project_memory first."
            )

        await self.memory_port.save_memory(memory)
        logger.info(
            f"Service: Successfully updated memory for project '{project_name}'"
        )
        return memory  # Return the updated object

    # Example of a more specific use case method:
    async def update_document_status_in_memory(
        self, project_name: str, document_name: str, new_status: DocumentStatus
    ) -> Optional[ProjectMemory]:
        """Updates the status of a specific document within a project's memory."""
        logger.debug(
            f"Service: Updating status for document '{document_name}' in project '{project_name}' to {new_status}"
        )
        memory = await self.get_project_memory(project_name)
        if not memory:
            logger.warning(
                f"Project '{project_name}' not found, cannot update document status."
            )
            return None

        if document_name not in memory.documents:
            logger.warning(
                f"Document '{document_name}' not found in project '{project_name}', cannot update status."
            )
            # Or should we raise an error?
            return memory  # Return unchanged memory?

        memory.update_document_status(
            document_name, new_status
        )  # Use domain model method

        # Save the updated memory
        await self.memory_port.save_memory(memory)
        logger.info(
            f"Service: Saved updated status for document '{document_name}' in project '{project_name}'"
        )
        return memory
