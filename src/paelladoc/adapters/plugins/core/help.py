from paelladoc.domain.core_logic import mcp
import logging

# Insert behavior config here

# TODO: Review imports and add any other necessary modules


@mcp.tool(
    name="core.help",
    description="This ensures that users can quickly access help without needing to know the specific HELP command syntax.",
)
def core_help() -> dict:
    """Provides help information for PAELLADOC commands.

    Can display general help or help for a specific command.
    This ensures that users can quickly access help without needing
    to know the specific HELP command syntax.
    """

    # TODO: Implement the actual logic of the command here
    # Access parameters using their variable names (e.g., param)
    # Access behavior config using BEHAVIOR_CONFIG dict (if present)
    logging.info("Executing stub for core.help...")

    # Example: Print parameters
    local_vars = locals()
    param_values = {}
    logging.info(f"Parameters received: {param_values}")

    # Replace with actual return value based on command logic
    return {"status": "ok", "message": "Successfully executed stub for core.help"}
