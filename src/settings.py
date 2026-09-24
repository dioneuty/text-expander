import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from src.repository import RepositoryError

ExpansionMode = Literal["immediate", "on_key"]
ExpansionKey = Literal["space", "enter", "tab"]

VALID_MODES: frozenset[str] = frozenset({"immediate", "on_key"})
VALID_KEYS: frozenset[str] = frozenset({"space", "enter", "tab"})


@dataclass(frozen=True)
class ExpansionSettings:
    mode: ExpansionMode = "on_key"
    expansion_key: ExpansionKey = "space"


DEFAULT_SETTINGS = ExpansionSettings()


class SettingsRepository:
    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> ExpansionSettings:
        if not self._path.exists():
            return DEFAULT_SETTINGS

        try:
            raw = self._path.read_text(encoding="utf-8")
            if not raw.strip():
                return DEFAULT_SETTINGS
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RepositoryError(f"JSON 파싱 오류: {self._path}") from exc
        except OSError as exc:
            raise RepositoryError(f"파일 읽기 오류: {self._path}") from exc

        if not isinstance(data, dict):
            return DEFAULT_SETTINGS

        mode = data.get("expansion_mode", DEFAULT_SETTINGS.mode)
        expansion_key = data.get("expansion_key", DEFAULT_SETTINGS.expansion_key)

        if mode not in VALID_MODES:
            mode = DEFAULT_SETTINGS.mode
        if expansion_key not in VALID_KEYS:
            expansion_key = DEFAULT_SETTINGS.expansion_key

        return ExpansionSettings(mode=mode, expansion_key=expansion_key)

    def save(self, settings: ExpansionSettings) -> None:
        payload = {
            "version": 1,
            "expansion_mode": settings.mode,
            "expansion_key": settings.expansion_key,
        }
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            raise RepositoryError(f"파일 저장 오류: {self._path}") from exc
