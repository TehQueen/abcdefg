"""
This module dynamically discovers and imports all Python modules in the current package directory,
excluding private modules (those starting with an underscore). It collects all `Router` instances
from the imported modules and exposes them as a public API.
Attributes:
    routers (list): A list of `Router` instances collected from the imported modules.
The module performs the following steps:
1. Recursively searches for all Python files in the current package directory, excluding private files.
2. Imports each discovered module relative to the current package.
3. Logs the success or failure of each module import.
4. Collects all `Router` instances from the imported modules and adds them to the `routers` list.
5. Exposes the `routers` list as part of the module's public API.
Logging:
    - Logs successful imports of handler modules at the INFO level.
    - Logs warnings for failed imports, including the exception message.
Raises:
    Any exceptions raised during module imports are caught and logged as warnings, but they do not
    interrupt the execution of the script.
"""

import logging

from pathlib import Path
from importlib import import_module
from aiogram import Router

logger = logging.getLogger(__name__)

# Initialize an empty list to collect Router instances
routers = []

# Recursively find and import all Python modules in the directory, excluding private ones (starting with '_')
for path in Path(__path__[0]).rglob("[!_]*"):
    if path.is_file():
        continue

    module_name = ".".join(path.relative_to(__path__[0]).with_suffix("").parts)

    try:
        # Import the module relative to the current package
        module = import_module(f".{module_name}", package=__package__)
        logger.info(f"Successfully imported handler: '{module.__name__}'")

        # Collect all Router instances from the module
        routers.extend(obj for obj in vars(module).values() if isinstance(obj, Router))
    except Exception as e:
        logger.warning(f"Failed to import '{module_name}': {e}")

# Expose the `routers` list as part of the module's public API
__all__ = ["routers"]
