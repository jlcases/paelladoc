"""
Core PAELLADOC MCP Logic.

Handles MCP instance creation, plugin loading, and base tool registration.
Uses FastMCP for compatibility with decorators.
"""
import logging
from mcp.server.fastmcp import FastMCP # Use FastMCP
from typing import Dict, Any

# Configure base logger (handlers will be added by server.py)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the MCP server instance using FastMCP
mcp = FastMCP("PAELLADOC")

# --- Register Tools/Prompts --- #

# Import plugins dynamically to register tools/prompts
try:
    # Import from the new adapters location
    import paelladoc.adapters.plugins
    logger.info("Successfully loaded plugins from paelladoc.adapters.plugins")
except ImportError as e:
    # Log as warning, server might still be usable with base tools
    logger.warning(f"Could not import plugins from paelladoc.adapters.plugins: {e}")
except Exception as e:
    # Log as error for unexpected issues during import
    logger.error(f"An unexpected error occurred during plugin import: {e}", exc_info=True)

@mcp.tool() # Use decorator again
def ping(random_string: str = "") -> Dict[str, Any]:
    """
    Basic health check; returns pong.
    
    Args:
        random_string (str, optional): Dummy parameter for no-parameter tools

    Returns:
        Dict[str, Any]: Response with status and message
    """
    logger.debug(f"Ping tool called with parameter: {random_string}")
    return {
        "status": "ok", 
        "message": "pong"
    }

# Tools will be registered here by plugins

# Note: No `if __name__ == "__main__":` block here.
# This file is intended to be imported by the entry point (server.py).