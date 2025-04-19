#!/usr/bin/env python3
"""
Basic PAELLADOC MCP Server using FastMCP from the official SDK.
"""

from mcp.server.fastmcp import FastMCP
import argparse
import logging
import sys
import socket

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_port_available(host, port):
    """Check if a port is available on the specified host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.bind((host, port))
            return True
    except (socket.error, OSError):
        return False

# Create the MCP server instance
mcp = FastMCP("PAELLADOC Experimental")

# --- Register Tools/Prompts --- #

# Import plugins dynamically to register tools/prompts
try:
    # Assuming mcp_server directory is in the same root as server.py
    # Adjust PYTHONPATH if server.py is moved or plugins are elsewhere
    import mcp_server.plugins
    logger.info("Successfully loaded plugins from mcp_server.plugins")
except ImportError as e:
    logger.warning(f"Could not import plugins from mcp_server.plugins: {e}. Ensure the directory and __init__.py exist.")
except Exception as e:
    logger.error(f"An unexpected error occurred during plugin import: {e}", exc_info=True)

# Example basic tool (keep ping for basic health check)
@mcp.tool()
def ping() -> dict:
    """Basic health check; returns pong."""
    logger.debug("Ping tool called")
    return {"status": "ok", "message": "pong"}

# --- Main Execution --- #

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PAELLADOC MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host interface to bind (default: 0.0.0.0)")
    args = parser.parse_args()

    host, port = args.host, args.port

    # Check port availability before starting
    if not is_port_available(host, port):
        logger.error(f"Port {port} is already in use on {host}. Please choose another port.")
        sys.exit(1)

    logger.info(f"Starting PAELLADOC MCP server on http://{host}:{port}")
    try:
        # Use mcp.run() which handles the underlying ASGI server (like uvicorn)
        mcp.run(host=host, port=port)
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}", exc_info=True)
        sys.exit(1) 