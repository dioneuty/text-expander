import sys
from pathlib import Path


def get_project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def get_data_path(filename: str = "shortcuts.json") -> Path:
    return get_project_root() / "data" / filename
