from app.core.db import Base

from pathlib import Path
import importlib

package_dir = Path(__file__).parent
for module_path in package_dir.glob("*.py"):
    if module_path.name != "__init__.py":
        importlib.import_module(f"app.models.{module_path.stem}")
