"""
Core plugin for project CRUD operations.
"""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from paelladoc.domain.models.language import SupportedLanguage
from paelladoc.domain.models.project import ProjectInfo
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

logger = logging.getLogger(__name__)


async def get_project(project_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific project.

    Args:
        project_name: Name of the project to retrieve.

    Returns:
        Dict with status and project information or error message.
    """
    try:
        adapter = SQLiteMemoryAdapter()
        project_memory = await adapter.load_memory(project_name)

        if not project_memory:
            return {
                "status": "error",
                "message": f"Project '{project_name}' not found.",
            }

        # Convert project info to dict and ensure base_path is str
        project_info = project_memory.project_info.model_dump()
        project_info["base_path"] = str(project_info["base_path"])

        return {"status": "ok", "project": project_info}

    except Exception as e:
        logger.error(f"Error retrieving project '{project_name}': {e}", exc_info=True)
        return {"status": "error", "message": f"Error retrieving project: {str(e)}"}


async def update_project(
    project_name: str, updates: Dict[str, Any], create_backup: bool = True
) -> Dict[str, Any]:
    """
    Update specific fields of a project.

    Args:
        project_name: Name of the project to update.
        updates: Dictionary of field names and their new values.
        create_backup: Whether to create a backup before updating.

    Returns:
        Dict with status and updated project info or error message.
    """
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
            backup_path = _create_backup(project_memory.project_info)

        # Validate updates
        for field, value in updates.items():
            if field == "documentation_language" and value not in [
                lang.value for lang in SupportedLanguage
            ]:
                return {
                    "status": "error",
                    "message": f"Invalid documentation language: {value}",
                }
            # Add more field validations as needed

        # Apply updates
        project_info_dict = project_memory.project_info.model_dump()
        project_info_dict.update(updates)
        project_memory.project_info = ProjectInfo(**project_info_dict)

        # Save changes
        await adapter.save_memory(project_memory)

        # Convert project info to dict and ensure base_path is str
        project_info = project_memory.project_info.model_dump()
        project_info["base_path"] = str(project_info["base_path"])

        result = {"status": "ok", "project": project_info}
        if backup_path:
            result["backup_path"] = str(backup_path)

        return result

    except Exception as e:
        logger.error(f"Error updating project '{project_name}': {e}", exc_info=True)
        return {"status": "error", "message": f"Error updating project: {str(e)}"}


async def delete_project(
    project_name: str, confirm: bool = False, create_backup: bool = True
) -> Dict[str, Any]:
    """
    Delete a project and optionally its files.

    Args:
        project_name: Name of the project to delete.
        confirm: Explicit confirmation required for deletion.
        create_backup: Whether to create a backup before deletion.

    Returns:
        Dict with status and optional backup path or error message.
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
            backup_path = _create_backup(project_memory.project_info)

        # Delete project files
        base_path = Path(project_memory.project_info.base_path)
        if base_path.exists():
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


def _create_backup(project_info: ProjectInfo) -> Optional[Path]:
    """Create a backup of project files."""
    try:
        base_path = Path(project_info.base_path)
        if not base_path.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{project_info.name}_backup_{timestamp}"
        backup_path = base_path.parent / f"{backup_name}.zip"

        shutil.make_archive(str(backup_path.with_suffix("")), "zip", base_path)

        return backup_path

    except Exception as e:
        logger.error(f"Error creating backup for project '{project_info.name}': {e}")
        return None
