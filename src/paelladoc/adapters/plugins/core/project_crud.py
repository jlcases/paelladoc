"""
Core plugin for project CRUD operations.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
import shutil  # Import shutil for directory deletion

from paelladoc.domain.core_logic import mcp
from paelladoc.domain.models.project import ProjectInfo
from .project_utils import (
    validate_project_updates,
    create_project_backup,
    format_project_info,
)

# Dependency Injection for User Management Port
from paelladoc.dependencies import dependencies  # Assuming dict-based DI
from paelladoc.ports.output.user_management_port import UserManagementPort
from paelladoc.ports.output.memory_port import MemoryPort

logger = logging.getLogger(__name__)


@mcp.tool(
    name="core_get_project",
    description="Get detailed information about a specific project.",
)
async def get_project(
    project_name: str,
    # --- REMOVE Injected Dependencies --- #
    # memory_adapter: Optional[MemoryPort] = None
) -> Dict[str, Any]:
    """Get detailed information about a specific project.

    ACTION: Retrieves complete project information for the specified project name.

    INPUT:
    - project_name: Name of the project to retrieve (required)

    OUTPUT: MUST return ONLY the raw JSON response from the execution.
    - On success: { "status": "ok", "project": ProjectInfo }
    - On error: { "status": "error", "message": "Error description" }

    EXECUTION RULES:
    1. This tool performs ONLY the project retrieval action
    2. DO NOT add any introductory or explanatory text
    3. DO NOT interpret the project data or suggest actions
    4. DO NOT ask any questions

    Args:
        project_name: Name of the project to retrieve
        # REMOVE memory_adapter from Args

    Returns:
        Dict[str, Any]: Dictionary containing project info or error message
    """
    # --- Get dependencies INSIDE function (WITHOUT type hints) --- #
    memory_adapter = dependencies.get(MemoryPort)
    if not memory_adapter:
        logger.error("MemoryPort not found in dependencies.")
        return {
            "status": "error",
            "message": "Internal configuration error: MemoryPort missing.",
        }
    # --- End Dependency Resolution --- #

    try:
        project_memory = await memory_adapter.load_memory(project_name)

        if not project_memory:
            return {
                "status": "error",
                "message": f"Project '{project_name}' not found.",
            }

        # Format project info for response
        project_info = project_memory.project_info.model_dump()
        project_info = format_project_info(project_info)

        return {"status": "ok", "project": project_info}

    except Exception as e:
        logger.error(f"Error retrieving project '{project_name}': {e}", exc_info=True)
        return {"status": "error", "message": f"Error retrieving project: {str(e)}"}


@mcp.tool(
    name="core_update_project", description="Update specific fields of a project."
)
async def update_project(
    project_name: str,
    updates: Dict[str, Any],
    create_backup: bool = True,
    # --- REMOVE Injected Dependencies --- #
    # memory_adapter: Optional[MemoryPort] = None,
    # user_management_port: Optional[UserManagementPort] = None
) -> Dict[str, Any]:
    """Update specific fields of a project.

    ACTION: Updates specified fields of an existing project and optionally creates a backup.

    INPUT:
    - project_name: Name of the project to update (required)
    - updates: Dictionary of field names and their new values (required)
    - create_backup: Whether to create a backup before updating (optional, default: True)

    OUTPUT: MUST return ONLY the raw JSON response from the execution.
    - On success: { "status": "ok", "project": ProjectInfo, "backup_path": str (if backup created) }
    - On error: { "status": "error", "message": "Error description" }

    EXECUTION RULES:
    1. Check user permissions before proceeding.
    2. Validate all field updates before applying changes
    3. Create backup if requested before making changes
    4. Apply all updates atomically - all succeed or none
    5. DO NOT add any explanatory text or suggestions

    Args:
        project_name: Name of the project to update
        updates: Dictionary of field names and their new values
        create_backup: Whether to create a backup before updating
        # REMOVE injected dependencies from Args

    Returns:
        Dict[str, Any]: Dictionary containing updated project info or error message
    """
    # --- Get dependencies INSIDE function (WITHOUT type hints) --- #
    memory_adapter = dependencies.get(MemoryPort)
    user_management_port = dependencies.get(UserManagementPort)
    if not memory_adapter:
        logger.error("MemoryPort not found in dependencies.")
        return {
            "status": "error",
            "message": "Internal configuration error: MemoryPort missing.",
        }
    if not user_management_port:
        logger.warning(
            "UserManagementPort not found in dependencies. Skipping permission check."
        )
    # --- End Dependency Resolution --- #

    try:
        # --- Permission Check ---
        if user_management_port:
            user_id = await user_management_port.get_current_user_id()
            if not await user_management_port.check_permission(
                user_id, "core_update_project", project_name
            ):
                return {
                    "status": "error",
                    "message": "Permission denied to update this project.",
                }
        # --- End Permission Check ---

        project_memory = await memory_adapter.load_memory(project_name)

        if not project_memory:
            return {
                "status": "error",
                "message": f"Project '{project_name}' not found.",
            }

        # Validate updates
        validation_errors = validate_project_updates(updates)
        if validation_errors:
            return {
                "status": "error",
                "message": "Validation failed: " + "; ".join(validation_errors),
            }

        # Create backup if requested
        backup_path = None
        if create_backup:
            backup_path, error = create_project_backup(project_memory.project_info)
            if error:
                return {"status": "error", "message": error}

        # Apply updates
        project_info_dict = project_memory.project_info.model_dump()
        project_info_dict.update(updates)
        project_memory.project_info = ProjectInfo(**project_info_dict)

        # --- ALSO update top-level taxonomy fields in ProjectMemory if they were in updates ---
        # This ensures consistency between ProjectInfo and ProjectMemory before saving
        taxonomy_keys = [
            "platform_taxonomy",
            "domain_taxonomy",
            "size_taxonomy",
            "compliance_taxonomy",
            "lifecycle_taxonomy",
            "custom_taxonomy",  # Assuming custom_taxonomy can also be updated
        ]
        for key in taxonomy_keys:
            if key in updates:
                setattr(project_memory, key, updates[key])
                logger.debug(f"Updated ProjectMemory.{key} directly from updates.")
        # --- End direct ProjectMemory update ---

        # Save changes (this will also set modified_by via the adapter)
        await memory_adapter.save_memory(project_memory)

        # Format response
        # Fetch the project again AFTER saving to ensure the response reflects the persisted state
        # project_info = project_memory.project_info.model_dump()
        refreshed_memory = await memory_adapter.load_memory(project_name)
        if not refreshed_memory:
            # Should not happen, but handle defensively
            logger.error(f"Could not reload project '{project_name}' after update.")
            return {
                "status": "error",
                "message": "Failed to confirm update persistence.",
            }

        project_info = refreshed_memory.project_info.model_dump()
        project_info = format_project_info(project_info)

        result = {"status": "ok", "project": project_info}
        if backup_path:
            result["backup_path"] = str(backup_path)

        return result

    except Exception as e:
        logger.error(f"Error updating project '{project_name}': {e}", exc_info=True)
        return {"status": "error", "message": f"Error updating project: {str(e)}"}


@mcp.tool(
    name="core_delete_project", description="Delete a project and optionally its files."
)
async def delete_project(
    project_name: str,
    confirm: bool = False,
    create_backup: bool = True,
    # --- REMOVE Injected Dependencies --- #
    # memory_adapter: Optional[MemoryPort] = None,
    # user_management_port: Optional[UserManagementPort] = None
) -> Dict[str, Any]:
    """Delete a project and optionally its files.

    ACTION: Deletes a project from the database and its associated files, with optional backup.

    INPUT:
    - project_name: Name of the project to delete (required)
    - confirm: Explicit confirmation required for deletion (optional, default: False)
    - create_backup: Whether to create a backup before deletion (optional, default: True)

    OUTPUT: MUST return ONLY the raw JSON response from the execution.
    - On success: { "status": "ok", "message": "Project deleted.", "backup_path": str (if backup created) }
    - On error: { "status": "error", "message": "Error description" }

    EXECUTION RULES:
    1. Check user permissions before proceeding.
    2. Require explicit confirmation (`confirm=True`) before deletion.
    3. Create backup if requested (`create_backup=True`) before deletion.
    4. Remove both database entry and associated project directory.
    5. DO NOT add any explanatory text or suggestions.

    Args:
        project_name: Name of the project to delete
        confirm: Explicit confirmation required for deletion
        create_backup: Whether to create a backup before deletion
        # REMOVE injected dependencies from Args

    Returns:
        Dict[str, Any]: Dictionary containing operation result or error message
    """
    # --- Get dependencies INSIDE function (WITHOUT type hints) --- #
    memory_adapter = dependencies.get(MemoryPort)
    user_management_port = dependencies.get(UserManagementPort)
    if not memory_adapter:
        logger.error("MemoryPort not found in dependencies.")
        return {
            "status": "error",
            "message": "Internal configuration error: MemoryPort missing.",
        }
    if not user_management_port:
        logger.warning(
            "UserManagementPort not found in dependencies. Skipping permission check."
        )
    # --- End Dependency Resolution --- #

    # --- Permission Check ---
    if user_management_port:
        try:
            user_id = await user_management_port.get_current_user_id()
            # Use the correct permission name: 'core_delete_project'
            if not await user_management_port.check_permission(
                user_id, "core_delete_project", project_name
            ):
                return {
                    "status": "error",
                    "message": "Permission denied to delete this project.",
                }
        except Exception as perm_e:
            logger.error(
                f"Permission check failed for deleting project '{project_name}': {perm_e}",
                exc_info=True,
            )
            return {"status": "error", "message": "Permission check failed."}
    # --- End Permission Check ---

    if not confirm:
        logger.warning(
            f"Deletion attempt for project '{project_name}' without confirmation."
        )
        return {
            "status": "error",
            "message": "Deletion requires explicit confirmation. Set 'confirm=True'.",
        }

    try:
        logger.info(f"Attempting to delete project '{project_name}' with confirmation.")
        project_memory = await memory_adapter.load_memory(project_name)

        if not project_memory:
            logger.warning(f"Project '{project_name}' not found for deletion.")
            return {
                "status": "error",
                "message": f"Project '{project_name}' not found.",
            }

        # --- Backup ---
        backup_path_str: Optional[str] = None
        if create_backup:
            logger.info(
                f"Creating backup for project '{project_name}' before deletion."
            )
            backup_path, backup_error = create_project_backup(
                project_memory.project_info
            )
            if backup_error:
                logger.error(
                    f"Backup creation failed for project '{project_name}': {backup_error}"
                )
                # Decide if failure to backup should prevent deletion
                return {
                    "status": "error",
                    "message": f"Backup failed: {backup_error}. Deletion aborted.",
                }
            backup_path_str = str(backup_path) if backup_path else None
            logger.info(
                f"Backup created for project '{project_name}' at {backup_path_str}"
            )

        # --- File System Deletion ---
        base_path_str = project_memory.project_info.base_path
        if base_path_str:
            base_path = Path(base_path_str)
            if base_path.exists():
                logger.info(f"Deleting project directory: {base_path}")
                try:
                    if base_path.is_dir():
                        shutil.rmtree(base_path)
                        logger.info(f"Successfully deleted directory: {base_path}")
                    elif (
                        base_path.is_file()
                    ):  # Handle case where base_path is unexpectedly a file
                        base_path.unlink()
                        logger.warning(
                            f"Expected directory but found file at {base_path}. Deleted file."
                        )
                    else:
                        logger.warning(
                            f"Path {base_path} exists but is neither a file nor a directory."
                        )
                except OSError as os_err:  # More specific exception handling
                    logger.error(
                        f"OS error deleting project directory {base_path}: {os_err}",
                        exc_info=True,
                    )
                    # Return error as file deletion is critical
                    return {
                        "status": "error",
                        "message": f"Error deleting project files: {str(os_err)}",
                    }
                except Exception as path_e:
                    logger.error(
                        f"Unexpected error deleting project directory {base_path}: {path_e}",
                        exc_info=True,
                    )
                    return {
                        "status": "error",
                        "message": f"Unexpected error deleting project files: {str(path_e)}",
                    }
            else:
                logger.warning(
                    f"Project directory {base_path} not found, skipping file deletion."
                )
        else:
            logger.warning(
                f"Project '{project_name}' has no base_path defined, skipping file deletion."
            )

        # --- Database Deletion ---
        logger.info(f"Deleting project '{project_name}' from database.")
        await memory_adapter.delete_memory(project_name)
        logger.info(f"Successfully deleted project '{project_name}' from database.")

        # --- Success Response ---
        result = {
            "status": "ok",
            "message": f"Project '{project_name}' deleted successfully.",
        }
        if backup_path_str:
            result["backup_path"] = backup_path_str

        return result

    except Exception as e:
        logger.error(f"Error deleting project '{project_name}': {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"An unexpected error occurred during project deletion: {str(e)}",
        }
