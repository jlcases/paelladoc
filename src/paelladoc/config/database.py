"""Database configuration module."""

import os
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


def get_db_path() -> Path:
    """
    Get the database path based on environment variable or default location.

    Priority:
    1. PAELLADOC_DB_PATH environment variable if set.
    2. Default path in user's home directory (~/.paelladoc/memory.db).
    """
    # Check environment variable first
    env_path = os.getenv("PAELLADOC_DB_PATH")
    if env_path:
        return Path(env_path)

    # Default to production path in user's home
    # The development mode check based on PAELLADOC_ENV was removed as it's
    # unreliable and potentially problematic for installed packages.
    # Use the PAELLADOC_DB_PATH environment variable for development overrides.
    db_dir = Path.home() / ".paelladoc"
    db_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    return db_dir / "memory.db"


# Default paths for reference (These might become less relevant or just informative)
# DEVELOPMENT_DB_PATH = get_project_root() / "paelladoc_memory.db"
PRODUCTION_DB_PATH = Path.home() / ".paelladoc" / "memory.db"
DEFAULT_DB_PATH = get_db_path()
