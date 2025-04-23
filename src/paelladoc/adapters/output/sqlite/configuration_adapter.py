"""SQLite adapter implementation for the ConfigurationPort."""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from paelladoc.ports.output.configuration_port import ConfigurationPort
from .config_models import (
    BehaviorConfigDB,
    MECEDimensionDB,
    TaxonomyValidationDB,
    BucketOrderDB,
    CommandDB,
)

logger = logging.getLogger(__name__)


class SQLiteConfigurationAdapter(ConfigurationPort):
    """SQLite implementation of the ConfigurationPort."""

    def __init__(self, session: AsyncSession):
        """Initialize the adapter with a database session.

        Args:
            session: SQLAlchemy async session for database operations.
        """
        self.session = session

    async def get_behavior_config(
        self, category: Optional[str] = None
    ) -> Dict[str, Any]:
        """Retrieves behavior configuration settings from the database.

        Args:
            category: Optional category to filter configurations.

        Returns:
            Dictionary of configuration key-value pairs.
        """
        try:
            statement = select(BehaviorConfigDB)
            if category:
                statement = statement.where(BehaviorConfigDB.category == category)

            results = await self.session.execute(statement)
            configs = results.scalars().all()

            return {config.key: config.value for config in configs}
        except Exception as e:
            logger.error(f"Error retrieving behavior config: {e}", exc_info=True)
            return {}

    async def get_mece_dimensions(self) -> Dict[str, Dict[str, Any]]:
        """Retrieves MECE dimension configurations from the database.

        Returns:
            Dictionary containing dimension configurations and validations.
        """
        try:
            # Get dimensions
            dimensions_stmt = select(MECEDimensionDB)
            dimensions_result = await self.session.execute(dimensions_stmt)
            dimensions = dimensions_result.scalars().all()

            # Get validations
            validations_stmt = select(TaxonomyValidationDB)
            validations_result = await self.session.execute(validations_stmt)
            validations = validations_result.scalars().all()

            # Structure the response
            allowed_dimensions = [dim.name for dim in dimensions]
            required_dimensions = [dim.name for dim in dimensions if dim.is_required]

            validation_rules = {
                val.platform: {
                    "domain": val.domain,
                    "warning": val.warning,
                    "severity": val.severity,
                }
                for val in validations
            }

            return {
                "allowed_dimensions": allowed_dimensions,
                "required_dimensions": required_dimensions,
                "validation_rules": validation_rules,
                "dimensions": {
                    dim.name: {
                        "required": dim.is_required,
                        "description": dim.description,
                        "rules": dim.validation_rules,
                    }
                    for dim in dimensions
                },
            }
        except Exception as e:
            logger.error(f"Error retrieving MECE dimensions: {e}", exc_info=True)
            return {
                "allowed_dimensions": [],
                "required_dimensions": [],
                "validation_rules": {},
                "dimensions": {},
            }

    async def get_bucket_order(self, category: Optional[str] = None) -> List[str]:
        """Retrieves the ordered list of buckets from the database.

        Args:
            category: Optional category to filter bucket types.

        Returns:
            List of bucket names in their defined order.
        """
        try:
            statement = select(BucketOrderDB).order_by(BucketOrderDB.order_index)
            if category:
                statement = statement.where(BucketOrderDB.category == category)

            results = await self.session.execute(statement)
            buckets = results.scalars().all()

            return [bucket.bucket_name for bucket in buckets]
        except Exception as e:
            logger.error(f"Error retrieving bucket order: {e}", exc_info=True)
            return []

    async def get_commands_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Retrieves metadata about available commands from the database.

        Returns:
            Dictionary of command definitions including descriptions,
            parameters, and examples.
        """
        try:
            statement = select(CommandDB)
            results = await self.session.execute(statement)
            commands = results.scalars().all()

            return {
                cmd.name: {
                    "description": cmd.description,
                    "parameters": cmd.parameters,
                    "example": cmd.example,
                }
                for cmd in commands
            }
        except Exception as e:
            logger.error(f"Error retrieving commands metadata: {e}", exc_info=True)
            return {}

    async def save_behavior_config(
        self, config: Dict[str, Any], category: Optional[str] = None
    ) -> None:
        """Saves behavior configuration settings to the database.

        Args:
            config: Dictionary of configuration key-value pairs.
            category: Optional category for the configuration.
        """
        try:
            for key, value in config.items():
                # Check if config already exists
                statement = select(BehaviorConfigDB).where(
                    BehaviorConfigDB.key == key, BehaviorConfigDB.category == category
                )
                result = await self.session.execute(statement)
                existing_config = result.scalars().first()

                if existing_config:
                    # Update existing config
                    existing_config.value = value
                    existing_config.updated_at = datetime.utcnow()
                else:
                    # Create new config
                    new_config = BehaviorConfigDB(
                        key=key, value=value, category=category
                    )
                    self.session.add(new_config)

            await self.session.commit()
        except Exception as e:
            logger.error(f"Error saving behavior config: {e}", exc_info=True)
            await self.session.rollback()
            raise
