"""
Plugin for listing existing PAELLADOC projects.
"""

import logging
from typing import Dict, Any
from pathlib import Path

from paelladoc.domain.core_logic import mcp

# Adapter for persistence
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter
# Project model is not needed here, we only list names

logger = logging.getLogger(__name__)


@mcp.tool(
    name="core.list_projects",
    description="Lists the names of existing PAELLADOC projects found in the memory.",
)
async def list_projects(
    db_path: str = None,
) -> Dict[str, Any]:  # Keep db_path for testing
    """Retrieves the list of project names from the persistence layer.

    Args:
        db_path: Optional database path to use (primarily for testing).

    Returns:
        A dictionary containing the status and a list of project names.
    """
    logger.info(f"Executing core.list_projects command. DB path: {db_path}")

    try:
        # Use the provided db_path (for tests) or the default path from the adapter
        memory_adapter = (
            SQLiteMemoryAdapter(db_path=Path(db_path))
            if db_path
            else SQLiteMemoryAdapter()
        )
        logger.info(
            f"core.list_projects using DB path: {memory_adapter.db_path.resolve()}"
        )  # Log the actual path used
    except Exception as e:
        logger.error(f"Failed to instantiate SQLiteMemoryAdapter: {e}", exc_info=True)
        return {
            "status": "error",
            "message": "Internal server error: Could not initialize memory adapter.",
            "projects": [],  # Return empty list on error
        }

    try:
        # Use the correct method to get only names
        project_names = await memory_adapter.list_projects()
        count = len(project_names)
        message = (
            f"Found {count} project{'s' if count != 1 else ''}."
            if count > 0
            else "No projects found."
        )
        logger.info(message)
        return {
            "status": "ok",  # Use 'ok' for success
            "message": message,
            "projects": project_names,  # Return the list of names
        }
    except Exception as e:
        logger.error(
            f"Error retrieving projects from memory adapter: {e}", exc_info=True
        )
        return {
            "status": "error",
            "message": f"Error retrieving projects: {str(e)}",
            "projects": [],  # Return empty list on error
        }
