#!/usr/bin/env python3
"""
PAELLADOC MCP Server entry point (Input Adapter).

Relies on paelladoc_core.py (now core_logic.py in domain) for MCP functionality and FastMCP instance.
Simply runs the imported MCP instance.
Adds server-specific resources and prompts using decorators.
"""

import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import time # Add time import

# Import TextContent for prompt definition
from mcp.types import TextContent # Assuming mcp is installed in .venv

# Import the core FastMCP instance and logger from the domain layer
from paelladoc.domain.core_logic import mcp, logger # Corrected import path

# --- Add specific tools/resources/prompts for this entry point using decorators --- #

@mcp.tool() # Use decorator
def generate_documentation(repo_path: str, output_path: Optional[str] = None) -> Dict[str, Any]:
    """Generate documentation for a repository."""
    try:
        # TODO: Implement actual documentation generation logic using Application layer
        logger.info(f"Placeholder: Generating docs for {repo_path} to {output_path or 'default'}")
        return {"status": "success", "message": "Documentation generation (placeholder) complete"}
    except Exception as e:
        logger.error(f"Error generating documentation: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}

@mcp.tool() # Use decorator
def verify_documentation(docs_path: str) -> Dict[str, Any]:
    """Verify documentation against codebase."""
    try:
        # TODO: Implement actual documentation verification logic using Application layer
        logger.info(f"Placeholder: Verifying docs at {docs_path}")
        return {"status": "success", "message": "Documentation verification (placeholder) complete"}
    except Exception as e:
        logger.error(f"Error verifying documentation: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}

@mcp.resource("docs://readme") # Use decorator
def get_readme() -> str:
    """Get the project README content."""
    try:
        # Assuming README.md is in the project root (cwd)
        readme_path = Path("README.md")
        if readme_path.exists():
            return readme_path.read_text()
        else:
            logger.warning("README.md not found in project root.")
            return "README.md not found" # Keep simple return for resource
    except Exception as e:
        logger.error(f"Error reading README.md: {e}", exc_info=True)
        return f"Error reading README.md: {str(e)}"

@mcp.resource("docs://templates/{template_name}") # Use decorator
def get_template(template_name: str) -> str:
    """Get a documentation template."""
    # Corrected path relative to src directory
    base_path = Path(__file__).parent.parent.parent.parent # Should point to src/
    template_path = base_path / "paelladoc" / "adapters" / "plugins" / "templates" / f"{template_name}.md"
    try:
        if template_path.exists():
            return template_path.read_text()
        else:
            logger.warning(f"Template {template_name} not found at {template_path}")
            return f"Error: Template {template_name} not found"
    except Exception as e:
        logger.error(f"Error reading template {template_name}: {e}", exc_info=True)
        return f"Error reading template {template_name}: {str(e)}"

@mcp.prompt() # Use decorator
def paella_command(project_name: str) -> TextContent:
    """Create a PAELLA command prompt."""
    return TextContent(
        type="text",
        text=f"Initiating PAELLADOC for project: {project_name}.\n" 
             f"Please specify: 1. Project type, 2. Methodologies, 3. Git workflow."
    )

# --- Main Execution Logic --- #

if __name__ == "__main__":
    # Configure file logging
    try:
        log_file = 'paelladoc_server.log' 
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().setLevel(logging.DEBUG)
        logger.info(f"Logging configured. Outputting to {log_file}")
    except Exception as log_e:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        # Re-get logger after basicConfig potentially reconfigured root
        logger = logging.getLogger(__name__) 
        logger.error(f"Could not configure file logging: {log_e}. Logging to stderr.")

    # Check command line arguments to determine run mode
    run_mode = "stdio" if "--stdio" in sys.argv else "web" # Default to stdio if --stdio present

    try:
        if run_mode == "stdio":
            logger.info("Starting PAELLADOC MCP server in STDIO mode via FastMCP mcp.run(transport='stdio')...")
            logger.debug("Waiting 10 seconds before mcp.run()...")
            time.sleep(10) # Add sleep before run
            logger.debug("Attempting mcp.run(transport=\"stdio\")")
            mcp.run(transport="stdio") # Explicitly request stdio transport
        else:
            # Attempt to run the default web server (SSE)
            # Note: FastMCP's default run() might try stdio first anyway if no host/port specified
            logger.warning("Starting PAELLADOC MCP server in default mode (likely web/SSE) via FastMCP mcp.run()...")
            logger.warning("Use --stdio argument for direct client integration.")
            mcp.run() # Run with default settings (tries SSE/web)

        logger.info(f"PAELLADOC MCP server finished (mode: {run_mode}).") 
    except Exception as e:
        logger.critical(f"Failed to start or run MCP server: {e}", exc_info=True)
        sys.exit(1) 