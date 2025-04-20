"""
Plugin for listing existing PAELLADOC projects.
"""

import logging
from typing import List, Optional
from pathlib import Path

from paelladoc.domain.core_logic import mcp
# Adapter for persistence
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

logger = logging.getLogger(__name__)

@mcp.tool(
    name="core.list_projects",
    description="Lists the names of existing PAELLADOC projects found in the memory."
)
async def list_projects(db_path: str = None) -> dict:
    """Retrieves the list of project names from the persistence layer.
    
    Args:
        db_path: Optional database path to use (primarily for testing).
        
    Returns:
        A dictionary containing the status and a list of project names.
        Example:
        {
            "status": "ok",
            "message": "Found 2 projects.",
            "projects": ["project-a", "project-b"]
        }
        Or:
        {
            "status": "ok",
            "message": "No projects found.",
            "projects": []
        }
        Or:
        {
            "status": "error",
            "message": "Error retrieving projects: [error details]"
        }
    """
    logger.info(f"Executing core.list_projects command. DB path: {db_path}")
    
    try:
        # Use the provided db_path (for tests) or default
        if db_path:
            memory_adapter = SQLiteMemoryAdapter(db_path=Path(db_path))
        else:
            memory_adapter = SQLiteMemoryAdapter()
    except Exception as e:
        logger.error(f"Failed to instantiate SQLiteMemoryAdapter: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Internal server error: Could not initialize memory adapter.",
        }

    try:
        project_names = await memory_adapter.list_projects()
        count = len(project_names)
        message = f"Found {count} project{'s' if count > 1 else ''}." if count > 0 else "No projects found."
        logger.info(message)
        return {
            "status": "ok",
            "message": message,
            "projects": project_names
        }
    except Exception as e:
        logger.error(f"Error retrieving projects from memory adapter: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error retrieving projects: {e}"
        } 