"""Dependency Injection Container for Paelladoc."""

import logging
from functools import lru_cache
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from paelladoc.config.database import get_db_path
from paelladoc.ports.output.configuration_port import ConfigurationPort
from paelladoc.adapters.output.sqlite.configuration_adapter import (
    SQLiteConfigurationAdapter,
)

logger = logging.getLogger(__name__)


class Container:
    """Simple dependency injection container."""

    def __init__(self):
        logger.info("Initializing Dependency Container...")
        self._db_path = get_db_path()
        logger.info(f"Container using DB path: {self._db_path.resolve()}")
        self._async_engine = create_async_engine(
            f"sqlite+aiosqlite:///{self._db_path}",
            echo=False,  # Set to True for SQL query logging
        )
        self._async_session_factory = sessionmaker(
            self._async_engine, class_=AsyncSession, expire_on_commit=False
        )
        logger.info("Async engine and session factory created.")

    @lru_cache()  # Cache the adapter instance
    def get_db_session(self) -> AsyncSession:
        """Provides a new database session."""
        logger.debug("Providing new DB session from factory.")
        return self._async_session_factory()

    @lru_cache()  # Cache the adapter instance
    def get_configuration_port(self) -> ConfigurationPort:
        """Provides an instance of the ConfigurationPort implementation."""
        # We pass the session factory, adapter can create sessions as needed
        # OR pass a session directly if request-scoped sessions are desired
        # For simplicity now, let adapter manage its session needs implicitly
        # via the factory or create a new one per call.
        # Passing the factory allows more flexibility.
        # Revisit if session management becomes complex.

        # CORRECTION: Adapter expects an AsyncSession instance, not factory
        # Let's provide a session. Since this is cached, it will be reused.
        # Consider request-scoped sessions for web apps later.
        logger.info("Creating and caching SQLiteConfigurationAdapter instance.")
        session = self._async_session_factory()
        return SQLiteConfigurationAdapter(session=session)


# Global container instance
container = Container()


def get_container() -> Container:
    """Returns the global container instance."""
    return container
