from abc import ABC, abstractmethod
from typing import Dict, List


class TaxonomyProvider(ABC):
    """Abstract interface for providing available taxonomy information."""

    @abstractmethod
    def get_available_taxonomies(self) -> Dict[str, List[str]]:
        """Returns a dictionary of available taxonomies grouped by category.

        Example:
            {
                "platform": ["web-frontend", "ios-native", ...],
                "domain": ["ecommerce", "ai-ml", ...],
                ...
            }
        """
        pass
