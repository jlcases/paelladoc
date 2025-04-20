import pkgutil
import importlib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Dynamically import all submodules (like core, code, styles, etc.)
# This ensures their __init__.py files are executed, which should in turn
# import the actual plugin files containing @mcp.tool decorators.

package_path = str(Path(__file__).parent)
package_name = __name__

logger.info(f"Dynamically loading plugins from: {package_path}")

for module_info in pkgutil.iter_modules([package_path]):
    if module_info.ispkg: # Only import potential packages (directories)
        sub_package_name = f"{package_name}.{module_info.name}"
        try:
            importlib.import_module(sub_package_name)
            logger.debug(f"Successfully imported plugin package: {sub_package_name}")
        except Exception as e:
            logger.warning(f"Could not import plugin package {sub_package_name}: {e}")

logger.info("Finished dynamic plugin package loading.")
