"""전역 키보드 후킹 디버그 로그 (--debug 또는 SHORTCUT_DEBUG=1)."""

import logging
import os
import sys
from pathlib import Path

from src.paths import get_project_root

_configured = False


def configure(enabled: bool | None = None) -> bool:
    global _configured
    if enabled is None:
        enabled = os.environ.get("SHORTCUT_DEBUG", "").lower() in ("1", "true", "yes")

    if not enabled:
        return False

    log_path = get_project_root() / "data" / "hook_debug.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger("shortcut")
    root.setLevel(logging.DEBUG)
    root.handlers.clear()

    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    )
    root.addHandler(handler)

    if sys.stderr:
        stream = logging.StreamHandler(sys.stderr)
        stream.setFormatter(handler.formatter)
        root.addHandler(stream)

    _configured = True
    root.info("debug logging enabled: %s", log_path)
    return True


def is_enabled() -> bool:
    return _configured


def log(message: str, *args: object) -> None:
    if _configured:
        logging.getLogger("shortcut").debug(message, *args)
