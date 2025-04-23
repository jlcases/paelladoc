from paelladoc.domain.core_logic import mcp
import logging

# Adapter for taxonomy loading
from paelladoc.adapters.output.filesystem.taxonomy_provider import (
    FileSystemTaxonomyProvider,
)

# Dependency Injection
from paelladoc.dependencies import get_container
from paelladoc.ports.output.configuration_port import ConfigurationPort

# Instantiate the taxonomy provider
# TODO: Replace direct instantiation with Dependency Injection
TAXONOMY_PROVIDER = FileSystemTaxonomyProvider()

# Get configuration port from container
container = get_container()
config_port: ConfigurationPort = container.get_configuration_port()

# Insert behavior config here

# TODO: Review imports and add any other necessary modules


@mcp.tool(
    name="core_help",
    description="Shows help information about available commands",
)
async def core_help(command: str = None, format: str = "detailed") -> dict:
    """Provides help information about available PAELLADOC commands.

    Args:
        command: Optional specific command to get help for
        format: Output format (detailed, summary, examples)

    Returns:
        Dictionary with help information
    """
    logging.info(f"Executing core.help with command={command}, format={format}")

    # Load commands from DB via ConfigurationPort
    try:
        commands_config = await config_port.get_commands_metadata()
        if not commands_config:
            logging.warning(
                "No commands found in config DB. Using fallback empty dict."
            )
            commands_config = {}

        logging.info(f"Loaded {len(commands_config)} commands from configuration DB")
    except Exception as e:
        logging.error(f"Failed to load commands from DB: {e}", exc_info=True)
        # Return error if commands can't be loaded (critical)
        return {
            "status": "error",
            "message": "Failed to load commands information from database.",
        }

    # If a specific command is requested
    if command and command in commands_config:
        return {"status": "ok", "command": command, "help": commands_config[command]}

    # Otherwise return all commands
    result = {
        "status": "ok",
        "available_commands": list(commands_config.keys()),
        "format": format,
    }

    # Add command information based on format
    if format == "detailed":
        result["commands"] = commands_config
        try:
            available_taxonomies = TAXONOMY_PROVIDER.get_available_taxonomies()
            if "select_taxonomy" in commands_config:
                commands_config["select_taxonomy"]["available_options"] = (
                    available_taxonomies
                )
            if "taxonomy_info" in commands_config:
                commands_config["taxonomy_info"]["available_taxonomies"] = (
                    available_taxonomies
                )
        except Exception as e:
            logging.error(f"Failed to load taxonomies for help: {e}", exc_info=True)
            # Continue without taxonomy info if loading fails
    elif format == "summary":
        result["commands"] = {
            cmd: info["description"] for cmd, info in commands_config.items()
        }
    elif format == "examples":
        result["commands"] = {
            cmd: info.get("example", "") for cmd, info in commands_config.items()
        }

    return result
