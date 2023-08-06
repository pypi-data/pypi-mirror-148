from pathlib import Path
from packaging.version import parse

with Path(__file__).with_name("_version.txt").open("r") as f:
    version_obj = parse(f.readline().strip())

# Representation of version_info as (x, y, z)
__version__ = str(version_obj)

__all__ = ("__version__", "version_obj")
