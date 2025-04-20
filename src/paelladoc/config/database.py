"""Database configuration module."""

import os
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def get_db_path() -> Path:
    """
    Get the database path based on environment and configuration.

    Priority:
    1. PAELLADOC_DB_PATH environment variable if set
    2. Development path if in development mode
    3. Production path in user's home directory
    """
    # Check environment variable first
    env_path = os.getenv("PAELLADOC_DB_PATH")
    if env_path:
        return Path(env_path)

    # Check if we're in development mode (can be expanded with more checks)
    if os.getenv("PAELLADOC_ENV") == "development":
        return get_project_root() / "paelladoc_memory.db"

    # Default to production path in user's home
    return Path.home() / ".paelladoc" / "memory.db"


# Default paths for reference
DEVELOPMENT_DB_PATH = get_project_root() / "paelladoc_memory.db"
PRODUCTION_DB_PATH = Path.home() / ".paelladoc" / "memory.db"
DEFAULT_DB_PATH = get_db_path()
