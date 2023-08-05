from pathlib import Path

import toml

from wavy.panel import *


def get_version():
    path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject = toml.loads(open(str(path)).read())
    return pyproject["tool"]["poetry"]["version"]


__version__ = get_version()
