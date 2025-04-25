"""
Core plugin for project CRUD operations.
"""

import logging
from pathlib import Path
from typing import Dict, Any

from paelladoc.domain.core_logic import mcp
from paelladoc.domain.models.project import ProjectInfo
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
from .project_utils import (
    validate_project_updates,
    create_project_backup,
    format_project_info,
)

logger = logging.getLogger(__name__)


@mcp.tool(
    name="core_get_project",
    description="Get detailed information about a specific project.",
)
async def get_project(project_name: str) -> Dict[str, Any]:
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

    Returns:
        Dict[str, Any]: Dictionary containing project info or error message
    """
    try:
        adapter = SQLiteMemoryAdapter()
        project_memory = await adapter.load_memory(project_name)

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
    project_name: str, updates: Dict[str, Any], create_backup: bool = True
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
    1. Validate all field updates before applying changes
    2. Create backup if requested before making changes
    3. Apply all updates atomically - all succeed or none
    4. DO NOT add any explanatory text or suggestions

    Args:
        project_name: Name of the project to update
        updates: Dictionary of field names and their new values
        create_backup: Whether to create a backup before updating

    Returns:
        Dict[str, Any]: Dictionary containing updated project info or error message
    """
    try:
        adapter = SQLiteMemoryAdapter()
        project_memory = await adapter.load_memory(project_name)

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

        # Save changes
        await adapter.save_memory(project_memory)

        # Format response
        project_info = project_memory.project_info.model_dump()
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
    project_name: str, confirm: bool = False, create_backup: bool = True
) -> Dict[str, Any]:
    """Delete a project and optionally its files.

    ACTION: Deletes a project from the database and its associated files, with optional backup.

    INPUT:
    - project_name: Name of the project to delete (required)
    - confirm: Explicit confirmation required for deletion (optional, default: False)
    - create_backup: Whether to create a backup before deletion (optional, default: True)

    OUTPUT: MUST return ONLY the raw JSON response from the execution.
    - On success: { "status": "ok", "backup_path": str (if backup created) }
    - On error: { "status": "error", "message": "Error description" }

    EXECUTION RULES:
    1. Require explicit confirmation before deletion
    2. Create backup if requested before deletion
    3. Remove both database entry and associated files
    4. DO NOT add any explanatory text or suggestions

    Args:
        project_name: Name of the project to delete
        confirm: Explicit confirmation required for deletion
        create_backup: Whether to create a backup before deletion

    Returns:
        Dict[str, Any]: Dictionary containing operation result or error message
    """
    if not confirm:
        return {
            "status": "error",
            "message": "Confirmation required for project deletion.",
        }

    try:
        adapter = SQLiteMemoryAdapter()
        project_memory = await adapter.load_memory(project_name)

        if not project_memory:
            return {
                "status": "error",
                "message": f"Project '{project_name}' not found.",
            }

        # Create backup if requested
        backup_path = None
        if create_backup:
            backup_path, error = create_project_backup(project_memory.project_info)
            if error:
                return {"status": "error", "message": error}

        # Delete project files
        base_path = Path(project_memory.project_info.base_path)
        if base_path.exists():
            try:
                base_path.rmdir()  # Try safe rmdir first
            except OSError:
                # If directory not empty, use rmtree
                import shutil

                shutil.rmtree(base_path)

        # Delete from database
        await adapter.delete_memory(project_name)

        result = {"status": "ok"}
        if backup_path:
            result["backup_path"] = str(backup_path)

        return result

    except Exception as e:
        logger.error(f"Error deleting project '{project_name}': {e}", exc_info=True)
        return {"status": "error", "message": f"Error deleting project: {str(e)}"}
