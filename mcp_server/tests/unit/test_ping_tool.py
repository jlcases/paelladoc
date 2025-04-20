"""
Unit tests for Paelladoc MCP tools.

Following TDD approach - tests are written before implementation.
"""

import unittest
import sys
import os
from pathlib import Path

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# The module where ping will be implemented
# Note: At this stage, the ping function doesn't exist yet
import paelladoc_core

class TestPingTool(unittest.TestCase):
    """Unit tests for the ping tool following TDD methodology."""
    
    def test_ping_exists(self):
        """Test that the ping function exists."""
        self.assertTrue(hasattr(paelladoc_core, "ping"), 
                       "The ping function does not exist in paelladoc_core")
    
    def test_ping_returns_dict(self):
        """Test that ping returns a dictionary."""
        result = paelladoc_core.ping()
        self.assertIsInstance(result, dict, 
                             "ping should return a dictionary")
    
    def test_ping_has_required_fields(self):
        """Test that ping response has the required fields."""
        result = paelladoc_core.ping()
        self.assertIn("status", result, 
                     "ping response should contain a 'status' field")
        self.assertIn("message", result, 
                     "ping response should contain a 'message' field")
    
    def test_ping_returns_expected_values(self):
        """Test that ping returns the expected values."""
        result = paelladoc_core.ping()
        self.assertEqual(result["status"], "ok", 
                        f"ping status should be 'ok', got '{result['status']}'")
        self.assertEqual(result["message"], "pong", 
                        f"ping message should be 'pong', got '{result['message']}'")

if __name__ == "__main__":
    unittest.main() 