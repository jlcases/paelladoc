# README_CMP.md

This document explains how to configure the `.cursor/mcp.json` file so that Cursor can properly connect to the Paelladoc MCP server and avoid communication issues.

## Example `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "Paelladoc Server (Local Dev)": {
      "command": "/Users/<user>/codigo/paelladoc/.venv/bin/python",
      "args": [
        "-m",
        "paelladoc.ports.input.mcp_server_adapter",
        "--stdio"
      ],
      "cwd": "/Users/<user>/codigo/paelladoc",
      "env": {
        "PYTHONPATH": "/Users/<user>/codigo/paelladoc/src:/Users/<user>/codigo/paelladoc",
        "DEBUG": "true"
      },
      "disabled": false
    }
  },
  "mcp.timeout": 120000
}
```

### Field Descriptions

- **command**: Absolute path to the Python interpreter in your virtual environment (e.g., `.venv/bin/python`).
- **args**:
  - `-m`: Specifies the Python module to run.
  - `paelladoc.ports.input.mcp_server_adapter`: The entry-point module for your MCP server.
  - `--stdio`: Enables stdio-based transport for stdin/stdout communication.
- **cwd**: Working directory where the server runs (the root of your Paelladoc project).
- **env**:
  - `PYTHONPATH`: Include the `src` directory first, then the project root, so Python imports resolve correctly.
  - `DEBUG`: Set to `true` to enable debug-level logging.
- **disabled**: Must be `false` to activate the server configuration.
- **mcp.timeout**: Maximum time (in milliseconds) that Cursor will wait for the server to respond before timing out.

## Additional Recommendations

1. Add `.cursor/mcp.json` to your `.gitignore` (e.g., `.cursor/mcp.json`) to prevent environment-specific configurations from being committed.
2. Adjust the file paths (`<user>`, `codigo`, `paelladoc`) to match your system.
3. If your virtual environment is named differently (e.g., `venv` instead of `.venv`), update the `command` path accordingly.
4. To verify the connection, use the `ping` tool:

```json
{
  "name": "ping",
  "arguments": { "random_string": "test" }
}
```

You should receive:
```json
{
  "status": "ok",
  "message": "pong"
}
``` 