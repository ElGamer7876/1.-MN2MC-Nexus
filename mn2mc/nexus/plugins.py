"""Load trusted local Python extension modules explicitly selected by operator."""
import importlib
import re
from loguru import logger

_SAFE_MODULE = re.compile(r"^[A-Za-z_]\w*(\.[A-Za-z_]\w*)*$")
_loaded: set[str] = set()

def load_plugins(modules: list[str]) -> None:
    for name in modules:
        if not isinstance(name, str) or not _SAFE_MODULE.fullmatch(name):
            raise ValueError("Invalid plugin module name")
        if name not in _loaded:
            importlib.import_module(name)
            _loaded.add(name)
            logger.info("Loaded trusted extension {}", name)
