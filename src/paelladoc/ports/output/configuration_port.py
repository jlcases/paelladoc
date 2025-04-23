"""Configuration port for accessing system configurations."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class ConfigurationPort(ABC):
    """Port for accessing system configurations and metadata."""

    @abstractmethod
    async def get_behavior_config(
        self, category: Optional[str] = None
    ) -> Dict[str, Any]:
        """Retrieves behavior configuration settings.

        Args:
            category: Optional category to filter configurations.

        Returns:
            Dictionary of configuration key-value pairs.
        """
        pass

    @abstractmethod
    async def get_mece_dimensions(self) -> Dict[str, Dict[str, Any]]:
        """Retrieves MECE dimension configurations.

        Returns:
            Dictionary containing:
            - allowed_dimensions: List of allowed dimension names
            - required_dimensions: List of required dimension names
            - validations: Dictionary of validation rules
        """
        pass

    @abstractmethod
    async def get_bucket_order(self, category: Optional[str] = None) -> List[str]:
        """Retrieves the ordered list of buckets.

        Args:
            category: Optional category to filter bucket types.

        Returns:
            List of bucket names in their defined order.
        """
        pass

    @abstractmethod
    async def get_commands_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Retrieves metadata about available commands.

        Returns:
            Dictionary of command definitions including descriptions,
            parameters, and examples.
        """
        pass

    @abstractmethod
    async def save_behavior_config(
        self, config: Dict[str, Any], category: Optional[str] = None
    ) -> None:
        """Saves behavior configuration settings.

        Args:
            config: Dictionary of configuration key-value pairs.
            category: Optional category for the configuration.
        """
        pass
