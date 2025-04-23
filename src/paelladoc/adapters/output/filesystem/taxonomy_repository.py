import json
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional
import importlib.resources

from paelladoc.ports.output.taxonomy_repository import TaxonomyRepository

logger = logging.getLogger(__name__)


class FileSystemTaxonomyRepository(TaxonomyRepository):
    """Implementation of TaxonomyRepository that reads from filesystem."""

    def __init__(self):
        """Initializes the repository."""
        self._cached_dimensions: Optional[List[str]] = None
        self._cached_dimension_values: Dict[str, List[str]] = {}
        self._cached_dimension_buckets: Dict[str, Dict[str, List[str]]] = {}
        self._cached_all_buckets: Optional[List[str]] = None
        self._cached_bucket_descriptions: Optional[Dict[str, str]] = None

        # Base taxonomy.json path for all buckets
        self.taxonomy_path = (
            Path(__file__).parent.parent.parent.parent.parent / "taxonomy.json"
        )
        if not self.taxonomy_path.exists():
            logger.warning(
                f"Main taxonomy.json file not found at: {self.taxonomy_path}"
            )

    def _get_base_taxonomy_path(self) -> Path:
        """Get the base path to the taxonomy directories within the package."""
        try:
            return Path(importlib.resources.files("paelladoc").joinpath("taxonomies"))
        except Exception as e:
            logger.error(f"Error locating taxonomy path: {e}")
            return Path(__file__).parent.parent.parent.parent / "taxonomies"

    def get_available_dimensions(self) -> List[str]:
        """Returns a list of available dimensions."""
        if self._cached_dimensions is not None:
            return self._cached_dimensions

        base_path = self._get_base_taxonomy_path()
        if not base_path.is_dir():
            logger.error(f"Taxonomy base path not found: {base_path}")
            return []

        dimensions = []
        for item in base_path.iterdir():
            if item.is_dir():
                dimensions.append(item.name)

        self._cached_dimensions = sorted(dimensions)
        return self._cached_dimensions

    def get_dimension_values(self, dimension: str) -> List[str]:
        """Returns a list of available values for a specific dimension."""
        if dimension in self._cached_dimension_values:
            return self._cached_dimension_values[dimension]

        base_path = self._get_base_taxonomy_path() / dimension
        if not base_path.is_dir():
            logger.error(f"Dimension directory not found: {base_path}")
            return []

        values = []
        for item in base_path.iterdir():
            if item.is_file() and item.suffix == ".json":
                values.append(item.stem)

        self._cached_dimension_values[dimension] = sorted(values)
        return self._cached_dimension_values[dimension]

    def get_buckets_for_dimension_value(self, dimension: str, value: str) -> List[str]:
        """Returns the list of taxonomy buckets associated with a specific dimension value."""
        # Check cache first
        if (
            dimension in self._cached_dimension_buckets
            and value in self._cached_dimension_buckets[dimension]
        ):
            return self._cached_dimension_buckets[dimension][value]

        # Initialize the dimension cache if needed
        if dimension not in self._cached_dimension_buckets:
            self._cached_dimension_buckets[dimension] = {}

        # Read from file
        file_path = self._get_base_taxonomy_path() / dimension / f"{value}.json"
        if not file_path.exists():
            logger.error(f"Dimension value file not found: {file_path}")
            return []

        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                buckets = data.get("buckets", [])
                self._cached_dimension_buckets[dimension][value] = buckets
                return buckets
        except Exception as e:
            logger.error(f"Error reading dimension value file {file_path}: {e}")
            return []

    def get_buckets_for_project(
        self,
        platform: str,
        domain: str,
        size: str,
        lifecycle: str,
        compliance: Optional[str] = None,
    ) -> Set[str]:
        """Returns the combined set of taxonomy buckets for a project with the given dimensions."""
        all_buckets = set()

        # Add buckets from required dimensions
        all_buckets.update(self.get_buckets_for_dimension_value("platform", platform))
        all_buckets.update(self.get_buckets_for_dimension_value("domain", domain))
        all_buckets.update(self.get_buckets_for_dimension_value("size", size))
        all_buckets.update(self.get_buckets_for_dimension_value("lifecycle", lifecycle))

        # Add buckets from optional dimensions if provided
        if compliance:
            all_buckets.update(
                self.get_buckets_for_dimension_value("compliance", compliance)
            )

        return all_buckets

    def get_all_available_buckets(self) -> List[str]:
        """Returns a list of all available bucket IDs from the taxonomy."""
        if self._cached_all_buckets is not None:
            return self._cached_all_buckets

        try:
            with open(self.taxonomy_path, "r") as f:
                data = json.load(f)
                buckets = list(data.get("mece_taxonomy", {}).keys())
                self._cached_all_buckets = buckets
                return buckets
        except Exception as e:
            logger.error(f"Error reading main taxonomy file {self.taxonomy_path}: {e}")
            return []

    def get_bucket_description(self, bucket_id: str) -> Optional[str]:
        """Returns the description for a specific bucket ID, or None if not found."""
        if self._cached_bucket_descriptions is None:
            try:
                with open(self.taxonomy_path, "r") as f:
                    data = json.load(f)
                    self._cached_bucket_descriptions = {
                        bucket: info.get("description", "")
                        for bucket, info in data.get("mece_taxonomy", {}).items()
                    }
            except Exception as e:
                logger.error(
                    f"Error reading main taxonomy file {self.taxonomy_path}: {e}"
                )
                self._cached_bucket_descriptions = {}

        return self._cached_bucket_descriptions.get(bucket_id)
