"""Utilities for project management."""

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

from paelladoc.domain.models.language import SupportedLanguage
from paelladoc.domain.models.project import ProjectInfo

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when project validation fails."""

    pass


def validate_project_updates(updates: Dict[str, Any]) -> List[str]:
    """
    Validate project field updates.

    Args:
        updates: Dictionary of field names and their new values.

    Returns:
        List of validation error messages. Empty if validation passes.
    """
    errors = []

    # Validate documentation_language
    if "documentation_language" in updates:
        value = updates["documentation_language"]
        if value not in [lang.value for lang in SupportedLanguage]:
            errors.append(f"Invalid documentation_language: {value}")

    # Validate interaction_language
    if "interaction_language" in updates:
        value = updates["interaction_language"]
        if value not in [lang.value for lang in SupportedLanguage]:
            errors.append(f"Invalid interaction_language: {value}")

    # Validate base_path
    if "base_path" in updates:
        value = updates["base_path"]
        if not value:  # Check for empty string or None
            errors.append("base_path cannot be empty")
        else:
            try:
                path = Path(value)
                if not path.is_absolute():
                    path = path.resolve()
                updates["base_path"] = str(path)
            except Exception as e:
                errors.append(f"Invalid base_path: {e}")

    # Validate name (if present)
    if "name" in updates:
        if not updates["name"] or not isinstance(updates["name"], str):
            errors.append("Project name cannot be empty and must be a string")

    return errors


def create_project_backup(
    project_info: ProjectInfo, backup_dir: Optional[Path] = None
) -> Tuple[Optional[Path], Optional[str]]:
    """
    Create a backup of project files.

    Args:
        project_info: Project information.
        backup_dir: Optional directory to store backups. Defaults to project's parent dir.

    Returns:
        Tuple of (backup_path, error_message). If backup fails, path will be None.
    """
    try:
        base_path = Path(project_info.base_path)
        if not base_path.exists():
            return None, "Project directory does not exist"

        # Use provided backup dir or project's parent
        backup_dir = backup_dir or base_path.parent
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Create timestamped backup name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{project_info.name}_backup_{timestamp}"
        backup_path = backup_dir / f"{backup_name}.zip"

        # Create zip backup
        shutil.make_archive(str(backup_path.with_suffix("")), "zip", base_path)

        logger.info(f"Created backup at {backup_path}")
        return backup_path, None

    except Exception as e:
        error_msg = f"Error creating backup: {e}"
        logger.error(error_msg)
        return None, error_msg


def format_project_info(project_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format project information for API response.

    Args:
        project_info: Raw project info dictionary.

    Returns:
        Formatted project info with consistent types.
    """
    # Ensure base_path is string
    if "base_path" in project_info:
        project_info["base_path"] = str(project_info["base_path"])

    # Convert any Path objects to strings
    for key, value in project_info.items():
        if isinstance(value, Path):
            project_info[key] = str(value)

    return project_info
