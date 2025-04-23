import logging
from typing import Dict, List
import importlib.resources

from paelladoc.ports.output.taxonomy_provider import TaxonomyProvider

logger = logging.getLogger(__name__)

# Removed old path calculation based on __file__
# # Determine the base path relative to this file's location
# # Assumes this structure: src/paelladoc/adapters/output/filesystem/taxonomy_provider.py
# # And taxonomies are at: project_root/taxonomies/
# ADAPTER_DIR = Path(__file__).parent
# SRC_DIR = ADAPTER_DIR.parent.parent.parent
# PROJECT_ROOT = SRC_DIR.parent
# TAXONOMY_BASE_PATH = PROJECT_ROOT / "taxonomies"


class FileSystemTaxonomyProvider(TaxonomyProvider):
    """Provides available taxonomy information by scanning package resources."""

    def __init__(self):
        """Initializes the provider."""
        # Base path is now determined dynamically using importlib.resources
        # self.base_path = base_path # Removed base_path argument
        # if not self.base_path.is_dir(): # Check happens within get_available_taxonomies
        #     logger.error(
        #         f"Taxonomy base path not found or not a directory: {self.base_path.resolve()}"
        #     )
        self._cached_taxonomies: Dict[str, List[str]] | None = None

    def get_available_taxonomies(self) -> Dict[str, List[str]]:
        """Scans the package resources for taxonomy directories and loads available taxonomy names.

        Uses a simple cache to avoid repeated resource scanning.
        """
        if self._cached_taxonomies is not None:
            logger.debug("Returning cached taxonomies")
            return self._cached_taxonomies

        available_taxonomies = {}
        categories = ["platform", "domain", "size", "compliance"]

        try:
            # Get the base path to the 'taxonomies' directory within the 'paelladoc' package
            base_taxonomy_path_resource = importlib.resources.files(
                "paelladoc"
            ).joinpath("taxonomies")
            logger.debug(
                f"Scanning for taxonomies in package resource: {base_taxonomy_path_resource}"
            )

            if not base_taxonomy_path_resource.is_dir():
                logger.error(
                    f"Cannot scan taxonomies, package resource directory not found: {base_taxonomy_path_resource}"
                )
                self._cached_taxonomies = {cat: [] for cat in categories}
                return self._cached_taxonomies

            for category in categories:
                category_path_resource = base_taxonomy_path_resource.joinpath(category)
                if category_path_resource.is_dir():
                    try:
                        tax_files = sorted(
                            f.name.removesuffix(
                                ".json"
                            )  # Get filename without .json extension
                            for f in category_path_resource.iterdir()
                            if f.is_file() and f.name.endswith(".json")
                        )
                        available_taxonomies[category] = tax_files
                        logger.debug(
                            f"Found {len(tax_files)} taxonomies in '{category}': {tax_files}"
                        )
                    except OSError as e:
                        logger.error(
                            f"Error reading taxonomy package resource directory {category_path_resource}: {e}"
                        )
                        available_taxonomies[category] = []
                else:
                    available_taxonomies[category] = []
                    logger.warning(
                        f"Taxonomy package resource directory not found: {category_path_resource}"
                    )

        except ModuleNotFoundError:
            logger.error(
                "Could not find package 'paelladoc' via importlib.resources. Is the package installed correctly?"
            )
            self._cached_taxonomies = {cat: [] for cat in categories}
            return self._cached_taxonomies
        except Exception as e:
            logger.error(
                f"Unexpected error scanning taxonomy resources: {e}", exc_info=True
            )
            self._cached_taxonomies = {cat: [] for cat in categories}
            return self._cached_taxonomies

        self._cached_taxonomies = available_taxonomies
        logger.info(
            f"Loaded {sum(len(v) for v in available_taxonomies.values())} taxonomies across {len(categories)} categories from package resources."
        )
        return available_taxonomies
