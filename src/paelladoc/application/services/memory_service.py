import logging
from typing import Optional, Dict, Any, List, Callable, Awaitable

# Domain Models
from paelladoc.domain.models.project import (
    ProjectMemory,
    DocumentStatus,
    ArtifactMeta,
    Bucket,
)

# Ports
from paelladoc.ports.output.memory_port import MemoryPort

logger = logging.getLogger(__name__)

# Type definition for event handlers
EventHandler = Callable[[str, Dict[str, Any]], Awaitable[None]]


class MemoryService:
    """Application service for managing project memory operations.

    Uses the MemoryPort to interact with the persistence layer.
    """

    def __init__(self, memory_port: MemoryPort):
        """Initializes the service with a MemoryPort implementation."""
        self.memory_port = memory_port
        self._event_handlers: Dict[str, List[EventHandler]] = {}
        logger.info(
            f"MemoryService initialized with port: {type(memory_port).__name__}"
        )

    # --- Event System ---

    async def _emit_event(self, event_name: str, event_data: Dict[str, Any]) -> None:
        """Emits an event to all registered handlers for that event type.

        Args:
            event_name: The name of the event (e.g., 'artifact_created')
            event_data: Dictionary with event data
        """
        if event_name not in self._event_handlers:
            logger.debug(f"No handlers registered for event: {event_name}")
            return

        handlers = self._event_handlers[event_name]
        logger.debug(f"Emitting event '{event_name}' to {len(handlers)} handlers")

        for handler in handlers:
            try:
                await handler(event_name, event_data)
            except Exception as e:
                logger.error(
                    f"Error in event handler for '{event_name}': {e}", exc_info=True
                )

    def register_event_handler(self, event_name: str, handler: EventHandler) -> None:
        """Registers a handler function for a specific event type.

        Args:
            event_name: The event name to listen for
            handler: Async function that will be called when the event occurs
        """
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []

        self._event_handlers[event_name].append(handler)
        logger.debug(f"Registered handler for event: {event_name}")

    def unregister_event_handler(self, event_name: str, handler: EventHandler) -> bool:
        """Unregisters a handler function for a specific event type.

        Args:
            event_name: The event name
            handler: The handler function to remove

        Returns:
            True if the handler was removed, False if not found
        """
        if event_name not in self._event_handlers:
            return False

        handlers = self._event_handlers[event_name]
        if handler in handlers:
            handlers.remove(handler)
            logger.debug(f"Unregistered handler for event: {event_name}")
            return True

        return False

    # --- Memory Service Methods ---

    async def get_project_memory(self, project_name: str) -> Optional[ProjectMemory]:
        """Retrieves the memory for a specific project."""
        logger.debug(f"Service: Attempting to get memory for project '{project_name}'")
        memory = await self.memory_port.load_memory(project_name)

        if memory:
            await self._emit_event(
                "memory_loaded",
                {
                    "project_name": project_name,
                    "memory_id": str(memory.project_info.name),
                    "timestamp": memory.last_updated_at.isoformat()
                    if memory.last_updated_at
                    else None,
                },
            )

        return memory

    async def check_project_exists(self, project_name: str) -> bool:
        """Checks if a project memory already exists."""
        logger.debug(f"Service: Checking existence for project '{project_name}'")
        return await self.memory_port.project_exists(project_name)

    async def create_project_memory(self, memory: ProjectMemory) -> ProjectMemory:
        """Creates a new project memory entry.

        Raises:
            ValueError: If a project with the same name already exists.
        """
        project_name = memory.project_info.name
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

        # Emit project_created event
        await self._emit_event(
            "project_created",
            {
                "project_name": project_name,
                "base_path": str(memory.project_info.base_path)
                if memory.project_info.base_path
                else None,
                "timestamp": memory.created_at.isoformat()
                if memory.created_at
                else None,
                "project_info_details": {
                    k: v
                    for k, v in memory.project_info.dict().items()
                    if k not in ["name", "base_path"] and v is not None
                },
            },
        )

        # Emit taxonomy event if taxonomy fields were provided
        if (
            memory.platform_taxonomy
            or memory.domain_taxonomy
            or memory.size_taxonomy
            or memory.compliance_taxonomy
            or memory.custom_taxonomy
        ):
            await self._emit_event(
                "taxonomy_updated",
                {
                    "project_name": project_name,
                    "new_taxonomy": {
                        "platform": memory.platform_taxonomy,
                        "domain": memory.domain_taxonomy,
                        "size": memory.size_taxonomy,
                        "compliance": memory.compliance_taxonomy,
                        "custom": memory.custom_taxonomy,
                    },
                    "old_taxonomy": None,  # First time setting it
                },
            )

        # Emit artifact_created events for initial artifacts
        for bucket, artifacts in memory.artifacts.items():
            for artifact in artifacts:
                await self._emit_event(
                    "artifact_created",
                    {
                        "project_name": project_name,
                        "artifact_id": str(artifact.id),
                        "artifact_name": artifact.name,
                        "bucket": bucket.value,
                        "path": str(artifact.path),
                        "status": artifact.status.value,
                        "timestamp": artifact.created_at.isoformat()
                        if artifact.created_at
                        else None,
                        "created_by": artifact.created_by,
                    },
                )

        return memory  # Return the saved object (could also reload it)

    async def update_project_memory(self, memory: ProjectMemory) -> ProjectMemory:
        """Updates an existing project memory entry.

        Raises:
            ValueError: If the project does not exist.
        """
        project_name = memory.project_info.name
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

        # Get the old memory to compare changes
        old_memory = await self.memory_port.load_memory(project_name)

        # Save the updated memory
        await self.memory_port.save_memory(memory)
        logger.info(
            f"Service: Successfully updated memory for project '{project_name}'"
        )

        # Emit project_updated event
        await self._emit_event(
            "project_updated",
            {
                "project_name": project_name,
                "timestamp": memory.last_updated_at.isoformat()
                if memory.last_updated_at
                else None,
            },
        )

        # Check if taxonomy fields changed
        if old_memory and (
            memory.platform_taxonomy != old_memory.platform_taxonomy
            or memory.domain_taxonomy != old_memory.domain_taxonomy
            or memory.size_taxonomy != old_memory.size_taxonomy
            or memory.compliance_taxonomy != old_memory.compliance_taxonomy
        ):
            await self._emit_event(
                "taxonomy_updated",
                {
                    "project_name": project_name,
                    "timestamp": memory.last_updated_at.isoformat()
                    if memory.last_updated_at
                    else None,
                    "new_taxonomy": {
                        "platform": memory.platform_taxonomy,
                        "domain": memory.domain_taxonomy,
                        "size": memory.size_taxonomy,
                        "compliance": memory.compliance_taxonomy,
                    },
                    "old_taxonomy": {
                        "platform": old_memory.platform_taxonomy,
                        "domain": old_memory.domain_taxonomy,
                        "size": old_memory.size_taxonomy,
                        "compliance": old_memory.compliance_taxonomy,
                    },
                },
            )

        # Check for new or updated artifacts
        if old_memory:
            # Track artifacts by ID to detect changes
            for bucket, artifacts in memory.artifacts.items():
                # Skip empty buckets
                if not artifacts:
                    continue

                old_bucket_artifacts = old_memory.artifacts.get(bucket, [])
                old_artifact_ids = {str(a.id): a for a in old_bucket_artifacts}

                # Check each artifact in the new memory
                for artifact in artifacts:
                    artifact_id = str(artifact.id)

                    # If artifact didn't exist before, it's new
                    if artifact_id not in old_artifact_ids:
                        await self._emit_event(
                            "artifact_created",
                            {
                                "project_name": project_name,
                                "artifact_id": artifact_id,
                                "artifact_name": artifact.name,
                                "bucket": bucket.value,
                                "path": str(artifact.path),
                                "status": artifact.status.value,
                                "timestamp": artifact.created_at.isoformat()
                                if artifact.created_at
                                else None,
                                "created_by": artifact.created_by,
                            },
                        )
                    else:
                        # If artifact existed, check if it was updated
                        old_artifact = old_artifact_ids[artifact_id]
                        if (
                            artifact.status != old_artifact.status
                            or artifact.updated_at != old_artifact.updated_at
                        ):
                            await self._emit_event(
                                "artifact_updated",
                                {
                                    "project_name": project_name,
                                    "artifact_id": artifact_id,
                                    "artifact_name": artifact.name,
                                    "bucket": bucket.value,
                                    "path": str(artifact.path),
                                    "old_status": old_artifact.status.value,
                                    "new_status": artifact.status.value,
                                    "timestamp": artifact.updated_at.isoformat()
                                    if artifact.updated_at
                                    else None,
                                    "modified_by": artifact.modified_by,
                                },
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

        # Get old status for event
        old_status = memory.documents[document_name].status

        # Update status
        memory.update_document_status(
            document_name, new_status
        )  # Use domain model method

        # Save the updated memory
        await self.memory_port.save_memory(memory)
        logger.info(
            f"Service: Saved updated status for document '{document_name}' in project '{project_name}'"
        )

        # Emit document_status_changed event
        await self._emit_event(
            "document_status_changed",
            {
                "project_name": project_name,
                "document_name": document_name,
                "old_status": old_status.value,
                "new_status": new_status.value,
                "timestamp": memory.last_updated_at.isoformat()
                if memory.last_updated_at
                else None,
            },
        )

        return memory

    async def add_artifact(
        self, project_name: str, artifact: ArtifactMeta, author: Optional[str] = None
    ) -> Optional[ProjectMemory]:
        """Adds a new artifact to a project's memory.

        Args:
            project_name: The name of the project
            artifact: The artifact to add
            author: Optional name of the author creating the artifact

        Returns:
            The updated project memory, or None if project not found
        """
        logger.debug(
            f"Service: Adding artifact '{artifact.name}' to project '{project_name}'"
        )

        # Set author if provided
        if author and not artifact.created_by:
            artifact.created_by = author
            artifact.modified_by = author

        memory = await self.get_project_memory(project_name)
        if not memory:
            logger.warning(f"Project '{project_name}' not found, cannot add artifact.")
            return None

        # Add the artifact
        added = memory.add_artifact(artifact)
        if not added:
            logger.warning(
                f"Artifact with path '{artifact.path}' already exists in project '{project_name}'"
            )
            return memory

        # Save the updated memory
        await self.memory_port.save_memory(memory)
        logger.info(
            f"Service: Saved new artifact '{artifact.name}' in project '{project_name}'"
        )

        # Emit artifact_created event
        await self._emit_event(
            "artifact_created",
            {
                "project_name": project_name,
                "artifact_id": str(artifact.id),
                "artifact_name": artifact.name,
                "bucket": artifact.bucket.value,
                "path": str(artifact.path),
                "status": artifact.status.value,
                "timestamp": artifact.created_at.isoformat()
                if artifact.created_at
                else None,
                "created_by": artifact.created_by,
            },
        )

        return memory

    async def update_artifact_status(
        self,
        project_name: str,
        bucket: Bucket,
        artifact_name: str,
        new_status: DocumentStatus,
        modifier: Optional[str] = None,
    ) -> Optional[ProjectMemory]:
        """Updates the status of a specific artifact within a project's memory.

        Args:
            project_name: The name of the project
            bucket: The bucket containing the artifact
            artifact_name: The name of the artifact to update
            new_status: The new status to set
            modifier: Optional name of the person making the change

        Returns:
            The updated project memory, or None if project not found
        """
        logger.debug(
            f"Service: Updating status for artifact '{artifact_name}' in project '{project_name}' to {new_status}"
        )

        memory = await self.get_project_memory(project_name)
        if not memory:
            logger.warning(
                f"Project '{project_name}' not found, cannot update artifact status."
            )
            return None

        # Get the artifact to check its current status
        artifact = memory.get_artifact(bucket, artifact_name)
        if not artifact:
            logger.warning(
                f"Artifact '{artifact_name}' not found in bucket '{bucket.value}' for project '{project_name}'"
            )
            return memory

        old_status = artifact.status

        # Update the artifact status
        updated = memory.update_artifact_status(
            bucket, artifact_name, new_status, modifier
        )
        if not updated:
            logger.warning(
                f"Failed to update status for artifact '{artifact_name}' in project '{project_name}'"
            )
            return memory

        # Save the updated memory
        await self.memory_port.save_memory(memory)
        logger.info(
            f"Service: Saved updated status for artifact '{artifact_name}' in project '{project_name}'"
        )

        # Emit artifact_updated event
        await self._emit_event(
            "artifact_updated",
            {
                "project_name": project_name,
                "artifact_id": str(artifact.id),
                "artifact_name": artifact_name,
                "bucket": bucket.value,
                "old_status": old_status.value,
                "new_status": new_status.value,
                "timestamp": artifact.updated_at.isoformat()
                if artifact.updated_at
                else None,
                "modified_by": modifier or artifact.modified_by,
            },
        )

        return memory
