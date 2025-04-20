"""
End-to-End tests for Paelladoc MCP Server.

This simulates how Cursor would interact with the server.
"""

import unittest
import sys
from pathlib import Path

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import directly from the domain layer
from paelladoc.domain.core_logic import mcp, ping


class TestCursorE2E(unittest.TestCase):
    """End-to-End tests simulating Cursor interacting with Paelladoc."""

    def test_direct_ping_call(self):
        """Test direct call to the ping function."""
        # Call the ping function directly
        result = ping()

        # Verify the result
        self.assertIsInstance(result, dict, "Ping should return a dict")
        self.assertEqual(result["status"], "ok", "Status should be 'ok'")
        self.assertEqual(result["message"], "pong", "Message should be 'pong'")

    def test_ping_with_parameter(self):
        """Test ping function with a parameter."""
        # Call ping with a test parameter
        result = ping(random_string="test-parameter")

        # Verify the result
        self.assertIsInstance(result, dict, "Ping should return a dict")
        self.assertEqual(result["status"], "ok", "Status should be 'ok'")
        self.assertEqual(result["message"], "pong", "Message should be 'pong'")

    def test_mcp_tool_registration(self):
        """Verify that the ping tool is registered with MCP."""
        # Get tools registered with MCP
        tool_manager = getattr(mcp, "_tool_manager", None)
        self.assertIsNotNone(tool_manager, "MCP should have a tool manager")

        tools = tool_manager.list_tools()

        # Check if the ping tool is registered
        tool_names = [tool.name for tool in tools]
        self.assertIn("ping", tool_names, "Ping tool should be registered with MCP")


if __name__ == "__main__":
    unittest.main()
