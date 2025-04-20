"""Unit tests for database configuration module."""

import os
from pathlib import Path
import pytest

from paelladoc.config.database import (
    get_project_root,
    get_db_path,
    PRODUCTION_DB_PATH,
)


@pytest.fixture
def clean_env():
    """Remove relevant environment variables before each test."""
    # Store original values
    original_db_path = os.environ.get("PAELLADOC_DB_PATH")
    original_env = os.environ.get("PAELLADOC_ENV")

    # Remove variables
    if "PAELLADOC_DB_PATH" in os.environ:
        del os.environ["PAELLADOC_DB_PATH"]
    if "PAELLADOC_ENV" in os.environ:
        del os.environ["PAELLADOC_ENV"]

    yield

    # Restore original values
    if original_db_path is not None:
        os.environ["PAELLADOC_DB_PATH"] = original_db_path
    if original_env is not None:
        os.environ["PAELLADOC_ENV"] = original_env


def test_get_project_root():
    """Test that get_project_root returns a valid directory."""
    root = get_project_root()
    assert isinstance(root, Path)
    assert root.exists()
    assert root.is_dir()
    assert (root / "src").exists()
    assert (root / "src" / "paelladoc").exists()
    assert (root / "pyproject.toml").exists()


def test_get_db_path_with_env_var(clean_env):
    """Test that PAELLADOC_DB_PATH environment variable takes precedence."""
    custom_path = "/custom/path/db.sqlite"
    os.environ["PAELLADOC_DB_PATH"] = custom_path

    db_path = get_db_path()
    assert isinstance(db_path, Path)
    assert str(db_path) == custom_path


def test_get_db_path_production_default(clean_env):
    """Test that production mode uses home directory."""
    db_path = get_db_path()
    assert isinstance(db_path, Path)
    assert db_path == PRODUCTION_DB_PATH
    assert db_path.name == "memory.db"
    assert db_path.parent.name == ".paelladoc"
    assert db_path.parent.parent == Path.home()


def test_production_db_path_constant():
    """Test that PRODUCTION_DB_PATH is correctly set."""
    assert isinstance(PRODUCTION_DB_PATH, Path)
    assert PRODUCTION_DB_PATH.name == "memory.db"
    assert PRODUCTION_DB_PATH.parent.name == ".paelladoc"
    assert PRODUCTION_DB_PATH.parent.parent == Path.home()
