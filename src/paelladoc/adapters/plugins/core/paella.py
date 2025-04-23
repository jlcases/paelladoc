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


@mcp.tool(
    name="paella_init",
    description="Initiates the conversational workflow to define and document a new PAELLADOC project",
)
async def paella_init(
    base_path: str,
    documentation_language: str,
    interaction_language: str,
    new_project_name: str,
    platform_taxonomy: str,  # e.g., "pwa", "web-frontend", "vscode-extension"
    domain_taxonomy: str,
    size_taxonomy: str,
    compliance_taxonomy: str,
    lifecycle_taxonomy: str,
    custom_taxonomy: Optional[Dict] = None,  # Still optional
) -> Dict:
    """
    Initiates the conversational workflow to define and document a new PAELLADOC project.

    This tool gathers essential project details, including the core taxonomies (platform,
    domain, size, compliance) which are mandatory for project setup and analysis.

    It creates the project structure and persists the initial memory state with all
    provided information.

    Once executed successfully, the project is initialized with its defined taxonomies and ready
    for the next conversational steps.

    Args:
        base_path: Base path where the project documentation will be stored.
        documentation_language: Primary language for the generated documentation (e.g., 'en', 'es').
        interaction_language: Language used during conversational interactions (e.g., 'en', 'es').
        new_project_name: Unique name for the new PAELLADOC project.
        platform_taxonomy: Identifier for the target platform (e.g., "pwa", "web-frontend").
        domain_taxonomy: Identifier for the project's domain (e.g., "ecommerce", "healthcare").
        size_taxonomy: Identifier for the estimated project size (e.g., "mvp", "enterprise").
        compliance_taxonomy: Identifier for any compliance requirements (e.g., "gdpr", "none").
        lifecycle_taxonomy: Identifier for the project's lifecycle (e.g., "startup", "growth").
        custom_taxonomy: (Optional) A dictionary for any user-defined taxonomy.

    Returns:
        A dictionary confirming the project's creation ('status': 'ok') or detailing an error ('status': 'error').
        On success, includes the 'project_name' and resolved 'base_path'.
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

        # Create project memory - passing required taxonomies directly
        project_memory = ProjectMemory(
            project_info=ProjectInfo(
                name=new_project_name,
                interaction_language=interaction_language,
                documentation_language=documentation_language,
                base_path=abs_base_path,
                platform_taxonomy=platform_taxonomy,
                domain_taxonomy=domain_taxonomy,
                size_taxonomy=size_taxonomy,
                compliance_taxonomy=compliance_taxonomy,
                lifecycle_taxonomy=lifecycle_taxonomy,
                custom_taxonomy=custom_taxonomy if custom_taxonomy else {},
            ),
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
            platform_taxonomy=platform_taxonomy,
            domain_taxonomy=domain_taxonomy,
            size_taxonomy=size_taxonomy,
            compliance_taxonomy=compliance_taxonomy,
            lifecycle_taxonomy=lifecycle_taxonomy,
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


@mcp.tool(
    name="paella_list",
    description="Retrieves detailed information for all PAELLADOC projects stored in the system memory",
)
async def paella_list() -> Dict:
    """Retrieves detailed information (ProjectInfo objects) for all PAELLADOC projects stored in the system memory.

    This tool provides comprehensive information about each project, including:
    - Project name and languages
    - Base path and purpose
    - Target audience and objectives
    - All taxonomy configurations
    - Validation status

    This is useful for:
    - Getting an overview of all projects
    - Selecting a project to work on with 'paella_select'
    - Verifying project configurations

    Returns:
        A dictionary containing:
        - status: 'ok' or 'error'
        - projects: List[ProjectInfo] - Complete information for each project
        - message: Description of the operation result
    """
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


@mcp.tool(
    name="paella_select",
    description="Loads the memory of an existing PAELLADOC project and sets it as the active context",
)
async def paella_select(project_name: str) -> Dict:
    """
    Loads the memory of an existing PAELLADOC project and sets it as the active context.

    This tool makes the specified project the current focus for subsequent conversational
    commands and actions within the Paelladoc session. It retrieves the project's state
    from the persistent memory.

    Args:
        project_name: The name of the existing PAELLADOC project to activate.

    Returns:
        A dictionary containing the operation status ('ok' or 'error'), a confirmation message,
        and key details of the selected project (name, base path). Returns an error status
        if the project is not found.
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
