import logging
from pathlib import Path
from typing import Dict, List

from paelladoc.ports.output.taxonomy_provider import TaxonomyProvider

logger = logging.getLogger(__name__)

# Determine the base path relative to this file's location
# Assumes this structure: src/paelladoc/adapters/output/filesystem/taxonomy_provider.py
# And taxonomies are at: project_root/taxonomies/
ADAPTER_DIR = Path(__file__).parent
SRC_DIR = ADAPTER_DIR.parent.parent.parent
PROJECT_ROOT = SRC_DIR.parent
TAXONOMY_BASE_PATH = PROJECT_ROOT / "taxonomies"


class FileSystemTaxonomyProvider(TaxonomyProvider):
    """Provides available taxonomy information by scanning filesystem directories."""

    def __init__(self, base_path: Path = TAXONOMY_BASE_PATH):
        """Initializes the provider with the base path to the taxonomy directories."""
        self.base_path = base_path
        if not self.base_path.is_dir():
            logger.error(
                f"Taxonomy base path not found or not a directory: {self.base_path.resolve()}"
            )
            # Raise an error or handle appropriately? For now, log and continue.
            # raise FileNotFoundError(f"Taxonomy base path not found: {self.base_path}")
        self._cached_taxonomies: Dict[str, List[str]] | None = None

    def get_available_taxonomies(self) -> Dict[str, List[str]]:
        """Scans the taxonomy directories and loads available taxonomy names.

        Uses a simple cache to avoid repeated filesystem scans.
        """
        if self._cached_taxonomies is not None:
            logger.debug("Returning cached taxonomies")
            return self._cached_taxonomies

        logger.debug(f"Scanning for taxonomies in: {self.base_path.resolve()}")
        available_taxonomies = {}
        categories = ["platform", "domain", "size", "compliance"]

        if not self.base_path.is_dir():
            logger.error(
                f"Cannot scan taxonomies, base path is invalid: {self.base_path.resolve()}"
            )
            return {cat: [] for cat in categories}  # Return empty if base path is bad

        for category in categories:
            category_path = self.base_path / category
            if category_path.is_dir():
                try:
                    tax_files = sorted(
                        f.stem  # Get filename without .json extension
                        for f in category_path.glob("*.json")
                        if f.is_file()
                    )
                    available_taxonomies[category] = tax_files
                    logger.debug(
                        f"Found {len(tax_files)} taxonomies in '{category}': {tax_files}"
                    )
                except OSError as e:
                    logger.error(
                        f"Error reading taxonomy directory {category_path}: {e}"
                    )
                    available_taxonomies[category] = []
            else:
                available_taxonomies[category] = []
                logger.warning(f"Taxonomy directory not found: {category_path}")

        self._cached_taxonomies = available_taxonomies
        logger.info(
            f"Loaded {sum(len(v) for v in available_taxonomies.values())} taxonomies across {len(categories)} categories."
        )
        return available_taxonomies
