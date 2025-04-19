#!/usr/bin/env python
"""
Integration tests for the Paelladoc MCP server.

These tests verify that the server correctly starts and responds to requests
via STDIO communication.
"""

import unittest
import sys
import os
import json
import time
import subprocess
import uuid
from pathlib import Path

# Ensure we can import Paelladoc modules
project_root = Path(__file__).parent.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Constants
SERVER_SCRIPT = os.path.join(str(project_root), "server.py")

class TestServerIntegration(unittest.TestCase):
    """Integration tests for the MCP server STDIO communication."""
    
    def test_server_responds_to_ping(self):
        """Verify that the server responds to a ping request via STDIO."""
        # Generate a unique ID for the request
        request_id = str(uuid.uuid4())
        
        # Set up the environment for the server
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root)
        
        # Start the server as a separate process
        server_process = subprocess.Popen(
            [sys.executable, SERVER_SCRIPT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            universal_newlines=True
        )
        
        try:
            # Wait a moment for the server to start
            time.sleep(1)
            
            # Create MCP request for ping tool
            mcp_request = {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": "tool",
                "params": {
                    "name": "ping",
                    "parameters": {"random_string": "integration-test"}
                }
            }
            
            # Print debug info
            print(f"Sending request: {json.dumps(mcp_request)}")
            
            # Send the request to the server
            server_process.stdin.write(json.dumps(mcp_request) + "\n")
            server_process.stdin.flush()
            
            # Wait for response with timeout
            response_timeout = time.time() + 5
            response_line = None
            
            while time.time() < response_timeout and not response_line:
                if server_process.stdout.readable():
                    line = server_process.stdout.readline().strip()
                    if line:
                        response_line = line
                        break
                time.sleep(0.1)
            
            # Debug output if no response
            if not response_line:
                # Check if there's any stderr output
                stderr_output = server_process.stderr.read()
                print(f"No response received. Server stderr: {stderr_output}")
                self.fail("No response received from MCP server")
            
            print(f"Received response: {response_line}")
            
            # Parse the response
            response = json.loads(response_line)
            
            # Verify the response structure
            self.assertIn("jsonrpc", response, "Response should be a JSON-RPC object")
            self.assertEqual(response.get("id"), request_id, 
                           f"Response ID ({response.get('id')}) does not match request ID ({request_id})")
            self.assertIn("result", response, "Response should contain a 'result' field")
            
            # Verify the response content
            result = response["result"]
            self.assertIn("status", result, "Result should contain a 'status' field")
            self.assertEqual(result["status"], "ok", 
                           f"Incorrect status: expected 'ok', got '{result['status']}'")
            self.assertIn("message", result, "Result should contain a 'message' field")
            self.assertEqual(result["message"], "pong", 
                           f"Incorrect message: expected 'pong', got '{result['message']}'")
            
        finally:
            # Ensure the server is stopped
            try:
                if server_process.stdin:
                    server_process.stdin.close()
                server_process.terminate()
                server_process.wait(timeout=2)
            except:
                try:
                    server_process.kill()
                except:
                    pass

if __name__ == "__main__":
    unittest.main() 