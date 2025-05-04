"""
handlers_dir (Path): The directory path where the handler modules are located.
This module dynamically imports all Python modules in the current directory 
(excluding those starting with an underscore) and collects all `Router` 
instances defined in those modules.
Attributes:
    handlers_dir (str): The directory path where the handler modules are located.
    routers (list): A list of `Router` instances collected from the imported modules.
The module performs the following steps:
1. Identifies all Python files in the current directory, excluding private files 
   (those starting with an underscore).
2. Dynamically imports each identified module.
3. Logs the successful import of each module or a warning if the import fails.
4. Collects all `Router` instances defined in the imported modules and adds 
   them to the `routers` list.
The `routers` list is exposed as part of the module's public API via the `__all__` attribute.
"""

import logging

from pathlib import Path
from importlib import import_module
from aiogram import Router


logger = logging.getLogger(__name__)

# Define the directory containing handler modules
handlers_dir = Path(__file__).parent

# Initialize an empty list to collect Router instances
routers = []

# Iterate over all Python files in the directory, excluding private ones (starting with '_')
for module_path in handlers_dir.glob("[!_]*.py"):
    module_name = f"{handlers_dir.name}.{module_path.stem}"
    try:
        # Dynamically import the module
        module = import_module(f".{module_path.stem}", package=handlers_dir.name)
        logger.info(f"Successfully imported handler: \'{module_name}\'")
        
        # Collect all Router instances from the module
        for obj in vars(module).values():
            if isinstance(obj, Router):
                routers.append(obj)
    except Exception as e:
        logger.warning(f"Failed to import \'{module_name}\': {e}")

# Expose the `routers` list as part of the module's public API
__all__ = ["routers"]
