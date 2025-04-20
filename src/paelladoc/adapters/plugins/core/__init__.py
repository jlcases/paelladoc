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
