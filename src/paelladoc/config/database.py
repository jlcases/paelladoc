"""Database configuration module."""

import os
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

CONFIG_FILE_NAME = "paelladoc_config.json"


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def get_config_file() -> Path:
    """Get the path to the configuration file."""
    # Check multiple locations in order of precedence
    possible_locations = [
        Path.cwd() / CONFIG_FILE_NAME,  # Current directory (development)
        Path.home() / ".paelladoc" / CONFIG_FILE_NAME,  # User's home directory
        Path("/etc/paelladoc") / CONFIG_FILE_NAME,  # System-wide configuration
    ]

    for location in possible_locations:
        if location.exists():
            return location

    # If no config file exists, use the default in user's home
    default_location = Path.home() / ".paelladoc" / CONFIG_FILE_NAME
    default_location.parent.mkdir(parents=True, exist_ok=True)
    if not default_location.exists():
        default_config = {
            "db_path": str(Path.home() / ".paelladoc" / "memory.db"),
            "environment": "production",
        }
        with open(default_location, "w") as f:
            json.dump(default_config, f, indent=2)

    return default_location


def get_db_path() -> Path:
    """
    Get the database path based on multiple configuration sources.

    Priority:
    1. PAELLADOC_DB_PATH environment variable if set
    2. Path specified in configuration file
    3. Default path in user's home directory (~/.paelladoc/memory.db)

    The configuration can be set during package installation with:
    pip install paelladoc --install-option="--db-path=/path/to/db"

    Or by editing the config file at:
    - ./paelladoc_config.json (development)
    - ~/.paelladoc/paelladoc_config.json (user)
    - /etc/paelladoc/paelladoc_config.json (system)
    """
    # 1. Check environment variable first (highest priority)
    env_path = os.getenv("PAELLADOC_DB_PATH")
    if env_path:
        db_path = Path(env_path)
        logger.info(f"Using database path from environment variable: {db_path}")
        return db_path

    # 2. Check configuration file
    config_file = get_config_file()
    try:
        with open(config_file) as f:
            config = json.load(f)
            if "db_path" in config:
                db_path = Path(config["db_path"])
                logger.info(
                    f"Using database path from config file {config_file}: {db_path}"
                )
                return db_path
    except Exception as e:
        logger.warning(f"Error reading config file {config_file}: {e}")

    # 3. Default to production path in user's home
    db_path = Path.home() / ".paelladoc" / "memory.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Using default database path: {db_path}")
    return db_path


def set_db_path(path: str | Path) -> None:
    """
    Set the database path in the configuration file.

    This can be used programmatically or during package installation.
    """
    config_file = get_config_file()
    try:
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
        else:
            config = {}

        config["db_path"] = str(Path(path).resolve())

        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

        logger.info(f"Updated database path in {config_file} to: {path}")
    except Exception as e:
        logger.error(f"Error updating database path in config file: {e}")
        raise


# Default paths for reference (These might become less relevant or just informative)
# DEVELOPMENT_DB_PATH = get_project_root() / "paelladoc_memory.db"
PRODUCTION_DB_PATH = Path.home() / ".paelladoc" / "memory.db"
DEFAULT_DB_PATH = get_db_path()
