import pkgutil
import importlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Dynamically import all modules within this 'core' package
# to ensure @mcp.tool decorators are executed.

package_path = str(Path(__file__).parent)
package_name = __name__

logger.info(f"Dynamically loading core plugins from: {package_path}")

for module_info in pkgutil.iter_modules([package_path]):
    # Import all .py files (except __init__.py itself)
    if module_info.name != "__init__" and not module_info.ispkg:
        module_name = f"{package_name}.{module_info.name}"
        try:
            importlib.import_module(module_name)
            logger.debug(f"Successfully loaded core plugin module: {module_name}")
        except Exception as e:
            logger.warning(f"Could not load core plugin module {module_name}: {e}")

logger.info("Finished dynamic core plugin loading.")

"""
Core plugins for PAELLADOC command handling.

Imports:
    - help: Provides the HELP command functionality.
    - paella: Initiates new documentation projects.
    - continue_proj: Continues existing documentation projects.
    - verification: Verifies documentation integrity.
    - list_projects: Lists existing projects.
"""

# Removed explicit imports and __all__, relying on dynamic loading above
# from .help import core_help
# from .paella import core_paella # This was causing issues
# from .continue_proj import core_continue
# from .verification import core_verification
# from .list_projects import list_projects
#
# __all__ = [
#     "core_help",
#     "core_paella",
#     "core_continue",
#     "core_verification",
#     "list_projects",
# ]
