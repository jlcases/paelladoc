from paelladoc.domain.core_logic import mcp
import logging

# Adapter for taxonomy loading
from paelladoc.adapters.output.filesystem.taxonomy_provider import (
    FileSystemTaxonomyProvider,
)

# Instantiate the taxonomy provider
# TODO: Replace direct instantiation with Dependency Injection
TAXONOMY_PROVIDER = FileSystemTaxonomyProvider()

# Insert behavior config here

# TODO: Review imports and add any other necessary modules


@mcp.tool(
    name="core.help",
    description="Shows help information about available commands",
)
def core_help(command: str = None, format: str = "detailed") -> dict:
    """Provides help information about available PAELLADOC commands.

    Args:
        command: Optional specific command to get help for
        format: Output format (detailed, summary, examples)

    Returns:
        Dictionary with help information
    """

    logging.info(f"Executing core.help with command={command}, format={format}")

    # Define available commands
    commands = {
        "paella": {
            "description": "Initiates the documentation process for a new project",
            "parameters": [
                {
                    "name": "project_name",
                    "type": "string",
                    "required": True,
                    "description": "Name of the project to document",
                },
                {
                    "name": "base_path",
                    "type": "string",
                    "required": True,
                    "description": "Base path for project documentation",
                },
                {
                    "name": "documentation_language",
                    "type": "string",
                    "required": False,
                    "description": "Language for documentation (e.g. 'es', 'en')",
                },
                {
                    "name": "interaction_language",
                    "type": "string",
                    "required": False,
                    "description": "Language for interaction (e.g. 'es', 'en')",
                },
            ],
            "example": "PAELLA my_project ~/projects/my_project en en",
        },
        "continue": {
            "description": "Continues working on an existing project",
            "parameters": [
                {
                    "name": "project_name",
                    "type": "string",
                    "required": True,
                    "description": "Name of the project to continue with",
                },
            ],
            "example": "CONTINUE my_project",
        },
        "verification": {
            "description": "Verifies documentation coverage against the MECE taxonomy",
            "parameters": [
                {
                    "name": "project_name",
                    "type": "string",
                    "required": True,
                    "description": "Name of the project to verify",
                },
            ],
            "example": "VERIFY my_project",
        },
        "select_taxonomy": {
            "description": "Guides users through selecting and customizing a project taxonomy",
            "parameters": [
                {
                    "name": "project_name",
                    "type": "string",
                    "required": True,
                    "description": "Name of the project to customize taxonomy for",
                },
                {
                    "name": "size_category",
                    "type": "string",
                    "required": False,
                    "description": "Project size category (personal, hobbyist, mvp, startup, enterprise)",
                },
                {
                    "name": "domain_type",
                    "type": "string",
                    "required": False,
                    "description": "Project domain type (web, mobile, iot, ai/ml, etc.)",
                },
                {
                    "name": "platform_type",
                    "type": "string",
                    "required": False,
                    "description": "Platform implementation type (chrome-extension, ios-native, android-native, etc.)",
                },
                {
                    "name": "compliance_needs",
                    "type": "string",
                    "required": False,
                    "description": "Compliance requirements (none, hipaa, gdpr, etc.)",
                },
                {
                    "name": "custom_threshold",
                    "type": "float",
                    "required": False,
                    "description": "Custom coverage threshold (0.0-1.0)",
                },
            ],
            "example": "SELECT-TAXONOMY my_project --size=mvp --domain=web --platform=chrome-extension",
        },
        "taxonomy_info": {
            "description": "Shows information about available taxonomies and categories",
            "parameters": [],
            "example": "TAXONOMY-INFO",
        },
        "help": {
            "description": "Shows help information about available commands",
            "parameters": [
                {
                    "name": "command",
                    "type": "string",
                    "required": False,
                    "description": "Specific command to get help for",
                },
                {
                    "name": "format",
                    "type": "string",
                    "required": False,
                    "description": "Output format (detailed, summary, examples)",
                },
            ],
            "example": "HELP paella",
        },
    }

    # If a specific command is requested
    if command and command in commands:
        return {"status": "ok", "command": command, "help": commands[command]}

    # Otherwise return all commands
    result = {
        "status": "ok",
        "available_commands": list(commands.keys()),
        "format": format,
    }

    # Add command information based on format
    if format == "detailed":
        result["commands"] = commands
        try:
            available_taxonomies = TAXONOMY_PROVIDER.get_available_taxonomies()
            if "select_taxonomy" in commands:
                commands["select_taxonomy"]["available_options"] = available_taxonomies
            if "taxonomy_info" in commands:
                commands["taxonomy_info"]["available_taxonomies"] = available_taxonomies
        except Exception as e:
            logging.error(f"Failed to load taxonomies for help: {e}", exc_info=True)
            # Continue without taxonomy info if loading fails
    elif format == "summary":
        result["commands"] = {
            cmd: info["description"] for cmd, info in commands.items()
        }
    elif format == "examples":
        result["commands"] = {cmd: info["example"] for cmd, info in commands.items()}

    return result
