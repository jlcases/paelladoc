"""PAELLADOC project initialization module."""

from pathlib import Path
from typing import Dict, Optional

# Import the shared FastMCP instance from core_logic
from paelladoc.domain.core_logic import mcp, logger

# Domain models and services
from paelladoc.domain.models.project import (
    ProjectMemory,
    ProjectInfo,
    Bucket,
    DocumentStatus,
    set_time_service,
)
from paelladoc.adapters.services.system_time_service import SystemTimeService

# Adapter for persistence
from paelladoc.adapters.output.sqlite.sqlite_memory_adapter import SQLiteMemoryAdapter

# Initialize logger for this module
# logger is already imported from core_logic

# Create FastMCP instance - REMOVED, using imported instance
# mcp = FastMCP("PAELLADOC")


@mcp.tool()
async def paella_init(
    base_path: str,
    documentation_language: str,
    interaction_language: str,
    new_project_name: str,
    # Add optional taxonomy arguments
    platform_taxonomy: Optional[str] = None,
    domain_taxonomy: Optional[str] = None,
    size_taxonomy: Optional[str] = None,
    compliance_taxonomy: Optional[str] = None,
    custom_taxonomy: Optional[Dict] = None,  # Allow passing custom taxonomy data
) -> Dict:
    """
    Initialize a new PAELLADOC project.

    Args:
        base_path: Base path for project documentation
        documentation_language: Language for documentation (e.g. 'es', 'en')
        interaction_language: Language for interaction (e.g. 'es', 'en')
        new_project_name: Name of the new project
        platform_taxonomy: Selected platform taxonomy identifier.
        domain_taxonomy: Selected domain taxonomy identifier.
        size_taxonomy: Selected size taxonomy identifier.
        compliance_taxonomy: Selected compliance taxonomy identifier.
        custom_taxonomy: Dictionary containing custom taxonomy data.
    """
    logger.info(
        f"Initializing new project: {new_project_name} with taxonomies: Platform={platform_taxonomy}, Domain={domain_taxonomy}, Size={size_taxonomy}, Compliance={compliance_taxonomy}"
    )

    try:
        # Initialize TimeService with SystemTimeService implementation
        set_time_service(SystemTimeService())

        # Initialize memory adapter
        memory_adapter = SQLiteMemoryAdapter()

        # Create absolute path
        abs_base_path = Path(base_path).expanduser().resolve()

        # Ensure the base directory exists
        abs_base_path.mkdir(parents=True, exist_ok=True)

        # Create project memory
        project_memory = ProjectMemory(
            project_info=ProjectInfo(
                name=new_project_name,
                interaction_language=interaction_language,
                documentation_language=documentation_language,
                base_path=abs_base_path,
                # Pass taxonomy info to ProjectInfo
                platform_taxonomy=platform_taxonomy,
                domain_taxonomy=domain_taxonomy,
                size_taxonomy=size_taxonomy,
                compliance_taxonomy=compliance_taxonomy,
                custom_taxonomy=custom_taxonomy if custom_taxonomy else {},
            ),
            # Keep the initial artifact example or adjust as needed
            artifacts={
                Bucket.INITIATE_INITIAL_PRODUCT_DOCS: [
                    {
                        "name": "Project Charter",
                        "status": DocumentStatus.PENDING,
                        "bucket": Bucket.INITIATE_INITIAL_PRODUCT_DOCS,
                        "path": Path("Project_Charter.md"),
                    }
                ]
            },
            # Set taxonomy fields also directly on ProjectMemory if needed by its logic
            # (Based on current model, ProjectInfo holds them primarily)
            platform_taxonomy=platform_taxonomy,
            domain_taxonomy=domain_taxonomy,
            size_taxonomy=size_taxonomy,
            compliance_taxonomy=compliance_taxonomy,
            custom_taxonomy=custom_taxonomy if custom_taxonomy else {},
        )

        # Save to memory
        await memory_adapter.save_memory(project_memory)

        return {
            "status": "ok",
            "message": f"Project '{new_project_name}' created successfully at {abs_base_path}",
            "project_name": new_project_name,
            "base_path": str(abs_base_path),
        }

    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        return {"status": "error", "message": f"Failed to create project: {str(e)}"}


@mcp.tool()
async def paella_list() -> Dict:
    """List all available PAELLADOC projects."""
    try:
        memory_adapter = SQLiteMemoryAdapter()
        projects = await memory_adapter.list_projects()

        return {
            "status": "ok",
            "projects": projects,
            "message": "Projects retrieved successfully",
        }
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        return {"status": "error", "message": f"Failed to list projects: {str(e)}"}


@mcp.tool()
async def paella_select(project_name: str) -> Dict:
    """
    Select an existing PAELLADOC project.

    Args:
        project_name: Name of the project to select
    """
    try:
        memory_adapter = SQLiteMemoryAdapter()
        project_memory = await memory_adapter.load_memory(project_name)

        if project_memory:
            return {
                "status": "ok",
                "message": f"Project '{project_name}' selected",
                "project_name": project_name,
                "base_path": str(project_memory.project_info.base_path),
            }
        else:
            return {"status": "error", "message": f"Project '{project_name}' not found"}
    except Exception as e:
        logger.error(f"Error selecting project: {str(e)}")
        return {"status": "error", "message": f"Failed to select project: {str(e)}"}


# Remove the main execution block as this module is not meant to be run directly
# if __name__ == "__main__":
#     mcp.run()
