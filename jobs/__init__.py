import importlib
import logging
import pkgutil

logger = logging.getLogger(__name__)

for _, module_name, _ in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{__name__}.{module_name}")
