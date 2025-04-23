"""Alembic environment configuration."""

import asyncio
import os
import sys
from pathlib import Path
from logging.config import fileConfig

# Add project root to sys.path to allow importing models
project_root = Path(__file__).parent.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from alembic import context
# Import SQLModel
from sqlmodel import SQLModel
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

# Import models just to ensure they are registered with SQLModel.metadata
from paelladoc.adapters.output.sqlite.db_models import ArtifactMetaDB, ProjectMemoryDB
from paelladoc.config.database import get_db_path

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# Use SQLModel.metadata directly
target_metadata = SQLModel.metadata

# Determine DB path precedence: environment variable overrides helper
_db_path = os.getenv("PAELLADOC_DB_PATH", str(get_db_path()))
_sqlalchemy_url = f"sqlite+aiosqlite:///{_db_path}"
# Ensure the URL is set correctly in the config object Alembic uses
config.set_main_option("sqlalchemy.url", _sqlalchemy_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Use the URL set in the config object
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True, # Enable type comparison
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    # Configure context inside the sync function
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True, # Enable type comparison
        # Inform Alembic context that we're handling the transaction
        transactional_ddl=False
    )
    # Handle transaction explicitly
    with connection.begin():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Get the config section using config_ini_section
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section, {}), # Get section correctly
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True, # Keep future=True for AsyncEngine
            url=config.get_main_option("sqlalchemy.url") # Pass URL explicitly
        )
    )

    async with connectable.connect() as connection:
        # Use lambda to ensure do_run_migrations is called correctly by run_sync
        await connection.run_sync(lambda sync_conn: do_run_migrations(sync_conn))

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Check if an event loop is already running (e.g., under pytest-asyncio)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # If loop exists and is running, schedule the coroutine
        task = loop.create_task(run_migrations_online())
    else:
        # If no loop running, use asyncio.run as before
        asyncio.run(run_migrations_online())
