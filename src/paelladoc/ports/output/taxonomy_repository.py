from abc import ABC, abstractmethod
from typing import List, Set, Optional


class TaxonomyRepository(ABC):
    """Abstract interface for providing taxonomy information."""

    @abstractmethod
    def get_available_dimensions(self) -> List[str]:
        """Returns a list of available dimensions (e.g., platform, domain, size, compliance, lifecycle)."""
        pass

    @abstractmethod
    def get_dimension_values(self, dimension: str) -> List[str]:
        """Returns a list of available values for a specific dimension."""
        pass

    @abstractmethod
    def get_buckets_for_dimension_value(self, dimension: str, value: str) -> List[str]:
        """Returns the list of taxonomy buckets associated with a specific dimension value."""
        pass

    @abstractmethod
    def get_buckets_for_project(
        self,
        platform: str,
        domain: str,
        size: str,
        lifecycle: str,
        compliance: Optional[str] = None,
    ) -> Set[str]:
        """
        Returns the combined set of taxonomy buckets for a project with the given dimensions.

        This is the union of all buckets from each dimension value, with duplicates removed.
        """
        pass

    @abstractmethod
    def get_all_available_buckets(self) -> List[str]:
        """Returns a list of all available bucket IDs from the taxonomy."""
        pass

    @abstractmethod
    def get_bucket_description(self, bucket_id: str) -> Optional[str]:
        """Returns the description for a specific bucket ID, or None if not found."""
        pass
